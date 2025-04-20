#!/usr/bin/python3
"""
    Talks to SRU repositories, mainly underlies L{koop_sru}

    SRU is a search-and-retrieve protocol; 
    to dig more into the what and how to use this in a more advanced way,
    look for the sru-related notebook (somewhere in extras).

    Very minimal SRU implementationm and not meant to be a generic implementation. 

    It was written because existing python SRU libraries we tried didn't seem to like
    the apparently-custom URL component (x-connection) that the KOOP rpositories use, 
    so until we figure out a clean solution, 
    here's a just-enough-to-work implementation for our specific use cases.
"""
# https://www.loc.gov/standards/sru/sru-1-1.html

import time
import sys

import requests

import wetsuite.helpers.escape
import wetsuite.helpers.etree


# TODO: centralize parsing of originalData / enrichedData as much as we can,
#       so that each individual use doesn't have to.


class SRUBase:
    """Very minimal SRU implementation - just enough to access the KOOP repositories.

    @ivar base_url: The base URL that other things add to; added from instantiation.
    @ivar x_connection: The x_connection attribute that some of these need; 
    added from instantiation.
    @ivar sru_version: hardcoded to "1.2"
    @ivar extra_query: extra piece of query to add to the quiery you do late.
    This lets us representing subsets of larger repositories.
    @ivar number_of_records: the number of results reported in the last query we did.
    None before you do a query. CONSIDER: changing that.
    @ivar verbose: whether to print out things while we do them.
    """

    def __init__(
        self,
        base_url: str,
        x_connection: str = None,
        extra_query: str = None,
        verbose=False,
    ):
        """
        @param base_url: The base URL that other things add to. Basically everything up to the '?'
        @param x_connection: an attribute that some of these need in the URL. 
        Seems to be non-standard and required for these repos.
        @param extra_query: is used to let us AND something into the query, 
        and is intended to restrict to a subset of documents. 
        This lets us representing subsets of larger repositories (somewhat related to x_connection).
        @param verbose: whether to print out things while we do them.
        """
        self.base_url = base_url
        self.x_connection = x_connection
        self.sru_version = "1.2"
        self.extra_query = extra_query
        self.verbose = verbose
        self.number_of_records = None  # hackish, TODO: rethink

    def _url(self):
        """
        Combines the basic URL parts given to the constructor, and ensures there's a ?
        (so you know you can add &k=v)
        This can probably go into the constructor, when I know how much is constant across SRU URLs
        """
        ret = self.base_url
        if "?" not in ret:
            ret += "?"
        # escape.uri_dict might be a little clearer/cleaner
        if self.sru_version not in ("", None):
            ret += "&version=%s" % self.sru_version
        if self.x_connection not in ("", None):
            ret += "&x-connection=%s" % wetsuite.helpers.escape.uri_component(
                self.x_connection
            )
        return ret

    def explain(self, readable=True, strip_namespaces=True, timeout=10):
        """
        Does an explain operation,
        Returns the XML
          - if readable==False, it returns it as-is
          - if readable==True (default), it will ease human readability:
            - strips namespaces
            - reindent
        The XML is a unicode string (for consistency with other parts of this codebase)
        """
        url = self._url()
        url += "&operation=explain"
        r = requests.get(url, timeout=timeout)

        if readable:
            tree = wetsuite.helpers.etree.fromstring(r.content)
            if strip_namespaces is True:
                tree = wetsuite.helpers.etree.strip_namespace(
                    tree
                )  # easier without namespaces
            tree = wetsuite.helpers.etree.indent(tree)
            return wetsuite.helpers.etree.tostring(tree, encoding="unicode")
        else:
            return r.content.decode("utf-8")

    def explain_parsed(self, timeout=10):
        """
        Does an explain operation,
        Returns a dict with some of the more interesting details.

        TODO: actually read the standard instead of assuming things.
        """
        url = self._url()
        url += "&operation=explain"

        ret = {"explain_url": url}

        if self.verbose:
            print(url)
        r = requests.get(url, timeout=timeout)
        tree = wetsuite.helpers.etree.fromstring(r.content)
        tree = wetsuite.helpers.etree.strip_namespace(tree)  # easier without namespaces

        explain = tree.find("record/recordData/explain")

        def get_attrtext(treenode, name, attr):
            """ under etree object :treenode:, 
                find a node called :name:,
                and get the value of its :attr: attribute
            """
            if treenode is not None:
                node = treenode.find(name)
                if node is not None:
                    return name, attr, node.get(attr)

        def get_nodetext(treenode, name):
            """ under etree object :treenode:, 
                find a node called :name:,
                and get the inital text under it
            """
            if treenode is not None:
                node = treenode.find(name)
                if node is not None:
                    return node.text
            return None

        for treenode, name, attr in (
            (explain.find("serverInfo"), "database", "numRecs"),
        ):
            name, attr, val = get_attrtext(treenode, name, attr)
            ret[f"{name}/{attr}"] = val

        for treenode, name in (  # TODO: make this more complete
            (explain.find("serverInfo"), "host"),
            (explain.find("serverInfo"), "port"),
            (explain.find("databaseInfo"), "title"),
            (explain.find("databaseInfo"), "description"),
            (explain.find("databaseInfo"), "extent"),
        ):
            val = get_nodetext(treenode, name)
            ret[name] = val

        indices, sets = [], []
        index_info = explain.find("indexInfo")
        for index in index_info.findall("index"):
            map_elem = index.find("map")
            name = map_elem.find("name")
            set_attr = name.get("set")
            val = name.text
            indices.append((set_attr, val))

        for set_attr in index_info.findall("set"):
            name = set_attr.get("name")
            identifier = set_attr.get("identifier")
            title = None
            if set_attr.find("title") is not None:
                title = set_attr.find("title").text
            sets.append((name, identifier, title))

        ret["indices"] = indices
        ret["sets"] = sets
        return ret

    def num_records(self):
        """
        After you do a search_retrieve, this should be set to a number.

        This function may change.
        """
        if self.number_of_records is None:
            raise ValueError("num_records is not filled in before you do a search")
        return self.number_of_records

    def search_retrieve(
        self,
        query: str,
        start_record=None,
        maximum_records=None,
        callback=None,
        verbose=False,
    ):
        """
        Fetches a range of results for a particular query.
        Returns each result record as a separate ElementTree object.

        Exactly what each record contains will vary per repository,
        sometimes even per presumably-sensible-subset of records,
        but you may well _want_ access to this detail in raw form
        because in some cases, it can contain metadata not as easily fetched
        from the result documents themselves.

        You mat want to fish out the number of results (TODO: make that easier)

        Notes:
          - strips namespaces from the results - makes writing code more convenient


        CONSIDER:
          - option to returning URL instead of searching

        @param query: the query string, in CQL form (see the Library of Congress spec)
        the list of indices you can search in (e.g. e.g. 'dcterms.modified>=2000-01-01')
        varies with each repo take a look at explain_parsed() (a parsed summary)
        or explain() (the actual explain XML)
        @param start_record: what record offset to start fetching at. Note: one-based counting
        @param maximum_records: how many records to fetch (from start_offset).
        Note that repositories may not like high values here.
        ...so if you care about _all_ results of a possible-large set,
        then you probably want to use search_retrieve_many() instead.
        @param callback: if not None, this function calls it for each such record node.
        You can instead wait for the entire range of fetches to conclude
        and hand you the complete list of result records.
        @param verbose: whether to be even more verbose during this query
        """

        if self.extra_query is not None:
            query = "%s and %s" % (self.extra_query, query)

        url = self._url()
        url += "&operation=searchRetrieve"

        if start_record is not None:
            url += "&startRecord=%d" % start_record
        if maximum_records is not None:
            url += "&maximumRecords=%d" % maximum_records

        url += "&query=%s" % wetsuite.helpers.escape.uri_component(query)

        if self.verbose:
            print("[SRU searchRetrieve] fetching %r" % url)

        try:
            r = requests.get(url, timeout=(20, 20))  # CONSIDER: use general fetcher?
        except requests.exceptions.ReadTimeout:
            r = requests.get(
                url, timeout=(20, 20)
            )  # TODO: this makes no sense, don't do it

        # The following two seem the most likely errors, report them a little bit more clearly.
        if r.status_code == 500:
            raise ValueError(
                "SRU server reported an Internal Server Error (HTTP status 500) for %r"
                % url
            )
            # raise RuntimeError( "SRU server reported an Internal Server Error (HTTP status 500) for %r"%url )

        if r.status_code == 503:
            # also comes with HTML body (that won't parse as XML)
            raise ValueError(
                "SRU server reported an Service Unavailable (HTTP status 503) for %r"
                % url
            )

        try:
            tree = wetsuite.helpers.etree.fromstring(r.content)
        except Exception:
            print(r.status_code)
            print(r.content)  # error response is probably a    b'<!DOCTYPE html>\n<html>\n  
            raise

        # easier without namespaces, they serve no disambiguating function in most of these cases anyway
        # TODO: think about that, user code may not expact that
        tree = wetsuite.helpers.etree.strip_namespace(tree)

        # TODO: it seems some errors messages are actually incorrect XML; figure out whether we want to handle that

        if tree.tag == "diagnostics":  # TODO: figure out if this actually happened
            raise RuntimeError(
                "SRU server said: "+
                wetsuite.helpers.etree.strip_namespace(tree)
                .find("diagnostic/message")
                .text
            )
        elif tree.find("diagnostics") is not None:
            raise RuntimeError(
                "SRU server said: "+
                wetsuite.helpers.etree.strip_namespace(tree)
                .find("diagnostics/diagnostic/message")
                .text
            )

        elif tree.tag == "explainResponse":
            tree = wetsuite.helpers.etree.strip_namespace(tree)  # bit lazy
            raise RuntimeError("SRU search returned explain response instead")

        if verbose:
            print(
                wetsuite.helpers.etree.tostring(
                    wetsuite.helpers.etree.indent(tree)
                ).decode("u8")
            )

        self.number_of_records = int(tree.find("numberOfRecords").text)
        if verbose:
            print("numberOfRecords:", self.number_of_records, file=sys.stderr)

        ret = []
        for record in tree.findall("records/record"):
            ret.append(record)
            if callback is not None:
                callback(
                    record
                )  # CONSIDER: callback( record, query )  and possibly pas other things
        return ret  # maybe return list, like _many does?

    def search_retrieve_many(
        self,
        query: str,
        at_a_time: int = 10,
        start_record: int = 1,
        up_to: int = 250,
        callback=None,
        wait_between_sec: float = 0.5,
        verbose: bool = False,
    ):
        """This function builds on search_retrieve() to "fetch _many_ results results in chunks",
        by calling search_retrieve() repeatedly.
        
        (search_retrieve() will have a limit on how many to search at once,
        though is still useful to see e.g. if there are results at all)

        Like search_retrieve, it (eventually) returns each result record as an elementTree objects,
        (this can be more convenient if you an to handle the results as a whole)
         
        ...and if callback is not None,
        this will be called on each result _during_ the fetching process.
        (this can be more convenient way of dealing with many results while they come in)

        @param query:        like in search_retrieve()
        @param start_record: like in search_retrieve()
        @param callback:     like in search_retrieve()
        @param up_to:        is the last record to fetch - as an absolute offset, 
        so e.g. start_offset=200,up_to=250 gives you records 200..250,  not 200..450.
        @param at_a_time:        
        how many records to fetch in a single request
        @param wait_between_sec: a backoff sleep between each search request, 
        to avoid hammering a server too much.
        you can lower this where you know this is overly cautious
        note that we skip this sleep if one fetch was enough
        @param verbose: whether to be even more verbose during this query

        since we fetch in chunks, we may overshoot in the last fetch, 
        by up to at_a_time amount of entries.
        The code should avoid returning those.

        CONSIDER:
          - maybe yield something including numberOfRecords before yielding results?
        """
        ret = []
        current_offset = start_record

        while True:  # offset < up_to:
            records = self.search_retrieve(
                query=query,
                start_record=current_offset,
                maximum_records=at_a_time,
                callback=None,
                verbose=verbose,
            )
            if len(records) == 0:
                break

            for fetched_chunk_offset, record in enumerate(records):
                # add to what we will return
                ret.append(record)

                #if you requested a callback do it.
                if callback is not None:
                    callback(record)

                # stop at the requested record amount,
                #   even if the chunk fetcked more due to at_a_time
                if current_offset + fetched_chunk_offset >= up_to:
                    break # then stop

            current_offset += at_a_time

            # crossed beyond what was asked for?  (we don't return it even if we fetched it)
            if current_offset >= up_to:
                break

            # crossed beyond what exists in the search result?
            if self.number_of_records is not None and current_offset > self.number_of_records:
                break

            # (note that this is avoided if the first, single fetch was enough)
            time.sleep( wait_between_sec )

        return ret
