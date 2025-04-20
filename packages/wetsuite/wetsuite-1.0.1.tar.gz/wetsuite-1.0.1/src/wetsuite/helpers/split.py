""" This module tries to wrangle distinct types of documents for you,
    from HTML to PDF,
    from varied specific sources, 
    into plain text, 
    so that you can consume it more easily.

    It tries to give those into smallish chunks, 
    ideally informed by the document structure.

 
    Ideally, this module gets ongoing attention 
    to cover all the documents that this project cares about,
    and to that end is a somwhat modular design.

    You won't care about that until you want to add your own,
    but it does have some implications to how it should be used:
      - decide(docbytes) will give you (score, splitter_object) tuples
        - you can avoid looser-structured splitters by testing for bad scores, _or_ by using C{decide}'s thresh to the same effect.
      
      - each splitter object, when called, gives (metadata, intermediate, flat_text) tuples
        - flat_text is a string. Sometimes you care about only this
        - the other two are more source-specific
          - intermeiate tends to be the structure that that flat_text is from, in case that 
          - metadata i

    So if you want more control, dealing with the structure hints it also spits out, 
    your code might look somehing like::
        for score, splitter in wetsuite.helpers.split.decide( docbytes ):
            for metadata, intermediate, text in splitter.fragments():
                print( text )
                print( '--------------------' )

    **If you just want text**, with little control over the details::
        string_list = feeling_lucky( docbytes )

                
    TODO: 
      - parameters, like "OCR that PDF if you have to"
      
    CONSIDER: 
      - think about separating the "read document at lower level" code 
        into functions you can use without having to rip it out these classes here.
        Right now, even if you know the class you want, you need to do::
            f = Fragments_XML_BWB()
            f.accepts()
            f.suitableness()
            for frag in f.fragments():
                print( frag )

      - in particular the HTML code can probably be made rather faster
        - using lxml.html (or specifically iterparse?) instad of bs4, because bs4 is currently the slowest part of this
            ...bit of a rewrite, though.
        - having one class contain all of these - mostly to _share_ state like 'we tried to parse with bs4'

      - always have a reasonable fallback for each document type (TODO: XML?)

      - settling the intermediate format more?
        - Maybe we shouldn't make too many decisions for you, and merely yield suggestions you can easily ignore, e.g.
            - 'seems like same section, <TEXT>'
            - 'seems like new section, <TEXT>'
            - 'seems like page header/footer, <TEXT>'
            - 'seems like page footnotes, <TEXT>'
        - ...so that you, or a helper function, can group into different-sized chunks in the way you need it.

      - maybe rename feeling_lucky, maybe move it to lazy?

      - we were trying to be inspired by LaTeX hyphenation, 
          which has a simple-but-pretty-great "this is the cost of breaking off here"
          the analogue of which wo7uld make "Hey can you break this to different degrees (sections, paragraphs)" possible

      - There was an earlier idea to specify pattern matchers entirely as data, like::
            presets = {
                'beleidsregels': {
                    'body': { 'name': 'div', 'id': 'PaginaContainer' },
                    'keep_headers_html': True,
                    'keep_tables_html':  True,
                },
            }
        - with a 'this is how to select for the document' and 'this is how to get the body from it', etc.
        - which is worth re-visiting, because 
          - it may be more easily altered in the long run, 
          - it would probably be more portable than this code currently is.
        - a limitation might be expressing more complex selection
"""


import re
import warnings
import pprint

import bs4   # arguably should be inside each class so we can function without some of these imports
import fitz  # arguably should be inside each class so we can function without some of these imports

import wetsuite.helpers.strings
import wetsuite.helpers.koop_parse
import wetsuite.helpers.etree
import wetsuite.extras.pdf
import wetsuite.datacollect.rechtspraaknl


header_tag_names = ("h1", "h2", "h3", "h4", "h5", "h6")


def fix_ascii_blah(bytesdata: bytes):
    """There are a bunch of XMLs that are invalid _only_ because they contain UTF8 but say they are US-ASCII.
    This seems constrained to some parliamentary XMLs.

    This is a crude patch-up for someone else's mistake, so arguably doesn't really belong in this module, but hey.
    """
    if b'<?xml version="1.0" encoding="US-ASCII"?>' in bytesdata:
        return bytesdata.replace(
            b'<?xml version="1.0" encoding="US-ASCII"?>',
            b'<?xml version="1.0" encoding="UTF-8"?>',
        )
    return bytesdata


def _split_officielepublicaties_xml(tree, start_at):
    """Code shared between a lot of the officiele-publicaties XML extraction"""
    ret = []  #  (metadata, intermediate, debugsomething, text)

    ## ensure start_at_node is a node object, and atart_at_path is a string path (to it)
    if (
        start_at is None
    ):  # if not specified, then assume we care about everything and can start at the root
        start_at_node = tree
        start_at_path = "."  # hack to indicate / without using /
    elif isinstance(start_at, str):
        start_at_path = start_at  # assuming that makes sense
        start_at_node = tree.xpath(start_at)
        if (
            start_at_node is None or len(start_at_node) == 0
        ):  # TODO: check that both can actually happen
            raise ValueError("Did not find %s within %s" % (start_at, tree))
    elif isinstance(start_at, list):
        raise ValueError(
            "_split_officielepublicaties_xml() does not know what to do when given a list"
        )
    else:  # assume it was a node in the tree you find'd or xpath'd yourself (keep in mind that xpath returns a list of nodes)
        start_at_node = start_at
        start_at_path = wetsuite.helpers.etree.path_between(tree, start_at_node)

    ## extract under that node/path
    for fragment in wetsuite.helpers.koop_parse.alineas_with_selective_path(
        tree,
        start_at_path=start_at_path,
        alinea_elemnames=(
            "al",
            "tussenkop",
            "dagtekening",
            "context.al",
            "considerans.al",
            "Al",
            #'entry',
        ),
    ):
        # print('FR',fragment)
        meta = fragment
        inter = {
            "raw": fragment.pop("raw"),
            "rawtype": "xml",
            "raw_etree": fragment.pop("raw_etree"),
        }
        text_flat = fragment.pop("text-flat")
        ret.append((meta, inter, text_flat))
    return ret


_op_re = re.compile(r".*officiele-publicatie.*")
_content_re = re.compile(r".*\bcontent\b.*")
_stuk_re = re.compile(r".*\bstuk\b.*")
_inhoud_re = re.compile(r".*\binhoud\b.*")

_p_re = re.compile(r".*_p_.*")


def _split_officielepublicaties_html(soup):
    """Code shared between a lot of the officiele-publicaties HTML extraction"""
    ret = []
    warnings.warn("_split_officielepublicaties_html() needs some basic refinement")

    # This seems to be based on varied templates/transforms over time, so this may need more work to be complete
    body = soup.find("body")
    dop = body.find(
        "div", attrs={"class": _op_re}
    )  # this seems to be transformed from the XML, is
    stuk = body.find("div", attrs={"class": _stuk_re})
    inhoud = body.find("div", attrs={"class": _inhoud_re})
    article = body.find("article")
    idc = body.find("div", attrs={"id": _content_re})

    # if article is not None:
    #    print( wetsuite.helpers.etree.debug_pretty( wetsuite.helpers.etree.fromstring( str(article ) ) ) )
    #    text = article.find_all(text=True)
    #    print( text )
    #    ret.append(({},str( article ), text))
    #    raise ValueError( text )

    # alert = body.find('div', attrs={'class':'alert__inner'})
    # if alert is not None:
    #     raise ValueError(alert.text)
    #     #if 'Deze publicatie is niet beschikbaar' in alert.text:
    #     #    raise ValueError(alert.text)

    # found_one = False # set but not currently used
    for maybe in (dop, stuk, inhoud, article, idc):
        if maybe is not None:
            # print(maybe.name)
            # print(maybe)
            # found_one = True

            # look for divs that have a _p_ class; these seem to come from tempate that converted this from... XML perhaps?
            # there seem to be some variants, though. If there is anything with _p_ inside that, iterate over those _instead_
            # to make that the fine-grainedness.
            # TODO: check for most sense -- maybe '_p_al'-parent-based logic makes more sense?
            elems = maybe.find_all("div", attrs={"class": _p_re})
            if len(elems) == 0:
                elems = maybe.find_all(["p", "h1", "h2", "h3", "h4"])

            for elem in elems:  # if div contains _p_ elements
                # "is this split into smaller _p_ fragments?"
                # TODO: This implicitly assumes that we _only_ care about elements with _p_; CHECK that that is actually valid (and non-nested)
                p_inside = elem.find_all(True, attrs={"class": _p_re})
                if len(p_inside) > 0:
                    for ip in p_inside:
                        ret.append(
                            (
                                {"class": ip.get("class"), "hints": ["pblock"]},
                                {"raw": str(ip), "rawtype": "html"},
                                " ".join(ip.find_all(string=True)),
                            )
                        )
                else:  # no _p_ inside, whatever is in that whole chunk
                    ret.append(
                        (
                            {"class": elem.get("class"), "hints": ["pblock"]},
                            {"raw": str(elem), "rawtype": "html"},
                            " ".join(elem.find_all(string=True)),
                        )
                    )
            break

    # if not found_one:
    #     print("ELSE")
    #     text = body.find_all(string=True)
    #     print( text )
    #     ret.append(({},str( body ), text))
    #     #raise ValueError( text )

    return ret
    # ret.append(({},{},str( body )))


###################################################################################################


class Fragments:
    "Abstractish base class explaining the purpose of implementing this"
    # CONSIDER: adding a function that describes the parser

    def __init__(self, docbytes: bytes, debug: bool = False):
        """Hand the document bytestring into this. Nothing happens yet; you call accepts(), then suitableness(), then possibly fragments() -- see example use in decide()."""
        if not isinstance(docbytes, bytes):
            raise ValueError("This class only accepts files as bytestrings")
        self.docbytes = docbytes
        self.debug = debug

    def accepts(self) -> bool:
        """whether we would consider parsing that at all.
        Often, "is this the right file type".
        """
        raise NotImplementedError(
            "Please implement this, it comes from an essentially-abstract class"
        )

    def suitableness(self) -> int:
        """e.g.
        - 5: I recognize that's PDF, from OP, and specifically Stcrt so I probably know how to fetch out the text fairly well
        - 50: I recognize that's PDF, from OP, so I may do better than entirely generic
        - 500: I recognize that's PDF, I will do something generic (because I am a fallback for PDFs)
        - 5000: I recognize that's PDF, but I'm specific and it's probably a bad idea if I do something generic
        The idea is that with multiple of these, we can find the thing that (says) is most specific to this document.
        """
        raise NotImplementedError(
            "Please implement this, it comes from an essentially-abstract class"
        )

    def fragments(self):
        "yields a tuple for each fragment"
        raise NotImplementedError(
            "Please implement this, it comes from an essentially-abstract class"
        )

    # CONSIDER: meta()


#########################################################

class Fragments_XML_BWB(Fragments):
    "Turn BWB in XML form into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        return b'<toestand' in self.docbytes[:200]   # CONSIDER: testing for the namespace URL once we check whether it actually has versions
        #if self.tree.tag == "toestand":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        self.tree = wetsuite.helpers.etree.fromstring(      self.docbytes )
        self.tree = wetsuite.helpers.etree.strip_namespace( self.tree     ) # choice to remove namespaces unconditionally

        # PRELIMINARY TESTS
        ret = []
        fragments = wetsuite.helpers.koop_parse.alineas_with_selective_path(self.tree)
        # TODO: detect what level gives reasonably-sized chunks on average, to hand into mer
        for part_id, part_text_list in wetsuite.helpers.koop_parse.merge_alinea_data( fragments ):
            for part in part_text_list:
                if self.debug:
                    print(part)
                ret.append(
                    (
                        {
                            "hints": ["mergedpart"],
                            "part_id": part_id,
                            "part_name": ", ".join(" ".join(tup) for tup in part_id),
                        },
                        {},  #'raw':part_text_list},
                        part,
                    )
                )
        return ret


class Fragments_XML_CVDR(Fragments):
    "Turn CVDR in XML form into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        if b'standaarden.overheid.nl/cvdr/terms' in self.docbytes[:500]: #part of the namespace URL, seems better than '<cvdr' ?
            return 5
        else:
            return 5000
        #if self.tree.tag == "cvdr":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        self.tree = wetsuite.helpers.etree.fromstring(      self.docbytes )
        self.tree = wetsuite.helpers.etree.strip_namespace( self.tree     )  # choice to remove namespaces unconditionally

        # PRELIMINARY TESTS
        ret = []
        for fragment in wetsuite.helpers.koop_parse.alineas_with_selective_path( self.tree ):
            raw = fragment.pop("raw")
            fragment.pop("raw_etree")
            text_flat = fragment.pop("text-flat")
            ret.append(
                (
                    fragment,
                    {"raw": raw, "rawtype": "xml"},  #'raw':part_text_list},
                    text_flat,
                )
            )

        # # TODO: detect what level gives reasonably-sized chunks on average, to hand into merge
        # for part_id, part_text_list in wetsuite.helpers.koop_parse.merge_alinea_data( fragments ):
        #     for part in part_text_list:
        #         print(part)
        #         ret.append( (
        #             {'hints':['mergedpart'], 'part_id':part_id, 'part_name':', '.join( ' '.join(tup)  for tup in part_id )},
        #             {},#'raw':part_text_list},
        #             part
        #         ) )
        return ret


class Fragments_HTML_CVDR(Fragments):
    "Turn CVDR in HTML form into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        return wetsuite.helpers.util.is_html(self.docbytes)

    def suitableness(self):
        if b'DCTERMS.identifier' in self.docbytes  and  b'cvdr_meta' in self.docbytes: # TODO: check that this doesn't over- or under-accept
            return 5
        else:
            return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        return _split_officielepublicaties_html(
            self.soup
        )  # preliminary do-anything; TODO: this is a case where we can probably do better


class Fragments_HTML_OP_Stcrt(Fragments):
    "Turn staatscourat in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        if b'OVERHEIDop.publicationName' in self.docbytes and b'Staatscourant' in self.docbytes: # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000

        #pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #if pname is not None and pname.get("content") == "Staatscourant":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")

        ret = _split_officielepublicaties_html(self.soup)
        return ret


class Fragments_HTML_OP_Stb(Fragments):
    "Turn staatsblad in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        if b'OVERHEIDop.publicationName' in self.docbytes and b'Staatsblad' in self.docbytes: # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000
        #with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
        #    warnings.simplefilter("ignore")
        #    self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        #pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #if pname is not None and pname.get("content") == "Staatsblad":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        ret = _split_officielepublicaties_html(self.soup)
        return ret


class Fragments_HTML_OP_Gmb(Fragments):
    "Turn gemeenteblad in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        if b'OVERHEIDop.publicationName' in self.docbytes and b'Gemeenteblad' in self.docbytes: # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000
        #with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
        #    warnings.simplefilter("ignore")
        #    self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        #pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #if pname is not None and pname.get("content") == "Gemeenteblad":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        ret = _split_officielepublicaties_html(self.soup)
        return ret


class Fragments_HTML_OP_Trb(Fragments):
    "Turn tractatenblad in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        if b'OVERHEIDop.publicationName' in self.docbytes and b'Tractatenblad' in self.docbytes: # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000
        #with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
        #    warnings.simplefilter("ignore")
        #    self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        #pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #if pname is not None and pname.get("content") == "Tractatenblad":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        ret = _split_officielepublicaties_html(self.soup)
        return ret


class Fragments_HTML_OP_Prb(Fragments):
    "Turn provincieblad in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        if b'OVERHEIDop.publicationName' in self.docbytes and (
                b'Provincieblad' in self.docbytes or
                b'Provinciaal blad' in self.docbytes
                ): # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000
        #with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
        #    warnings.simplefilter("ignore")
        #    self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        #pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #if pname is not None and pname.get("content") == "Provincieblad":
        #    return 5
        #elif pname is not None and pname.get("content") == "Provinciaal blad":
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        ret = _split_officielepublicaties_html(self.soup)
        return ret


class Fragments_HTML_OP_Wsb(Fragments):
    "Turn waterschapsblad in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        if b'OVERHEIDop.publicationName' in self.docbytes and b'Waterschapsblad' in self.docbytes: # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000
        #$with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
        #$    warnings.simplefilter("ignore")
        #$    self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        #$pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #$if pname is not None and pname.get("content") == "Waterschapsblad":
        #$    return 5
        #$else:
        #$    return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        ret = _split_officielepublicaties_html(self.soup)
        return ret

class Fragments_HTML_OP_Bgr(Fragments):
    "Turn blad gemeenschappelijke regeling in HTML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        # TODO: (here and for all others): make a string from 
        if b'OVERHEIDop.publicationName' in self.docbytes and b'Blad gemeenschappelijke regeling' in self.docbytes: # TODO: this probably overaccepts, check
            return 5
        else:
            return 5000
        #with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
        #    warnings.simplefilter("ignore")
        #    self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        #pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        #if (
        #    pname is not None
        #    and pname.get("content") == "Blad gemeenschappelijke regeling"
        #):
        #    return 5
        #else:
        #    return 5000

    def fragments(self):
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        ret = _split_officielepublicaties_html(self.soup)
        return ret


#######################################################################################################################

# CONSIDER: It seems that for OP, the meta fields are the same between HTML and XML,
#           which would mean the detection methods could be similar (and more code shared)
#           On the other hand, the //looking-for//specifics is great at highlighting weird edge caes


# There is an argument that many of the XPaths below should be made more wide, because while e.g.
#   //gemeenteblad//regeling-tekst/tekst
# may focus on the core text,
#   //gemeenteblad//regeling-tekst
# will not ignore some text around it (which is why /tekst is mentioned in comments below)
# but then, there are also a few weird cases like the below and e.g. gmb-2014-45427,
# where the contents are all in the aanhef, that argue that that we'll catch more like:
#   //gemeenteblad//regeling

# <gemeenteblad>
#     <kop>
#       <titel>Gereserveerde gehandicaptenparkeerplaats nabij het perceelnummer 143, aan de Vijzelstraat te Den Haag.</titel>
#     </kop>
#     <regeling>
#       <aanhef>
#         <context>
#           <context.al>Onderwerp: toewijzing gehandicaptenparkeerplaats bestuurder nabij het woonadres.</context.al>
#           <context.al>Geachte heer, mevrouw,</context.al>
#           <context.al>Dit is het besluit op uw ingekomen aanvraag voor een gehandicaptenparkeerplaats ten behoeve van bestuurders.</context.al>
#           [...]
#         </context>
#       </aanhef>
#       <regeling-tekst>
#         <tekst/>
#       </regeling-tekst>
#     </regeling>
#   </gemeenteblad>


class Fragments_XML_OP_Gmb(Fragments):
    "Turn gemeenteblad in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            # ('//gemeenteblad//regeling-tekst', 5),
            ("//gemeenteblad//zakelijke-mededeling", 10),  # -tekst/tekst
            ("//gemeenteblad//regeling", 10),
            ("//Gemeenteblad//BesluitCompact", 25),
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Stcrt(Fragments):
    "Turn staatscourant in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally

        for test_xpath, score in (
            ("//staatscourant//circulaire-tekst", 5),  # /tekst
            ("//staatscourant//vrije-tekst", 5),  # /tekst
            ("//staatscourant//zakelijke-mededeling-tekst", 5),  # /tekst
            ("//staatscourant//regeling-tekst", 5),
            ("//staatscourant", 50),
            ("/stcart", 50),  # is this wrong?
            ("/avvcao//body", 75),  # exception?
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Stb(Fragments):
    "Turn sstaatsblad in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            ("//staatsblad//wettekst", 5),
            ("//staatsbl//body", 10),  # which excludes some
            ("//staatsblad/verbeterblad/vrije-tekst", 5),  #  /tekst    exception?
            # elif self.tree.xpath('//staatsblad'):  return 50
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Trb(Fragments):
    "Turn tractatenblad in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            ("//tractatenblad//vrije-tekst", 5),
            ("//trblad//body", 10),  # which excludes some
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Prb(Fragments):
    "Turn provincieblad in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            ("//provinciaalblad//regeling", 15),  # -tekst/tekst
            # ('//provinciaalblad//regeling-tekst', 15),
            ("//provinciaalblad//zakelijke-mededeling", 5),  # -tekst/tekst
            ("//provincieblad//zakelijke-mededeling", 5),  # -tekst/tekst
            ("//provincieblad//regeling", 15),  # -tekst
            ("//Provinciaalblad//Lichaam", 10),
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score

        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Wsb(Fragments):
    "Turn waterschapsblad in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            ("//waterschapsblad//zakelijke-mededeling", 10),  # -tekst/tekst
            ("//waterschapsblad//regeling", 10),  # regeling-tekst
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Bgr(Fragments):
    "Turn blad gemeenschappelijke regeling in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            ("//bladgemeenschappelijkeregeling//regeling", 5),  # -tekst
            (
                "//bladgemeenschappelijkeregeling//zakelijke-mededeling",
                5,
            ),  # -tekst/tekst
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_OP_Handelingen(Fragments):
    "Turn handelingen in XML form (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        self.docbytes = fix_ascii_blah(self.docbytes)
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        for test_xpath, score in (
            ("//handelingen", 5),
            ("/handeling", 50),  # is this wrong?
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score
        return 5000

    def fragments(self):
        ret = []
        # print( self.startpaths )
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_XML_BUS_Kamer(Fragments):
    "Turn other kamer XMLs (from KOOP's BUS) into fragments (TODO: re-check which these are)"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None
        self.startpaths = None

    def accepts(self):
        self.docbytes = fix_ascii_blah(self.docbytes)
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        # may raise - maybe return very high score instead?
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally

        for test_xpath, score in (
            ("/kamerwrk", 5),  # ?
            ("//kamerstuk//vrije-tekst", 5),  # /tekst
            ("//kamervragen", 15),
            (
                "//niet-dossier-stuk//vrije-tekst",
                10,
            ),  # or maybe //niet-dossier-stuk/nds-stuk  ?
            ("//kamerstuk//stuk", 50),  # ?
            ("/vraagdoc", 50),  # is this wrong?
            (
                "//agenda",
                100,
            ),  # TODO: split the cacses that jsut say to look at the PDF instead?
        ):
            sel = self.tree.xpath(test_xpath)
            if len(sel) > 0:
                self.startpaths = list(
                    wetsuite.helpers.etree.path_between(
                        self.tree, selnode, excluding=True
                    )
                    for selnode in sel
                )
                return score

        return 5000

    def fragments(self):
        ret = []
        for sp in self.startpaths:
            ret.extend(_split_officielepublicaties_xml(self.tree, sp))
        return ret


class Fragments_HTML_BUS_kamer(Fragments):
    "Turn kamer-related HTMLs (from KOOP's BUS) into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # unpack the one-html zip into the html
            return True
        return False

    def suitableness(self):
        # may raise - maybe return very high score instead?
        with warnings.catch_warnings():  # meant to ignore the "It looks like you're parsing an XML document using an HTML parser." warning
            warnings.simplefilter("ignore")
            self.soup = bs4.BeautifulSoup(self.docbytes, features="lxml")
        pname = self.soup.find("meta", attrs={"name": "OVERHEIDop.publicationName"})
        if pname is not None and pname.get("content") == "Kamervragen (Aanhangsel)":
            return 5
        elif (
            pname is not None and pname.get("content") == "Kamervragen zonder antwoord"
        ):
            return 5
        elif pname is not None and pname.get("content") == "Kamerstuk":
            return 5
        else:
            return 5000

    def fragments(self):
        ret = _split_officielepublicaties_html(self.soup)
        return ret


# class Fragments_HTML_Rechtspraak( Fragments ):
#     def __init__(self, docbytes, debug=False):
#         Fragments.__init__(self, docbytes, debug)
#
#     def accepts( self ):
#         return wetsuite.helpers.util.is_html( self.docbytes )
#
#     def suitableness( self ):
#         self.soup = bs4.BeautifulSoup( self.docbytes, features='lxml' )
#         ht = self.soup.find('head/title')
#         if ht is not None and ht.text is not None and ht.text.startswith('Rechtspraak.nl'):
#             return 5
#         else:
#             return 5000
#
#     #def fragments


class Fragments_XML_Rechtspraak(Fragments):
    "turn rechtspraak.nl's open-rechtspraak XML form into fragments"
    # examples:
    # https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:RBDHA:2023:18504

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        self.tree = wetsuite.helpers.etree.fromstring(self.docbytes)
        self.tree = wetsuite.helpers.etree.strip_namespace(
            self.tree
        )  # choice to remove namespaces unconditionally
        if self.tree.tag == "open-rechtspraak":
            return 5
        else:
            return 5000

    def fragments(self):
        ret = []

        # we currently ignore the 'inhoudsindicatie', being a sumamry, but it might be worth adding
        # if ii is not None:
        #     print( '[%s]  %s'%(
        #         'inhoudsindicatie', ' '.join( wetsuite.datacollect.rechtspraaknl._para_text( ii ) )
        #     ) )

        t = None
        if self.tree.find("uitspraak") is not None:
            t = self.tree.find("uitspraak")
        elif self.tree.find("conclusie") is not None:
            t = self.tree.find("conclusie")
        if t is not None:
            # top-level, ideally is something like <uitspraak.info> followed by <section>s
            structured_things = t.xpath("uitspraak.info|section")
            if len(structured_things) == 0:
                # raise ValueError("Not structured like the rest?  %s"%list( tag.tag  for tag in t) )
                # TODO: figure out whether this make sense
                structured_things = [t]
            else:
                pass
                # print( "YAY %s"%list( tag.tag  for tag in t) )

            for structured_thing in structured_things:
                last_nr = None
                # last_title = None
                for ch in structured_thing.getchildren():
                    # CONSIDER checking ch.tag for parablock, etc. to handle them more specifically, but for now:
                    meta = {
                        "part": wetsuite.helpers.etree.path_between(
                            self.tree, structured_thing
                        ),
                        "path": wetsuite.helpers.etree.path_between(self.tree, ch),
                    }
                    raw = wetsuite.helpers.etree.tostring(ch)

                    hints = []
                    nr = ch.find("nr")
                    if nr is not None:
                        meta["nr"] = nr.text.strip()
                        nr.text = ""  # so that it doesn't land in flat_text
                        last_nr = nr
                    if last_nr is not None and last_nr.text is not None:
                        meta["lastnr"] = last_nr.text.strip()

                    if ch.tag == "title":  # title = ch.find('title')
                        # if title is not None:
                        title_text = (
                            " ".join(wetsuite.helpers.etree.all_text_fragments(ch))
                        ).strip()
                        meta["title"] = title_text
                        # last_title = title_text
                        hints.append("is-title")

                    flat_text = (
                        " ".join(wetsuite.helpers.etree.all_text_fragments(ch))
                    ).strip()

                    if ch.find("emphasis"):
                        hints.append("has-emphasis")
                        # emphasis role="bold caps

                    # if len(flat_text) > 0:
                    #    hints.append('is-empty')
                    #   #emphasis role="bold caps

                    if ch.find("informaltable") is not None:
                        hints.append("has-table")
                        # emphasis role="bold caps

                    # if len(hints)>0:
                    meta["hints"] = hints

                    ret.append(
                        (
                            meta,
                            {"raw": raw, "rawtype": "xml"},
                            flat_text,
                        )
                    )

        # # head before
        # #    pre-head b
        # # uitspraak, inleiding, procesverloop, overwegingen, beslissing
        # # smaller sections:
        # #   Proceskosten, Standpunt van verzoeker, Wettelijk kader, Bevoegdheid, Conclusie en gevolgen, Rechtsmiddel
        # # Bijlage
        return ret


####################################################################################

class Fragments_HTML_Geschillencommissie(Fragments):
    "Turn HTML pages from degeschillencommissie.nl into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        return False

    def suitableness(self):
        if b'href="https://www.degeschillencommissie.nl' in self.docbytes: # TODO: consider better test
            return 5
        else:
            return 5000

    #def fragments(self):
    #    return ret


class Fragments_HTML_Tuchtrecht(Fragments):
    "Turn HTML pages from  into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.soup = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        return False

    def suitableness(self):
        if b'Overheid.nl | Tuchtrecht' in self.docbytes: # TODO: consider better test
            return 5
        else:
            return 5000

    #def fragments(self):
    #    return ret



####################################################################################


class Fragments_HTML_Fallback(Fragments):
    "Extract text from HTML from non-specific source into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.etree = None

    def accepts(self):
        if wetsuite.helpers.util.has_xml_header(self.docbytes):
            return False
        if wetsuite.helpers.util.is_html(self.docbytes):
            return True
        if wetsuite.helpers.util.is_htmlzip(self.docbytes):
            self.docbytes = wetsuite.helpers.util.get_ziphtml(
                self.docbytes
            )  # fetch the html from the one-html zip
            return True
        return False

    def suitableness(self):
        " Mostly just says we're a bad example but we'll try; our accepts() is the real filter here "
        # TODO: see whether lxml.html seems to creatively make it work regardless, or whether there are exceptions to catch and return worse scores
        self.etree = wetsuite.helpers.etree.parse_html(self.docbytes)
        return 500

    def fragments(self):
        " No metadata at all, just text split by \n\n"
        ret = []
        onestring = wetsuite.helpers.etree.html_text(self.etree, join=True)
        for plain in re.split( r'[\n]{2,}', onestring) : # as of this writing, .split('\n\n') should be functionally identical, but assume parse_html may change.
            ret.append( ({},{},plain) )
        return ret



class Fragments_XML_Fallback(Fragments):
    "Extract text from XML from non-specific source into fragments"

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.tree = None

    def accepts(self):
        return wetsuite.helpers.util.is_xml(self.docbytes)

    def suitableness(self):
        return 500

    def fragments(self):
        #ret = []
        raise NotImplementedError("TODO: implement this fallback")
        # ret.append( (
        #    {},
        #    {},
        #    (' '.join( wetsuite.helpers.etree.all_text_fragments( ch ) )) .strip(),
        # ))
        #return ret


class Fragments_PDF_Fallback(Fragments):
    """Extract text from PDF from non-specific source into fragments

    Tries to look at section titles,
    but is currently too crude to deal with page headers, footers.
    """

    def __init__(self, docbytes, debug=False):
        Fragments.__init__(self, docbytes, debug)
        self.part_name = None
        self.part_ary = None

    def accepts(self):
        return wetsuite.helpers.util.is_pdf(self.docbytes)

    def suitableness(self):
        # assuming is_pdf approved, we can read it,
        # but also, we are not as good as anything more targeted that you can register, so:
        return 100

    def fragments(self):
        ret = wetsuite.extras.pdf.document_fragments( self.docbytes ) # this will be useful to other things, so was moved
        return ret




# In theory you could nest these (e.g. OP detects and deals with all OP documents)
# but it may be nicer to have it be more pluggible with a registerable list

# ...which might also keep it easier/clearer how this can be extended

####################################################################################

_registered_fragment_parsers = [
    # order doesn't matter, all are checked.
    Fragments_XML_BWB,
    Fragments_XML_CVDR,
    Fragments_HTML_CVDR,

    Fragments_XML_Rechtspraak,
    # Fragments_HTML_Rechtspraak,

    Fragments_XML_OP_Stcrt,
    Fragments_XML_OP_Stb,
    Fragments_XML_OP_Trb,
    Fragments_XML_OP_Gmb,
    Fragments_XML_OP_Prb,
    Fragments_XML_OP_Wsb,
    Fragments_XML_OP_Bgr,

    Fragments_HTML_OP_Stcrt,
    Fragments_HTML_OP_Stb,
    Fragments_HTML_OP_Gmb,
    Fragments_HTML_OP_Trb,
    Fragments_HTML_OP_Prb,
    Fragments_HTML_OP_Wsb,
    Fragments_HTML_OP_Bgr,

    Fragments_XML_OP_Handelingen,
    Fragments_XML_BUS_Kamer,
    Fragments_HTML_BUS_kamer,

    # TODO: tuchtrecht
    # TODO: geschillencommissie

    Fragments_PDF_Fallback,
    Fragments_HTML_Fallback,
    # CONSIDER: Only add the following once they give output: (except one of the tests, test_firstonly, relies on it being there, so...)
    #Fragments_XML_Fallback,
    #(maybe add an opendocument fallback?)
]


def decide(docbytes, thresh=1000, first_only=False, debug=False):
    """Ask all processors to say how well they would do,
    pick any that seem applicable enough (by our threshold).

    Returns a list of (score, processing_object)

    Note that that procobject has had accepts() and suitableness() called,
    so you can now call fragments() to get the fragments.
    """
    options = []

    for PerhapsClass in _registered_fragment_parsers:
        processing_object = PerhapsClass(docbytes, debug=debug)
        if processing_object.accepts():  # does it say it's getting the right file type?
            score = (
                processing_object.suitableness()
            )  # how well does it figure it would treat this?
            if score < thresh:
                options.append([score, processing_object])
                if first_only:
                    break

    options.sort(key=lambda x: x[0])
    return options


def feeling_lucky(docbytes):
    """If you are sure this code understands a particular document format,
    you can hand it in here, and it will returns a list of strings for a document.
    No control, just text from whatever said it applied best.

    This needs to be renamed. Maybe this needs to go to wetsuite.helpers.lazy instead.
    
    @return: a list of strings
    """
    ret = []
    for _, fragclass in decide(docbytes):
        for _, _, textfrag in fragclass.fragments():
            ret.append(textfrag)
        break
    return ret


class SplitDebug:
    """A notebook-style formatter that does little more than take a list of tuple of three things
    (meant for the output of fragments()), and print them in a table.
    """

    def __init__(self, fragments):
        "Takes the output of one of these classes's C{fragments}"
        self.fragments = fragments

    def _repr_html_(self):
        "Takes the tuples we were initiated with, show in a HTML table"

        def oe(o):
            "decide how exactly to print object in HTML, depending on its type"
            if isinstance(o, str):
                return o
            elif isinstance(o, (list, tuple, dict)):
                # return str(o)
                return pprint.pformat(o, width=50)
            else:
                return str(o)
            #    raise TypeError('blah %s'%type(o))

        ret = ['<table border="1">']
        ret.append(
            "<tr><th>meta</th><th>intermediate</th><th>len</th><th>text</th></tr>"
        )
        for metadict, intermediate, textstr in self.fragments:
            ret.append("<tr>")
            ret.append(
                '<td style="text-align:left"><pre>%s</pre></td>'
                % wetsuite.helpers.escape.nodetext(oe(metadict))
            )
            # ret.append('<td>%s</td>'%wetsuite.helpers.escape.nodetext( oe(intermediate) ))
            ret.append(
                '<td style="text-align:left"><pre>%s</pre></td>'
                % wetsuite.helpers.escape.nodetext(oe(intermediate))
            )
            ret.append('<td style="text-align:left">%d</td>' % len(textstr))
            ret.append(
                '<td style="text-align:left">%r</td>'
                % wetsuite.helpers.escape.nodetext(textstr)
            )
            ret.append("</tr>")
        ret.append("</table>")
        return "".join(ret)


# display(
#     wetsuite.helpers.split.SplitDebug( [ ({'sec':'foo'},    '<tt>bar</tt>', 'bar'),
#                 ({'sec':['bar']},  {1:'<bla>'},    'bar'),
#                 ({'type':'image'}, '(STUF))',      '')     ] )
# )
