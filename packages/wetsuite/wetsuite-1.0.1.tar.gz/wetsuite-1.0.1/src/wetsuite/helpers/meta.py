""" Things that parse metadata.
    
    Specifically for things not tied to a singular API or data source, 
    or we otherwise expect to see some reuse of.

    There are similar function in other places, in particular when they are specific.
    For example helpers speciic to KOOP's presentations BWB, CVDR, and OP sits in helpers.koop_parse

    The function name should give you some indication how what it associates with, 
    and how specific it is.
"""

import re
import collections
import urllib.parse
import warnings

import wetsuite.extras.gerechtcodes
import wetsuite.helpers.strings


_RE_JCIFIND = re.compile(
    r'(?:jci)?([0-9.]+):([a-z]):(BWB[RV][0-9]+)([^\s;"\']*)',
    flags=re.M
)  # NOTE: not meant for finding in free-form text

_RE_ECLIFIND = re.compile(
    r"ECLI:[A-Za-z]{2}:[A-Za-z0-9.]{1,7}:[0-9]{1,4}:[A-Z-z0-9.]{1,25}",
    flags=re.M
)


# CONSIDER: a findall_jci, taking either etree or a string?


def parse_jci(text: str):
    """Takes something in the form of C{jci{version}:{type}:{BWB-id}{key-value}*},
    so e.g. ::
        jci1.31:c:BWBR0012345&g=2005-01-01&artikel=3.1
    returns something like ::
        {'version': '1.31', 'type': 'c', 'bwb': 'BWBR0012345',
         'params': {'g': ['2005-01-01'], 'artikel': ['3.1']}}

    Notes:
      - params is actually an an OrderedDict, so you can also fetch them
        in the order they appeared, for the cases where that matters.
      - tries to be robust to a few non-standard things we've seen in real use
      - for type=='c' (single consolidation), expected params include
        - C{g}  geldigheidsdatum
        - C{z}  zichtdatum
      - for type=='v' (collection), expected params include
        - C{s}  start of geldigheid
        - C{e}  end of geldigheid
        - C{z}  zichtdatum
      Note that precise interpretation, and generation of these links,
      is a little more involved,
      in that versions made small semantic changes to the meanings of some parts.

    @param text: jci-style identifier as string. Will be parsed.
    """
    ret = {}

    # hack for observed bad escaping (hacky in that is assumes things about other values)
    text = text.replace("&amp;", "&")

    match_object = _RE_JCIFIND.match(text)
    if match_object is None:
        raise ValueError("%r does not look like a valid jci" % text)
    else:
        version, typ, bwb, rest = match_object.groups()
        ret["version"] = version
        ret["type"] = typ
        ret["bwb"] = bwb
        # The jci standard doesn't seem to make it clear
        #   whether it's supposed to be a conformant URL or URN,
        #   so it's unsure whether there is specific parameter encoding.
        # The below is somewhat manual, but might prove more robust then just
        #   d['params']  = urllib.parse.parse_qs(rest)
        params = collections.OrderedDict()
        for param in rest.split("&"):
            param_dict = urllib.parse.parse_qs(param)
            for key, value in param_dict.items():
                if key not in params:
                    params[key] = value
                else:
                    params[key].extend(value)
        ret["params"] = params
    return ret


# CONSIDER: adding the lists of dutch courts. It might change over time, but is still useful.


def findall_ecli(string: str, rstrip_dot=True):
    """Within plain text, this tries to find all occurences of things
    that look like an ECLI identifier

    @param string: the string to look in

    @param rstrip_dot: whether to return the match stripped of any final dot(s).
    While dots are valid in an ECLI (typically used as a separator),
    it is more likely that a dot on the end is an ECLI into a sentence
    than it is to be part of the ECLI.
    This stripping is enabled by default, but it would be more correct for you
    to always control this parameter, and for well-controlled metadata fields
    it may be more correct to use False.

    @return: a list of strings.
    """
    ret = []
    for match_str in _RE_ECLIFIND.findall(string):
        if rstrip_dot:
            match_str = match_str.rstrip(".")
        ret.append(match_str)
    return ret


def parse_ecli(string: str):
    """Parses something we know is an ECLI, reports the parts in a dict.

    Currently hardcoded to remove any final period.

    Returns a dict with keys that contain at least::
        'country_code': 'NL',
        'court_code': 'HR',
        'year': '1977',
        'caseid': 'AC1784',
    And perhaps (TODO: settle this)::
        'normalized': 'ECLI:NL:HR:1977:AC1784',
        'removed': ').',
        'court_details': {'abbrev': 'HR', 'extra': ['hr'], 'name': 'Hoge Raad'}

    As an experiment, we try to report more about the court in question,
    but note the key ('court_details') is not guaranteed to be there.

    @param string: the string to parse as an ECLI
    """
    ret = {}

    # in case you gave something in running text...
    m = re.search(r"[^A-Za-z0-9:.]", string)
    if m is not None:
        ret["removed_pre"] = string[m.end() :]
        string = string[: m.end() - 1]

    ecli_list = string.strip().split(":")

    # :DOC or :INH stuck on an ECLI is an internal convention at... was it open-rechtspraak?
    if len(ecli_list) == 6 and ecli_list[-1] in ("DOC", "INH"):
        # remove that, that may well leave us with a valid ECLI
        ecli_list = ecli_list[:5]

    if len(ecli_list) != 5:
        raise ValueError(
            "ECLI is expected to have 5 elements (not %d) separated by four colons, %r does not"
            % (len(ecli_list), string)
        )

    uppercase_ecli, country_code, court_code, year, caseid = ecli_list

    if uppercase_ecli.upper() != "ECLI":
        raise ValueError(f"First ECLI string isn't 'ECLI' in {repr(string)}")

    if len(country_code) != 2:
        raise ValueError(f"ECLI country {repr(country_code)} isn't two characters")

    if len(court_code) > 7:  # TODO: check that
        raise ValueError(f"ECLI court code too long: {repr(court_code)}")

    mo_caseid = re.match(r"([A-Z-z0-9.]{1,25})", caseid)
    if mo_caseid is None:
        raise ValueError(f"Does not look like a valid ECLI: {repr(string)}")

    end = mo_caseid.end()
    while end > 0 and caseid[end - 1] == ".":
        end -= 1

    if end < len(caseid):  # we are removing things
        rest = caseid[end:]
        caseid = caseid[:end]
        # raise ValueError( repr(rest) )
        ret["removed"] = rest

    ret["normalized"] = (
        ":".join([uppercase_ecli, country_code, court_code, year, caseid])
    ).upper()

    ret["country_code"] = country_code
    ret["court_code"] = court_code
    ret["year"] = year
    ret["caseid"] = caseid

    # court codes (experiment)
    try:

        if court_code in wetsuite.extras.gerechtcodes.data:
            ret["court_details"] = wetsuite.extras.gerechtcodes.data[court_code]
    except ImportError:  # pragma nocover
        warnings.warn("Could not find our own gerechtcodes")
        # pass

    return ret


# members slowly change over time,
#  so maybe we should just accept any three letters,
#  or more pragmatically, any existing nearby country?
CELEX_COUNTRIES = [
    "BEL",
    "DEU",
    "FRA",
    "CZE",
    "ESP",
    "PRT",
    "AUT",
    "CYP",
    "BGR",
    "EST",
    "FIN",
    "GBR",
    "HUN",
    "IRL",
    "LTU",
    "MLT",
    "LVA",
    "SVN",
    "SWE",
    "GRC",
    "POL",
    "DNK",
    "ITA",
    "LUX",
    "NLD",
    "SVK",
    "ROU",
    "HRV",
]
" The three-letter codes that CELEX uses to refer to countries "

CELEX_SECTORS = {
    "1": "Treaties",
    "2": "External Agreements",
    "3": "Legislation",
    "4": "Internal Agreements",
    "5": "Proposals + other preparatory documents",
    "6": "Case Law",
    "7": "National Implementation",
    "8": "National Case Law",
    "9": "Parliamentary Questions",
    "0": "Consolidated texts",
    "C": "OJC Documents",
    "E": "EFTA Documents",
}
" The sectors defined within CELEX "


# https://eur-lex.europa.eu/content/tools/TableOfSectors/types_of_documents_in_eurlex.html

CELEX_DOCTYPES = (
    ("1", "K", "Treaty establishing the European Coal and Steel Community (ECSC Treaty) 1951"),
    ("1", "A", "Treaty establishing the European Atomic Energy Community (EAEC Treaty or Euratom) (1957); Euratom Treaty consolidated versions (2010, 2012, 2016)"),
    ("1", "E", "Treaty establishing the European Economic Community (EEC Treaty or Treaty of Rome) (1957); Treaty establishing the European Community (TEC or EC Treaty) Maastricht consolidated version (1992), Amsterdam consolidated version (1997), Nice consolidated version (2002) and Athens consolidated version (2006); Treaty on the Functioning of the European Union (TFEU) consolidated versions (2008, 2010, 2012, 2016)"),
    ("1", "F", "Merger Treaty or Treaty of Brussels (1965); Treaty amending certain budgetary provisions or Treaty of Luxembourg (1970)"),
    ("1", "B", "Treaty of Accession of Denmark, Ireland, Norway* and the United Kingdom (1972)"),
    ("1", "R", "Treaty amending certain financial provisions (1975); Treaty amending certain provisions of the Protocol on the Statute of the European Investment Bank (1975)"),
    ("1", "H", "Treaty of Accession of Greece (1979)"),
    ("1", "I", "Treaty of Accession of Spain and Portugal (1985)"),
    ("1", "G", "Greenland Treaty (1985)"),
    ("1", "U", "Single European Act (SEA) 1986"),
    ("1", "M", "Treaty on the European Union (TEU or Treaty of Maastricht) consolidated versions (1992, 1997, 2002, 2006, 2008, 2010, 2012, 2016); Treaty of Amsterdam consolidated version (1997); Treaty of Nice consolidated version (2002); Treaty of Athens consolidated version (2006); Treaty of Lisbon consolidated versions (2008, 2010, 2012)"),
    ("1", "N", "Treaty of Accession of Austria, Finland and Sweden (1994)"),
    ("1", "D", "Treaty of Amsterdam (1997)"),
    ("1", "C", "Treaty of Nice (2001)"),
    ("1", "T", "Treaty of Accession of the Czech Republic, Estonia, Cyprus, Latvia, Lithuania, Hungary, Malta, Poland, Slovenia and Slovakia (2003)"),
    ("1", "V", "Treaty establishing a Constitution for Europe (2004)"),
    ("1", "S", "Treaty of Accession of the Republic of Bulgaria and Romania (2005)"),
    ("1", "L", "Treaty of Lisbon (2007)"),
    ("1", "P", "Charter of Fundamental Rights of the European Union consolidated versions (2007, 2010, 2012, 2016)"),
    ("1", "J", "Treaty of Accession of Croatia (2012)"),
    ("1", "W", "EU-UK Withdrawal agreement (2019)"),
    ("1", "X", "Treaty amending certain provisions of the Protocol on the Statute of the European Investment Bank (1975)"),
    ("1", "ME","Consolidated versions of the Treaty on the European Union (TEU or Treaty of Maastricht) and Treaty on the Functioning of the European Union (TFEU) 2016"),
    ("2", "A", "Agreements with non-member States or international organisations"),
    ("2", "D", "Acts of bodies created by international agreements"),
    ("2", "P", "Acts of parliamentary bodies created by international agreements"),
    ("2", "X", "Other acts"),
    ("3", "E", "CFSP: common positions; joint actions; common strategies (pre-Lisbon title V of EU Treaty)"),
    ("3", "F", "Police and judicial co-operation in criminal matters (pre-Lisbon title VI of EU Treaty)"),
    ("3", "R", "Regulations"),
    ("3", "L", "Directives"),
    ("3", "D", "Decisions (with or without addressee)"),
    ("3", "S", "ECSC Decisions of general interest"),
    ("3", "M", "Non-opposition to a notified concentration"),
    ("3", "J", "Non-opposition to a notified joint venture"),
    ("3", "B", "Budget"),
    ("3", "K", "ECSC recommendations"),
    ("3", "O", "ECB guidelines"),
    ("3", "H", "Recommendations"),
    ("3", "A", "Opinions"),
    ("3", "G", "Resolutions"),
    ("3", "C", "Declarations"),
    ("3", "Q", "Institutional arrangements: Rules of procedure; Internal agreements"),
    ("3", "X", "Other documents published in OJ L (or pre-1967)"),
    ("3", "Y", "Other documents published in OJ C"),
    ("4", "A", "Agreements between Member States"),
    ("4", "D", "Decisions of the representatives of the governments of the Member States"),
    ("4", "X", "Other acts published in OJ L"),
    ("4", "Y", "Other acts published in OJ C"),
    ("4", "Z", "Complementary legislation"),
    ("5", "AG", "Council and MS - Council positions and statement of reasons"),
    ("5", "KG", "Council and MS - Council assents (ECSC Treaty)"),
    ("5", "IG", "Council and MS - Member States – initiatives"),
    ("5", "XG", "Council and MS - Other documents of the Council or the Member States"),
    ("5", "PC", "European Commission - COM – legislative proposals, and documents related"),
    ("5", "DC", "European Commission - Other COM documents (green papers, white papers, communications, reports, etc.)"),
    ("5", "JC", "European Commission - JOIN documents"),
    ("5", "SC", "European Commission - SEC and SWD documents"),
    ("5", "EC", "European Commission - Proposals of codified versions of regulations"),
    ("5", "FC", "European Commission - Proposals of codified versions of directives"),
    ("5", "GC", "European Commission - roposals of codified versions of decisions"),
    ("5", "M", "European Commission - Merger control documents"),
    ("5", "AT", "European Commission - Antitrust"),
    ("5", "AS", "European Commission - State aid"),
    ("5", "XC", "European Commission - Other documents of the Commission"),
    ("5", "AP", "European Parliament - Legislative resolutions of the EP"),
    ("5", "BP", "European Parliament - Budget (EP)"),
    ("5", "IP", "European Parliament - Other resolutions and declarations of the EP"),
    ("5", "DP", "European Parliament - Internal decisions of the EP"),
    ("5", "XP", "European Parliament - Other documents of the EP"),
    ("5", "AA", "European Court of Auditors - ECA Opinions"),
    ("5", "TA", "European Court of Auditors - ECA Reports"),
    ("5", "SA", "European Court of Auditors - ECA Special reports"),
    ("5", "XA", "European Court of Auditors - Other documents of the ECA"),
    ("5", "AB", "European Central Bank - ECB Opinions"),
    ("5", "HB", "European Central Bank - ECB Recommendations"),
    ("5", "XB", "European Central Bank - Other documents of the ECB"),
    ("5", "AE", "European Economic and Social Committee - EESC Opinions on consultation"),
    ("5", "IE", "European Economic and Social Committee - EESC Own-initiative opinions"),
    ("5", "AC", "European Economic and Social Committee - EESC Opinions"),
    ("5", "XE", "European Economic and Social Committee - Other documents of the EESC"),
    ("5", "AR", "European Committee of the Regions - CoR Opinions on consultation"),
    ("5", "IR", "European Committee of the Regions - CoR Own-initiative opinions"),
    ("5", "XR", "European Committee of the Regions - Other documents of the CoR"),
    ("5", "AK", "ECSC Commitee - ECSC Consultative Committee Opinions"),
    ("5", "XK", "ECSC Commitee - Other documents of the ECSC Committee"),
    ("5", "XX", "Other organs - Other documents"),
    ("6", "CJ", "Court of Justice - Judgment"),
    ("6", "CO", "Court of Justice - Order"),
    ("6", "CC", "Court of Justice - Opinion of the Advocate-General"),
    ("6", "CS", "Court of Justice - Seizure"),
    ("6", "CT", "Court of Justice - Third party proceeding"),
    ("6", "CV", "Court of Justice - Opinion"),
    ("6", "CX", "Court of Justice - Ruling"),
    ("6", "CD", "Court of Justice - Decision"),
    ("6", "CP", "Court of Justice - View"),
    ("6", "CN", "Court of Justice - Communication: new case"),
    ("6", "CA", "Court of Justice - Communication: judgment"),
    ("6", "CB", "Court of Justice - Communication: order"),
    ("6", "CU", "Court of Justice - Communication: request for an opinion"),
    ("6", "CG", "Court of Justice - Communication: opinion"),
    ("6", "TJ", "General Court (pre-Lisbon: Court of First Instance) - Judgment"),
    ("6", "TO", "General Court (pre-Lisbon: Court of First Instance) - Order"),
    ("6", "TC", "General Court (pre-Lisbon: Court of First Instance) - Opinion of the Advocate-General"),
    ("6", "TT", "General Court (pre-Lisbon: Court of First Instance) - Third party proceeding"),
    ("6", "TN", "General Court (pre-Lisbon: Court of First Instance) - Communication: new case"),
    ("6", "TA", "General Court (pre-Lisbon: Court of First Instance) - Communication: judgment"),
    ("6", "TB", "General Court (pre-Lisbon: Court of First Instance) - Communication: order"),
    ("6", "FJ", "Civil Service Tribunal - Judgment"),
    ("6", "FO", "Civil Service Tribunal - Order"),
    ("6", "FT", "Civil Service Tribunal - Third party proceeding"),
    ("6", "FN", "Civil Service Tribunal - Communication: new case"),
    ("6", "FA", "Civil Service Tribunal - Communication: judgment"),
    ("6", "FB", "Civil Service Tribunal - Communication: order"),
    ("7", "L", "National measures to transpose directives"),
    ("7", "F", "National measures to transpose framework decisions"),
    ("8", "BE", "Belgium"),
    ("8", "BG", "Bulgaria"),
    ("8", "CZ", "Czech Republic"),
    ("8", "DK", "Denmark"),
    ("8", "DE", "Germany"),
    ("8", "EE", "Estonia"),
    ("8", "IE", "Ireland"),
    ("8", "EL", "Greece"),
    ("8", "ES", "Spain"),
    ("8", "FR", "France"),
    ("8", "HR", "Croatia"),
    ("8", "IT", "Italy"),
    ("8", "CY", "Cyprus"),
    ("8", "LV", "Latvia"),
    ("8", "LT", "Lithuania"),
    ("8", "LU", "Luxembourg"),
    ("8", "HU", "Hungary"),
    ("8", "MT", "Malta"),
    ("8", "NL", "Netherlands"),
    ("8", "AT", "Austria"),
    ("8", "PL", "Poland"),
    ("8", "PT", "Portugal"),
    ("8", "RO", "Romania"),
    ("8", "SI", "Slovenia"),
    ("8", "SK", "Slovakia"),
    ("8", "FI", "Finland"),
    ("8", "SE", "Sweden"),
    ("8", "UK", "United Kingdom"),
    ("8", "CH", "Switzerland"),
    ("8", "IS", "Iceland"),
    ("8", "NO", "Norway"),
    ("8", "XX", "Other countries, EFTA Court, European Court of Human Rights"),
    ("9", "E", "Written questions"),
    ("9", "H", "Questions at question time"),
    ("9", "O", "Oral questions"),
    ("E", "A", "Agreements between EFTA Member States"),
    ("E", "C", "Acts of the EFTA Surveillance Authority"),
    ("E", "G", "Acts of the EFTA Standing Committee"),
    ("E", "J", "Decisions, orders, consultative opinions of the EFTA Court"),
    ("E", "P", "Pending cases of the EFTA Court"),
    ("E", "X", "Information and communications"),
    ("E", "O", "Other acts"),
)
" The document types defined within CELEX sectors "


def _celex_doctype(sector_number: str, document_type: str):
    "helper to search in CELEX_DOCTYPES.  Returns None if nothing matches."
    # keep in mind that sector number isn't a number (see C and E)
    for d_sn, d_dt, d_descr in CELEX_DOCTYPES:
        if d_sn == sector_number and d_dt == document_type:
            return d_descr
    return None


def is_equivalent_celex(celex1: str, celex2: str):
    """Do two CELEX identifiers refer to the same document?

    Currently:
      - ignores sector to be able to ignore sector 0
      - tries to ignore
    This is currently based on estimation - we should read up on the details.
    @param celex1: CELEX identifier as string. Will be parsed.
    @param celex2: CELEX identifier as string. Will be parsed.
    """
    d1 = parse_celex(celex1)
    d2 = parse_celex(celex2)
    return d1["id"][1:] == d2["id"][1:]


_RE_CELEX = re.compile(
    r"(\b[1234567890CE])([0-9]{4})([A-Z][A-Z]?)([0-9\(\)]{4,})(\b[^\s\"\>&.]*)?"
)
# _RE_CELEX = re.compile( r'([1234567890CE])([0-9]{4})([A-Z][A-Z]?)([0-9\(\)]+)([A-Z0-9\(\)_]*)?' )

# 94994L1


def parse_celex(celex: str):
    """Describes CELEX's parts in more readable form, where possible.
    All values are returned as strings, even where they are (ostensibly) numbers.

    Also produces a somewhat-normalized form (e.g. strips a 'CELEX:' in front)

    Returns a dict detailing the parts.
    NOTE that the details will change when I actually read the specs properly
      - norm is what you fed in, uppercased, and with an optional 'CELEX:' stripped
        but otherwise untouched
      - id is recoposed from sector_number, year, document_type, document_number
        which means it is stripped of additions - it may strip more than you want!

    Keep in mind that this will _not_ resolve things like
    "go to the consolidated version" like the EUR-Lex site will do

    TODO: read the spec, because I'm not 100% on
      - sector 0
      - sector C
      - whether additions like (01) in e.g. 32012A0424(01) are part of the identifier or not
        (...yes. Theyse are unique documents)
      - national transposition
      - if you have multiple additions like '(01)' and '-20160504' and 'FIN_240353',
        ...what order they should appear in

    TODO: we might be able to assist common in those cases (e.g. a test for "is this equivalent").
    I e.g. do not know whether id_nonattrans is useful or correct

    @param celex: CELEX identifier as string. Will be parsed.
    """
    norm = celex.strip()
    norm = (
        norm.upper()
    )  # the whole thing is case insensitive, so this is also normalisation
    if norm.startswith("CELEX:"):
        norm = norm[6:].strip()

    ret = {"norm": norm}
    # TODO: read up on the possible additions, how they combine, because the current parsing is probably incomplete
    match = _RE_CELEX.match(norm)
    # -[0-9]{8}|[A-Z]{3}_[0-9]+

    if match is None:
        raise ValueError("Did not understand %r (%r) as CELEX number" % (celex, norm))

    sector_number, year, document_type, document_number, addition = match.groups()

    # If there's more string to it, see if it makes sense to us.
    nattrans, specdate = "", ""
    # print( document_number, addition )
    if addition not in (None, ""):
        if (
            addition[:3] in CELEX_COUNTRIES
        ):  # CONSIDER: accept any three-letter combination, to be future-compatible
            nattrans = addition
        elif addition[0] == "-":
            specdate = addition
        else:
            raise ValueError(
                "Did not understand extra value %r on %r" % (addition, norm)
            )

    ret["sector_number"] = sector_number  # actually a string, because of C and E
    if sector_number in CELEX_SECTORS:
        ret["sector_name"] = CELEX_SECTORS[sector_number]
    ret["year"] = year
    ret["document_type"] = document_type
    ret["document_type_description"] = _celex_doctype(sector_number, document_type)
    ret["document_number"] = document_number
    ret["nattrans"] = nattrans
    ret["specdate"] = specdate

    ret["id"] = "".join((sector_number, year, document_type, document_number))
    # ret['id_nonattrans']   = ''.join( (sector_number, year, document_type, document_number) )

    return ret


def _is_all_digits(s):  # perhaps could be helpers.strings.is_numeric?
    return len(s.strip("0123456789")) == 0


_re_bekendid = re.compile(r"((?:ag-tk|ag-ek|ag-vv|ag|ah-tk|ah-ek|ah-tk|h-ek|h-tk|kv-tk|kv|blg|kst|stcrt|stb|gmb|prb|wsb|bgr|trb|nds-tk|nds-ek|nds)-[a-z0-9-]+)")

def findall_bekendmaking_ids(instring: str):
    """Look for identifiers like C{stcrt-2009-9231} and C{ah-tk-20082009-2945}
    Might find a few things that are not.

    TODO: give this function a better name, it's not just bekendmakingen.

    @param instring: the string to look in
    @return: a list of values, like ["stcrt-2009-9231", "ah-tk-20082009-2945"]
    """
    # Note that knowing most of the variants, we could refine this and avoid some false positives
    return _re_bekendid.findall( instring )


def parse_bekendmaking_id(s):
    """
    Parses identifiers like
    - C{kst-26643-144-h1}
    - C{h-tk-20082009-7140-7144}
    - C{ah-tk-20082009-2945}
    - C{stcrt-2009-9231}

    TODO: give this function a better name, it's not just bekendmakingen.

    Notes:
    - as of this writing it still fails on ~ .01% of of keys I've seen, but most of those seem to be invalid (though almost all of those are kst-, so we may just not known an uncommon variant).
    - if you match on something like ([a-z-]+)[0-9A-Z], you get more than the below - but it depends on the documents you source. 
      - sometimes you get a bunch of ids that suggest a soft subcategory, e.g. nds-bzk0700034-b1
      - sometmies you get a capital you weren't expecting, e.g. Stcrt-2001-130-CAO1965

    CONSIDER: also producing citation form(s) of each.

    @param s: the string to parse as a single identifier.
    @return: dict with basic details, e.g. parse_bekendmaking_id('stb-2023-281') == {'type':'stb', 'jaar':'2023', 'docnum':'281'}
    where 'type' and 'docnum' are guaranteed to be there, and 'jaar' is often but not always there.
    If it not a known type of identifier, or it is known but seems invalid, it raises a ValueError.
    """
    ret = {}
    parts = s.split("-")

    # Some of these require staying in roughly this order, or you might introduce prefix ambiguity
    # These can also be simplified into fewer cases if and when we know they are without idiosyncracies

    if s.startswith("ah-tk-"):
        # ah-tk-20082009-2945
        # ah-tk-20072008-2031-h1
        ret["type"] = "ah-tk"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("ah-ek-"):
        # ah-ek-20072008-5
        # ah-ek-20082009-14-n1
        ret["type"] = "ah-ek"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("ah-"):  # not 100% on this one
        ret["type"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("h-tk-"):
        ret["type"] = "h-tk"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)  # TODO: check that always makes sense

    elif s.startswith("h-ek-"):
        ret["type"] = "h-ek"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)  # TODO: check that always makes sense

    elif s.startswith("h-vv-"):
        # h-vv-19961997-2191-2192
        ret["type"] = "h-vv"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)  # TODO: check that always makes sense

    elif s.startswith("h-"):
        ret["type"] = "h"
        parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("ag-tk-"):
        ret["type"] = "ag-tk"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("ag-ek-"):
        ret["type"] = "ag-ek"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("ag-vv-"):
        ret["type"] = "ag-vv"
        parts.pop(0)
        parts.pop(0)
        ret["jaar"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("ag-"):
        ret["type"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("kv-tk-"):
        # seems to appear in multiple forms:
        # - kv-tk-20062007-KVR27039
        # - kv-tk-2010Z06025  (more common)
        ret["type"] = "kv-tk"
        parts.pop(0)
        parts.pop(0)
        if len(parts) == 2:
            ret["jaar"] = parts.pop(0)
            ret["docnum"] = parts.pop(0)
        elif len(parts) == 1:
            ret["docnum"] = parts.pop(0)
        else:  # seems to not happen in a lot of data I've thrown at it
            raise ValueError("kv-tk-check")

    elif s.startswith("kv-"):
        ret["type"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("blg-"):
        # blg-929493
        # blg-26241-10F
        ret["type"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("kst-"):
        # a little more complex, handled by a separate function
        ret = parse_kst_id(s)

    elif s.lower().startswith(
        "stcrt-"
    ):  # for some reason only that area gets casing presumably-wrong
        # TODO: check variants
        ret["type"] = "stcrt"
        parts.pop(0)
        ret["jaar"] = parts[0]
        ret["docnum"] = "-".join(parts[1:])

    elif s.startswith("stb-"):
        # stb-1983-294
        # stb-1983-297-n1
        ret["type"] = parts.pop(0)
        ret["jaar"] = parts[0]
        ret["docnum"] = "-".join(parts[1:])

    elif s.startswith("gmb-"):
        # TODO: check variants
        ret["type"] = parts.pop(0)
        if len(parts) == 2:
            ret["jaar"] = parts[0]
            ret["docnum"] = "-".join(parts[1:])
        else:
            raise ValueError("HUH gmb - %r" % parts)

    elif s.startswith("prb-"):
        # TODO: check variants
        ret["type"] = parts.pop(0)
        if len(parts) == 2:
            ret["jaar"] = parts[0]
            ret["docnum"] = "-".join(parts[1:])
        else:
            raise ValueError("HUH prb - %r" % parts)

    elif s.startswith("wsb-"):
        # TODO: check variants
        ret["type"] = parts.pop(0)
        if len(parts) == 2:
            ret["jaar"] = parts[0]
            ret["docnum"] = "-".join(parts[1:])
        else:
            raise ValueError("HUH wsb - %r" % parts)

    elif s.startswith("bgr-"):
        # TODO: check variants
        ret["type"] = parts.pop(0)
        if len(parts) == 2:
            ret["jaar"] = parts[0]
            ret["docnum"] = "-".join(parts[1:])
        else:
            raise ValueError("HUH gmb - %r" % parts)

    elif s.startswith(
        "trb-"
    ):  # includes interesting cases like trb-2009-mei-v1, which is part of trb-2009-mei
        # TODO: check variants
        ret["type"] = parts.pop(0)
        # if len(parts)==2:
        ret["jaar"] = parts[0]
        ret["docnum"] = "-".join(parts[1:])
        # else:
        #    raise ValueError('HUH trb - %r'%parts)

    elif s.startswith("nds-tk-"):
        ret["type"] = "nds-tk"
        parts.pop(0)
        parts.pop(0)
        ret["docnum"] = "-".join(parts)

    elif s.startswith("nds-ek-"):
        # ret['type'] = 'nds-ek'
        # parts.pop(0)
        # parts.pop(0)
        raise ValueError("you do exist")

    elif s.startswith("nds-"):
        # nds-16451
        # nds-2009D05284-b1
        # nds-buza030067-b1
        # nds-vrom050481-b1
        # nds-wwi0700033-b1
        # nds-vws0800900-b1
        # nds-tk-2014D45599
        # nds-bzk
        ret["type"] = parts.pop(0)
        ret["docnum"] = "-".join(parts)

    else:
        raise ValueError("ERR2", s, parts)

    return ret


def parse_kst_id(string:str, debug:bool=False):
    """Parse kamerstukken identifiers like C{kst-26643-144-h1}

    Also a helper for C{parse_bekendmaking_id} to parse this particular subset.

    There is more description of the variations in one of our notebooks

    @param string: kst-style identifier as string. Will be parsed.
    @param debug: whether to point out some debug
    @return: a dict with keys 
      - C{dossiernum} - a kamerstukdossier, where it applies
      - C{docnum} - a document identifier
      - C{_var} to mention an internal variant that our parsing used
    """
    # e.g. so that you can do 'https://zoek.officielebekendmakingen.nl/dossier/'+ d['dossiernum']

    ret = {}  # {'input':s}
    dossiernum = []
    parts = string.split("-")

    #    ret['_var'] = 'e'
    #    return ret

    if parts[0] == "kst":
        ret["type"] = parts.pop(0)
    else:
        raise ValueError("Does not start with kst: %r" % string)

    if len(parts[0]) == 8:
        # this is a good source of vergaderjaar, but only present in _some_ of the types of kst
        #   so we might as well breed the expectation you need to parse the metadata for it,
        #   and NOT add vergaderjaar here
        parts.pop(0) # so the only thing left is to remove and ignore it

    # so what is left now is the thing after kst- OR kst-vergaderjaar-


    # 1 part left, longer number; cases like kst-1158283  which do not seem to be part of a dossier,  and let's assume that number is a document number
    if len(parts)==1 and len(parts[0]) in (7,6):   # TODO: and test that it's all numeric
        ret["_var"] = "3"
        ret["docnum"] = parts.pop(0)
        return ret

    # first part length 5 (and a _rare_ added letter) suggests dossier number.
    #    ...but there might be more parts to that laters, so we collect it into a variable.
    m = re.match( r'([0-9][0-9][0-9][0-9][0-9][A-Z]?)$', parts[0] )
    if m is not None:
        dossiernum.append( m.group(1) )
        parts.pop(0)
    else:
        raise ValueError("ERR1 Don't know what to do with %r - %r" % (string, parts))

    # in the context of a kst- identifier, we know we are referring to a document so can make some assumptions,
    # e.g. that there is always a document number following the dosssier number.
    # There are a few dozen exceptions, though, e.g. kst-20072008-31200
    #   https://repository.overheid.nl/frbr/officielepublicaties/kst/20072008/kst-20072008-31200/1/metadata/metadata.xml

    if len(parts) == 0:
        # so while we otherwise could have considered this an error, it's valid for these few cases and we should accept this.
        ret["_var"]   = "ndn"
        ret["docnum"] = "" # I guess.
        return ret
        #raise ValueError("ERR0 Don't know what to do with %r -  %r"%(string, parts,))

    elif len(parts) == 1:
        # cases like kst-1160535
        # there must be a document number, so this must be it
        ret["docnum"] = parts.pop(0)
        ret["_var"] = "1"

    elif len(parts) == 2:
        # cases like  kst-32123-[I-5],   kst-21501-[33-226] kst-20082009-31700-[IV-D]
        #             kst-32168-[3-b2],
        if _is_all_digits(
            parts[-1]
        ):  # must be a singular full document number (?) so the first part must be dossiernum
            dossiernum.append(parts.pop(0))
            ret["docnum"] = parts.pop(0)
            ret["_var"] = "2a"
        elif wetsuite.helpers.strings.has_lowercase_letter(
            parts[-1]
        ):  # that's the second part of a document numer
            ret["docnum"] = "-".join(parts)
            ret["_var"] = "2b"
        else:  # assume last part is just a document number (so it's actually the first case again)
            dossiernum.append(parts.pop(0))
            ret["docnum"] = parts.pop(0)
            ret["_var"] = "2c"
            # raise ValueError("ERR2 Don't know what to do with %r - %r"%(s, parts))

    elif len(parts) == 3:
        ret["_var"] = "3"
        # cases like kst-32123-[XIV-A-b1]
        # TODO: check we can actually assume this is always moredossiernum-docnum-moredocnum
        dossiernum.append(parts.pop(0))
        ret["docnum"] = "-".join(parts)
        # raise ValueError("ERR3 Don't know what to do with %r - %r"%(s, parts))

    else:
        raise ValueError("ERR4 Don't know what to do with %r - %r  (%s)" % (string, parts, len(parts)))

    ret["dossiernum"] = "-".join(dossiernum)

    if not debug:
        ret.pop("_var")
    return ret
