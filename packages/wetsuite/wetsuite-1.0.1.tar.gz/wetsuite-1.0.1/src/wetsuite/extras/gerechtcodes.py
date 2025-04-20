""" Some information about the gerechtcodes use in ECLIs 

    Note that this overlaps with the output of wetsuite.datacollect.rechtspraaknl.parse_instanties()
"""


def case_insensitive_lookup(code_text: str):
    """Case insensitive code lookup, in part because ECLI is technically case insensitive

    @return: either None, or a a dict with some details like::
        {'abbrev': 'GHARL',
         'extra': ['gerechtshof'],
         'name': 'Gerechtshof Arnhem-Leeuwarden'}
    """
    code_text = code_text.upper()
    for key, value in data.items():
        if key.upper() == code_text:
            return value
    return None


# CONSIDER: putting this in a .json file or similar, also to be able to update it more easily.
data = {
    "AGAMS": {
        "abbrev": "AGAMS",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Amsterdam",
    },
    "AGARN": {
        "abbrev": "AGARN",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Arnhem",
    },
    "AGGRO": {
        "abbrev": "AGGRO",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Groningen",
    },
    "AGHAA": {
        "abbrev": "AGHAA",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Haarlem",
    },
    "AGROE": {
        "abbrev": "AGROE",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Roermond",
    },
    "AGROT": {
        "abbrev": "AGROT",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Rotterdam",
    },
    "AGSGR": {
        "abbrev": "AGSGR",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht 's-Gravenhage",
    },
    "AGSHE": {
        "abbrev": "AGSHE",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht 's-Hertogenbosch",
    },
    "AGUTR": {
        "abbrev": "AGUTR",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Utrecht",
    },
    "AGZWO": {
        "abbrev": "AGZWO",
        "extra": ["opgeheven", "ambtenarengerecht"],
        "name": "Ambtenarengerecht Zwolle",
    },
    "CBB": {
        "abbrev": "CBB",
        "extra": ["cbb"],
        "name": "College van Beroep voor het bedrijfsleven",
    },
    "CRVB": {"abbrev": "CRVB", "extra": ["crvb"], "name": "Centrale Raad van Beroep"},
    "CVBSTUF": {
        "abbrev": "CVBSTUF",
        "extra": ["opgeheven", "unsorted"],
        "name": "College van Beroep Studiefinanciering",
    },
    "DETARCO": {
        "abbrev": "DETARCO",
        "extra": ["opgeheven", "unsorted"],
        "name": "Tariefcommissie",
    },
    "GHAMS": {
        "abbrev": "GHAMS",
        "extra": ["gerechtshof"],
        "name": "Gerechtshof Amsterdam",
    },
    "GHARL": {
        "abbrev": "GHARL",
        "extra": ["gerechtshof"],
        "name": "Gerechtshof Arnhem-Leeuwarden",
    },
    "GHARN": {
        "abbrev": "GHARN",
        "extra": ["opgeheven", "gerechtshof"],
        "name": "Gerechtshof Arnhem",
    },
    "GHDHA": {
        "abbrev": "GHDHA",
        "extra": ["gerechtshof"],
        "name": "Gerechtshof Den Haag",
    },
    "GHLEE": {
        "abbrev": "GHLEE",
        "extra": ["opgeheven", "gerechtshof"],
        "name": "Gerechtshof Leeuwarden",
    },
    "GHSGR": {
        "abbrev": "GHSGR",
        "extra": ["opgeheven", "gerechtshof"],
        "name": "Gerechtshof 's-Gravenhage",
    },
    "GHSHE": {
        "abbrev": "GHSHE",
        "extra": ["gerechtshof"],
        "name": "Gerechtshof 's-Hertogenbosch",
    },
    "HR": {"abbrev": "HR", "extra": ["hr"], "name": "Hoge Raad"},
    "KTGAAR": {
        "abbrev": "KTGAAR",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Alphen aan den Rijn",
    },
    "KTGALK": {
        "abbrev": "KTGALK",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Alkmaar",
    },
    "KTGALM": {
        "abbrev": "KTGALM",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Almelo",
    },
    "KTGAMF": {
        "abbrev": "KTGAMF",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Amersfoort",
    },
    "KTGAMS": {
        "abbrev": "KTGAMS",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Amsterdam",
    },
    "KTGAPD": {
        "abbrev": "KTGAPD",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Apeldoorn",
    },
    "KTGARN": {
        "abbrev": "KTGARN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Arnhem",
    },
    "KTGASS": {
        "abbrev": "KTGASS",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Assen",
    },
    "KTGBEE": {
        "abbrev": "KTGBEE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Beetsterzwaag",
    },
    "KTGBOX": {
        "abbrev": "KTGBOX",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Boxmeer",
    },
    "KTGBOZ": {
        "abbrev": "KTGBOZ",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Bergen op Zoom",
    },
    "KTGBRE": {
        "abbrev": "KTGBRE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Breda",
    },
    "KTGBRI": {
        "abbrev": "KTGBRI",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Brielle",
    },
    "KTGDEL": {
        "abbrev": "KTGDEL",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Delft",
    },
    "KTGDEV": {
        "abbrev": "KTGDEV",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Deventer",
    },
    "KTGDHD": {
        "abbrev": "KTGDHD",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Den Helder",
    },
    "KTGDOR": {
        "abbrev": "KTGDOR",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Dordrecht",
    },
    "KTGEIN": {
        "abbrev": "KTGEIN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Eindhoven",
    },
    "KTGEMM": {
        "abbrev": "KTGEMM",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Emmen",
    },
    "KTGENS": {
        "abbrev": "KTGENS",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Enschede",
    },
    "KTGGNL": {
        "abbrev": "KTGGNL",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Groenlo",
    },
    "KTGGOU": {
        "abbrev": "KTGGOU",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Gouda",
    },
    "KTGGRC": {
        "abbrev": "KTGGRC",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Gorinchem",
    },
    "KTGGRO": {
        "abbrev": "KTGGRO",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Groningen",
    },
    "KTGHAA": {
        "abbrev": "KTGHAA",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Haarlem",
    },
    "KTGHAR": {
        "abbrev": "KTGHAR",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Harderwijk",
    },
    "KTGHFD": {
        "abbrev": "KTGHFD",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Hoofddorp",
    },
    "KTGHIL": {
        "abbrev": "KTGHIL",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Hilversum",
    },
    "KTGHMD": {
        "abbrev": "KTGHMD",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Helmond",
    },
    "KTGHRL": {
        "abbrev": "KTGHRL",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Heerlen",
    },
    "KTGHRN": {
        "abbrev": "KTGHRN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Hoorn",
    },
    "KTGHRV": {
        "abbrev": "KTGHRV",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Heerenveen",
    },
    "KTGLDN": {
        "abbrev": "KTGLDN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Leiden",
    },
    "KTGLEE": {
        "abbrev": "KTGLEE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Leeuwarden",
    },
    "KTGLLY": {
        "abbrev": "KTGLLY",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Lelystad",
    },
    "KTGMAA": {
        "abbrev": "KTGMAA",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Maastricht",
    },
    "KTGMEP": {
        "abbrev": "KTGMEP",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Meppel",
    },
    "KTGMID": {
        "abbrev": "KTGMID",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Middelburg",
    },
    "KTGNMG": {
        "abbrev": "KTGNMG",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Nijmegen",
    },
    "KTGOBL": {
        "abbrev": "KTGOBL",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Oud-Beijerland",
    },
    "KTGOOS": {
        "abbrev": "KTGOOS",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Oostburg",
    },
    "KTGPAR": {
        "abbrev": "KTGPAR",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Parimaribo",
    },
    "KTGROE": {
        "abbrev": "KTGROE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Roermond",
    },
    "KTGROT": {
        "abbrev": "KTGROT",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Rotterdam",
    },
    "KTGSCH": {
        "abbrev": "KTGSCH",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Schiedam",
    },
    "KTGSGR": {
        "abbrev": "KTGSGR",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht 's-Gravenhage",
    },
    "KTGSHE": {
        "abbrev": "KTGSHE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht 's-Hertogenbosch",
    },
    "KTGSIT": {
        "abbrev": "KTGSIT",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Sittard",
    },
    "KTGSNK": {
        "abbrev": "KTGSNK",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Sneek",
    },
    "KTGSOM": {
        "abbrev": "KTGSOM",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Sommelsdijk",
    },
    "KTGSTW": {
        "abbrev": "KTGSTW",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Steenwijk",
    },
    "KTGTIE": {
        "abbrev": "KTGTIE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Tiel",
    },
    "KTGTIL": {
        "abbrev": "KTGTIL",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Tilburg",
    },
    "KTGTRB": {
        "abbrev": "KTGTRB",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Terborg",
    },
    "KTGTRN": {
        "abbrev": "KTGTRN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Terneuzen",
    },
    "KTGUTR": {
        "abbrev": "KTGUTR",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Utrecht",
    },
    "KTGVEE": {
        "abbrev": "KTGVEE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Veendam",
    },
    "KTGVEN": {
        "abbrev": "KTGVEN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Venlo",
    },
    "KTGWAG": {
        "abbrev": "KTGWAG",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Wageningen",
    },
    "KTGWIN": {
        "abbrev": "KTGWIN",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Winschoten",
    },
    "KTGZAA": {
        "abbrev": "KTGZAA",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Zaandam",
    },
    "KTGZEV": {
        "abbrev": "KTGZEV",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Zevenbergen",
    },
    "KTGZIE": {
        "abbrev": "KTGZIE",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Zierikzee",
    },
    "KTGZUI": {
        "abbrev": "KTGZUI",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Zuidbroek",
    },
    "KTGZUT": {
        "abbrev": "KTGZUT",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Zutphen",
    },
    "KTGZWO": {
        "abbrev": "KTGZWO",
        "extra": ["opgeheven", "kantongerecht"],
        "name": "Kantongerecht Zwolle",
    },
    "OCHM": {
        "abbrev": "OCHM",
        "extra": ["eilanden"],
        "name": "Constitutioneel Hof Sint Maarten",
    },
    "OGAACMB": {
        "abbrev": "OGAACMB",
        "extra": ["eilanden"],
        "name": "Gerecht in Ambtenarenzaken van Aruba, Curaçao, Sint "
        "Maarten en van Bonaire, Sint Eustatius en Saba",
    },
    "OGANA": {
        "abbrev": "OGANA",
        "extra": ["opgeheven", "eilanden"],
        "name": "Gerecht in Ambtenarenzaken van de Nederlandse Antillen",
    },
    "OGEAA": {
        "abbrev": "OGEAA",
        "extra": ["eilanden"],
        "name": "Gerecht in Eerste Aanleg van Aruba",
    },
    "OGEAB": {
        "abbrev": "OGEAB",
        "extra": ["opgeheven", "eilanden"],
        "name": "Gerecht in Eerste Aanleg Bonaire",
    },
    "OGEABES": {
        "abbrev": "OGEABES",
        "extra": ["eilanden"],
        "name": "Gerecht in eerste aanleg van Bonaire, Sint Eustatius en " "Saba",
    },
    "OGEAC": {
        "abbrev": "OGEAC",
        "extra": ["eilanden"],
        "name": "Gerecht in eerste aanleg van Curaçao",
    },
    "OGEAM": {
        "abbrev": "OGEAM",
        "extra": ["eilanden"],
        "name": "Gerecht in eerste aanleg van Sint Maarten",
    },
    "OGEANA": {
        "abbrev": "OGEANA",
        "extra": ["opgeheven", "eilanden"],
        "name": "Gerecht in Eerste Aanleg van de Nederlandse Antillen",
    },
    "OGHACMB": {
        "abbrev": "OGHACMB",
        "extra": ["eilanden"],
        "name": "Gemeenschappelijk Hof van Justitie van Aruba, Curaçao, "
        "Sint Maarten en van Bonaire, Sint Eustatius en Saba",
    },
    "OGHNAA": {
        "abbrev": "OGHNAA",
        "extra": ["opgeheven", "eilanden"],
        "name": "Gemeenschappelijk Hof van Justitie van de Nederlandse "
        "Antillen en Aruba",
    },
    "OHJNA": {
        "abbrev": "OHJNA",
        "extra": ["opgeheven", "eilanden"],
        "name": "Hof van Justitie van de Nederlandse Antillen",
    },
    "ORBAACM": {
        "abbrev": "ORBAACM",
        "extra": ["raadvanberoep", "eilanden"],
        "name": "Raad van Beroep in Ambtenarenzaken van Aruba, Curaçao, "
        "Sint Maarten en van Bonaire, Sint Eustatius en Saba",
    },
    "ORBANAA": {
        "abbrev": "ORBANAA",
        "extra": ["opgeheven", "raadvanberoep", "eilanden"],
        "name": "Raad van Beroep in Ambtenarenzaken (Nederlandse Antillen " "en Aruba)",
    },
    "ORBBACM": {
        "abbrev": "ORBBACM",
        "extra": ["raadvanberoep", "eilanden"],
        "name": "Raad van Beroep voor Belastingzaken van Aruba, Curaçao, "
        "Sint Maarten en van Bonaire, Sint Eustatius en Saba",
    },
    "ORBBNAA": {
        "abbrev": "ORBBNAA",
        "extra": ["opgeheven", "raadvanberoep", "eilanden"],
        "name": "Raad van Beroep voor Belastingzaken (Nederlandse "
        "Antillen en Aruba)",
    },
    "PHR": {"abbrev": "PHR", "extra": ["hr"], "name": "Parket bij de Hoge Raad"},
    "RBALK": {
        "abbrev": "RBALK",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Alkmaar",
    },
    "RBALM": {
        "abbrev": "RBALM",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Almelo",
    },
    "RBAMS": {"abbrev": "RBAMS", "extra": ["rechtbank"], "name": "Rechtbank Amsterdam"},
    "RBARN": {
        "abbrev": "RBARN",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Arnhem",
    },
    "RBASS": {
        "abbrev": "RBASS",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Assen",
    },
    "RBBRE": {
        "abbrev": "RBBRE",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Breda",
    },
    "RBDHA": {"abbrev": "RBDHA", "extra": ["rechtbank"], "name": "Rechtbank Den Haag"},
    "RBDOR": {
        "abbrev": "RBDOR",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Dordrecht",
    },
    "RBGEL": {
        "abbrev": "RBGEL",
        "extra": ["rechtbank"],
        "name": "Rechtbank Gelderland",
    },
    "RBGRO": {
        "abbrev": "RBGRO",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Groningen",
    },
    "RBHAA": {
        "abbrev": "RBHAA",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Haarlem",
    },
    "RBLEE": {
        "abbrev": "RBLEE",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Leeuwarden",
    },
    "RBLIM": {"abbrev": "RBLIM", "extra": ["rechtbank"], "name": "Rechtbank Limburg"},
    "RBMAA": {
        "abbrev": "RBMAA",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Maastricht",
    },
    "RBMID": {
        "abbrev": "RBMID",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Middelburg",
    },
    "RBMNE": {
        "abbrev": "RBMNE",
        "extra": ["rechtbank"],
        "name": "Rechtbank Midden-Nederland",
    },
    "RBNHO": {
        "abbrev": "RBNHO",
        "extra": ["rechtbank"],
        "name": "Rechtbank Noord-Holland",
    },
    "RBNNE": {
        "abbrev": "RBNNE",
        "extra": ["rechtbank"],
        "name": "Rechtbank Noord-Nederland",
    },
    "RBOBR": {
        "abbrev": "RBOBR",
        "extra": ["rechtbank"],
        "name": "Rechtbank Oost-Brabant",
    },
    "RBONE": {
        "abbrev": "RBONE",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Oost-Nederland",
    },
    "RBOVE": {
        "abbrev": "RBOVE",
        "extra": ["rechtbank"],
        "name": "Rechtbank Overijssel",
    },
    "RBROE": {
        "abbrev": "RBROE",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Roermond",
    },
    "RBROT": {"abbrev": "RBROT", "extra": ["rechtbank"], "name": "Rechtbank Rotterdam"},
    "RBSGR": {
        "abbrev": "RBSGR",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank 's-Gravenhage",
    },
    "RBSHE": {
        "abbrev": "RBSHE",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank 's-Hertogenbosch",
    },
    "RBUTR": {
        "abbrev": "RBUTR",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Utrecht",
    },
    "RBZLY": {
        "abbrev": "RBZLY",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Zwolle-Lelystad",
    },
    "RBZUT": {
        "abbrev": "RBZUT",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Zutphen",
    },
    "RBZWB": {
        "abbrev": "RBZWB",
        "extra": ["rechtbank"],
        "name": "Rechtbank Zeeland-West-Brabant",
    },
    "RBZWO": {
        "abbrev": "RBZWO",
        "extra": ["opgeheven", "rechtbank"],
        "name": "Rechtbank Zwolle",
    },
    "RVBALK": {
        "abbrev": "RVBALK",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Alkmaar",
    },
    "RVBAMS": {
        "abbrev": "RVBAMS",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Amsterdam",
    },
    "RVBARN": {
        "abbrev": "RVBARN",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Arnhem",
    },
    "RVBBRE": {
        "abbrev": "RVBBRE",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Breda",
    },
    "RVBGRO": {
        "abbrev": "RVBGRO",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Groningen",
    },
    "RVBHAA": {
        "abbrev": "RVBHAA",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Haarlem",
    },
    "RVBLDN": {
        "abbrev": "RVBLDN",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Leiden",
    },
    "RVBLEE": {
        "abbrev": "RVBLEE",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Leeuwarden",
    },
    "RVBMID": {
        "abbrev": "RVBMID",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Middelburg",
    },
    "RVBROE": {
        "abbrev": "RVBROE",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Roermond",
    },
    "RVBROT": {
        "abbrev": "RVBROT",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Rotterdam",
    },
    "RVBSGR": {
        "abbrev": "RVBSGR",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep 's-Gravenhage",
    },
    "RVBSHE": {
        "abbrev": "RVBSHE",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep 's-Hertogenbosch",
    },
    "RVBTIL": {
        "abbrev": "RVBTIL",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Tilburg",
    },
    "RVBUTR": {
        "abbrev": "RVBUTR",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Utrecht",
    },
    "RVBZWO": {
        "abbrev": "RVBZWO",
        "extra": ["opgeheven", "raadvanberoep"],
        "name": "Raad van beroep Zwolle",
    },
    "RVS": {"abbrev": "RVS", "extra": ["rvs"], "name": "Raad van State"},
    "TACAKN": {
        "abbrev": "TACAKN",
        "extra": ["unsorted"],
        "name": "Accountantskamer NIVRA",
    },
    "TADRAMS": {
        "abbrev": "TADRAMS",
        "extra": ["tucht"],
        "name": "Raad van Discipline Amsterdam",
    },
    "TADRARL": {
        "abbrev": "TADRARL",
        "extra": ["tucht"],
        "name": "Raad van Discipline Arnhem-Leeuwarden",
    },
    "TADRARN": {
        "abbrev": "TADRARN",
        "extra": ["opgeheven", "tucht"],
        "name": "Raad van Discipline Arnhem",
    },
    "TADRLEE": {
        "abbrev": "TADRLEE",
        "extra": ["opgeheven", "tucht"],
        "name": "Raad van Discipline Leeuwarden",
    },
    "TADRSGR": {
        "abbrev": "TADRSGR",
        "extra": ["tucht"],
        "name": "Raad van Discipline 's-Gravenhage",
    },
    "TADRSHE": {
        "abbrev": "TADRSHE",
        "extra": ["tucht"],
        "name": "Raad van Discipline 's-Hertogenbosch",
    },
    "TAHVD": {"abbrev": "TAHVD", "extra": ["unsorted"], "name": "Hof van Discipline"},
    "TAKTPA": {
        "abbrev": "TAKTPA",
        "extra": ["tucht"],
        "name": "Tuchtgerecht Productschap Akkerbouw",
    },
    "TBBBKD": {
        "abbrev": "TBBBKD",
        "extra": ["tucht"],
        "name": "Tuchtgerecht Bloembollenkeuringsdienst",
    },
    "TBPSKAL": {"abbrev": "TBPSKAL", "extra": ["tucht"], "name": "Skal-Tuchtgerecht"},
    "TDIVBC": {
        "abbrev": "TDIVBC",
        "extra": ["unsorted"],
        "name": "Veterinair Beroepscollege",
    },
    "TDIVTC": {
        "abbrev": "TDIVTC",
        "extra": ["tucht"],
        "name": "Veterinair Tuchtcollege",
    },
    "TGDKG": {
        "abbrev": "TGDKG",
        "extra": ["unsorted"],
        "name": "Kamer voor Gerechtsdeurwaarders",
    },
    "TGFKCB": {
        "abbrev": "TGFKCB",
        "extra": ["tucht"],
        "name": "Tuchtgerecht Kwaliteits-Controle-Bureau",
    },
    "TGZCTG": {
        "abbrev": "TGZCTG",
        "extra": ["tucht"],
        "name": "Centraal Tuchtcollege voor de Gezondheidszorg",
    },
    "TGZRAMS": {
        "abbrev": "TGZRAMS",
        "extra": ["tucht"],
        "name": "Regionaal Tuchtcollege voor de Gezondheidszorg " "Amsterdam",
    },
    "TGZREIN": {
        "abbrev": "TGZREIN",
        "extra": ["tucht"],
        "name": "Regionaal Tuchtcollege voor de Gezondheidszorg " "Eindhoven",
    },
    "TGZRGRO": {
        "abbrev": "TGZRGRO",
        "extra": ["tucht"],
        "name": "Regionaal Tuchtcollege voor de Gezondheidszorg " "Groningen",
    },
    "TGZRSGR": {
        "abbrev": "TGZRSGR",
        "extra": ["tucht"],
        "name": "Regionaal Tuchtcollege voor de Gezondheidszorg " "'s-Gravenhage",
    },
    "TGZRZWO": {
        "abbrev": "TGZRZWO",
        "extra": ["tucht"],
        "name": "Regionaal Tuchtcollege voor de Gezondheidszorg Zwolle",
    },
    "TNOKALK": {
        "abbrev": "TNOKALK",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Alkmaar",
    },
    "TNOKALM": {
        "abbrev": "TNOKALM",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Almelo",
    },
    "TNOKAMS": {
        "abbrev": "TNOKAMS",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Amsterdam",
    },
    "TNOKARN": {
        "abbrev": "TNOKARN",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Arnhem",
    },
    "TNOKASS": {
        "abbrev": "TNOKASS",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Assen",
    },
    "TNOKBRE": {
        "abbrev": "TNOKBRE",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Breda",
    },
    "TNOKDOR": {
        "abbrev": "TNOKDOR",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Dordrecht",
    },
    "TNOKGRO": {
        "abbrev": "TNOKGRO",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Groningen",
    },
    "TNOKHAA": {
        "abbrev": "TNOKHAA",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Haarlem",
    },
    "TNOKLEE": {
        "abbrev": "TNOKLEE",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Leeuwarden",
    },
    "TNOKMAA": {
        "abbrev": "TNOKMAA",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Maastricht",
    },
    "TNOKMID": {
        "abbrev": "TNOKMID",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Middelburg",
    },
    "TNOKROE": {
        "abbrev": "TNOKROE",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Roermond",
    },
    "TNOKROT": {
        "abbrev": "TNOKROT",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Rotterdam",
    },
    "TNOKSGR": {
        "abbrev": "TNOKSGR",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen 's-Gravenhage",
    },
    "TNOKSHE": {
        "abbrev": "TNOKSHE",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen 's-Hertogenbosch",
    },
    "TNOKUTR": {
        "abbrev": "TNOKUTR",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen Utrecht",
    },
    "TNOKZLY": {
        "abbrev": "TNOKZLY",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen\xa0Zwolle-Lelystad",
    },
    "TNOKZUT": {
        "abbrev": "TNOKZUT",
        "extra": ["opgeheven", "notar"],
        "name": "Kamer van Toezicht over de notarissen en "
        "kandidaat-notarissen\xa0Zutphen",
    },
    "TNORAMS": {
        "abbrev": "TNORAMS",
        "extra": ["notar"],
        "name": "Kamer voor het notariaat in het ressort Amsterdam",
    },
    "TNORARL": {
        "abbrev": "TNORARL",
        "extra": ["notar"],
        "name": "Kamer voor het notariaat in het ressort " "Arnhem-Leeuwarden",
    },
    "TNORDHA": {
        "abbrev": "TNORDHA",
        "extra": ["notar"],
        "name": "Kamer voor het notariaat in het ressort Den Haag",
    },
    "TNORSHE": {
        "abbrev": "TNORSHE",
        "extra": ["notar"],
        "name": "Kamer voor het notariaat in het ressort " "'s-Hertogenbosch",
    },
    "TPETPVE": {
        "abbrev": "TPETPVE",
        "extra": ["tucht"],
        "name": "Tuchtgerecht Productschap Pluimvee en Eieren",
    },
    "TSCTS": {
        "abbrev": "TSCTS",
        "extra": ["tucht"],
        "name": "Tuchtcollege voor de Scheepvaart",
    },
    "TVSTPV": {
        "abbrev": "TVSTPV",
        "extra": ["tucht"],
        "name": "Tuchtgerecht Productschap Vis",
    },
    "TVVTPVV": {
        "abbrev": "TVVTPVV",
        "extra": ["tucht"],
        "name": "Tuchtgerecht Productschap Vee en Vlees",
    },
    "XX": {
        "abbrev": "XX",
        "extra": ["xx"],
        "name": "Gerechtscode voor uitspraken van nationale rechterlijke en "
        "niet-rechterlijke instanties die geen eigen gerechtscode hebben, "
        "of voor uitspraken van buitenlandse, Europese of internationale instanties "
        "waaraan door het daartoe bevoegde orgaan (nog) geen eigen ECLI is toegekend "
        "(artikel 1 lid 1 sub c onder vii van de Annex bij de Raadsconclusies "
        "waarin de invoering wordt aanbevolen van een Europese identificatiecode"
        "voor jurisprudentie (ECLI), en van een "
        "minimumaantal uniforme metagegevens betreffende jurisprudentie (2011/C 127/01))",
    },
}
""" nested dict with gerecthtcode-data """
