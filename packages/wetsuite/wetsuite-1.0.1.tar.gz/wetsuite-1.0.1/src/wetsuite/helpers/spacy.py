"""
helper functions related to spacy natural language parsing.

TODO: decide whether we want to import spacy globally - if a user hadn't yet it would be a heavy import
and there may be things you want to control before that, like tensorflow warning suppression.
...though chances are you'll import this helper after that, so it might be fine.

TODO: cleanup
"""

# import time, json, collections
import re


def reload():
    "quick and dirty way to save some time reloading during development"
    import importlib
    import wetsuite.helpers.spacy

    importlib.reload(wetsuite.helpers.spacy)


def span_as_doc(span):
    "unused?  Also, what was its purpose again?"
    return span.as_doc()


class notebook_content_visualisation:
    """Python notebook visualisation to give some visual idea of contents:
    marks out-of-vocabulary tokens red, and highlight the more interesting words (by POS).

    Uses a sort of dark-mode scheme
    """

    def __init__(self, doc, mark_oov=True, highlight_content=True):
        if isinstance(doc, (str, list)):
            raise TypeError('This visualization takes a spacy doc object, not a %s'%type(doc))
        self.doc = doc
        self.mark_oov = mark_oov
        self.highlight_content = highlight_content

    def _repr_html_(self):
        from wetsuite.helpers.escape import attr, nodetext

        ret = []
        for token in list(self.doc):
            style = "padding:1px 4px; outline:1px solid #0002"
            if self.highlight_content:
                if token.pos_ in (
                    "PUNCT",
                    "SPACE",
                    "X",
                    "AUX",
                    "DET",
                    "CCONJ",
                ):
                    style += ";opacity:0.3"
                elif token.pos_ in (
                    "NOUN",
                    "PROPN",
                ):
                    style += ";opacity:0.9;color:#fafaff; "
                elif token.pos_ in (
                    "ADP",
                    "VERB",
                ):
                    style += ";opacity:0.7;color:#fee"
            if self.mark_oov and token.is_oov and token.pos_ not in ("SPACE",):
                style += ";background-color:#833"
            ret.append(
                '<span title="%s" style="%s">%s</span>'
                % (
                    attr(token.pos_) + " " + attr(token.tag_),
                    style,
                    nodetext(token.text),
                )
            )
            ret.append("<span>%s</span>" % token.whitespace_)
        return '<div style="background:#3b3759">%s</div>'%("".join(ret),)


def sentence_complexity_spacy(span):
    """Takes an already-parsed spacy sentence

    Mainly uses the distance of the dependencies involved,
    ...which is fairly decent for how simple it is.

    Consider e.g.
        - long sentences aren't necessarily complex at all (they can just be separate things joined by a comma),
            they mainly become harder to parse if they introduce long-distance references.
        - parenthetical sentences will lengthen references across them
        - lists and flat compounds will drag the complexity down

    Also, this doesn't really need normalization

    Downsides include that spacy seems to assign some dependencies just because it needs to, not necessarily sensibly.
    Also, we should probably count most named entities as a single thing, not the amount of tokens in them
    """
    dists = []
    # print( "-")
    for tok in span:
        dist = tok.head.i - tok.i
        # print("%s --%s--> %s (dist %d)"%(tok, tok.dep_, tok.head, dist) )
        dists.append(dist)
        # no abs, we may want to weigh forward referenes harder than backwards -- but probably check that with each specific dependency type?
    # print( dists, sent )
    abs_dists = list(abs(d) for d in dists)
    avg_dist = float(sum(abs_dists)) / len(abs_dists)

    # token.is_oov

    # other ideas:
    # - count amount of referents / people
    # - word frequency
    # - collocations

    # https://raw.githubusercontent.com/proycon/tscan/master/docs/tscanhandleiding.pdf

    return avg_dist


def interesting_words(
    span, ignore_stop=True, ignore_pos_=("PUNCT", "SPACE", "X", "AUX", "DET", "CCONJ"), as_text=False
):
    """
    Takes an already-parsed spacy span (or something else that iterates as tokens),
    uses the pos_ attribute to 
    return only the more interesting tokens, ignoring stopwords, function words, and such.

    Currently tries to include only tokens where the part of speech (`pos_`) is one of 
    "NOUN", "PROPN", "NUM", "ADJ", "VERB", "ADP", "ADV"

    @param span: the doc, sentence, or other span to iterate for Tokens
    @param ignore_stop: whether to ignore what spacy considers is_stop
    @param ignore_pos_: what list of pos_ to ignore (meant to avoid the things that it would normally include)
    @param as_text: return a list of strings, rather than a list of spans
    @return: list of either tokens, or strings (according to as_text)
    """
    # import spacy
    import spacy.tokens.span_group
    import spacy.tokens.span

    docref = span.doc

    ret = []

    for tok in span:
        if ignore_stop and tok.is_stop:
            pass
        elif tok.pos_ in ignore_pos_:
            pass
        elif tok.pos_ in ("NOUN", "PROPN", "NUM"):
            if as_text:
                ret.append( tok.text )
            else:
                ret.append(spacy.tokens.span.Span(docref, tok.i, tok.i + 1))  # pylint: disable=c-extension-no-member
            # print( '1 %s/%s'%(tok.text, tok.pos_) )
        elif tok.pos_ in ("ADJ", "VERB", "ADP", "ADV"):
            if as_text:
                ret.append( tok.text )
            else:
                ret.append(spacy.tokens.span.Span(docref, tok.i, tok.i + 1))  # pylint: disable=c-extension-no-member
            # print( '2 %s/%s'%(tok.text, tok.pos_) )
        else:
            pass
            # print( '? %s/%s'%(tok.text, tok.pos_) )
    return ret




def subjects_in_doc(doc):
    """Given a parsed documment,
    returns the nominal/clausal subjects for each sentence individually,
    as a list of lists (of Tokens), e.g.
      - I am a fish. You are a moose  ->   [ [I ], [You] ]

    If no sentences are annotated, it will return None
    @param doc: spacy Document
    @return: list of list of tokens
    """
    if hasattr( doc, "sents" ):  # TODO: check that all docs have a .sents - presumably not
        return list((subjects_in_span(sent)) for sent in doc.sents)
    else:
        return None


def subjects_in_span(span):
    """For a given span, returns a list of subjects (there can zero, one, or more)

    If given a Doc that means all sentences's. Sometimes that's what you want,
    yet if you wanted them per sentence, see subjects_in_doc.

    Returns a mapping from each subject to related information, e.g.
       - Token(she):    { verb:Token(went) }
       - Token(Taking): { verb:Token(relax), object:Token(nap), clause:[Token(Taking), Token(a), Token(nap)] }
    You may only be interested in its keys. What's in the values is undecided and may change.

    Relevant here are
      - nsubj - nominal subject, a non-clausal constituent in the subject position  of an active verb.
        A nonclausal consituent with the SBJ function tag is considered a nsubj.

    TODO: actually implement
    """
    ret = {}
    for tok in span:
        if hasattr(tok, "tok.dep_"):  # maybe warn otherwise?
            if tok.dep_ == "nsubj":
                pass

    return ret


# CONSIDER: a our own prefer_gpu/prefer_cpu that we listen to if and when a function first loads spacy


################################################################################################################
# The rest will decide to load models themselves: CONSIDER: making that more flexible


# CONSIDER: making the following less hardcoded
_dutch = None


def nl_noun_chunks(text: str, load_model_name: str = "nl_core_news_lg") -> list:
    """Meant as a quick and dirty way to pre-process text for when experimenting with models,
    as a particularly to remove function words

    To be more than that we might use something like spacy's pattern matching

    # CONSIDER: taking a model name, and/or nlp object.
    """
    global _dutch
    if _dutch is None:  # TODO: look for and accept any/best installed duch model
        import spacy

        # spacy.prefer_gpu() # TODO: conditional
        _dutch = spacy.load(load_model_name)
    doc = _dutch(text)
    ret = []
    for nc in doc.noun_chunks:
        ret.append(nc.text)
    return ret


_english = None


def en_noun_chunks(text: str, load_model_name: str = "en_core_web_trf") -> list:
    "Quick and dirty way to get some noun chunks out of english text"
    global _english
    if _english is None:
        import spacy

        # spacy.prefer_gpu() # TODO: conditional
        _english = spacy.load(load_model_name)
    doc = _english(text)
    ret = []
    for nc in doc.noun_chunks:
        ret.append(nc.text)
    return ret



_langdet_model = None

def detect_language(string: str):  #  -> tuple(str, float)
    """ Detects language
    Note that this depends on the spacy_fastlang library, which depends on the fasttext library.

    Returns (lang, score)
      - lang string as used by spacy          (xx if don't know)
      - score is an approximated certainty

    Depends on spacy_fastlang and loads it on first call of this function.  Which will fail if not installed.

    CONSIDER: truncate the text to something reasonable to not use too much memory.   On parameter?

    @param string: the text to determine the language of 
    """
    # monkey patch done before the import to suppress "`load_model` does not return WordVectorModel or SupervisedModel any more, but a `FastText` object which is very similar."
    try:
        import fasttext

        fasttext.FastText.eprint = lambda x: None
    except ImportError:
        pass

    import spacy_fastlang # if this fails, you may need a    pip install spacy_fastlang     (also, yes pylint, it is used, spacy just does it in an obscured way     pylint: disable=unused-import)
    import spacy

    global _langdet_model
    if _langdet_model is None:
        # print("Loading spacy_fastlang into pipeline")
        _langdet_model = spacy.blank("xx")
        _langdet_model.add_pipe("language_detector")
        # lang_model.max_length = 10000000 # we have a trivial pipeline, though  TODO: still check its memory requirements
    # else:
    #    print("Using loaded spacy_fastlang")

    doc = _langdet_model(string)

    return doc._.language, doc._.language_score


_xx_sent_model = None


def sentence_split(string: str, as_plain_sents=False):
    """A language-agnostic sentence splitter based on the `xx_sent_ud_sm` model.

    @param string: the text to split into sentences

    @return:
      - if as_plain_sents==False: a Doc so you can pick out the .sents attribute
      - if as_plain_sents==False: a sequence of strings (from each sentence Span)
    """
    import spacy

    global _xx_sent_model
    if _xx_sent_model is None:
        _xx_sent_model = spacy.load("xx_sent_ud_sm") # if this fails, you may need   python3 -m spacy download xx_sent_ud_sm

    doc = _xx_sent_model(string)
    if as_plain_sents:
        return list(sent.text for sent in doc.sents)
    else:
        return doc


# _xx_ner_model = None
# def test_xx_ner(text):
#     ''' Trying out the xx_ent_wiki_sm NER model '''
#     import spacy
#     global _xx_ner_model
#     if _xx_ner_model==None:
#         _xx_ner_model  = spacy.load("xx_ent_wiki_sm")
#     doc = _xx_ner_model(text)
#     return doc


def list_installed_models():
    ''' List loadable spacy model names.
        Spacy models are regular python packages, so this is somewhat tricky to do directly, 
        but was implemented in spacy.util in version 3.something.
        
        @return: model names, as a list of strings
    '''
    import spacy.util
    return spacy.util.get_installed_models()


def installed_model_for_language(lang, prefer=('_lg$','_md$','_sm$')):
    ''' Picks an installed model for the given language (where language is the initial string in the model name, e.g. 'en' or 'nl')
        You can crudely give some preference as to which among multiple model names to prefer.

        @param lang:   a language string, like 'nl' or 'en'
        @param prefer: a list treated as regexes to be matched against each model name, where matches earlier in that list are preferred
        @return: the model name that seems to match best.  Raises a ValueError if there are no models for the given language.
    '''
    scoring = {}
    for i, string in enumerate(prefer):
        scoring[string] = i # note: lower is better

    scores = {}
    for model_name in list_installed_models():
        model_lang = model_name.split('_',1)[0]
        if model_lang != lang:
            continue
        for pre, score in scoring.items():
            if re.search(pre, model_name) is not None:
                scores[model_name] = score

    if len(scores)==0:
        raise ValueError("We seem to have no installed models for language %r"%lang)

    scoso = sorted( (score, name)  for name, score in scores.items() )

    return scoso[0][1] # name for the lowest score
