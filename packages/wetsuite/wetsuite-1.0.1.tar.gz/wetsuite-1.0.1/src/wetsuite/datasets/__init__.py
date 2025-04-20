#!/usr/bin/python3
"""
Fetch and load already-created datasets that we provide. (to see a list of actual datasets, look for the wetsuite_datasets.ipynb notebook)

As this is often structured data, each dataset may work a little differently, 
so there is an describe() to get you started, that each dataset should fill out.

TODO: 
  - If we want updateable datasets (right now there is no plan for that), 
    think more about the robustness around re-fetching indices.
    Decide it's cheap enough to fetch each time? (but fall back onto stored?)
"""

import sys
import os
import re
import json
import time
import tempfile
import bz2
import fnmatch
import shutil
import lzma  # standard library since py3.3, before that we could fall back to backports.lzma
import zipfile

import wetsuite.helpers.util
import wetsuite.helpers.net
import wetsuite.helpers.strings
import wetsuite.helpers.date
import wetsuite.helpers.localdata
import wetsuite.helpers.notebook


### Index of current datasets
#
# early versions had a hardcoded index here, which is a bad idea for a few reasons,
# but largely because we cannot fix the fact that code versions link to things that no longer exist.
#
# The better intermediate was hosting that contained the data files,
# and automatically generated an index alongside it.
# The index is always live, and never goes out of sync with the data for more than a few minutes,
# won't contain mistakes/typos.
# Something with such properties is best when the data will regularly change.
#
# Then we looked for hosting that would last beyond the project. Right now that means ReearchDrive,
# an ownCloud instance from SurfSara, which implies download links will be based on content hashes
# IF/WHEN the data and/or this code will ever change again, then this setup is far from ideal,
# because it is easy for links to change, and more manual care is necessary
# because the the index ''must'' still be kept up to date,
# and also cannot be stored in either this code (back to early breakage), OR in that that owncloud instance
# (because _its_ link would also change, so most of our library versions would be broken).

# Long story short, for now the index is still stored on a VPS not technically related to the project.

_INDEX_URL = "https://wetsuite.knobs-dials.com/datasets/index.json"
_index_data = None  # should be None at first, and a dict once loaded
_index_fetch_time = 0
_index_fetch_no_more_often_than_sec = 600



def fetch_index():
    """Index is expected to be a list of dicts, each with keys including
      - C{url}
      - C{version}             (should probably become semver)
      - C{description_short}   one-line summary of what this is
      - C{description}         longer description, perhaps with some example data
      - C{download_size}       how much transfer you'll need
      - C{real_size}           Disk storage we expect to need once decompressed
      - C{download_size_human}, real_size_human: more readable version,
        e.g. where C{real_size} might be the integer 397740, C{real_size_human} would be 388KiB
      - C{type}                content type of dataset

    TODO: an example

    CONSIDER: keep hosting generic (HTTP fetch?) so that any hoster will do.
    """
    global _index_data, _index_data, _index_fetch_time

    if (
        _index_data is None
        or time.time() - _index_fetch_time > _index_fetch_no_more_often_than_sec
    ):
        # print('FETCHING INDEX')
        # try:
        _fetched_data = wetsuite.helpers.net.download(_INDEX_URL) # this could raise
        _index_data = json.loads(_fetched_data)
        # print("Fetched index")
        _index_fetch_time = time.time()
        # except Exception:
        #    raise
    # else:
    #    print('CACHED INDEX')
    return _index_data


def list_datasets():
    """
    Fetch index, report dataset names _only_.
    If you also want the details,
    see C{fetch_index} if you care about the data form,
    or C{print_dataset_summary} if want it printed on the console/notebook output.

    @return: a list of strings, e.g. ['bwb-mostrecent-xml','woo_besluiten_docs_text']
    """
    fetch_index()
    return sorted(_index_data.keys())
    # return list( _index.items() )


def print_dataset_summary():
    """
    Print short summary per dataset, on stdout.
    A little more to go on than just the names from list_datasets(),
    a little less work than shifting through the dicts for each yourself,
    but only useful in notebooks or from the console
    """
    for name, details in fetch_index().items():
        real_size_human = details.get("real_size_human")
        print(
            f"{name:<40}\t{real_size_human:>8s}\t{details.get('description_short','').strip()}"
        )


def description(dataset_name: str):
    """
    Fetch the description field, for a specifically named dataset. 
    Simple, but less typing than picking it out yourself.
    """
    return fetch_index()[dataset_name].get("description", "")


class Dataset:
    """
    If you're looking for details about the specific dataset, look at the .description

    This classis mostly meant to be instantiated by load(),
    not by you - it's the thinnest of wrapper classes so you probably wouldn't care to.

    This class is provisional and likely to change. Right now it does little more than
      - put a description into a .description attribute
      - put data into .data attribute
        without even saying what that is
        though it's probably an interable giving individually useful things,
        and be able to tell you its len()gth
        ...also so that it's harder to accidentally dump gigabytes of text to your console.

    This is not the part that does the interpretation.
    This just contains its results.
    """

    def __init__(self, description: str, data, name: str = ""):
        """@param description: A description that load() would lift from the underlying data.
        @param data: A reference to the main data, that load() would load from the underlying data.
        @param name: a name that would be printed into str() representation. Usually set by load().
        """
        # for key in self.data:
        #    setattr(self, key, self.data[key])
        # the above seems powerful but potentially iffy, so for now:
        self.data = data
        self.description = description
        self.name = name
        self.num_items = len(self.data)  # TODO: don't rely on that being possible.

    def __str__(self):
        "String representation that mentions the name and the number of items"
        return "<wetsuite.datasets.Dataset name=%r num_items=%r>" % (
            self.name,
            self.num_items,
        )

    def export_files(self, in_dir_path=None, to_zipfile_path=None):
        """
        Try to export each item to a file, 
        for people who want to continue working on data elsewhere.

        Mostly useful when the dataset actually _does_ store one file (bytes object) per item.
        For other underlying types we might do some conversion, e.g. dict becomes JSON.
        We estimate the file extension it should have.
        """

        if to_zipfile_path is not None:
            if os.path.exists(to_zipfile_path):
                raise RuntimeError(
                    "Target ZIP file (%r) already exists. Please rename or remove it."
                    % to_zipfile_path
                )
            zob = zipfile.ZipFile(
                to_zipfile_path, "a", compression=zipfile.ZIP_DEFLATED, allowZip64=True
            )

        if in_dir_path is not None:
            if not os.path.exists(in_dir_path):
                os.mkdir(in_dir_path)

        if in_dir_path is None and to_zipfile_path is None:
            raise ValueError("Specify either in_dir_path or to_zipfile_path.")

        i = 0
        for key, value in self.data.items():
            i += 1
            # if i > 200:
            #    break

            ## figure out bytes to store,    also estimate decent file extension from the content
            if isinstance(value, bytes):
                if b"<?xml" in value[:50]:
                    typ = "xml"
                else:
                    typ = "bin"
            elif isinstance(value, dict):
                typ = "json"  # assumption based on what datasets we currently provide, may not keep in the future
                value = json.dumps(value).encode("u8")
            elif isinstance(value, str):
                typ = "txt"
                value = value.encode("u8")
            else:
                raise ValueError("Do not know what to do with %r" % type(value))

            safe_fn = (
                "%08d_%s__%s.%s"
                % (
                    i,  # for uniqueness
                    wetsuite.helpers.util.hash_hex(key)[
                        :12
                    ],  # likely to make it unique even without that counter
                    re.sub("[^A-Za-z0-9_-]", "", re.sub("[.:/]+", "-", key))[
                        :220
                    ],  # not for uniqueness, but for some indication of what this is. Primarily aimed at URLs
                    typ[:5],
                )[:254]
            )

            ## write out
            if in_dir_path is not None:
                ffn = os.path.join(in_dir_path, safe_fn)

                if os.path.exists(ffn):
                    raise IOError(
                        "You probably did not mean to overwrite %r, please remove anything existing before retrying. "
                        % ffn
                    )
                # implied else: either it doesn't exist, or overwrite==True

                with open(ffn, "wb") as f:
                    f.write(value)

            if to_zipfile_path is not None:
                # note: for content you know won't compress well,
                # you can save some time with compress_type=zipfile.ZIP_STORED
                zob.writestr(safe_fn, value)

        if to_zipfile_path is not None:
            zob.close()


def _data_from_path(data_path):
    """Given a path to a data file,
    return the data in python-object form -- and and description (based on contents).
    This wraps opening and dealing with file type, and separates that from the download phase.
    """
    f = open(data_path, "rb")
    first_bytes = f.read(15)
    f.seek(0)

    if first_bytes == b"SQLite format 3":
        f.close()

        # the type enforcement is irrelevant when opened read-only
        data = wetsuite.helpers.localdata.LocalKV(data_path, None, None, read_only=True)

        ret_description = data._get_meta(
            "description", missing_as_none=True
        )  # pylint: disable=protected-access
        # This seems very hackish - TODO: avoid this
        if (
            data._get_meta("valtype", missing_as_none=True) == "msgpack"
        ):  # pylint: disable=protected-access
            data.close()
            data = wetsuite.helpers.localdata.MsgpackKV(
                data_path, None, None, read_only=True
            )

    elif first_bytes.strip().startswith(
        b"{"
    ):  # Assume that's a decent indicator of JSON (given that our downloads aren't a lot of different things)
        # expected to be a dict with two main keys, 'data' and 'description'
        loaded = json.loads(f.read())
        f.close()

        # TODO: remove the need for JSON, or at least make this alternative go away
        #       ...by being more consistent in dataset generation
        if "description" in loaded:
            data = loaded.get("data")
            ret_description = loaded.get("description")
        else:
            raise ValueError("This JSON does not have the structure we expect.")
    else:
        f.close()
        raise ValueError(
            "Don't know how to deal with file called %r  that starts with %r"
            % (os.path.basename(data_path), first_bytes)
        )

    return (data, ret_description)


def _load_bare(
    dataset_name: str, verbose=None, force_refetch=False, check_free_space=True
):
    """Takes a dataset name (that you learned of from the index),
    Downloads it if necessary - after the first time it's cached in your home directory

    If compressed, will uncompress.
    Does not think about the type of data

    Note: You normally would use load(),
    which takes the same name but gives you a usable object, instead of just a filename.

    @return: the filename we fetched to
    """
    global _index_data
    if _index_data is None:
        _index_data = fetch_index()

    if verbose is None:
        # even when not asked, show some extra feedback -- (only) if we are in an itneractive setting
        verbose = wetsuite.helpers.notebook.is_interactive()

    if dataset_name not in _index_data:
        raise ValueError("Do not know dataset name %r" % dataset_name)

    dir_dict = wetsuite.helpers.util.wetsuite_dir()
    ws_dir = dir_dict["wetsuite_dir"]
    datasets_dir = dir_dict["datasets_dir"]

    ## figure out path in that directory
    dataset_details = _index_data[dataset_name]
    data_url = dataset_details["url"]
    # quick and dirty way to get a safe filename regardless of index contents
    location_hash = wetsuite.helpers.util.hash_hex(data_url.encode("utf8"))
    # CONSIDER: using dataset_name instead of location_hash
    #   (BUT that would mean restricting the characters allowed in there)
    data_path = os.path.join(datasets_dir, location_hash)
    # right now the data_path is a single file per dataset, expected to be a JSON file.
    # TODO: decide on whether that is our standard, or needs changing

    if check_free_space:
        ds = dataset_details["download_size"]
        rs = dataset_details["real_size"]
        if (
            ds != rs
        ):  # assume that we will need to store both the compressed and uncompressed size, if only for a moment
            needed_space_byteamt = ds + rs
        else:  # assume ds==rs means it's not compressed, and we download it into place
            needed_space_byteamt = ds
        free_space_byteamt = wetsuite.helpers.util.free_space(path=datasets_dir)
        if needed_space_byteamt > free_space_byteamt:
            mebibyte = 1024 * 1024
            raise IOError(
                "To fetch %r we would need %.1f MiByte free. We have only %.1f MiByte in the directory we would place it."
                % (
                    dataset_name,
                    needed_space_byteamt / mebibyte,
                    free_space_byteamt / mebibyte,
                )
            )

    # If we don't have it in our cache, or a re-fetch was forced, then download it.
    if force_refetch or not os.path.exists(data_path):
        if verbose:
            print("Downloading %r to %r" % (data_url, data_path), file=sys.stderr)

        # CONSIDER: using context manager variant if that's cleaner
        tmp_handle, tmp_path = tempfile.mkstemp(
            prefix="tmp_dataset_download", dir=ws_dir
        )
        os.close(
            tmp_handle
        )  # the open file handle is fairly secure, but here we only care about a non-clashing filename

        # download it to that temporary filename
        wetsuite.helpers.net.download(
            data_url, tofile_path=tmp_path, show_progress=verbose
        )

        ## if it was compressed, decompress it in the cache -
        # as part of the download, not the load compressed into its fina place.
        # There is a race condition in multiple loads() of the same thing. 
        # CONSIDER: fixing that via a second temporary file
        # CONSIDER: it may be preferable to store it compressed, and decompress every load. 
        #           Or at least make this a parameter
        def decompress_stream(instream, outstream):
            # TODO: allowing a "we know the output size" argument to decompress_stream so we can show a percentage
            uncompressed_data_bytes = 0
            while True:
                data = instream.read(2 * 1048576)
                if len(data) == 0:
                    break
                outstream.write(data)
                uncompressed_data_bytes += len(data)
                if verbose:
                    print(
                        "\rDecompressing... %3sB    "
                        % (
                            wetsuite.helpers.format.kmgtp(
                                uncompressed_data_bytes, kilo=1024
                            ),
                        ),
                        end="",
                        file=sys.stderr,
                    )
            if verbose:
                print("", file=sys.stderr)

        if data_url.endswith(".xz"):  # or file magic, b'\xfd7zXZ\x00\x00'
            with lzma.open(tmp_path) as compressed_file_object:
                with open(data_path, "wb") as write_file_object:
                    decompress_stream(compressed_file_object, write_file_object)
            os.unlink(tmp_path)

        elif data_url.endswith(".bz2"):
            # print('Decompressing...', file=sys.stderr)
            with bz2.BZ2File(tmp_path, "rb") as compressed_file_object:
                with open(data_path, "wb") as write_file_object:
                    decompress_stream(compressed_file_object, write_file_object)
            print("  done.", file=sys.stderr)
            os.unlink(tmp_path)

        # CONSIDER: add gz and zip cases, because they're standard library anyway

        else:  # assume it was uncompressed, just move it into place
            shutil.move(tmp_path, data_path) # os.rename would fail if it's not the same filesystem

    return data_path


def load(dataset_name: str, verbose=None, force_refetch=False, check_free_space=True):
    """Takes a dataset name (that you learned of from the index),
    downloads it if necessary - after the first time it's cached in your home directory

    Wraps _load_bare, which does most of the heavy lifting.

    This primarily adds what is necessary to load that downloaded thing
    and give it to you as a usable Dataset object

    @param verbose: tells you more about the download (on stderr)
    Can be given True or False.
    By default (None), we try to detect whether we are in an interactive context,
    and print only if we are.

    @param force_refetch: whether to remove the current contents before fetching
    dataset naming should prevent the need for this (except if you're the wetsuite programmer)

    @return: a Dataset object - which is a container object with little more than
      - a C{.description} (a string)
      - a C{.data} member, some kind of iterable of items.
        The .description should mention what .data will contain
        and should give an example of how to use it.
    """
    # CONSIDER: have load('datasetname-*') automatically merge_datasets,
    # one for each matched datasets, with an attribute named for the last bit of the dataset name.
    # However, this only makes sense if dataset convention _and_ dataset naming convention are always considered,
    # so maybe the benefit is not enough here.
    # CONSIDER: giving up on that idea, which also lets us remove some code below

    # if '*' in dataset_name:
    global _index_data
    if _index_data is None:
        _index_data = fetch_index()
    all_dataset_names = list(_index_data.keys())

    dataname_matches = fnmatch.filter(all_dataset_names, dataset_name)
    if len(dataname_matches) == 0:
        closest_names = wetsuite.helpers.strings.ngram_sort_by_matches(dataset_name, all_dataset_names)
        raise ValueError(
            "No exact match for dataset name %r. Options include (sorted by similarity): %r"
            % (
                dataset_name,
               ", ".join(closest_names)
            )
        )
        # CONSIDER: noting closest match (n-gram style)

    elif len(dataname_matches) == 1:
        data_path = _load_bare(
            dataname_matches[0],
            verbose=verbose,
            force_refetch=force_refetch,
            check_free_space=check_free_space,
        )
        data, description = _data_from_path(data_path)
        # data_path = _load_bare( dataset_name=dataname_matches[0] )
        return Dataset(data=data, description=description, name=dataname_matches[0])

    else:  # implied  >=1
        raise ValueError(
            "Your dataset pattern %r matched %d of %s. We might give you a merger in the future, but right now, choose more specifically."
            % (dataset_name, len(dataname_matches), ", ".join(all_dataset_names))
        )


def generated_today_text():
    """Used when generating datasets
    @return: a string like 'This dataset was generated on 2024-02-02'
    """
    return "This dataset was generated on %s" % (
        wetsuite.helpers.date.date_today().strftime("%Y-%m-%d")
    )
