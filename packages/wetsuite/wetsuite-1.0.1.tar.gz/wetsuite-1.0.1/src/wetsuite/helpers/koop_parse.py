"""
Data and metadata parsing that is probably specific to KOOP's SRU repositories.

For more general things, see 
  - meta.py
  - patterns.py
"""

import re
import sys
import urllib.parse
import warnings
import collections
from typing import Union

import wetsuite.datacollect.koop_sru
import wetsuite.helpers.meta

import wetsuite.helpers.etree

from wetsuite.helpers.etree import _Comment, _ProcessingInstruction, tostring


def cvdr_meta(tree, flatten=False):
    """Extracts metadata from a CVDR SRU search result's individual record, or CVDR content xml's root.

    Because various elements can repeat - and various things frequently do (e.g. 'source'), each value is a list.
    using flatten=True MAY CLOBBER DATA and is only recommended for quick and dirty debug prints, not for real use.

    Context for flatten:
    ====================
    In a lot of cases we care mainly for tagname and text, and there are no attributes, e.g.
      - owmskern's    <identifier>CVDR641872_2</identifier>
      - owmskern's    <title>Nadere regels jeugdhulp gemeente Pijnacker-Nootdorp 2020</title>
      - owmskern's    <language>nl</language>
      - owmskern's    <modified>2022-02-17</modified>
      - owmsmantel's  <alternative>Nadere regels jeugdhulp gemeente Pijnacker-Nootdorp 2020</alternative>
      - owmsmantel's  <subject>maatschappelijke zorg en welzijn</subject>
      - owmsmantel's  <issued>2022-02-08</issued>
      - owmsmantel's  <rights>De tekst in dit document is vrij van auteursrecht en databankrecht</rights>

    In others you may also care about an attribute or two, e.g.:
      - owmskern's    <type scheme="overheid:Informatietype">regeling</type>  (except there's no variation in that value anyway)
      - owmskern's    <creator scheme="overheid:Gemeente">Pijnacker-Nootdorp</creator>
      - owmsmantel's  <isRatifiedBy scheme="overheid:BestuursorgaanGemeente">college van burgemeester en wethouders</isRatifiedBy>
      - owmsmantel's  <isFormatOf resourceIdentifier="https://zoek.officielebekendmakingen.nl/gmb-2022-66747">gmb-2022-66747</isFormatOf>
      - owmsmantel's  <source resourceIdentifier="https://lokaleregelgeving.overheid.nl/CVDR641839">Verordening jeugdhulp gemeente Pijnacker-Nootdorp 2020</source>

    When those attributes matter, you want C{flatten=False} (the default) and you will get a dict like: ::
            { 'creator': [{'attr': {'scheme': 'overheid:Gemeente'}, 'text': 'Zuidplas'}], ... }


    @param tree: an etree object that is either
      - a search result's individual record
        (in which case we're looking for ./recordData/gzd/originalData/meta
      - CVDR content xml's root
        (in which case it's              ./meta)
    ...because both contain almost the same metadata almost the same way (the difference is enrichedData in the search results).

    @param flatten: For quick and dirty presentation (only) you may wish to ask to creatively smush those into one string by asking for C{flatten==True}
    in which case you get something like: ::
            { 'creator': 'Zuidplas (overheid:Gemeente)', ... }
    Please avoid this when you care to deal with data in a structured way  (even if you can sometimes get away with it due to empty attributs).

    @return: a dict containing owmskern, owmsmantel, and cvdripm's elements merged into a single dict.
    If it's a search result, it will also mention its enrichedData.
    """
    # allow people to be lazier - hand in the XML bytes without parsing it into etree
    if isinstance(tree, bytes):
        tree = wetsuite.helpers.etree.fromstring(tree)

    ret = {}
    tree = wetsuite.helpers.etree.strip_namespace(tree)
    # print( wetsuite.helpers.etree.tostring(tree).decode('u8') )

    # we want tree to be the node under which ./meta lives
    # TODO: review, this looks unclear
    if tree.find("meta") is not None:
        meta_under = tree
    else:
        meta_under = tree.find("recordData/gzd/originalData")
        if meta_under is None:
            raise ValueError(
                "got XML that seems to be neither a document or a search result record"
            )

    # this would lead flatten to overwrite data
    enriched_data = tree.find("recordData/gzd/enrichedData")
    if (
        enriched_data is not None
    ):  # only appears in search results, not the XML that points to
        for enriched_key, enriched_val in wetsuite.helpers.etree.kvelements_to_dict(
            enriched_data
        ).items():  # this assumes there is no tag duplication, which only seems to be true here
            if enriched_key not in ret:
                ret[enriched_key] = []
            ret[enriched_key].append(
                {"text": enriched_val, "attr": {}}
            )  # imitate the structure the below use

    owmskern = meta_under.find("meta/owmskern")
    for child in owmskern:
        tagname = child.tag
        if child.text is not None:
            tagtext = child.text
            if tagname not in ret:
                ret[tagname] = []
            ret[tagname].append({"text": tagtext, "attr": child.attrib})

    owmsmantel = meta_under.find("meta/owmsmantel")
    for child in owmsmantel:
        tagname = child.tag
        tagtext = child.text
        if child.text is not None:
            if tagname not in ret:
                ret[tagname] = []
            ret[tagname].append({"text": tagtext, "attr": child.attrib})

    cvdripm = meta_under.find("meta/cvdripm")
    for child in cvdripm:
        tagname = child.tag
        text = "".join(wetsuite.helpers.etree.all_text_fragments(child))
        if tagname not in ret:
            ret[tagname] = []
        ret[tagname].append({"text": text, "attr": child.attrib})

    if flatten:
        simpler = {}
        for meta_key, value_list in ret.items():  # each of the metadata
            simplified_text = []
            for item in value_list:
                text = item["text"]
                if item["attr"]:
                    for _, attr_val in item["attr"].items():
                        # this seems to make decent sense half the time (the attribute name is often less interesting)
                        if len(attr_val.strip()) == 0:  # present but empty
                            text = "%s" % (text,)
                        else:
                            text = "%s (%s)" % (text, attr_val)
                simplified_text.append(text)
            simpler[meta_key] = (",  ".join(simplified_text)).strip()
        ret = simpler

    return ret


def cvdr_parse_identifier(text: str, prepend_cvdr: bool = False):
    """Given a CVDR style identifier string (sometimes called JCDR),
    gives a more normalized version, e.g. useful for indexing.

    For example::
        cvdr_parse_identifier('101404_1')     ==  ('101404', '101404_1')
        cvdr_parse_identifier('CVDR101405_1') ==  ('101405', '101405_1')
        cvdr_parse_identifier('CVDR101406')   ==  ('101406',  None     )
        cvdr_parse_identifier('1.0:101407_1') ==  ('101407', '101407_1')

    @param text:         the thing to parse
    @param prepend_cvdr: whether to put 'CVDR' in front of the work and the expression. Defaults to false.
    @return: a tuple of strings: (work ID, expression ID), the latter of which will be None if input was a work ID; see the examples above.
    If it makes _no_ sense as a CVDR number, it may raise a ValueError instead.
    """
    if ":" in text:
        text = text.split(":", 1)[1]
    cvdr_matchobject = re.match("(?:CVDR)?([0-9]+)([_][0-9]+)?", text.replace("/", "_"))
    if cvdr_matchobject is not None:
        work, enum = cvdr_matchobject.groups()
        if prepend_cvdr:
            work = "CVDR%s" % work
        if enum is None:
            return work, None
        else:
            return work, work + enum
    else:
        raise ValueError("%r does not look like a CVDR identifier" % text)


def cvdr_normalize_expressionid(text: str):
    """When indexing, you may care to transform varied forms (e.g. "112779_1" and "CVDR112779_1")
    into just one normalized form.

    Note that this does not work on workids - we raise an exception for them.
    
    @param text: the identifier to work on.

    @return: the expression - basically the thing cvdr_parse_identifier() returns, _including_ the 'CVDR' at the start

    """
    nex = cvdr_parse_identifier(text, prepend_cvdr=True)[1]
    if nex is None:
        raise ValueError(
            "The given string did not look like a CVDR expression ID  (might be a work ID?)"
        )
    return nex


def cvdr_param_parse(rest: str):
    """Picks the parameters from a juriconnect (jci) style identifier string.

    Mostly a helper function, used e.g. by cvdr_sourcerefs.  Duplicates code in meta.py - TODO: centralize that

    Would turn "BWB://1.0:c:BWBR0008903&artikel=12&g=2011-11-08" into a dict where 'artikel' maps to ['12'], etc.
    @param rest: the string to parse
    @return: a dict containing each variable to a list of values present in this URL-like string
    """
    rest = rest.replace(
        "&amp;", "&"
    )  # hack for observed bad escaping (hacky in that is assumes things about values)
    params = {}
    for param in rest.split("&"):
        pd = urllib.parse.parse_qs(param)
        for key, val in pd.items():
            if key == "artikel":
                val = list(v.lstrip("artikel.") for v in val)
            if key not in params:
                params[key] = val
            else:
                params[key].extend(val)
    return params


def cvdr_text(tree):
    """Given the XML content document as etree object, this is a quick and dirty 'give me mainly the plaintext in it',
    skipping any introductions and such.

    Returns a single string.
    This is currently a best-effort formatting, where you should e.g. find that paragraphs are split with double newlines.

    This is currently mostly copy-pasted from the bwb code TODO: unify, after I figure out all the varying structure

    TODO: write functions that support "give me flat text for each article separately"
    """
    # if isinstance(tree, bytes):
    #    tree = wetsuite.helpers.etree.fromstring( tree )
    ret = []
    tree = wetsuite.helpers.etree.strip_namespace(tree)

    body = tree.find("body")
    regeling = body.find("regeling")
    regeling_tekst = regeling.find("regeling-tekst")

    # identifier = tree.find('meta/owmskern/identifier')

    # TODO: decide on a best way to extract the text from this type of document, and use that in all places it happens

    for (
        artikel
    ) in (
        regeling_tekst.iter()
    ):  # assumes all tekst in these elements, and that they are not nested.  Ignores structure.
        if artikel.tag not in ["artikel", "enig-artikel", "tekst", "structuurtekst"]:
            continue

        if artikel.find("lid") is not None:
            aparts = artikel.findall("lid")
        else:
            aparts = [artikel]

        for apart in aparts:
            if apart.get("status") in ("vervallen",):
                break  # ?

            text = []  # collected per lid, effectively

            # TODO: decide which one of the following two to use, and clean up.

            # this seems a somewhat awkward way to do it, but may be more robust to unusual nesting
            for node in apart.iter():
                # print( node.tag )
                if node.tag in ("al", "table", "definitielijst"):
                    text.extend(
                        ["\n"] + wetsuite.helpers.etree.all_text_fragments(node)
                    )

                elif node.tag in ("extref",):
                    text.extend(wetsuite.helpers.etree.all_text_fragments(node))

                elif node.tag in ("titel",):
                    text.extend(wetsuite.helpers.etree.all_text_fragments(node) + [" "])

                elif node.tag in ("lid",):
                    text.extend(["\n"])

                elif (
                    node.tag
                    in (  # <kop> <label>Artikel</label> <nr>1</nr> <titel>Begripsbepalingen</titel> </kop>
                        "kop",
                        "label",
                        "nr",
                        "li",
                        "lijst",  # we will get its contents
                        "artikel",
                        "lid",
                        "lidnr",
                        "specificatielijst",
                        "li.nr",
                        "meta-data",
                        "tussenkop",
                        "plaatje",
                        "adres",
                    )
                ):
                    # print("%s IGNORE tag type %r"%(identifier, node.tag))
                    pass
                else:
                    pass
                    # print("%s UNKNOWN tag type %r"%(identifier, node.tag))
                    # print( wetsuite.helpers.etree.tostring( node ).decode('u8') )

            # else:
            #     for ch in apart.getchildren():
            #         if ch.tag in ('lidnr', 'meta-data'):
            #             continue

            #         if ch.tag == 'lijst':
            #             for li in ch.getchildren():
            #                 for lich in li:
            #                     if lich.tag in ('al',):
            #                         text.extend( wetsuite.helpers.etree.all_text_fragments( lich ) )
            #                     elif lich.tag in ('lijst',): # we can probably do this a little nicer
            #                         text.extend( wetsuite.helpers.etree.all_text_fragments( lich ) )
            #                     elif lich.tag in ('table',):
            #                         text.extend( wetsuite.helpers.etree.all_text_fragments( lich ) )
            #                     elif lich.tag in ('definitielijst',):
            #                         text.extend( wetsuite.helpers.etree.all_text_fragments( lich ) )
            #                     elif lich.tag in ('specificatielijst',):
            #                         pass
            #                     elif lich.tag in ('li.nr','meta-data',):
            #                         pass
            #                     elif lich.tag in ('tussenkop',):
            #                         pass
            #                     elif lich.tag in ('plaatje',):
            #                         pass
            #                     elif lich.tag in ('adres',):
            #                         pass
            #                     else:
            #                         print("%s IGNORE unknown lijst child %r"%(identifier, lich.tag))
            #                         print( wetsuite.helpers.etree.tostring(lich).decode('u8') )

            #         elif ch.tag in ('al',):
            #             text.extend( wetsuite.helpers.etree.all_text_fragments( ch ) )
            #         elif ch.tag in ('al-groep',):
            #             text.extend( wetsuite.helpers.etree.all_text_fragments( ch ) )
            #         elif ch.tag in ('table',):
            #             text.extend( wetsuite.helpers.etree.all_text_fragments( ch ) )
            #         elif ch.tag in ('definitielijst',):
            #             text.extend( wetsuite.helpers.etree.all_text_fragments( ch ) )

            #         elif ch.tag in ('specificatielijst',):
            #             pass
            #         elif ch.tag in ('kop','tussenkop',):
            #             pass
            #         elif ch.tag in ('adres','adreslijst'):
            #             pass
            #         elif ch.tag in ('artikel.toelichting',):
            #             pass
            #         elif ch.tag in ('plaatje','formule'):
            #             pass
            #         elif ch.tag in ('citaat','wetcitaat',):
            #             pass
            #         else:
            #             print( "%s IGNORE unknown lid-child %r"%(identifier, ch.tag) )
            #             print( wetsuite.helpers.etree.tostring(ch).decode('u8') )

            # print( text )
            lid_text = ("".join(text)).strip(" ")
            # lid_text = re.sub('\s+',' ', lid_text).strip()
            ret.append(lid_text)

    ret = ("\n".join(ret)).strip()
    ret = re.sub(r"\n{2,}", "\n\n", ret)
    return ret


def cvdr_sourcerefs(tree, ignore_without_id=True, debug=False):
    """Given the CVDR XML content document as an etree object,
    looks for the <source> tags (meta/owmsmantel/source), which are references to laws and other regulations (VERIFY)

    This function
      - extracts (only) the source tags that specify
        ...and ignores

    in part to normalize what is in there a bit.
    Be aware this is more creative than a helper function probably should be.

    Returns a list of ::
      (type, origref, specref, parts, source_text)
    where
      - type:         currently one of 'BWB' or 'CVDR'
      - origref:      URL-like reference
      - specref:      just the identifier
      - parts:        dict of parts parsed from URL, or None
      - source_text:  text (name  and often reference to a part);  seems to be more convention-based than standardized

    For example (mostly to point out there is _plenty_ of variation in most parts) ::
     ('BWB',
      '1.0:c:BWBR0015703&artikel=6&g=2014-11-13',
      'BWBR0015703',
      {'artikel': ['6'], 'g': ['2014-11-13']},
      'Participatiewet, art. 6')
    or ::
     ('BWB',
      'http://wetten.overheid.nl/BWBR0015703/geldigheidsdatum_15-05-2011#Hoofdstuk1_12',
      'BWBR0015703',
      {},
      'Wet werk en bijstand, art. 8, lid 1')
    or ::
     ('CVDR',
      'CVDR://103202_1',
      '103202_1',
      None,
      'Inspraakverordening Spijkenisse, art. 2')
    or ::
     ('CVDR',
      '1.1:CVDR229520-1',
      '229520',
      None,
      'Verordening voorzieningen maatschappelijke participatie 2012-A, artikel 4')
    """
    # if isinstance(tree, bytes):
    #    tree = wetsuite.helpers.etree.fromstring( tree )
    ret = []
    tree = wetsuite.helpers.etree.strip_namespace(tree)
    owmsmantel = tree.find("meta/owmsmantel")
    for source in owmsmantel.findall("source"):
        resource_identifier = source.get("resourceIdentifier")
        source_text = source.text

        if source_text is None:
            continue

        source_text = source_text.strip()
        if len(source_text) == 0:
            continue

        if resource_identifier.startswith("CVDR://") or "CVDR" in resource_identifier:
            orig = resource_identifier
            if resource_identifier.startswith("CVDR://"):
                resource_identifier = resource_identifier[7:]
            try:
                parsed = cvdr_parse_identifier(resource_identifier)
                specref = parsed[1]
                if specref is None:
                    specref = parsed[0]
                ret.append(("CVDR", orig, specref, None, source_text))
            except ValueError as ve:
                if debug:
                    print(
                        "failed to parse CVDR in %s (%s)" % (resource_identifier, ve),
                        file=sys.stderr,
                    )

            # print( '%r -> %r'%(orig, parsed ))

        elif resource_identifier.startswith("BWB://"):
            # I've not found its definition, probably because there is none, but it looks mostly jci?
            # BWB://1.0:r:BWBR0005416
            # BWB://1.0:c:BWBR0008903&artikel=12&g=2011-11-08
            # BWB://1.0:v:BWBR0015703&artikel=art. 30              which is messy
            m = re.match(
                "(?:jci)?([0-9.]+):([a-z]):(BWB[RV][0-9]+)(.*)", resource_identifier
            )
            if m is not None:
                version, typ, bwb, rest = m.groups()  # pylint: disable=W0612
                params = cvdr_param_parse(rest)
                ret.append(("BWB", resource_identifier, bwb, params, source_text))
                if debug:
                    print("BWB://-style   %r  %r" % (bwb, params), file=sys.stderr)

        elif resource_identifier.startswith(
            "http://"
        ) or resource_identifier.startswith("https://"):
            # TODO: centralize a 'reference_from_url' function, because there is more than this one style, and we can extract more

            # http://wetten.overheid.nl/BWBR0013016
            # http://wetten.overheid.nl/BWBR0003245/geldigheidsdatum_19-08-2009

            m = re.match(
                "https?://wetten.overheid.nl/(?:zoeken_op/)?(BWB[RV][0-9]+)(/.*)?",
                resource_identifier,
            )
            if m is not None:
                bwb, rest = m.groups()
                params = {}
                if rest is not None:
                    params = cvdr_param_parse(rest)
                if debug:
                    print("http-wetten: %r %r" % (bwb, params), file=sys.stderr)
                ret.append(("BWB", resource_identifier, bwb, params, source_text))

            # else:
            #    print("http-UNKNOWN: %r"%(resourceIdentifier), file=sys.stderr)
            #
            #
            # though also includes things that are specific but don't look like it, e.g.
            #   http://wetten.overheid.nl/cgi-bin/deeplink/law1/title=Gemeentewet/article=255
            # actually redirects to
            #   https://wetten.overheid.nl/BWBR0005416/2022-08-01/#TiteldeelIV_HoofdstukXV_Paragraaf4_Artikel255
            #
            # or completely free-form, like the following (which is a broken link)
            #   http://www.stadsregioamsterdam.nl/beleidsterreinen/ruimte_wonen_en/wonen/regelgeving_wonen

        elif (
            resource_identifier.startswith("jci")
            or "v:BWBR" in resource_identifier
            or "c:BWBR" in resource_identifier
        ):
            try:
                d = wetsuite.helpers.meta.parse_jci(resource_identifier)
            except ValueError as ve:
                if debug:
                    print("ERROR: bad jci in %r" % ve, file=sys.stderr)
                continue
            bwb, params = d["bwb"], d["params"]
            if debug:
                print("JCI: %r %r" % (bwb, params))
            ret.append(("BWB", resource_identifier, bwb, params, source_text))

        else:
            if not ignore_without_id:
                ret.append(("unknown", None, None, None, source_text))
            if debug and len(resource_identifier.strip()) > 0:
                print(
                    "UNKNOWN: %r %r" % (resource_identifier, source_text),
                    file=sys.stderr,
                )
                # print( wetsuite.helpers.etree.tostring(source) )

    return ret


def bwb_title_looks_boring(text):
    "Give title text, estimate whether the content has much to say"
    text = text.lower()
    for boringizing_substring in [
        "veegwet",
        "wijzigingswet",
        "herzieningswet",
        "aanpassingswet",
        "aanpassings- en verzamelwet",
        "reparatiewet",
        "overige fiscale maatregelen",
        "evaluatiewet",
        "intrekkingswet",
        "verzamelwet",
        "invoeringswet",
        "tijdelijke",
        "overgangswet",
        "aanpassingsbesluit",
        "wijzigingsbesluit",
        "wijzigingsregeling",
        "tot wijziging",  # not always
        "tot aanpassing",
        "tot herziening",
        #'tot vaststelling'  not actually, just figuring out the language
    ]:
        if re.search(r"\b%s\b" % boringizing_substring, text):
            return True
    return False


def bwb_searchresult_meta(record_node):
    """Takes individual SRU result record as an etree subtrees,
    picks out BWB-specific metadata (merging the separate metadata sections).
    Returns a dict
    """
    record_node = wetsuite.helpers.etree.strip_namespace(record_node)

    # recordSchema   = record.find('recordSchema')      # e.g. <recordSchema>http://standaarden.overheid.nl/sru/</recordSchema>
    # recordPacking  = record.find('recordPacking')     # probably <recordPacking>xml</recordPacking>
    record_data = record_node.find("recordData")  # the actual record
    # recordPosition = record.find('recordPosition')    # e.g. <recordPosition>12</recordPosition>
    payload = record_data[0]
    # print( etree.ElementTree.tostring( payload, encoding='unicode' ) )

    original_data = payload.find("originalData")
    owmskern = wetsuite.helpers.etree.kvelements_to_dict(
        original_data.find("meta/owmskern")
    )
    owmsmantel = wetsuite.helpers.etree.kvelements_to_dict(
        original_data.find("meta/owmsmantel")
    )
    bwbipm = wetsuite.helpers.etree.kvelements_to_dict(
        original_data.find("meta/bwbipm")
    )
    enriched_data = wetsuite.helpers.etree.kvelements_to_dict(
        payload.find("enrichedData")
    )

    merged = {}
    merged.update(owmskern)
    merged.update(owmsmantel)
    merged.update(bwbipm)
    merged.update(enriched_data)
    return merged


def bwb_toestand_usefuls(tree):
    """Fetch the most interesting metadata from parsed toestand XML.    TODO: finish"""
    ret = {}

    ret["bwb-id"] = tree.get("bwb-id")

    wetgeving = tree.find("wetgeving")  # TODO: also allow the alternative roots
    ret["intitule"] = wetgeving.findtext("intitule")
    ret["citeertitel"] = wetgeving.findtext("citeertitel")
    ret["soort"] = wetgeving.get("soort")
    ret["inwerkingtredingsdatum"] = wetgeving.get("inwerkingtredingsdatum")

    # this might contain nothing we can't get better in wti or manifest?
    # wetgeving_metadata = wetgeving.find('meta-data')
    return ret


def bwb_wti_usefuls(tree):
    """Fetch interesting  metadata from parsed WTI XML.
    TODO: finish, and actually do it properly -- e.g. look to the schema as to what may be omitted, may repeat, etc.
    """
    ret = {}
    tree = wetsuite.helpers.etree.strip_namespace(tree)

    # root level has these four
    algemene_informatie = tree.find("algemene-informatie")
    gerelateerde_regelgeving = tree.find("gerelateerde-regelgeving")
    wijzigingen = tree.find("wijzigingen")
    owms_meta = tree.find("meta")

    ### algemene_informatie ###########################################################################################
    ret["algemene_informatie"] = {}

    ret["algemene_informatie"]["citeertitels_withdate"] = []
    citeertitels = algemene_informatie.find("citeertitels")
    if citeertitels is not None:
        for citeertitel in citeertitels:
            ret["algemene_informatie"]["citeertitels_withdate"].append(
                (
                    citeertitel.get("geldig-van"),
                    citeertitel.get("geldig-tot"),
                    citeertitel.text,
                )
            )

    # CONSIDER: case-insensitive uniqueness
    ret["algemene_informatie"]["citeertitels_distinct"] = list(
        set(
            titel for _, _, titel in ret["algemene_informatie"]["citeertitels_withdate"]
        )
    )

    # TODO: similar for niet-officiele-titels

    for name in ("eerstverantwoordelijke", "identificatienummer"):
        ret["algemene_informatie"][name] = algemene_informatie.findtext(name)

    ret["algemene_informatie"]["rechtsgebieden"] = []
    for rechtsgebied in algemene_informatie.find("rechtsgebieden"):
        ret["algemene_informatie"]["rechtsgebieden"].append(
            (
                rechtsgebied.findtext("hoofdgebied"),
                rechtsgebied.findtext("specifiekgebied"),
            )
        )

    ret["algemene_informatie"]["overheidsdomeinen"] = []
    for overheidsdomein in algemene_informatie.find("overheidsdomeinen"):
        ret["algemene_informatie"]["overheidsdomeinen"].append(overheidsdomein.text)

    ### gerelateerde_regelgeving ######################################################################################
    ret["related"] = []
    for gnode in gerelateerde_regelgeving.find("regeling"):
        gname = gnode.tag
        for grel in gnode:
            bwbid = grel.get("bwb-id")
            extref = grel.find("extref")
            if extref is not None:  # TODO: figure out why that happens
                ret["related"].append((gname, bwbid, extref.get("doc"), extref.text))
    # TODO: parse the similar regelingelementen

    ### wijzigingen ###################################################################################################
    ret["wijzigingen"] = []
    for datum in wijzigingen.find("regeling"):
        wijziging = {}

        wijziging["waarde"] = datum.get("waarde")  # e.g. 1998-01-01
        details = datum.find("details")  # contains e.g. betreft, ontstaansbron
        wijziging["betreft"] = details.findtext(
            "betreft"
        )  # e.g. nieuwe-regeling, wijziging, intrekking-regeling

        ontstaansbron = details.find("ontstaansbron")
        bron = ontstaansbron.find("bron")

        wijziging["ondertekening"] = bron.findtext("ondertekening")

        bekendmaking = bron.find(
            "bekendmaking"
        )  # apparently the urlidentifier, that should be something like stb-1997-581, is sometimes missing
        if bekendmaking is not None:
            wijziging["bekendmaking"] = (
                bekendmaking.get("soort"),
                bekendmaking.findtext("publicatiejaar"),
                bekendmaking.findtext("publicatienummer"),
            )

        wijziging["dossiernummer"] = bron.findtext("dossiernummer")

        ret["wijzigingen"].append(wijziging)

    # TODO: also parse the similar regelingelementen

    ### owms-meta ###################################################################################################
    owms_kern = owms_meta.find("kern")
    for (
        node
    ) in (
        owms_kern
    ):  # TODO: check with schema this is actually flat and there are no dupe tags (there probably are)
        ret[node.tag] = node.text
    return ret


def bwb_manifest_usefuls(tree):
    """Fetch interesting metadata from manifest WTI XML.    TODO: finish"""
    ret = {"expressions": []}
    # metadata = tree.find('metadata')
    for expression in tree.findall("expression"):
        ex = {"manifestations": []}
        for node in expression.find("metadata"):
            ex[node.tag] = node.text

        for manifestation in expression.findall("manifestation"):
            # hashcode = manifestation.findtext('metadata/hashcode')
            # size     = manifestation.findtext('metadata/size')
            label = manifestation.find("item").get("label")
            ex["manifestations"].append(label)

        ret["expressions"].append(ex)

    # datum_inwerkingtreding
    return ret


def bwb_merge_usefuls(toestand_usefuls=None, wti_usefuls=None, manifest_usefuls=None):
    """Merge the result of the above, into a flatter structure"""
    merged = {}

    if wti_usefuls is not None:
        merged.update(wti_usefuls["algemene_informatie"])
        for k in wti_usefuls:
            if k not in ("algemene_informatie",):
                merged[k] = wti_usefuls[k]

    if manifest_usefuls is not None:
        merged.update(manifest_usefuls)

    if toestand_usefuls is not None:
        merged.update(toestand_usefuls)

    return merged


def bwb_toestand_text(tree, debug=False):
    """Given the document (as an etree object), this is a quick and dirty 'give me mainly the plaintext in it',
    skipping any introductions and such.

    Not structured data, intended to assist generic "how do these setences parse" code

    TODO:
     -  review this, it makes various assumptions about document structure
     -  review the handling of certain elements, like lijst, table, definitielijst

     -  see if there are contained elements to ignore, like maybe <redactie type="vervanging"> ?

     - generalize to have a parameter ignore_tags=['li.nr', 'meta-data', 'kop', 'tussenkop', 'plaatje', 'adres',
       'specificatielijst', 'artikel.toelichting', 'citaat', 'wetcitaat']
    """
    ret = []
    tree = wetsuite.helpers.etree.strip_namespace(tree)

    bwb_id = tree.get("bwb-id")  # only used in debug
    wetgeving = tree.find("wetgeving")
    soort = wetgeving.get("soort")  # only used in debug

    # The approach in here turned out to not be quite sustainable - that is, it's not particularly clear.

    for artikel in wetgeving.iter():  # assumes all tekst in these elements, and that they are not nested.  Ignores structure.

        if artikel.tag not in ["artikel", "enig-artikel", "tekst", "structuurtekst", "bijlage"]:
            continue

        if artikel.find("lid") is not None:
            aparts = artikel.findall("lid")
        else:
            aparts = [artikel]

        for apart in aparts:
            if apart.get("status") in ("vervallen",):
                break

            text = []  # collected per lid, effectively
            for ch in apart.getchildren():
                if ch.tag in ("lidnr", "meta-data"):
                    continue

                if ch.tag == "lijst":
                    for li in ch.getchildren():
                        for lich in li:
                            if lich.tag in ("al",):
                                text.extend( wetsuite.helpers.etree.all_text_fragments(lich) )
                            elif lich.tag in ("lijst",):  # we can probably do this a little nicer
                                text.extend( wetsuite.helpers.etree.all_text_fragments(lich) )
                            elif lich.tag in ("table",):
                                text.extend( wetsuite.helpers.etree.all_text_fragments(lich) )
                            elif lich.tag in ("definitielijst",):
                                text.extend( wetsuite.helpers.etree.all_text_fragments(lich) )
                            elif lich.tag in ("specificatielijst",):
                                pass
                            elif lich.tag in ("li.nr", "meta-data",):
                                pass
                            elif lich.tag in ("tussenkop",):
                                pass
                            elif lich.tag in ("plaatje",):
                                pass
                            elif lich.tag in ("adres",):
                                pass
                            else:
                                if debug:
                                    print( f"{bwb_id}/{soort} IGNORE unknown lijst child {lich.tag}" )
                                    print( wetsuite.helpers.etree.tostring(lich).decode("u8") )

                elif ch.tag in ("al",):
                    text.extend(wetsuite.helpers.etree.all_text_fragments(ch))
                elif ch.tag in ("al-groep", ):
                    text.extend(wetsuite.helpers.etree.all_text_fragments(ch))

                elif ch.tag in ("divisie", ): # TODO: handle better
                    text.extend(wetsuite.helpers.etree.all_text_fragments(ch))

                elif ch.tag in ("artikel", ): # TODO: ...what?
                    text.extend(wetsuite.helpers.etree.all_text_fragments(ch))

                elif ch.tag in ("table", ): # TODO: handle as table
                    #text.extend(wetsuite.helpers.etree.all_text_fragments(ch))
                    text.extend(wetsuite.helpers.etree.html_text(ch, join=False, bodynodename=None))
                
                elif ch.tag in ("definitielijst", ):
                    text.extend(wetsuite.helpers.etree.all_text_fragments(ch))

                elif ch.tag in ("specificatielijst", ):
                    pass
                elif ch.tag in ( "kop", "tussenkop", ):
                    pass
                elif ch.tag in ("adres", "adreslijst", ):
                    pass
                elif ch.tag in ("artikel.toelichting", ):
                    pass
                elif ch.tag in ("plaatje", "formule", "model", ):
                    pass
                elif ch.tag in ("officiele-inhoudsopgave", ):
                    pass
                elif ch.tag in ( "citaat", "wetcitaat", ):
                    pass
                elif ch.tag in ( "bijlage-sluiting",):
                    pass
                # TODO: ignore ProcessingInstruction 
                else:
                    print("%s/%s IGNORE unknown lid-child %r" % (bwb_id, soort, ch.tag))
                    print(wetsuite.helpers.etree.tostring(ch).decode("u8"))

            text = (" ".join(text)).rstrip()
            text = re.sub(r"[\ ]+", " ", text).strip().replace('\n ','\n')
            ret.append(text)

    return "\n\n".join(ret)


_versions_cache = {}


def cvdr_versions_for_work(cvdr_id: str) -> list:
    """takes a CVDR id (with or without _version, i.e. expression id or work id),
    searches KOOP's CVDR repo,
    Returns: a list of all matching version expression ids

    Keep in mind that this actively does requests, so preferably don't do this in bulk, and/or cache your results.

    @return: a list of a list expression ids
    """
    if cvdr_id in _versions_cache:
        # print( "HIT %r -> %r"%(cvdrid, _versions_cache[cvdrid]) )
        return _versions_cache[cvdr_id]

    sru_cvdr = (
        wetsuite.datacollect.koop_sru.CVDR()
    )  # TODO: see if doing this here stays valid
    work_id, _ = cvdr_parse_identifier(cvdr_id)
    results = sru_cvdr.search_retrieve_many(
        "workid = CVDR%s" % work_id, up_to=10000
    )  # only fetches as many as needed, usually a single page of results. TODO: maybe think about injection?
    # print(f"amt results: {len(results)}")
    ret = []
    for record in results:
        meta = cvdr_meta(record)
        result_expression_id = meta["identifier"][0]["text"]
        ret.append(result_expression_id)
    ret = sorted(ret)
    _versions_cache[cvdr_id] = ret
    return ret


def parse_op_metafile(
    input: Union[bytes, wetsuite.helpers.etree.ElementTree], as_dict=False
):
    """Parses two different metadata-only XML styles found in KOOP's Offiele Publicaties repositories
      - the one that looks like `<metadata_gegevens>` with a set of `<metadata name="DC.title" scheme="" content="...`
      - the one that (after a namespace strip) looks like `<owms-metadata><owmskern>` with e.g. `<dcterms:identifier>gmb-...`

    could also raise, e.g. a XMLSyntaxError

    NOT TO BE CONFUSED with parse_op_searchmeta

    CONSIDER: TODO: a similar  flatten parameter (probably defaulting False)

    Tries to return them in the same style, e.g.
      - taking off the name-based grouping from DC.title

      - taking off the tag-based grouping (ignoring owmskern tag)

    @return:
      - by default, a list of (key, schema, value) tuples
      - if as_dict=True, a dict like {key: [(schema, value), ...]}
    """
    if isinstance(input, bytes):
        root = wetsuite.helpers.etree.fromstring(input)
        root = wetsuite.helpers.etree.strip_namespace(root)
    else:  # assume it's an alrady-parsed etree
        root = input
    ret = []
    if root.tag == "metadata_gegevens":
        for metadata in root:
            name = metadata.get("name")
            name = name.split(".", 1)[
                1
            ]  # we ignore this grouping string; we could put it on a fourth element
            ret.append((name, metadata.get("scheme"), metadata.get("content")))
    elif root.tag == "owms-metadata":
        for (
            group
        ) in root:  # we ignore this grouping level; we could put it on a fourth element
            for node in group:
                ret.append((node.tag, node.get("scheme", ""), node.text))
    else:
        raise ValueError("Did not expect XML with root tag named %r" % root.tag)

    if not as_dict:
        return ret
    else:
        rdd = collections.defaultdict(list)
        for key, schema, value in ret:
            rdd[key].append((schema, value))
        return dict(rdd)


def parse_op_searchmeta(input, flatten=False):
    """similar to cvdr_meta; CONSIDER: abstract most of that into one helper function

    Note that
      - the 'enriched' and 'manifestations' keys show equivalent information
      - the 'enriched' and 'manifestations' keys are not affected by flattening.
    """
    # allow people to be lazier - hand in the XML bytes without parsing it into etree
    if isinstance(input, bytes):
        root = wetsuite.helpers.etree.fromstring(input)
        root = wetsuite.helpers.etree.strip_namespace(root)
    else:  # assume it's an alrady-parsed etree
        root = input

    ret = {}
    root = wetsuite.helpers.etree.strip_namespace(root)
    # print( wetsuite.helpers.etree.tostring(tree).decode('u8') )

    # we want tree to be the node under which ./meta lives
    # TODO: review, this looks unclear
    if root.find("meta") is not None:
        meta_under = root
    else:
        meta_under = root.find("recordData/gzd/originalData")
        if meta_under is None:
            raise ValueError(
                "got XML that seems to be neither a document or a search result record"
            )

    owmskern = meta_under.find("meta/owmskern")
    for child in owmskern:
        tagname = child.tag
        if child.text is not None:
            tagtext = child.text
            if tagname not in ret:
                ret[tagname] = []
            ret[tagname].append({"text": tagtext, "attr": child.attrib})

    owmsmantel = meta_under.find("meta/owmsmantel")
    for child in owmsmantel:
        tagname = child.tag
        tagtext = child.text
        if child.text is not None:
            if tagname not in ret:
                ret[tagname] = []
            ret[tagname].append({"text": tagtext, "attr": child.attrib})

    tpmeta = meta_under.find("meta/tpmeta")
    for child in tpmeta:
        tagname = child.tag
        text = "".join(wetsuite.helpers.etree.all_text_fragments(child))
        if tagname not in ret:
            ret[tagname] = []
        ret[tagname].append({"text": text, "attr": child.attrib})

    if flatten:
        simpler = {}
        for meta_key, value_list in ret.items():  # each of the metadata
            simplified_text = []
            for item in value_list:
                text = item["text"]
                if item["attr"]:
                    for _, attr_val in item["attr"].items():
                        # this seems to make decent sense half the time (the attribute name is often less interesting)
                        if len(attr_val.strip()) == 0:  # present but empty
                            text = "%s" % (text,)
                        else:
                            text = "%s (%s)" % (text, attr_val)
                simplified_text.append(text)
            simpler[meta_key] = (",  ".join(simplified_text)).strip()
        ret = simpler

    enriched_data = root.find("recordData/gzd/enrichedData")
    # Looks something like the following, so flattening would change its meaning, and it's handled separately.
    # <enrichedData>
    #     <url>https://repository.overheid.nl/frbr/officielepublicaties/kst/26100/kst-26100-1/1/pdf/kst-26100-1.pdf</url>
    #     <preferredUrl>https://zoek.officielebekendmakingen.nl/kst-26100-1.html</preferredUrl>
    #     <itemUrl manifestation="html">https://repository.overheid.nl/frbr/officielepublicaties/kst/26100/kst-26100-1/1/html/kst-26100-1.html</itemUrl>
    #     <itemUrl manifestation="metadata">https://repository.overheid.nl/frbr/officielepublicaties/kst/26100/kst-26100-1/1/metadata/metadata.xml</itemUrl>
    #     <itemUrl manifestation="metadataowms">https://repository.overheid.nl/frbr/officielepublicaties/kst/26100/kst-26100-1/1/metadataowms/metadata_owms.xml</itemUrl>
    #     <itemUrl manifestation="pdf">https://repository.overheid.nl/frbr/officielepublicaties/kst/26100/kst-26100-1/1/pdf/kst-26100-1.pdf</itemUrl>
    #     <itemUrl manifestation="xml">https://repository.overheid.nl/frbr/officielepublicaties/kst/26100/kst-26100-1/1/xml/kst-26100-1.xml</itemUrl>
    #     <timestamp>2020-04-16T14:47:53.69679+02:00</timestamp>
    #   </enrichedData>
    enriched = []
    manifs = {}
    if (
        enriched_data is not None
    ):  # only appears in search results, not the XML that points to
        for tag in enriched_data:
            if tag.tag not in ("timestamp",):
                # print( tag )
                enriched.append((tag.tag, tag.get("manifestation"), tag.text))
                if tag.tag == "itemUrl":
                    manifs[tag.get("manifestation")] = tag.text
    ret["enriched"] = enriched
    ret["manifestations"] = manifs

    return ret


###################################


# TODO: rename
def alineas_with_selective_path(
    tree, start_at_path=None, alinea_elemnames=("al",)
):  # , ignore=['meta-data'], add_raw=True
    """Given document-style XML data such as that of CVDR XML documents,
    tries to capture most of the interesting structure in easier-to-digest python data form,
    and lessen the nested nature without quite throwing it away.

    Whenever we hit an <al>,
    we emit a dict that details all the interesting elements between body and this <al>

    This is intended as the lower-level half of potential cleanup, grouping/splitting logic, and such.
    ...though it is specific to a handful of XML schemas, so not universal.
    For wider applicability you may want to look to helpers.split TODO

    @param tree:            the etree tree/node to work on
    @param start_at_path:   if you gave it the root of an etree, you can do a subset by handing in xpath here
    (alternatively, you could navigate yourself and hand the interesting section in directly)
    @param alinea_elemnames: will be ('al',) for the KOOP sources. Was made into a parameter only to make this perhaps-applicable elsewhere, you probably don't want to touch this.
    @return: Returns a list of dicts, one for each <al> (or whatever you handed into alinea_elemnames)

    While on some flat examples, e.g. officiele-publicaties XMLs, each output might not hold much structure,
    some of the better-structured cases, e.g. BWB XMLs, each such output dict might look something like: ::
        {
            'path':      '/cvdr/body/regeling/regeling-tekst/hoofdstuk[1]/artikel[1]/al',
            'parts': [   {'what': 'hoofdstuk',  'hoofdstuklabel': 'Hoofdstuk', 'hoofdstuknr': '1', 'hoofdstuktitel': 'Algemene bepalingen',},
                         {'what': 'artikel',    'artikellabel': 'Artikel',     'artikelnr': '1:1', 'artikeltitel': 'Begripsomschrijvingen',}  ],
            'merged':    {'hoofdstuklabel': 'Hoofdstuk',
                          'hoofdstuknr': '1',
                          'hoofdstuktitel': 'Algemene bepalingen'
                          'artikellabel': 'Artikel',
                          'artikelnr': '1:1',
                          'artikeltitel': 'Begripsomschrijvingen',
                          },
            'text-flat': 'In deze verordening wordt verstaan dan wel mede verstaan onder:'
        }
    Where:
      - 'parts' details each structural element (boek, hoofdstuk, afdeling paragraaf, artikel, lid)
         that encompasses this fragment
         the ...label keys are largely entirely redundant, but there are documents that abuse these, which you may want to know.
      - 'merged' is the part dicts, without the 'what' key, update()d into one dict.
         Intended to be the part you may want to filter on all in one place
         In simpler documents, this eases things and is correct
         In complex documents, this may be incorrect -- because when you e.g. have an afdeling nested in an afdeling, values from one overwrite the other.
      - 'path' points at the item we're describing (in xpath terms), in case you want to find this element in the original XML / etree form
      - 'text-flat' is plain text, with any markup elements flattened out

      - this is very much intended to be simplified further soon, likely using merge_alinea_data().
        This is separated largely for flexibility's sake,
        (CONSIDER: also provide a extract-text-with-reasonable-defaults fuction)
      - WARNING: currently NONE of these keys in parts or merged are settled on yet -- things may change.


    """
    warnings.warn(
        "The behaviour of alineas_with_selective_path() is not fully decided, and may still change"
    )

    # this is based on observations of CVDR and BWB
    structure_elements = {
        "boek": {},
        "hoofdstuk": {
            "kop/label": "hoofdstuklabel",
            "kop/nr": "hoofdstuknr",
            "kop/titel": "hoofdstuktitel",
        },
        "afdeling": {
            "kop/label": "afdelinglabel",
            "kop/nr": "afdelingnr",
            "kop/titel": "afdelingtitel",
        },
        "paragraaf": {
            "kop/label": "paragraaflabel",
            "kop/nr": "paragraafnr",
            "kop/titel": "paragraaftitel",
        },
        "sub-paragraaf": {
            "kop/label": "subparagraaflabel",
            "kop/nr": "subparagraafnr",
            "kop/titel": "subparagraaftitel",
        },
        "artikel": {
            "kop/label": "artikellabel",
            "kop/nr": "artikelnr",
            "kop/titel": "artikeltitel",
        },
        "lid": {"lidnr": "lidnr"},
        "deel": {},  # have
        "divisie": {
            "kop/label": "divisielabel",
            "kop/nr": "divisienr",
            "kop/titel": "divisietitel",
            "@bwb-ng-variabel-deel": "divisie_vd",
        },
        "circulaire.divisie": {"@bwb-ng-variabel-deel": "circulairedivisie_vd"},
        "definitielijst": {},
        "definitie-item": {"term": "term", "li.nr": "li.nr"},
        "li": {"@nr": "li-nr", "li.nr": "li.nr", "@bwb-ng-variabel-deel": "li_vd"},
        # some things to have in the stack-like thing, but which don't have details
        "aanhef": {},  #'afkondiging' 'preambule'
        "note-toelichting": {},
        "bijlage": {},
        "lijst": {},
        # table, plaatje?
        # rechtgeving.nl
        "uitspraak": {"@id": "id"},
        "section": {"@id": "id", "title/nr": "nr", "title": "title"},
        "listitem": {},
        "parablock": {"nr": "nr"},
        "uitspraak.info": {},
        "inhoudsindicatie": {"@id": "id"},
    }

    ret = []

    tree = wetsuite.helpers.etree.strip_namespace(tree)

    # adapted from node_walk
    if start_at_path is not None:
        start = tree.xpath(start_at_path)[
            0
        ]  # maybe use xpath() so it takes xpath paths
    else:
        start = tree

    path_to_element = []
    element_stack = [start]
    while element_stack:
        element = element_stack[-1]
        if path_to_element and element is path_to_element[-1]:
            path_to_element.pop()
            element_stack.pop()
            # print( path_to_element )

            if isinstance(element, _Comment) or isinstance(
                element, _ProcessingInstruction
            ):
                pass
            else:
                if element.tag in alinea_elemnames:
                    xpath_path = wetsuite.helpers.etree.path_between(tree, element)
                    emit = {"path": xpath_path, "parts": [], "merged": {}}
                    for pathelem in path_to_element:
                        if pathelem.tag in structure_elements:
                            part_dict = {}
                            for what_to_fetch, what_to_call_it in structure_elements[
                                pathelem.tag
                            ].items():
                                if (
                                    what_to_fetch[0] == "@"
                                ):  # TODO: less magical, maybe just call keys 'fetch_attr' and 'fetch_text'?
                                    part_dict[what_to_call_it] = pathelem.get(
                                        what_to_fetch[1:]
                                    )
                                else:
                                    pathelem_rel = pathelem.find(what_to_fetch)
                                    if pathelem_rel is None:
                                        pass
                                        # print("Did not find %r under %r"%(what_to_fetch, xpath_path))
                                    else:
                                        part_dict[what_to_call_it] = pathelem_rel.text
                            emit["merged"].update(
                                part_dict
                            )  # duplicated, easier to access, and clobbered whenever you have an element in the structure twice
                            part_dict["what"] = pathelem.tag
                            emit["parts"].append(part_dict)

                    emit["raw"] = wetsuite.helpers.etree.tostring(element)
                    emit["raw_etree"] = element
                    emit["text-flat"] = wetsuite.helpers.etree.all_text_fragments(
                        element, join=" "
                    )
                    # yield emit
                    ret.append(emit)

        else:
            path_to_element.append(element)
            for child in reversed(element):
                element_stack.append(child)
            # print( element_stack )
    return ret


def merge_alinea_data(
    alinea_dicts,
    if_same={
        # these first four rarely get into it
        "hoofdstuk": "hoofdstuknr",
        "afdeling": "afdelingnr",
        "paragraaf": "paragraafnr",
        "sub-paragraaf": "subparagraafnr",
        "artikel": "artikelnr",
        "lid": "lidnr",
        "definitie-item": "term",
        # rechtspraak
        "uitspraak": "id",
        "uitspraak.info": None,
        "section": "nr",
    },
):
    """Takes the output of alineas_with_selective_path()
    puts text fragments together when their specified ['parts'] values are the same.

    In other words, this lets you control just how flat to make the text, e.g.
      - flatten all text within a lid (e.g. flattening lists),
      - smush all lid text within an article together, etc.
      - mostly flatten out the text, but still group it by hoofdstuk if those are present
    ...etc.

    CONSIDER: returning a meta dict for each such grouped text (instead of the raw key)

    @return:
    """
    dummy_count = 0

    merged = collections.OrderedDict()
    key_meta = {}  # key -> meta dict

    for alinea_dict in alinea_dicts:
        # CONSIDER: a more readable/usable version of key
        key = []
        meta = []
        for part_dict in alinea_dict["parts"]:
            what = part_dict["what"]
            # print( part_dict)
            if what in if_same and if_same[what] in part_dict:
                sel = if_same[what]
                # print(sel)
                if sel is None:  # TODO: think about this adjustment
                    interesting_val = "_dummy_%d" % dummy_count
                    dummy_count += 1
                else:
                    interesting_val = part_dict[sel]
                    if interesting_val is None:  # maybe warn that there isn't?
                        interesting_val = ""
                key.append("%s:%s" % (what, interesting_val.strip()))
                meta.append((what, interesting_val.strip()))
        key = "  ".join(key)
        key_meta[key] = meta
        # print( key)

        if key not in merged:
            merged[key] = []

        merged[key].append(alinea_dict["text-flat"])

    ret = []
    for key, text in merged.items():
        ret.append((key_meta[key], text))
    return ret


# This was unfinished; decide whether to keep it
# def iter_chunks_xml(xml):
#     """The combination of  alineas_with_selective_path()  and  merge_alinea_data()

#     Notes:
#       - Sloppy initial implementation
#       - attempts to handle tables
#       - Currently geared specifically to CVDR xml
#     """
#     tree = wetsuite.helpers.etree.fromstring(xml)
#     tree_stripped = wetsuite.helpers.etree.strip_namespace(tree)

#     # Separate tables
#     for n, table in enumerate(list(tree_stripped.findall(".//table"))):
#         text = str(tostring(table))
#         if len(text) < 10:
#             continue
#         yield {
#             "n": n,
#             "part_id": f"table {n}",
#             "text": text,
#             "from_table": True,
#         }
#         table.getparent().remove(table)

#     alinea_dicts = alineas_with_selective_path(
#         tree_stripped, start_at_path="/"
#     )
#     merged = merge_alinea_data(
#         alinea_dicts,
#         if_same={
#             "hoofdstuk": "hoofdstuknr",
#             "afdeling": "afdelingnr",
#             "paragraaf": "paragraafnr",
#             "sub-paragraaf": "subparagraafnr",
#             "artikel": "artikelnr",
#         },
#     )

#     for n, (label, content) in enumerate(merged):
#         text = "\n".join(content)
#         # print(label, text)
#         # r = input('prompt? y/n')
#         # if r == 'y':
#         if len(text) > 10:
#             yield {
#                 "n": n,
#                 "part_id": " ".join(" ".join(l) for l in label),
#                 "text": text,
#                 "from_table": False,
#             }


def prefer_types(
    given_strlist,
    all_of=("metadata", "metadataowms", "xml"),
    first_of=("html", "html.zip", "pdf", "odt"),
    never=("coordinaten", "jpg", "ocr"),
    require_present=("metadata",),
    # debug=False,
):
    """Given a bunch of document types such as::
        ['metadata', 'metadataowms', 'pdf','odt', 'jpg', 'coordinaten', 'ocr', 'html', 'xml']
    return only a subset of types, for defaults::
        ['metadata', 'metadataowms', 'xml', 'html']
    ...because those defaults prefer smaller, smaller, more data-like/simpler-to-parse variants
    and avoid content redundancy that we probably won't end up reading (e.g. why prse odt, pdf when you have html, xml).

    DECISIONS/ASSUMPTIONS MADE:
      - things like 'don't care about HTML when we have XML' which might not fit your needs exactly.

      - Assumes xml is content, and it can be other things.
        You probably want to be sure about your specific purpose.

      - Consider that if you e.g. hand in `['metadata', 'metadataowms', 'xml', 'pdf']` it will return _both_ xml and PDF.
        If you specifically wanted only one content thing, wanted only one, xml, then you should probably say first_of=('xml, 'html', 'html.zip', 'pdf', 'odt')


    @param all_of:   always add these when they appear.
    Meant for things like metadata, and more data-like formats.

    @param first_of: add the first in this list that matches and stop (stop regardless of whether it was already added via always)
    Meant for things like "if always didn't find something, add a single next best thing, probably the one most reasonable to parse"

    @param never:    never have these in the returned list (_even_ if they were mentioned in always or first_of)

    @return: a list of strings (often shorter than what we were given)
    """
    ret = []

    # we only need to choose when it's types (not if it's e.g. frbr directory listing), using this as an indicator
    for test_r in require_present:
        if test_r not in given_strlist:
            raise ValueError("prefer_types got a list without %r" % test_r)

    for test_a in all_of:
        if test_a in given_strlist:
            if test_a not in ret:  # avoid duplicates
                # if debug:
                #    print("ADD A %s"%test_a)
                ret.append(test_a)

    for test_f in first_of:
        if test_f in given_strlist:
            if test_f not in ret:  # avoid duplicates
                # if debug:
                #    print("ADD F %s"%test_f)
                ret.append(test_f)
            # this indent level means  break on first match, regardless of whether we did add or not
            break

    for test_n in never:
        if test_n in ret:
            # if debug:
            #    print("DEL N %s"%test_n)
            ret.remove(test_n)

    unknown = set(given_strlist).difference(set(all_of).union(first_of).union(never))
    if len(unknown) > 0:
        warnings.warn(
            "the real data mentioned types you did not mention in your preference: %r"
            % sorted(unknown)
        )

    return ret


def op_data_xml_seems_empty( docbytes, minchars=1 ):
    """ Some of the XML files presented to us as XML data are actually devoid of content text.
        This determines if it's such a case.
        We actually parse it, so we can better distinguish between empty and near-empty. 
    """
    tree = wetsuite.helpers.etree.fromstring( docbytes ) # 
    if len(tree) <= 1: # amount of childeren under root; 1 means only its <meta> is there, and no content
        return True
    
    # Consider the subset of cases where there _is_ a basic template structure, but no text content in them.
    doctext = ''.join( tree[1].itertext() )
    doctext_strip = doctext.strip()
    
    if len( doctext_strip ) < minchars:
        return True
    
    if 'niet beschikbaar in HTML-formaat' in doctext: # happens in agendas
        return True
    
    return False


# the regexp is ugly and not very indicative of where it came from. 
#   It's here partly to some basic check of our assumptions about the parts of those URLs for this subset - 
#   anything not matching is printed - which seems prudent since we'll also be extracting information from it
_re_repourl_parl = re.compile( r'^https?://repository.overheid.nl/frbr/officielepublicaties/([a-z-]+)/([A-Za-z0-9-]+)/([A-Za-z0-9_-]+)/([a-z0-9-]+)/([a-z]+)/([A-Za-z0-9_-]+.[a-z]+)$' )
#                                                            e.g.                              h-ek       20092010     h-ek-20092010-1_2       1       xml    h-ek-20092010-1_2.xml

def parse_repo_url( url ):
    ''' 
    TODO: see how well this holds up to all areas

    @param url: an URL like C{https://repository.overheid.nl/frbr/officielepublicaties/ag-ek/1995/ag-ek-1995-02-08/1/xml/ag-ek-1995-02-08.xml},
    @return: a dict like::
        {'doctype': 'ag-ek',
        'group': '1995',
        'doc_id': 'ag-ek-1995-02-08',
        'mn': '1',
        'exprtype': 'xml',
        'bn': 'ag-ek-1995-02-08.xml',
        'url': 'https://repository.overheid.nl/frbr/officielepublicaties/ag-ek/1995/ag-ek-1995-02-08/1/xml/ag-ek-1995-02-08.xml'}

    '''
    match = _re_repourl_parl.match( url )
    if match is None:
        raise ValueError( f'ERROR understanding {repr(url)}' )
    else:
        doctype, group, doc_id, mn, exprtype, bn = match.groups()
        return {
            'doctype':doctype,
            'group':group,
            'doc_id':doc_id,
            'mn':mn,
            'exprtype':exprtype,
            'bn':bn,

            'url':url, # just to put the original value in the same place
        }
    
