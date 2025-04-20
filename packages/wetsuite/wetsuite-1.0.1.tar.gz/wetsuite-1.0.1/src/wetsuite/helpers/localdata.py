"""
This is intended to store store collections of data on disk,
relatively unobtrusive to use    (better than e.g. lots of files),
and with quick random access     (better than e.g. JSONL).

It currently centers on a key-value store.
See the docstring on the LocalKV class for more details.

This is used e.g. by various data collection, and by distributed datasets.

There are a lot of general notes in LocalKV's docstring (and a lot of it also applies to MsgpackKV)
"""

import os
import os.path
import time
import pathlib
import random
import collections.abc
from typing import Tuple

import sqlite3

# msgpack should be alittle more interoperable and/or a little faster than pickle or kson. 
# It is however, an extra dependency (and does a little less)
import msgpack

import wetsuite.helpers.util  # to get wetsuite_dir
import wetsuite.helpers.net
import wetsuite.helpers.format


class LocalKV:
    """
    A key-value store backed by a local filesystem - it's a wrapper around sqlite3.

    Given: ::
        db = LocalKV('path/to/dbfile')
    Basic use is: ::
        db.put('foo', 'bar')
        db.get('foo')

    Notes:
      - on the path/name argument:
        - just a name ( without os.sep, that is, / or \\ ) will be resolved 
          to a path where wetsuite keeps various stores
        - an absolute path will be passed through, used as-is
          ...but this is NOT very portable until you do things 
          like `os.path.join( myproject_data_dir, 'docstore.db')`
        - a relative path with os.sep will be passed through
          ...which is only as portable as the cwd is predictable)
        - ':memory:' is in-memory only
        - See also C{resolve_path} for more details

      - by default, each write is committed individually 
        (because SQlite3's driver defaults to autocommit).
        If you want more performant bulk writes,
        use put() with commit=False, and
        do an explicit commit() afterwards
        ...BUT if a script borks in the middle of something uncommited,
        you will need to do manual cleanup.

      - On typing:
          - SQLite will just store what it gets, which makes it easy to store mixed types.
            To allow programmers to enforce some runtime checking,
            you can specify key_type and value_type.

          - This class won't do conversions for you,
            it only enforces the values that go in are of the type you said you would put in.

          - This should make things more consistent,
            but is not a strict guaranteem, and you can subvert this easily.

          - Some uses may wish for a specific key and value type.
            You could change both key and value types,
            e.g. the cached_fetch function expects a str:bytes store

         - It is a good idea to open the store with the same typing every time,
           or you will still confuse yourself.
           CONSIDER: storing typing in the file in the meta table so we can warn you.

      - making you do CRUD via functions is a little more typing,
        - yet is arguably clearer than 'this particular dict-like happens to get stored magically'
        - and it lets us exposes some sqlite things (using transactions, vacuum)
          for when you know how to use them.

      - On concurrency: As per basic sqlite behaviour,
        multiple processes can read the same database,
        but only one can write,
        and writing is exclusive with reading.
        So
          - when you leave a writer with uncommited data for nontrivial amounts of time, 
            readers are likely to time out.
              - If you leave it on autocommit this should be a little rarer
          - and a very slow read through the database might time out a write.

      - It wouldn't be hard to also make it act largely like a dict,
        implementing __getitem__, __setitem__, and __delitem__
        but this muddies the waters as to its semantics,
        in particular when things you set are actually saved.

        So we try to avoid a leaky abstraction, 
        by making you write out all the altering operations,
        and actually all of them, e.g.  get(), put(),  keys(), values(), and items(),
        because those can at least have docstrings to warn you,
        rather than breaking your reasonable expectations.

        ...exceptions are
          - __len__        for amount of items                  (CONSIDER making that len())  
          - __contains__   backing 'is this key in the store')  (CONSIDER making that has_key())  
        and also:
          - __iter__       which is actually iterkeys()         CONSIDER: removing it
          - __getitem__    supports the views-with-a-len
        The last were tentative until keys(), values(), and items() started giving views.

        TODO: make a final decision where to sit between clean abstractions and convenience.

      - yes, you _could_ access these SQLite databses yourself, particularly when just reading.
        Our code is mainly there for convenience and checks.
        Consider: `sqlite3 store.db 'select key,value from kv limit 10 ' | less`
        It only starts getting special once you using MsgpackKV, 
        or the extra parsing and wrapping that wetsuite.datasets adds.

    @ivar conn: connection to the sqlite database that we set up
    @ivar path: the path we opened (after resolving)
    @ivar key_type: the key type you have set
    @ivar value_type: the value type you have set
    @ivar read_only: whether we have told ourselves to treat this as read-only.
    That _should_ also make it hard for _us_ to be the cause
    of leaving the database in a locked state.
    """

    def __init__(self, path, key_type, value_type, read_only=False):
        """Specify the path to the database file to open.

        key_type and value_type do not have defaults,
        so that you think about how you are using these,
        but we often use   str,str  and  str,bytes

        @param path: database name/pat. File will be created if it does not yet exist,
        so you proably want think to think about repeating the same path in absolute sense.
        See also the module docstring, and in particular resolve_path()'s docstring

        @param key_type:
        @param value_type:
        @param read_only: is only enforced in this wrapper to give slightly more useful errors.
        (we also give SQLite a PRAGMA)
        """
        self.path = path
        self.path = resolve_path(
            self.path
        )  # tries to centralize the absolute/relative path handling code logic

        self.read_only = read_only
        # self.use_wal = use_wal

        self._open()
        # here in part to remind us that we _could_ be using converters  https://docs.python.org/3/library/sqlite3.html#sqlite3-converters
        if key_type not in (str, bytes, int, None):
            raise TypeError(
                f"We are currently a little overly paranoid about what to allow as key types ({repr(key_type.__name__)} not allowed)"
            )
        if value_type not in (str, bytes, int, float, None):
            raise TypeError(
                f"We are currently a little overly paranoid about what to allow as value types ({repr(value_type.__name__)} not allowed)"
            )

        self.key_type = key_type
        self.value_type = value_type

        self._in_transaction = False

    def _open(self, timeout=3.0):
        """Open the path previously set by init.
        This function could probably be merged into init,
        it was separated mostly with the idea that we could keep it closed when not using it.

        timeout: how long wait on opening.
        Lowered from the default just to avoid a lot of waiting half a minute
        when it was usually just accidentally left locked.
        (note that this is different from busy_timeout)
        """
        # make_tables = (self.path==':memory:')  or  ( not os.path.exists( self.path ) )
        #    will be creating that file, or are using an in-memory database ?
        #    Also how to combine with read_only?
        self.conn = sqlite3.connect(self.path, timeout=timeout)
        # Note: curs.execute is the regular DB-API way,
        #       conn.execute is a shorthand that gets a temporary cursor
        with self.conn:
            if self.read_only:
                self.conn.execute(
                    "PRAGMA query_only = true"
                )  # https://www.sqlite.org/pragma.html#pragma_query_only
                # if read-only, we assume you are opening something that was aleady created before, so we don't do...
            else:
                # TODO: see that the auto_vacuum pragma does what I think it does    https://www.sqlite.org/pragma.html#pragma_auto_vacuum
                self.conn.execute("PRAGMA auto_vacuum = INCREMENTAL")

                self.conn.execute(
                    "CREATE TABLE IF NOT EXISTS meta (key text unique NOT NULL, value text)"
                )
                self.conn.execute(
                    "CREATE TABLE IF NOT EXISTS kv   (key text unique NOT NULL, value text)"
                )

                # if self.use_wal:
                #     self.conn.execute("pragma journal_mode=WAL")
                #     # notes
                #     # - if not possible (we know we can't get the necessary shm due to the VFS) this is effectively just ignroed
                #     # - using use_wal once persists with a database, in that future opens will use it even if you don't ask for it
                #     # - WAL requires sqlite >=3.7.0, but this seems fine because python's sqlite3 requires >=3.7.15

    def _checktype_key(self, val):
        "checks a value according to the key_type you handed into the constructor"
        if self.key_type is not None and not isinstance(
            val, self.key_type
        ):  # None means don't check
            raise TypeError(
                "You specified that only keys of type %s are allowed, and now asked for a %s"
                % (self.key_type.__name__, type(val).__name__)
            )

    def _checktype_value(self, val):
        "checks a value according to the value_type you handed into the constructor"
        if self.value_type is not None and not isinstance(val, self.value_type):
            raise TypeError(
                "You specified that only values of type %s are allowed, and now gave a %s"
                % (self.value_type.__name__, type(val).__name__)
            )

    def get(self, key, missing_as_none: bool = False):
        """Gets value for key.
        The key type is checked against how you constructed this localKV class 
        (doesn't guarantee it matches what's in the database)
        If not present, this will raise KeyError (by default) 
        or return None (if you set missing_as_None=True)
        (this is unlike a dict.get, which has a default=None)
        """
        self._checktype_key(key)
        curs = self.conn.cursor()
        curs.execute("SELECT value FROM kv WHERE key=?", (key,))
        row = curs.fetchone()
        if row is None:
            if missing_as_none:
                return None
            else:
                raise KeyError("Key %r not found" % key)
        else:
            return row[0]

    def put(self, key, value, commit: bool = True):
        """Sets/updates value for a key.

        Types will be checked according to what you inited this class with.

        commit=False lets us do bulk commits,
        mostly when you want to a load of (small) changes without becoming IOPS bound,
        at the risk of locking/blocking other access.
        If you care less about speed, and/or more about parallel access, ignore this.

        CONSIDER: making commit take an integer as well, meaning 'commit every X operations'
        """
        if self.read_only:
            raise RuntimeError(
                "Attempted put() on a store that was opened read-only.  (you can subvert that but may not want to)"
            )

        self._checktype_key(key)
        self._checktype_value(value)

        curs = self.conn.cursor()
        if not commit and not self._in_transaction:
            curs.execute("BEGIN")
            self._in_transaction = True

        curs.execute(
            "INSERT INTO kv (key, value) VALUES (?, ?)  ON CONFLICT (key) DO UPDATE SET value=?",
            (key, value, value),
        )
        if commit:
            self.commit()

    def delete(self, key, commit: bool = True):
        """delete item by key.

        Note that you should not expect the file to shrink until you do a vacuum()  (which will need to rewrite the file).
        """
        if self.read_only:
            raise RuntimeError(
                "Attempted delete() on a store that was opened read-only.  (you can subvert that but may not want to)"
            )

        self._checktype_key(key)

        curs = self.conn.cursor()  # TODO: check that's correct when commit==False
        if not commit and not self._in_transaction:
            curs.execute("BEGIN")
            self._in_transaction = True
        curs.execute("DELETE FROM kv where key=?", (key,))
        if commit:
            self.commit()

    def _get_meta(self, key: str, missing_as_none=False):
        """For internal use, preferably don't use.

        This is an extra str:str table in there that is intended to be separate,
        with some keys special to these classes.
        ...you could abuse this for your own needs if you wish, but try not to.

        If the key is not present, raises an exception - unless missing_as_none is set,
        in which case in returns None.
        """
        curs = self.conn.cursor()
        curs.execute("SELECT value FROM meta WHERE key=?", (key,))
        row = curs.fetchone()
        curs.close()
        if row is None:
            if missing_as_none:
                return None
            else:
                raise KeyError("Key %r not found" % key)
        else:
            return row[0]

    def _put_meta(self, key: str, value: str):
        """For internal use, preferably don't use.   See also _get_meta(), _delete_meta().   Note this does an implicit commit()"""
        if self.read_only:
            raise RuntimeError(
                "Attempted _put_meta() on a store that was opened read-only.  (you can subvert that but may not want to)"
            )
        curs = self.conn.cursor()
        curs.execute("BEGIN")
        curs.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?)  ON CONFLICT (key) DO UPDATE SET value=?",
            (key, value, value),
        )
        self.commit()
        curs.close()

    def _delete_meta(self, key: str):
        """For internal use, preferably don't use.   See also _get_meta(), _delete_meta().   Note this does an implicit commit()"""
        if self.read_only:
            raise RuntimeError(
                "Attempted _put_meta() on a store that was opened read-only.  (you can subvert that but may not want to)"
            )
        curs = self.conn.cursor()  # TODO: check that's correct when commit==False
        curs.execute("DELETE FROM meta where key=?", (key,))
        self.commit()
        curs.close()

    def commit(self):
        "commit changes - for when you use put() or delete() with commit=False to do things in a larger transaction"
        self.conn.commit()
        self._in_transaction = False

    def rollback(self):
        "roll back changes"
        # maybe only if _in_transaction?
        self.conn.rollback()
        self._in_transaction = False

    def close(self):
        "Closes file if still open. Note that if there was a transaction still open, it will be rolled back, not committed."
        if self._in_transaction:
            self.rollback()
        self.conn.close()

    # TODO: see if the view's semantics in keys(), values(), and items() are actually correct.
    #      Note there's a bunch of implied heavy lifting in hnading self to those view classes,
    #         which require that that relies on __iter__ and __getitem__ to be there

    def iterkeys(self):
        """Returns a generator that yields all keus
        If you wanted a list with all keys, use list( store.keys() )
        """
        curs = self.conn.cursor()
        for row in curs.execute("SELECT key FROM kv"):
            yield row[0]
        curs.close()

    def keys(self):
        """Returns an iterable of all keys.  (a view with a len, rather than just a generator)"""
        return collections.abc.KeysView(self)  # TODO: check that this is enough

    def itervalues(self):
        """Returns a generator that yields all values.
        If you wanted a list with all the values, use list( store.values )
        """
        curs = self.conn.cursor()
        for row in curs.execute("SELECT value FROM kv"):
            yield row[0]
        curs.close()

    def values(self):
        """Returns an iterable of all values.  (a view with a len, rather than just a generator)"""
        return collections.abc.ValuesView(self)

    def iteritems(self):
        """Returns a generator that yields all items"""
        curs = self.conn.cursor()
        try:  # TODO: figure out whether this is necessary
            for row in curs.execute("SELECT key, value FROM kv"):
                yield row[0], row[1]
        finally:
            curs.close()

    def items(self):
        """Returns an iteralble of all items.    (a view with a len, rather than just a generator)"""
        return collections.abc.ItemsView(
            self
        )  # this relies on __getitem__ which we didn't really want, maybe wrap a class to hide that?

    def __repr__(self):
        "show useful representation"
        return "<LocalKV(%r)>" % (os.path.basename(self.path),)

    def __len__(self):
        "Return the amount of entries in this store"
        return self.conn.execute("SELECT COUNT(*) FROM kv").fetchone()[
            0
        ]  # TODO: double check

    # Choice not to actually have it behave like a dict - this seems like a leaky abstraction,
    # so we make you write out the .get and .put to make you realize it's different behaviour not like a real dict

    def __iter__(self):  # TODO: check
        "Using this object as an iterator yields its keys (equivalent to .iterkeys())"
        return self.iterkeys()

    def __getitem__(self, key):
        "(only meant to support ValuesView and Itemsview)"
        return self.get(key)  # which would itself raise KeyError if applicable

    # def __setitem__(self, key, value):
    #    self.put(key, value)

    # def __delitem__(self, key):
    #    # TODO: check whether we can ignore it not being there, or must raise KeyError for interface correctness
    #    #if key not in self:
    #    #    raise KeyError(key)
    #    self.conn.execute('DELETE FROM kv WHERE key = ?', (key,))

    # ...but we still sneakily have:
    def __contains__(self, key):
        "will return whether the store contains a key"
        return (
            self.conn.execute("SELECT 1 FROM kv WHERE key = ?", (key,)).fetchone()
            is not None
        )

    ## Used as a context manager? do a close() at the end.
    def __enter__(self):
        "supports use as a context manager"
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        "supports use as a context manager - close()s on exit"
        self.close()

    ### Convenience functions, not core functionality

    def estimate_waste(self):
        "Estimate how many bytes might be cleaned by a .vacuum()"
        return self.conn.execute(
            "SELECT (freelist_count*page_size) as FreeSizeEstimate  FROM pragma_freelist_count, pragma_page_size"
        ).fetchone()[0]

    # def incremental_vacuum(self):
    #     ''' assuming we created with "PRAGMA auto_vacuum = INCREMENTAL" we can do cleanup.
    #         deally you do with some interval when you remove/update things
    #         CONSIDER our own logic to that?  Maybe purely per interpreter (after X puts/deletes),  and maybe do it on close?
    #     '''
    #     # https://www.sqlite.org/pragma.html#pragma_auto_vacuum
    #     if self._in_transaction:
    #         self.commit()
    #     self.conn.execute('PRAGMA schema.incremental_vacuum')

    def bytesize(self) -> int:
        """Returns the approximate amount of the contained data, in bytes
        (may be a few dozen kilobytes off, or more, because it counts in pages)
        """
        # if self.path == ':memory:'
        curs = self.conn.cursor()
        curs.execute(
            "select page_size, page_count from pragma_page_count, pragma_page_size"
        )
        page_size, page_count = curs.fetchone()
        curs.close()
        return page_size * page_count
        # else:
        #    return os.stat( self.path ).st_size

    def summary(self, get_num_items: bool = False):
        """Gives the byte size, and optionally the number of items and average size

        Note that the byte size includes waste, so this will over-estimate if you
        have altered/removed without doing a vacuum().

        @param get_num_items: Also find the amount of items, and calculate average size.
        Is slower than not doing this (proportionally slower with underlying size),
        adds entries like: ::
            'num_items':     856716,
            'avgsize_bytes': 63585,
            'avgsize_readable': '62K',

        @return: a dictionary with at least::
            {'size_bytes':     54474244096,
             'size_readable': '54G'}
        """
        # CONSIDER: a fast get_num_items via and-sqlite_stat1 if it exists
        # (and considering ANALYZE if it does not)
        # which after ANALYZE should always have a row like
        # tbl='kv',idx='sqlite_autoindex_kv_1', stat='1234 1'
        # (because our structure has a UNIQUE constraint on kv's key)
        # this would be more valid for unchanging datasets
        ret = {}
        bytesize = self.bytesize()
        ret["size_bytes"] = bytesize
        ret["size_readable"] = wetsuite.helpers.format.kmgtp(bytesize, kilo=1024) + "B"
        if get_num_items:
            ret["num_items"] = len(self)
            if ret["num_items"] == 0:
                ret["avgsize_bytes"] = 0
            else:
                ret["avgsize_bytes"] = round(float(bytesize) / ret["num_items"])
            ret["avgsize_readable"] = (
                wetsuite.helpers.format.kmgtp(ret["avgsize_bytes"], kilo=1024) + "B"
            )
        return ret

    def vacuum(self):
        """After a lot of deletes you could compact the store with vacuum().
        WARNING: rewrites the entire file, so the more data you store, the longer this takes.
        And it may make no difference - you probably want to check estimate_waste() first.
        NOTE: if we were left in a transaction (due to commit=False), ths is commit()ed first.
        """
        if self._in_transaction:
            self.commit()  # CONSIDER: think about the most sensible behaviour - maybe raising an error instead?
        self.conn.execute("vacuum")

    def truncate(self, vacuum=True):
        """remove all kv entries.
        If we were still in a transaction, we roll that back first
        """
        curs = self.conn.cursor()  # TODO: check that's correct when commit==False
        if self._in_transaction:
            self.rollback()
        curs.execute( "DELETE FROM kv" )  # https://www.techonthenet.com/sqlite/truncate.php
        self.commit()
        if vacuum:
            self.vacuum()

    def random_choice(self):
        """Returns a single (key, value) item from the store, selected randomly.

        A convenience function, because doing this properly yourself takes two or three lines
        (you can't random.choice/random.sample a view, so to do it properly you basically have to materialize all keys - and not accidentally all values)
        BUT assume this is slower than working on the keys yourself.
        """
        all_keys = list(self.keys())
        chosen_key = random.choice(all_keys)
        return chosen_key, self.get(chosen_key)

    def random_keys(self, n=10):
        """Returns a amount of keys in a list, selected randomly.
        Can be faster/cheaper to do than random_sample When the values are large

        On very large stores (tens of millions of items and/or hundred of gbytes)
        this still ends up being dozens of seconds, because we still skip through a bunch of that data.
        """
        all_keys = list(self.keys())
        chosen_keys = random.sample(all_keys, min(n, len(all_keys)))
        return chosen_keys

    def random_sample(self, n):
        """Returns an amount of [(key, value), ...] list from the store, selected randomly.

        WARNING: This materializes all keys and the chosen values in RAM,
        so can use considerable RAM if values are large.
        To avoid that RAM use, use random_keys() and get() one key at a time,
        or use random_sample_generator().

        Note that when you ask for a larger sample than the entire population, 
        you get the entire population (and unlike random.sample, we don't raise a ValueError 
        to point out this is no longer a subselection)
        """
        all_keys = list(self.keys())
        n = min(n, len(all_keys))
        #if amount > len(all_keys): # doing this would be consistent with random.sample
        #    raise ValueError(f"Sample larger than population (you asked for {amount}, we have {len(all_keys)})")
        chosen_keys = random.sample(all_keys, n)
        return list((chosen_key, self.get(chosen_key)) for chosen_key in chosen_keys)

    def random_sample_generator(self, n=10):
        """
        A generator that yields one (key,value) tuple at a time,
        intended to avoid materializing all values before we return.
        
        Still materializes all the keys before starting to yield, 
        but that should only start to add up troublesome on many-gigabyte stores,
        and it might avoid some locking issues.
        """
        for key in self.random_keys(n=n):
            yield key, self.get( key )

    def random_values(self, n=10):
        """Returns a amount of values in a list, selected randomly.

        WARNING: this materializes the values, so this can be very large in RAM. 
        Consider using C{random_values_generator}, or using random_keys and get() one key at a time.
        """
        ret = []
        for _key, value in self.random_sample(n=n):
            ret.append(value)
        return ret

    def random_values_generator(self, n=10):
        """
        A generator that yields one value at a time,
        intended to avoid materializing all values before we return.

        Still materializes all the keys before starting to yield,
        but that should only start to add up troublesome on many-gigabyte stores,
        and it might avoid some locking issues.
        """
        for key in self.random_keys(n=n):
            yield self.get( key )


class MsgpackKV(LocalKV):
    """Like localKV but the value can be a nested python type (serialized via msgpack)

    Will be a bit slower because it's doing that on the fly,
    but lets you more transparently store things like nested python dicts
    ...but only of primitive types, and not e.g. datetime.

    Typing is fixed, to str:bytes

    msgpack is used as a somewhat faster alternative to json and pickle
    (though that overhead barely matters for smaller structures)

    Note that this does _not_ change how the meta table works.
    """

    def __init__(self, path, key_type=str, value_type=None, read_only=False):
        """value_type is ignored; I need to restructure this"""
        super().__init__( path, key_type=key_type, value_type=value_type, read_only=read_only )

        # this is meant to be able to detect/signal incorrect interpretation, not fully used yet
        if self._get_meta("valtype", missing_as_none=True) is None:
            self._put_meta("valtype", "msgpack")

    def get(self, key: str, missing_as_none=False):
        """Note that unpickling could fail

        Note also that you may wish to never explicitly store just None,
        and/or never use missing_as_none,
        unless you like ambiguity.
        """
        if missing_as_none:
            value = super().get(key, missing_as_none=True)
            if value is None:
                return None
            # else value is a still-packed value
        else:
            value = super().get(key, missing_as_none=False)  # may raise

        unpacked = msgpack.loads(value)
        return unpacked

    def put(self, key: str, value, commit: bool = True):
        "See LocalKV.put().   Unlike that, value is not checked for type, just serialized. Which can fail with an exception."
        packed = msgpack.dumps(value)
        super().put(key, packed, commit)

    def itervalues(self):
        curs = self.conn.cursor()
        for row in curs.execute("SELECT value FROM kv"):
            yield msgpack.loads(row[0], strict_map_key=False)

    def iteritems(self):
        curs = self.conn.cursor()
        for row in curs.execute("SELECT key, value FROM kv"):
            yield row[0], msgpack.loads(row[1], strict_map_key=False)


def cached_fetch(
    store: LocalKV,
    url: str,
    force_refetch: bool = False,
    sleep_sec: float = None,
    timeout: float = 20,
    maxsize_bytes=500*1024*1024,
    commit: bool = True,
) -> Tuple[bytes, bool]:
    """Helper to fetch URL contents into str-to-bytes (url-to-content) LocalKV store:
      - if URL is a key in the given store,
        fetch from the store and return its value
      - if URL is not a key in the store,
        do wetsuite.helpers.net.download(url),
        store in store,
        and return its value.
          - note that it will do a commit, unless you tell it not to.

    Arguably belongs in a mixin or such, but for now its usefulness puts it here.

    @param store:         a store to get/put data from
    @param url:           an URL string to fetch
    @param force_refetch: fetch even if we had it already
    @param sleep_sec:     sleep this long whenever we did an actual fetch
    (and not when we return data from cache), 
    so that when you use this in scraping, we can easily be nicer to a server.
    @param timeout:       timeout of te fetch
    @param maxsize_bytes: don't try to store something larger than this 
    (because SQLite may trip over it anyway), defaults to 500MiB
    @param commit:        whether to put() with an immediate commit 
    (False can help some faster bulk updates)
    @return:              (data:bytes, whether_it_came_from_cache:bool)

    May raise
      - whatever requests.get may raise (e.g. "timeout waiting for store" type things)
      - ValueError when networking says C{(not response.ok)}, or if the HTTP code is >=400
        (which is behaviour from wetsuite.helpers.net.download())
        ...to force us to deal with issues and not store error pages.
    """
    if not isinstance(store, LocalKV):
        raise TypeError(
            f"the store parameter should be a LocalKV or descendant, not {repr(type(store))}  (note that a reload(localdata) also causes this)"
        )

    if store.key_type not in (str, None) or store.value_type not in (bytes, None):
        raise TypeError(
            "cached_fetch() expects a str:bytes store (or for you to disable checks with None,None),  not a {repr(store.key_type.__name__)}:{repr(store.value_type.__name__)}"
        )
    # yes, the following could be a few lines shorter, but this is arguably a little more readable
    if force_refetch is False:
        try:  # use cache?
            ret = store.get(url)
            return ret, True
        except KeyError as exc:  # get() notices it's not there, so fetch it ourselves
            data = wetsuite.helpers.net.download(
                url,
                timeout=timeout
            )  # note that this can error out, which we don't handle
            if len( data ) > maxsize_bytes:
                raise ValueError(f"fetched data is huge ({len(data)} bytes), specify larger maxsize if you really want to store this") from exc
            store.put(url, data, commit=commit)
            if sleep_sec is not None:
                time.sleep(sleep_sec)
            return data, False
    else:  # force_refetch is True
        data = wetsuite.helpers.net.download(
            url,
            timeout=timeout
        )
        if len( data ) > maxsize_bytes:
            raise ValueError("Value is huge (%d bytes), specify larger maxsize if you really want this"%len(data))
        store.put(url, data, commit=commit)
        if sleep_sec is not None:
            time.sleep(sleep_sec)
        return data, False


def resolve_path(name: str):
    """Note: the KV classes call this internally.
    This is here less for you to use directly, more to explain how it works and why.

    For context, handing a pathless base name to underlying sqlite would just put it in the current directory
    which would often not be where you think, so is likely to sprinkle databases all over the place.
    This is common point of confusion/mistake around sqlite (and files in general),
    so we make it harder to do accidentally.

    Using this function makes it a little more controlled where things go:
        - Given a **bare name**, e.g. 'extracted.db', this returns an absolute path
            within a "this is where wetsuite keeps its stores directory" within your user profile,
            e.g. /home/myuser/.wetsuite/stores/extracted.db or C:\\Users\\myuser\\AppData\\Roaming\\.wetsuite\\stores\\extracted.db
            Most of the point is that handing in the same name will lead to opening the same store, regardless of details.

        - hand in **`:memory:`** if you wanted a memory-only store, not backed by disk

        - given an absolute path, it will use that as-is
            so if you actually _wanted_ it in the current directory, instead of this function
            consider something like  `os.path.abspath('mystore.db')`

        - given a relative path, it will pass that through -- which will open it relative to the current directory

    Notes:
        - should be idempotent, so shouldn't hurt to call this more than once on the same path
            (in that it _should_ always produce a path with os.sep (...or :memory: ...),
            which it would pass through the second time)

        - When you rely on the 'base name means it goes to a wetsuite directory',
            it is suggested that you use descriptive names (e.g. 'rechtspraaknl_extracted.db', not 'extracted.db')
            so that you don't open existing stores without meaning to.

        - us figuring out a place in your use profile for you
          This _is_ double-edged, though, in that we will get fair questions like
            - "I can't tell why my user profile is full" and
            - "I can't find my files"   (sorry, they're not so useful to access directly)

    CONSIDER:
        - listening to a WETSUITE_BASE_DIR to override our "put in user's homedir" behaviour,
          this might make more sense e.g. to point it at distributed storage without
          e.g. you having to do symlink juggling

    @param name: the name or path to inrepret
    @return: a more resolved path, as described above
    """
    # deal with pathlib arguments by flattening it to a string
    if isinstance(name, pathlib.Path):
        name = str(name)

    if (
        name == ":memory:"
    ):  # special-case the sqlite value of ':memory:' (pass it through)
        return name
    elif (
        os.sep in name
    ):  # assume it's an absolute path, or a relative one you _want_ resolved relative to cwd
        return name
    else:  # bare name, do our "put in homedir" logic
        dirs = wetsuite.helpers.util.wetsuite_dir()
        return os.path.join(dirs["stores_dir"], name)


def list_stores(
    skip_table_check: bool = True, get_num_items: bool = False, look_under=None
):
    """Checks a directory for files that seem to be our stores, also lists some basic details about it.
    
    Does filesystem access and IO reading to do so,
    and with some parameter combinations will fail to open currently write-locked databases.

    By default look in the directory that (everything that uses) resolve_path() puts things in,
    you can give it another directory to look in.

    Will only look at direct contents of that directory.

    @param skip_table_check: if true, only tests whether it's a sqlite file, not whether it contains the table we expect.
    because when it's in the stores directory, chances are we put it there, and we can avoid IO and locking.

    @param get_num_items: does not by default get the number of items, because that can need a bunch of IO, and locking.

    @param look_under: a dict with details for each store

    @return: a dict with details for each store, like::
        {
            'path': '/home/example/.wetsuite/stores/thing.db',
            'basename': 'thing.db',
            'size_bytes': 40980480,
            'size_readable': '41M',
            'description': None
        },
    """
    ret = []

    if look_under is None:
        dirs = wetsuite.helpers.util.wetsuite_dir()
        look_under = dirs["stores_dir"]

    for basename in os.listdir(look_under):
        abspath = os.path.join(look_under, basename)
        if os.path.isfile(abspath):
            if is_file_a_store(abspath, skip_table_check=skip_table_check):
                kv = LocalKV(abspath, key_type=None, value_type=None, read_only=True)
                itemdict = {
                    "path": abspath,  # should be the same as kv.path ?
                    "basename": basename,  # should be the same as os.path.basename( kv.path ) ?
                }
                itemdict.update(kv.summary(get_num_items=get_num_items))

                try:
                    itemdict["valtype"] = kv._get_meta( # pylint: disable=protected-access
                        "valtype"
                    )
                except KeyError:
                    pass

                itemdict["description"] = kv._get_meta( # pylint: disable=protected-access
                    "description", True
                )
                ret.append(itemdict)
                kv.close()
    return ret


def is_file_a_store(path, skip_table_check: bool = False):
    """Checks that the path seems to point to one of our stores.
    More specifailly: whether it is an sqlite(3) database, and has a table called 'kv'

    You can skip the latter test. It avoids opening the file, so avoids a possible timeout on someone else having the store open for writing.

    @param path: the filesystem path to test
    @param skip_table_check: don't check for the right table name, e.g. to make it faster or avoid opening a store
    @return: Whether it seems like a store we could open
    """
    if not os.path.isfile(path):
        return False

    is_sqlite3 = None
    with open(path, "rb") as f:
        is_sqlite3 = f.read(15) == b"SQLite format 3"  # check file magic
    if not is_sqlite3:
        return False

    if skip_table_check:
        return True  # good enough for us, then

    has_kv_table = None
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("SELECT name  FROM sqlite_master  WHERE type='table'")
    for (tablename,) in curs.fetchall():
        if tablename == "kv":
            has_kv_table = True
    conn.close()
    return has_kv_table
