#!/usr/bin/python3
""" Tools for jupyter/ipython-style notebooks, and detection that you are, or are _not_, using one right now.

"""
import warnings
import time
import sys


def detect_env():
    """Use this to detect what kind of environment the calling code is running in.

    Returns a dict with keys that map to booleans:
        - 'interactive'  - whether it's interactive
                (e.g. regular python REPL, ipython REPL, notebook, or qtconsole)
        - 'notebook'     - whether it's a notebook
                (also including colab, qtconsole)
        - 'ipython'      - whether IPython is available
                (note this will also return True if the module just happens to be installed and available)

    (when we see pytest, we fake all False, because that's probably closer -- probably better than noticing the IPython that pytest seems to mock)
    """
    ret = {}

    if (
        "pytest" in sys.modules
    ):  # pytest seems to mock IPython, which confuses the below
        ret["ipython"] = False
        ret["interactive"] = False
        ret["notebook"] = False
        return ret

    try:  # probably slightly less nasty than by-classname below
        # pylint disable,  because it not being available or not is the thing under test, and the point
        import google.colab #   pylint: disable=unused-import

        ret["ipython"] = True
        ret["interactive"] = True
        ret["notebook"] = True
        ret["colab"] = True
        return ret
    except ImportError:  # probably also further errrs?
        pass

    try:
        import IPython  # pylint:disable=C0415

        ret["ipython"] = True
        ipyshell = IPython.get_ipython().__class__.__name__
        if ipyshell == "ZMQInteractiveShell":  # jupyter notebook or qtconsole
            ret["interactive"] = True
            ret["notebook"] = True
        elif ipyshell == "TerminalInteractiveShell":  # interactive ipython shell
            ret["interactive"] = True
            ret["notebook"] = False
        elif (
            ipyshell == "NoneType"
        ):  # ipython installed, but this is a regular interactive(?) python shell?  Possibly other cases?
            ret["interactive"] = True
            ret["notebook"] = False
        else:
            raise ValueError("we probably want to understand %r" % ipyshell)

    except ImportError:  # no IPython, no notebook, but possibly interactive
        ret["ipython"] = False
        ret["notebook"] = False
        if hasattr(
            sys, "ps1"
        ):  # see https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
            ret["interactive"] = True  # regular python, interactive
        else:
            ret["interactive"] = False  # regular python, not interactive
    return ret


def is_notebook():
    "returns whether we are running in a notebook (see detect_env)"
    return detect_env()["notebook"]


def is_ipython():
    """returns whether IPython is available (see detect_env) - note that you might want to combine this with is_interactive
    (depending on what you are really testing )"""
    return detect_env()["ipython"]


def is_interactive():
    "returns whether we are using an interactive thing (see detect_env)"
    return detect_env()["interactive"]


def is_ipython_interactive():
    "return whether this seems to be interactive in the REPL-like sense (is_ipython and is_interactive)"
    env = detect_env()
    return env["ipython"] and env["interactive"]


def progress_bar(maxval, description="", display=True):  # , **kwargs
    """A progress bar that should work in notebooks -- but also outside them if you have tqdm installed

    More precisely:
        - wraps tqdm and ipywidgets's IntProgress progress bar;
        - prefers tqdm if installed, falls back to IntProgress.

    CONSIDER: parameter to force text mode
        
    Compared to L{ProgressBar}, this one is more typing but also does a little more,
    letting you set (and get) .value and .description on the fly,
    so e.g. usable like::
        prog = progress_bar( 10, 'overall' )
        for i in range(10):
            prog.value += 1
            time.sleep(1)
        prog.description = 'finished'

    @param maxval: maximum value to count towards (required)
    @param description: text to also show in the progress bar
    @param display: if True, (default), then in a notebook we will call display() on the IPython widget, so you don't have to do so to get it visible.
    @return: an object representing a progress bar, that you can set the .value and .description on.
    """
    #console_only=False
    try:
        from tqdm import TqdmExperimentalWarning

        # TODO: actually read up on what that warning means exactly
        warnings.filterwarnings("ignore", category=TqdmExperimentalWarning) # TODO: use context manager

        #if console_only:
        #    import tqdm.std
        #else:
        import tqdm.autonotebook  # pylint: disable=C0415

        class TqdmWrap:
            "make it act enough like the ipywidget, in terms of our description"

            def __init__(self, maxval, description):
                #if console_only:
                #    self.tq = tqdm.std.tqdm(total=maxval, desc=description)
                #else:
                self.tq = tqdm.autonotebook.tqdm(total=maxval, desc=description)
                self._value = 0
                self._description = description

            def set_value(self, val):
                "setter wrapper (will be part of property decorator)"
                diff = val - self._value
                self._value = val
                # tqdm seems to want the amount of increase, not the new value
                if diff > 0:
                    self.tq.update(diff)

            def get_value(self):
                "getter wrapper (will be part of property decorator)"
                return self._value

            value = property(get_value, set_value)

            def set_description(self, val):
                "setter wrapper (will be part of property decorator)"
                self._description = val
                self.tq.desc = self._description

            def get_description(self):
                "getter wrapper (will be part of property decorator)"
                return self._description

            description = property(get_description, set_description)

        return TqdmWrap(maxval, description)

    except ImportError:  # tqdm not installed? fall back to ipywidgets.IntProgress bar
        import IPython.display, ipywidgets

        prog = ipywidgets.IntProgress(max=maxval, description=description)
        if display:
            IPython.display.display(prog)
        return prog


class ProgressBar:
    """A sequence-iterating progress bar (like tqdm) that supports both notebooks and console, 
    and prefers notebook over console style in notebooks.

    CONSIDER: parameter to force text mode

    e.g. usable like::
        data = ['a','b',3]
        for item in ProgressBar(data, 'parsing... '):
            time.sleep(1)

    Compared to the similar L{progress_bar}, this one is less typing, 
    but a little more basic, in that...
        - Unlike creating a progress_bar object, you don't get to change its description.
        - Unlike tqdm, we only work with something that has a length and is subscriptable,
          and has no fallback for...
            - unknown-length iterables
              (such as generators or enumerate)
            - known-length but unsubscriptable iterators
              (such as dict_items, and set type - yould need to wrap a list() around it)
              we could hardcode those to work, though...

    Yes, it's silly that we e.g. wrap tqdm in two layers of interfaces
    to then present a poorer version of what it does in the first place.
    We should probably try being cleverer.

    Also, it seems that the notebook variant can only take ~20K/s updates,
    so will effectively rate-limit anything that wants to go faster than that;
    """

    def __init__(self, iterable, description=""):
        self.is_notebook = is_notebook()

        if isinstance(iterable, enumerate):
            # enumarate has no len, even if the iterable it was based on did.
            # the following reads out all values from the enumeration and stores them.
            # If it was a lazy generator for a reason, THIS IS NOT NECESSARILY A SMART THING TO DO!
            iterable = list(iterable.__iter__())

        try:
            self._len = len(iterable)
        except TypeError as te:
            # if 'has no len' in str(te): # CONSIDER give a nicer answer
            raise te
            # self._len = 0  # bad idea?  Except our code needs _something_.

        # this may be a cleanish way to support things that are known-length but unsubscriptable,
        # like set or dict_items without materializing them entirely
        # (wraps an iterator around things that already are), but this needs reading up and testing
        if not hasattr(iterable, "__next__"):  # assumes py3
            # assumes what you handed in is iterable.  What do you expect of a progress bar otherwise?
            iterable = iter(iterable)
            # print( "making iterator over %s"%type(iterable) )
        # else:
        #    print( "already iterable: %s"%type(iterable) )

        self._iterable = iterable

        self._cur = -1
        self.pb = progress_bar(self._len, description=description, )

    def __len__(self):
        return self._len

    def __iter__(self):
        return self

    def __next__(self):
        self._cur += 1

        if self._cur == self._len:  #
            raise StopIteration

        # this is a hacky way to make it somewhat likelier
        #   that a dynamic in-notebook progress bar gets updated -- I _think_
        if self.is_notebook:
            time.sleep(0.000001)

        self.pb.value = self._cur
        # return self._iterable[self._cur]
        return self._iterable.__next__()


# TODO: for consistency, move this to etree, or other notebooks there to here
class etree_visualize_selection:
    """Produces a colorized representation of selection within an XML document.
    (works only within IPython/jupyter style notebooks,  via a HTML representation.)
    """

    def __init__(
        self,
        tree,
        xpath_or_elements,
        reindent: bool = True,
        mark_text: bool = True,
        mark_tail: bool = False,
        mark_subtree: bool = False,
    ):
        """Produces a colorized representation of selection within an XML document.
        (works only within IPython/jupyter style notebooks. works via a HTML representation.)

        Given
          - a parsed tree
            (or a bytes object, will be parsed, but you probably shouldn't do that)
          - either
            - a sequence of elements from a tree  (that you probably selected yourself)
            - or a string, interpreted as xpath
        ...and optionally:
          - reindent      display reindented copy of the tree
                          (defaults True, this is debug function)
          - mark_text:    mark initial text content of each matched element)
          - mark_tail:    mark tail-text after each matched element)
          - mark_subtree: mark entire tree under each matched element. Useful

        Mostly used in the tutorials
        """
        import wetsuite.helpers.etree

        if isinstance(tree, bytes):
            tree = wetsuite.helpers.etree.fromstring(tree)

        if reindent:
            tree = wetsuite.helpers.etree.indent(tree)
        self.tree = tree
        self.xpath_or_elements = xpath_or_elements
        self.mark_text = mark_text
        self.mark_tail = mark_tail
        self.mark_subtree = mark_subtree

    def _repr_html_(self):
        from wetsuite.helpers.escape import attr  # , nodetext
        from lxml.etree import _Comment, _ProcessingInstruction  # pylint:disable=E0611

        ret = ["<pre>"]

        if isinstance(self.xpath_or_elements, str):
            selection = self.tree.xpath(self.xpath_or_elements)
        else:
            selection = list(self.xpath_or_elements)

        def conditional_highlight(element):
            if element in selection:
                return '<span style="background-color:red; color:white">%s</span>' % (
                    element.tag
                )
            return "%s" % (element.tag)

        def serialize(element):
            if isinstance(element, _Comment) or isinstance(
                element, _ProcessingInstruction
            ):
                return

            ret.append("&lt;%s" % (conditional_highlight(element),))
            for ak, av in element.items():  # attributes
                ret.append(' %s="%s"' % (ak, attr(av)))
            ret.append("&gt;")

            if element.text:
                # if self.mark_text and element in selection:
                if (
                    self.mark_text and len(element.text.strip()) > 0
                ) and element in selection:
                    ret.append(
                        '<span style="background-color:#faa; color:black">%s</span>'
                        % element.text
                    )
                else:
                    ret.append(element.text)

            if self.mark_subtree and element in selection:
                ret.append('<span style="background-color:#caa; color:black">')

            for child in element:
                serialize(child)

            if self.mark_subtree and element in selection:
                ret.append("</span>")
            ret.append("&lt;/%s&gt;" % conditional_highlight(element))

            if element.tail:
                # if (self.mark_tail  and len(element.tail.strip())>0)  and  element in selection:
                if self.mark_tail and element in selection:
                    ret.append(
                        '<span style="background-color:#fab; color:black">%s</span>'
                        % element.tail
                    )
                else:
                    ret.append(element.tail)

        serialize(self.tree)
        ret.append("</pre>")
        return "".join(ret)


def set_proctitle(proctitle="wetsuite-notebook"):
    ''' 
    Might throw an exception, e.g. an ImportError'
    '''
    import setproctitle
    setproctitle.setproctitle( proctitle ) # pylint: disable=c-extension-no-member


if is_notebook():
    # for debug: make the process easier to recognize for people wondering what's taking so much CPU.
    # Should probably be in a function, or otherwise conditional, NOT happen globally on import
    try:
        set_proctitle("wetsuite-notebook") # pylint: disable=c-extension-no-member
    except ImportError:
        pass

