"""
    Code that accesses the https://repository.overheid.nl/frbr/ data in a bulk way.
    ...pending removal.
    
    It's not a viable route to download a lot of data 
    In particular the SRU interface seems to link to most of this and provide an actual search and filtering interface
    ...though it is perhaps a better route towards "the set of files for a single ID" more than BUS is.
"""

import time
import random
import urllib

import bs4
import requests

import wetsuite.helpers.net
import wetsuite.helpers.localdata
import wetsuite.helpers.koop_parse


class FRBRFetcher:
    """Helper class to fetch data from an area of https://repository.overheid.nl/frbr/
    See the constructor's docstring for more.
    In theory we could use the bulk service to do functionally the same,
    which is more efficient for both sides,
    yet almost no SSH tool seems to be able to negotiate with the way they configured it
    (SFTP imitating anonymous FTP, which is a grea idea in theory).
    """

    def __init__(self, fetch_store, cache_store, verbose=True, waittime_sec=1.0):
        """Hand in two LocalKV-style stores: 
        - one that the documents will get fetched into (almost all useful content), 
        - one that the intermediate folders get fetched into (mostly pointless outside of this fetcher)
        
        After this you will want to
          - hand in a starting point like::
              fetcher.add_page( 'https://repository.overheid.nl/frbr/cga?start=1' )
          - use fetcher.work() to start it fetching.
              - work() is a generator function that tries to frequently return,
              so that you can read out some "what have we done" ( see .count_* )
              - if you just want it to do things until it's done,
              you can do `list( fetcher.work() )`
        Will only go deeper from the starting page you give it.
        @param fetch_store:
        @param cache_store:
        @param verbose:
        @param waittime_sec: How long to sleep after every actual network fetch, to be nicer to the servers.
        """
        self.fetch_store = fetch_store
        self.cache_store = cache_store
        self.verbose = int(verbose)
        self.to_fetch_pages = set()
        self.to_fetch_folders = set()
        self.fetched = {}  # url -> True
        self.waittime_sec = waittime_sec
        self.count_fetches = 0
        self.count_cacheds = 0
        self.count_items = 0
        self.count_folders = 0
        self.count_pages = 0
        self.count_dupadd = 0
        self.count_skipped = 0
        self.count_errors = 0

    def uncached_fetch(self, url, retries=3):
        "Unconditional fetch from an URL"
        # print("UFETCH", url)
        while retries > 0:
            try:
                self.count_fetches += 1
                data = wetsuite.helpers.net.download(url)
                time.sleep(self.waittime_sec)
                return data
            except requests.exceptions.Timeout:
                if self.verbose >= 2:
                    print(
                        f"U TRYAGAIN {str(retries)}"
                    )  # trying again just once 'fixes' most cases
                retries -= 1
                time.sleep(max(2, self.waittime_sec))

    def cached_folder_fetch(self, url, retries=3):
        "cache-backed fetch  (from the first one you handed into the constructor)"
        retries = max(1, retries)
        while retries > 0:
            try:
                bytedata, came_from_cache = wetsuite.helpers.localdata.cached_fetch(
                    self.cache_store, url
                )
                if came_from_cache:
                    self.count_cacheds += 1
                    # if self.verbose:
                    # print("CFETCH_CACHED", url)
                else:
                    self.count_fetches += 1
                    # if self.verbose:
                    # print("CFETCH_FETCHED", url)
                    time.sleep(self.waittime_sec)
                return bytedata
            except requests.exceptions.Timeout:
                if self.verbose >= 2:
                    print(
                        f"C TRYAGAIN {retries}"
                    )  # trying again just once 'fixes' most cases
                retries -= 1
                time.sleep(1)
            # except urllib3.exceptions.ReadTimeoutError
        raise ValueError("Didn't manage to download")

    def add_page(self, page_url):
        """add an URL to an internal "pages to still look at" set
        (unless it was previously added / fetched)
        Mostly intended to be used by handle_url()
        """
        if page_url not in self.fetched:
            if self.verbose >= 1:
                print("ADD_PAGE", page_url)
            self.to_fetch_pages.add(page_url)

    def add_folder(self, folder_url):
        """add an URL to an internal "folders to still look at" set
        (unless it was previously added / fetched)
        Mostly intended to be used by handle_url()
        """
        if folder_url not in self.fetched:
            if self.verbose >= 2:
                print("ADD_FOL", folder_url)
            self.to_fetch_folders.add(folder_url)

    def handle_url(self, h_url, is_folder=False):
        """handle a URL that should be what we consider either a page or folder"""
        if is_folder:
            pagebytes = self.cached_folder_fetch(h_url)
            if pagebytes is None:
                print("\nERR cached_folder_fetch( %r ) returned None" % h_url)
                # TODO: count error
                return
        else:  # is page
            pagebytes = self.uncached_fetch(h_url)
            if pagebytes is None:
                print("\nERR uncached_fetch( %r ) returned None" % h_url)
                # TODO: count error
                return
        self.fetched[h_url] = True
        soup = bs4.BeautifulSoup(pagebytes, features="lxml")
        # browse items that are files - download
        for li in soup.select("ul[class*='list--sources'] > li "):
            si = li.select("div[class*='list--source__information'] ")[0]
            a = li.find("a")
            txt = si.find_all(string=True, recursive=False)[0]
            fil_absurl = urllib.parse.urljoin(h_url, a.get("href"))
            try:
                _, cached = wetsuite.helpers.localdata.cached_fetch(
                    self.fetch_store, fil_absurl
                )
                self.count_items += 1
                if cached:
                    self.count_cacheds += 1
                    if self.verbose >= 2:
                        print(f" ITEM CACHED  {txt:25s}  {fil_absurl}")
                else:
                    self.count_fetches += 1
                    if self.verbose >= 2:
                        print(f" ITEM FETCHED {txt:25s}  {fil_absurl}")
            except ValueError as ve:  # probably a 404
                print(f" ERROR {repr(ve):25s}  {fil_absurl}")
            except Exception as e:  # e.g. OperationalError
                print(f" ERROR TODO:HANDLE {repr(e):25s}  {fil_absurl}")
        # browse items that are folders - recurse
        folder_soup = soup.select(
            "div > ul[class*='browse__list'] > li[class*='browse__item'] > a "
        )
        folder_names = list(a.find(string=True) for a in folder_soup)
        chosen_types = wetsuite.helpers.koop_parse.prefer_types(folder_names)
        for a in folder_soup:
            fol_absurl = urllib.parse.urljoin(h_url, a.get("href"))
            text = a.find(string=True)
            # self.itemlinks[ fol_absurl ] = text
            # TODO: change to 'decide what subset to fetch based on what there is'
            if text not in chosen_types:
                # in ('pdf','odt', 'jpg','coordinaten','ocr'):
                # 'metadata' 'metadataowms' 'xml' 'html'
                self.count_skipped += 1
                # print( f' SKIP FOLDER: {url}  {text:8s}   {fol_absurl}       (of {folder_names})' )
            else:
                if (
                    fol_absurl not in self.fetched
                    and fol_absurl not in self.to_fetch_folders
                ):
                    self.add_folder(fol_absurl)
        # get links to other pagination - add and get to eventually
        for a in soup.select("div[class*='pagination__index'] > ul > li > a"):
            pag_absurl = urllib.parse.urljoin(h_url, a.get("href"))
            if "start=" in pag_absurl:
                if (
                    pag_absurl not in self.fetched
                    and pag_absurl not in self.to_fetch_pages
                ):
                    self.add_page(pag_absurl)

    def work(self):
        """This is a generator so that it can yield fairly frequently in its task,
        mainly so that you can do something like a progress bar.
        The simplest use is probably something like::
            for _ in fetcher.work():
                pass   # (you could access and print counters)
        The thing it yields is not functional to anything,
        and may be a dummy string, though parts try to make it something
        you might want to display maybe.

        Note that there actually is no real distinction between
        what this class calls folders  and pages,
        but the way the repositories are structured, pretending this is true helps us
        recurse into what we added as folders,
        before what we added as pages,
        so that we can act depth-first-like
        and will e.g. start fetching documents before we've gone through all pages.
        (which seems like a good idea when some things have 100K pages,
        and there are reasons our fetching gets interrupted)
        On a similar note, we cache things we consider folders, not things we consider pages
        (because we assume many things at a level means it's the level (or at least a level)
        at which things get added over time. As such, you can make the folder store persistent
        and it saves _some_ time updating a local copy.
        """
        did_new_things = True
        while did_new_things:
            did_new_things = False
            yield "LOOP"  # dummy value
            while len(self.to_fetch_folders) > 0:
                folder_url = random.sample(list(self.to_fetch_folders), 1)[0]
                self.to_fetch_folders.remove(folder_url)
                if self.verbose >= 2:
                    print("HANDLE_FOL", folder_url)
                try:
                    self.handle_url(folder_url, is_folder=True)
                    self.count_folders += 1
                except ValueError:
                    self.count_errors += 1
                did_new_things = True
                # yield "LOOP" # dummy value
                yield folder_url
            if len(self.to_fetch_pages) > 0:
                page_url = random.sample(list(self.to_fetch_pages), 1)[0]
                self.to_fetch_pages.remove(page_url)
                if self.verbose >= 1:
                    print("HANDLE_PAGE", page_url)
                self.handle_url(page_url, is_folder=False)
                self.count_pages += 1
                did_new_things = True
                # yield "LOOP" # dummy value
                yield page_url
