""" General utility functions, like "give me a path to where wetsuite can store data" and debug tools to the end of inspecting data. 
"""

import os
import difflib
import hashlib
import zipfile
import io
import lxml.etree


def wetsuite_dir():
    """Figure out where we can store data.

    Returns a dict with keys mentioning directories:
      - wetsuite_dir: a directory in the user profile we can store things
      - datasets_dir: a directory inside wetsuite_dir first that datasets.load() will put dataset files in
      - stores_dir:   a directory inside wetsuite_dir that localdata will put sqlite files in

    Keep in mind:
      - When windows users have their user profile on the network, we try to pick a directory more likely to be shared by your other logins
      - ...BUT keep in mind network mounts tend not to implement proper locking,
         so around certain things (e.g. our localdata.LocalKV) you invite corruption when multiple workstations write at the same time,
         ...so don't do that. If you need distributed work, use an actually networked store, or be okay with read-only access.
    """
    # CONSIDER: listen to an environment variable to override that base directory,
    #         to allow people to direct where to store this (might be useful e.g. on clustered filesystems)
    #         (an explicit argument wouldn't make sense when internals will call this)

    # CONSIDER: If we wanted to expose this to users, this function deserves to be in a more suitable location - maybe helpers/util?
    #         it's also used by localdata

    ret = {}

    # Note: expanduser("~") would do most of the work, as it works on win+linx+osx.
    #   These additional tests are mainly for the case of AD-managed workstations, to try to direct it to store it in a shared area
    #   HOMESHARE is picked up (and preferred over USERPROFILE) because in this context, USERPROFILE might be a local, non-synced directory
    #     (even if most of its contents are junctions to places that _are_)
    # Yes, we do assume this will stay constant over time.
    # we assume the following are only filled when it's actually windows - we could test that too via os.name or platform.system()
    userprofile = os.environ.get("USERPROFILE", None)
    homeshare = os.environ.get("HOMESHARE", None)
    chose_dir = None
    if homeshare is not None:
        r_via_hs = os.path.join(homeshare, "AppData", "Roaming")
        if os.path.exists(r_via_hs):
            chose_dir = os.path.join(r_via_hs, ".wetsuite")
    elif userprofile is not None:
        r_via_up = os.path.join(userprofile, "AppData", "Roaming")
        if os.path.exists(r_via_up):
            chose_dir = os.path.join(r_via_up, ".wetsuite")

    if chose_dir is None:
        home_dir = os.path.expanduser("~")
        ret["wetsuite_dir"] = os.path.join(home_dir, ".wetsuite")
    else:
        ret["wetsuite_dir"] = chose_dir

    # TODO:     more filesystem checking, so we can give clearer errors
    if not os.path.exists(ret["wetsuite_dir"]):
        os.makedirs(ret["wetsuite_dir"])
    if not os.access(ret["wetsuite_dir"], os.W_OK):
        raise OSError(
            "We cannot write to our local directory, %r" % ret["wetsuite_dir"]
        )

    ret["datasets_dir"] = os.path.join(ret["wetsuite_dir"], "datasets")
    if not os.path.exists(ret["datasets_dir"]):
        os.makedirs(ret["datasets_dir"])
    if not os.access(ret["datasets_dir"], os.W_OK):
        raise OSError(
            "We cannot write to our local directory of datasets, %r"
            % ret["datasets_dir"]
        )

    ret["stores_dir"] = os.path.join(ret["wetsuite_dir"], "stores")
    if not os.path.exists(ret["stores_dir"]):
        os.makedirs(ret["stores_dir"])
    if not os.access(ret["stores_dir"], os.W_OK):
        raise OSError(
            "We cannot write to our local directory of datasets, %r" % ret["stores_dir"]
        )

    return ret


def free_space(path=None):
    """Says how many bytes are free on the filesystem that stores that mentioned path.
    @param path: path to check for (shutil will figure out what filesystem that is on),
    Defaults to the directory we would store datasets into.
    """
    import shutil

    if path is None:
        path = wetsuite_dir()["datasets_dir"]
    return shutil.disk_usage(path).free


def unified_diff(before:str, after:str, strip_header=True, context_n=999) -> str:
    """Returns an unified-diff-like difference between two strings
    Not meant for actual patching, just for quick debug-printing of changes.

    @param before: a string to treat as the original
    @param after: a string  to treat as the new version
    @param strip_header: whether to strip the first lines
    @param context_n: how much context to include. 
    Defaults to something high so that it omits little to nothing.
    @return: a string that contains plain text unified-diff-like output (with initial header cut off)
    """
    lines = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile="before",
            tofile="after",
            n=context_n,
        )
    )
    if strip_header:
        lines = lines[4:]
    return "\n".join(lines)


def hash_color(string:str, on=None):
    """Give a CSS color for a string - consistently the same each time based on a hash.

    Takes a string, and returns C{(css_str, r,g,b)},
    where r,g,b are 255-scale r,g,b values for the same color.

    Usable e.g. to make tables with categorical values more skimmable.

    @param string: the string to hash
    @param on: if 'dark', we try for a bright color, 
    if 'light', we try to give a dark color, otherwise not restricted
    """
    dig = hash_hex(string.encode("utf8"), as_bytes=True)
    r, g, b = dig[0:3]
    if on == "dark":
        r = min(255, max(0, r / 2 + 128))
        g = min(255, max(0, g / 2 + 128))
        b = min(255, max(0, b / 2 + 128))
    elif on == "light":
        r = min(255, max(0, r / 2))
        g = min(255, max(0, g / 2))
        b = min(255, max(0, b / 2))
    r, g, b = int(r), int(g), int(b)
    css = "#%02x%02x%02x" % (r, g, b)
    return css, (r, g, b)


def hash_hex(data:bytes, as_bytes:bool = False):
    """Given some byte data, calculate SHA1 hash.
    Returns that hash as a hex string, unless you specify as_bytes=True

    If instead given a (unicode) string, it accepts it and deals with unicode 
    by UTF8-encoding it first. Warning: This is not always what you want.
    
    @param data: the bytes to hash
    @param as_bytes: whether to return the hash dugest as a bytes object. 
    Defaults to False, meaning a hex string (like 'a49d')
    """
    if   isinstance(data, bytes):
        pass
    elif isinstance( data, str ):  # assume you want _a_ consistent hash value for the same input, not necessarily according to any standard
        data = data.encode("u8")
    else:
        raise TypeError("hash_hex() only accepts byte/str data")
    s1h = hashlib.sha1()
    s1h.update(data)
    if as_bytes:
        return s1h.digest()
    else:
        return s1h.hexdigest()


def is_html(bytesdata:bytes) -> bool:
    """Do these bytes look loke a HTML document? (no specific distinction to XHTML)
    @param bytesdata: the bytestring to check is a HTML file.
    @return: whether it is HTML
    """
    firstbytes = bytesdata[:200]
    if not isinstance(bytesdata, bytes):
        raise TypeError(f"is_html() expects a bytestring, not a {type(bytesdata)}")
    if b"<!DOCTYPE html" in firstbytes: # note: strong indicator, but was optional before HTML5
        return True
    if b"<html" in firstbytes:
        return True
    return False


def has_xml_header(bytesdata:bytes):
    """ Mostly meant as a "reject as HTML?" optimization
        (it is not actually an is_xml test because the declaration is optional in 1.0 (required in 1.1)
        and this won't match e.g. UTF-16 XML, but it still catches a _lot_ of real-world XML)
    """
    initial_bytes = bytesdata[:100]
    if b'<?xml' in initial_bytes:
        return True
    # CONSIDER: UTF-16;
    # TODO: refresh about the BOM-ful and BOM-less variants, and that the following _usefully_ ignores that
    # TODO: test that the following works before adding it
    #if b'<\x00?\x00x\x00m\x00l\x00' in initial_bytes: # '<?xml'.encode('utf_16_le')
    #    return True
    #if b'\x00<\x00?\x00x\x00m\x00l' in initial_bytes: # '<?xml'.encode('utf_16_be')
    #    return True
    return False


def is_xml(bytesdata_or_filename, return_for_html=False, accept_after_n_nodes:int=25) -> bool:
    """Does this look and work like an XML file?

    Yes, we could answer "does it look vaguely like the start of an XML" 
    for a lot cheaper than parsing it.
    
    Yet that doesn't have a lot of value in practice, 
    because you would probably only use this function right before
    handing it to an XML parser to do a full parse - or deciding not to.

    A full parse is the best test, but that would just be double work.
    So in practice, a function that answers 'would a real XML parser probably accept this?'
    more cheapy than a full parse is probably more useful.
    
    It's probably lighter to see if the first bunch of nodes don't break XML semantics 
    (we use lxml's iterparse and stop after a number of nodes went fine).

    (TODO: the input-type code can be made lighter)

    Note on semantics: We consider HTML but also XHMTL to warrant a False,
    mostly due to the way we use this function ourselves.

    @param bytesdata_or_filename: 
    If given bytes, it considers it file contents.
    If given a str object, it considers that a _filesystem filename_ to read from

    @param accept_after_n_nodes: After how many nodes (that parsed fine) 
    do we accept this and stop parsing?

    @return: whether it is XML  - and probably not XHTML or HTML
    """
    # arguably a simple and thorough way is to tell that
    #   it parses in a fairly strict XML/HTML parser,
    #   and the root node is _not_ called 'html'  (HTML or XHTML)
    #
    # There are many other indicators that are cheaper -- but only a good guess, and not _always_ correct,
    #  depending on whether you are asking

    if isinstance(bytesdata_or_filename, bytes): # interpret as file contents
        f = io.BytesIO(bytesdata_or_filename)
    elif isinstance(bytesdata_or_filename, str): # interpret as filename
        f = bytesdata_or_filename
    else:
        raise TypeError("is_xml expects a bytestring, not a %s" % type(bytesdata_or_filename))


    # the ordering here is more about efficiency than function
    if is_html(bytesdata_or_filename):  # cheaper than parsing fully, at least (this makes some code below irrelevant)
        return False
    if is_pdf(bytesdata_or_filename):  # cheaper than parsing
        return False

    ## This is the "answer whether it would parse by parsing only the first so-much"
    root_tag = None
    try:
        seen_nodes = 0
        # iterparse expects to stream data, so takes either a filename or a file object, hence the BytesIO
        for event, element in lxml.etree.iterparse( f, events=('start',) ):
            seen_nodes += 1
            if root_tag is None and event=='start':
                root_tag = element.tag
                if root_tag == 'html': # should have been caught by is_html above
                    return False
                #print('root is', root_tag)
            if seen_nodes > accept_after_n_nodes:
                return True
            #print( seen_nodes, event, lxml.etree.tostring(element) )
            #element.clear() # if accept_after is lowish, we likely avoid large memory anyway and don't need the extra work of clear() or previous-sibling removal
    except lxml.etree.XMLSyntaxError:  # if it doesn't parse  (not 100% on the exception to use - what's lxml.etree.ParserError then, something wider perhaps?)
        return False

    ## This was the "answer whether it would parse by parsing it completely" implementation
    #try:
    #    root = wetsuite.helpers.etree.fromstring(bytesdata)
    #root_tag = root.tag
    #except lxml.etree.XMLSyntaxError as xse:  # if it doesn't parse  (not 100% on the exception? What's lxml.etree.ParserError then?)
    #    if debug:
    #        print(xse)
    #    return False

    #if it's valid as XML but the root node is 'html', we do not consider it XML
    if root_tag is not None and root_tag.startswith("{"):  # deal with a namespaced root without calling strip_namespaces
        root_tag = root_tag[root_tag.index("}")+1:]
    if root_tag == "html":
        return False
    return True



def is_pdf(bytesdata:bytes) -> bool:
    """Does this bytestring look like a PDF document?
    @param bytesdata: the bytestring to check looks like the start of a PDF
    @return: whether it is PDF
    """
    if not isinstance(bytesdata, bytes):
        raise TypeError(f"is_pdf expects a bytestring, not a {type(bytesdata)}")
    return bytesdata.startswith(b"%PDF")


def is_zip(bytesdata:bytes) -> bool:
    """Does this bytestring look like a ZIP file?
    @param bytesdata: the bytestring to check contains a ZIP file.
    @return: whether it is a ZIP
    """
    if not isinstance(bytesdata, bytes):
        raise TypeError(f"is_zip expects a bytestring, not a {type(bytesdata)}")
    if bytesdata.startswith( b"PK\x03\x04" ):  # (most)
        return True
    if bytesdata.startswith( b"PK\x05\x06" ): # still a zip, even if it's not practically useful for us
        return True
    return False


def is_empty_zip(bytesdata:bytes) -> bool:
    """Does this bytestring look like an empty ZIP file?
    @param bytesdata: the bytestring to check contains a ZIP file that stores nothing.
    @return: whether it is an empty ZIP
    """
    if not isinstance(bytesdata, bytes):
        raise TypeError(f"is_empty_zip expects a bytestring, not a {type(bytesdata)}")
    if bytesdata.startswith( b"PK\x05\x06" ):
        return True
    return False


def is_htmlzip(bytesdata:bytes) -> bool:
    """Made for the .html.zip files that KOOP puts e.g. in its BUS.

    Is this a ZIP file with one entry for which the name ends with .html?
    (we could test its content with is_html it but given the context we can assume it)

    @param bytesdata: the bytestring to check/treat as a ZIP file.
    @return: whether it is a ZIP containing HTML
    """
    if not isinstance(bytesdata, bytes):
        raise TypeError("is_htmlzip expects a bytestring, not a %s" % type(bytesdata))
    if not is_zip(bytesdata):
        return False
    z = zipfile.ZipFile(io.BytesIO(bytesdata))
    if len(z.filelist) == 0:
        return False
    for zipinfo in z.filelist:
        if zipinfo.filename.endswith(".html"):
            return True
    return False  # is zip, which has files, but no .html


def get_ziphtml(bytesdata:bytes):
    """Made for the .html.zip files that KOOP puts e.g. in its BUS.

    Gets the contents of the first file from the zip with a name ending in .html
    Assuming you tested with is_htmlzip() this should be the main file
    (there might also e.g. be images in there)

    Returns a bytestring, or raises and exception

    @param bytesdata: the bytestring to treat as a ZIP file.
    @return: the HTML file as a bytes object
    """
    if not isinstance(bytesdata, bytes):
        raise TypeError("get_ziphtml expects a bytestring, not a %s" % type(bytesdata))
    z = zipfile.ZipFile(io.BytesIO(bytesdata))
    if len(z.filelist) == 0:
        raise ValueError("empty ZIP file")
    else:
        for zipinfo in z.filelist:
            if zipinfo.filename.endswith(".html"):
                return z.read(zipinfo)
    raise ValueError("ZIP file without a .html")


def is_doc(bytesdata:bytes) -> bool:
    """Does this seem like some kind of office document type?
    This is currently quick and dirty based on some observations that may not even be correct.
    TODO: improve
    """
    # an empty docx seems to have at least

    # cfbf, assume early office document - or encrypted docx
    if bytesdata.startswith(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'):
        return True
        #Note: Apparently encrypted docx is stored within cfbf, not plain zip ?
        # if '\x57\x00\x6f\x00\x72\x00\x64\x00\x44\x00\x6f\x00\x63'

    # quick and dirty and won't catch different encodings
    if bytesdata.startswith(b'<?xml')  and  b'schemas.uof.org/cn/2003/uof' in bytesdata[:1000]:
        return True

    if is_zip(bytesdata):
        # Then it can be Office Open XML, OpenOffice.org XML, OpenDocument
        with zipfile.ZipFile(io.BytesIO(bytesdata)) as z:
            for zipinfo in z.filelist:
                #if debug:
                #    print(zipinfo)
                if "_rels/" in zipinfo.filename: # likely Office Open XML.   Technically OPC, we could be more specific.
                    return True
                if zipinfo.filename == "mimetype": # other things to match include meta.xml, styles.xml, META-INF/manifest.xml
                # the mimetype file's contest may be interesting, to find something like 'application/vnd.oasis.opendocument.text'
                    return True
    return False


def _filetype(docbytes:bytes):
    ' describe which of these basic types a bytes object contains '
    if is_doc(docbytes): # should appear before is_zip
        return 'doc'
    if is_pdf(docbytes):
        return 'pdf'
    if is_html(docbytes):
        return 'html'
    if is_xml(docbytes):
        return 'xml'
    if is_zip(docbytes):
        return 'zip'
    return 'other'
