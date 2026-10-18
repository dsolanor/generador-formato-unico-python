// ============================================================
// 📦 CORREOS - Relleno automático
// Uso: rellenarEnvio() — abre un modal para pegar la línea CSV
// Formato: el CSV de Big Cartel SIN cabeceras, separado por TABULADOR
// ============================================================

const PAISES = {
  // ── Afganistán ────────────────────────────────────────────
  "af": "3",   "afghanistan": "3",   "afganistan": "3",
  // ── Albania ───────────────────────────────────────────────
  "al": "6",   "albania": "6",
  // ── Alemania ──────────────────────────────────────────────
  "de": "54",  "germany": "54",  "alemania": "54",
  // ── Angola ────────────────────────────────────────────────
  "ao": "9",   "angola": "9",
  // ── Anguila ───────────────────────────────────────────────
  "ai": "5",   "anguilla": "5",  "anguila": "5",
  // ── Antigua y Barbuda ─────────────────────────────────────
  "ag": "4",   "antigua and barbuda": "4",  "antigua y barbuda": "4",
  // ── Antillas Holandesas ───────────────────────────────────
  "an": "8",   "netherlands antilles": "8", "antillas holandesas": "8",
  // ── Arabia Saudita ────────────────────────────────────────
  "sa": "191", "saudi arabia": "191",  "arabia saudita": "191",
  // ── Argelia ───────────────────────────────────────────────
  "dz": "59",  "algeria": "59",  "argelia": "59",
  // ── Argentina ─────────────────────────────────────────────
  "ar": "11",  "argentina": "11",
  // ── Armenia ───────────────────────────────────────────────
  "am": "7",   "armenia": "7",
  // ── Aruba ─────────────────────────────────────────────────
  "aw": "15",  "aruba": "15",
  // ── Ascensión ─────────────────────────────────────────────
  "ac": "261", "ascension": "261",
  // ── Australia ─────────────────────────────────────────────
  "au": "14",  "australia": "14",
  // ── Austria ───────────────────────────────────────────────
  "at": "13",  "austria": "13",
  // ── Azerbaiyán ────────────────────────────────────────────
  "az": "16",  "azerbaijan": "16",  "azerbaiyan": "16",
  // ── Azores ────────────────────────────────────────────────
  "azores": "170",
  // ── Bahamas ───────────────────────────────────────────────
  "bs": "30",  "bahamas": "30",
  // ── Bangladesh ────────────────────────────────────────────
  "bd": "19",  "bangladesh": "19",
  // ── Barbados ──────────────────────────────────────────────
  "bb": "18",  "barbados": "18",
  // ── Bélgica ───────────────────────────────────────────────
  "be": "20",  "belgium": "20",  "belgica": "20",
  // ── Belice ────────────────────────────────────────────────
  "bz": "35",  "belize": "35",  "belice": "35",
  // ── Benín ─────────────────────────────────────────────────
  "bj": "25",  "benin": "25",
  // ── Bermudas ──────────────────────────────────────────────
  "bm": "26",  "bermuda": "26",  "bermudas": "26",
  // ── Bielorrusia ───────────────────────────────────────────
  "by": "34",  "belarus": "34",  "bielorrusia": "34",
  // ── Bolivia ───────────────────────────────────────────────
  "bo": "28",  "bolivia": "28",
  // ── Bosnia Herzegovina ────────────────────────────────────
  "ba": "17",  "bosnia and herzegovina": "17",  "bosnia": "17",  "bosnia herzegovina": "17",
  // ── Botswana ──────────────────────────────────────────────
  "bw": "33",  "botswana": "33",
  // ── Brasil ────────────────────────────────────────────────
  "br": "29",  "brazil": "29",  "brasil": "29",
  // ── Brunéi ────────────────────────────────────────────────
  "bn": "27",  "brunei": "27",  "brunei darussalam": "27",
  // ── Bulgaria ──────────────────────────────────────────────
  "bg": "22",  "bulgaria": "22",
  // ── Burkina Faso ──────────────────────────────────────────
  "bf": "21",  "burkina faso": "21",
  // ── Burundi ───────────────────────────────────────────────
  "bi": "24",  "burundi": "24",
  // ── Bután ─────────────────────────────────────────────────
  "bt": "31",  "bhutan": "31",  "butan": "31",
  // ── Cabo Verde ────────────────────────────────────────────
  "cv": "50",  "cape verde": "50",  "cabo verde": "50",
  // ── Islas Caimán ──────────────────────────────────────────
  "ky": "122", "cayman islands": "122",  "cayman": "122",  "caiman islas": "122",
  // ── Camboya ───────────────────────────────────────────────
  "kh": "115", "cambodia": "115",  "camboya": "115",
  // ── Camerún ───────────────────────────────────────────────
  "cm": "45",  "cameroon": "45",  "camerun": "45",
  // ── Canadá ────────────────────────────────────────────────
  "ca": "36",  "canada": "36",
  // ── República Centroafricana ──────────────────────────────
  "cf": "39",  "central african republic": "39",  "centroafricana rep": "39",
  // ── Chad ──────────────────────────────────────────────────
  "td": "211", "chad": "211",
  // ── República Checa ───────────────────────────────────────
  "cz": "53",  "czech republic": "53",  "czechia": "53",  "checa rep": "53",
  // ── Chile ─────────────────────────────────────────────────
  "cl": "44",  "chile": "44",
  // ── China ─────────────────────────────────────────────────
  "cn": "46",  "china": "46",
  // ── Chipre ────────────────────────────────────────────────
  "cy": "52",  "cyprus": "52",  "chipre": "52",
  // ── Islas Cocos ───────────────────────────────────────────
  "cc": "37",  "cocos islands": "37",  "cocos keeling islands": "37",
  // ── Colombia ──────────────────────────────────────────────
  "co": "47",  "colombia": "47",
  // ── Comoras ───────────────────────────────────────────────
  "km": "117", "comoros": "117",  "comores": "117",
  // ── Congo (Rep.) ──────────────────────────────────────────
  "cg": "40",  "republic of the congo": "40",  "congo rep": "40",  "congo": "40",
  // ── Congo (Rep. Dem.) ─────────────────────────────────────
  "cd": "38",  "democratic republic of the congo": "38",  "congo rep dem": "38",
  // ── Islas Cook ────────────────────────────────────────────
  "ck": "43",  "cook islands": "43",  "cook islas": "43",
  // ── Corea del Norte ───────────────────────────────────────
  "kp": "119", "north korea": "119",  "corea del norte": "119",
  // ── Corea del Sur ─────────────────────────────────────────
  "kr": "120", "south korea": "120",  "korea": "120",  "corea del sur": "120",
  // ── Costa de Marfil ───────────────────────────────────────
  "ci": "42",  "ivory coast": "42",  "cote d'ivoire": "42",  "costa de marfil": "42",
  // ── Costa Rica ────────────────────────────────────────────
  "cr": "48",  "costa rica": "48",
  // ── Croacia ───────────────────────────────────────────────
  "hr": "98",  "croatia": "98",  "croacia": "98",
  // ── Cuba ──────────────────────────────────────────────────
  "cu": "49",  "cuba": "49",
  // ── Dinamarca ─────────────────────────────────────────────
  "dk": "56",  "denmark": "56",  "dinamarca": "56",
  // ── Yibuti ────────────────────────────────────────────────
  "dj": "55",  "djibouti": "55",  "djibuti": "55",
  // ── Dominica ──────────────────────────────────────────────
  "dm": "57",  "dominica": "57",
  // ── República Dominicana ──────────────────────────────────
  "do": "58",  "dominican republic": "58",  "dominicana republica": "58",
  // ── Ecuador ───────────────────────────────────────────────
  "ec": "60",  "ecuador": "60",
  // ── Egipto ────────────────────────────────────────────────
  "eg": "62",  "egypt": "62",  "egipto": "62",
  // ── El Salvador ───────────────────────────────────────────
  "sv": "207", "el salvador": "207",
  // ── Eritrea ───────────────────────────────────────────────
  "er": "64",  "eritrea": "64",
  // ── Eslovaquia ────────────────────────────────────────────
  "sk": "200", "slovakia": "200",  "eslovaquia": "200",
  // ── Eslovenia ─────────────────────────────────────────────
  "si": "198", "slovenia": "198",  "eslovenia": "198",
  // ── Estados Unidos ────────────────────────────────────────
  "us": "229", "united states": "229",  "estados unidos": "229",
  // ── Estonia ───────────────────────────────────────────────
  "ee": "61",  "estonia": "61",
  // ── Etiopía ───────────────────────────────────────────────
  "et": "66",  "ethiopia": "66",  "etiopia": "66",
  // ── Islas Feroe ───────────────────────────────────────────
  "fo": "71",  "faroe islands": "71",  "feroe islas": "71",
  // ── Fiyi ──────────────────────────────────────────────────
  "fj": "68",  "fiji": "68",  "fidji islas": "68",
  // ── Filipinas ─────────────────────────────────────────────
  "ph": "176", "philippines": "176",  "filipinas": "176",
  // ── Finlandia ─────────────────────────────────────────────
  "fi": "67",  "finland": "67",  "finlandia": "67",
  // ── Francia ───────────────────────────────────────────────
  "fr": "72",  "france": "72",  "francia": "72",
  // ── Gabón ─────────────────────────────────────────────────
  "ga": "77",  "gabon": "77",
  // ── Gambia ────────────────────────────────────────────────
  "gm": "85",  "gambia": "85",
  // ── Georgia (país) ────────────────────────────────────────
  "ge": "80",  "georgia": "80",
  // ── Georgia del Sur ───────────────────────────────────────
  "gs": "90",  "south georgia": "90",
  // ── Ghana ─────────────────────────────────────────────────
  "gh": "82",  "ghana": "82",
  // ── Gibraltar ─────────────────────────────────────────────
  "gi": "83",  "gibraltar": "83",
  // ── Granada ───────────────────────────────────────────────
  "gd": "79",  "grenada": "79",  "granada": "79",
  // ── Grecia ────────────────────────────────────────────────
  "gr": "89",  "greece": "89",  "grecia": "89",
  // ── Groenlandia ───────────────────────────────────────────
  "gl": "84",  "greenland": "84",  "groenlandia": "84",
  // ── Guadalupe ─────────────────────────────────────────────
  "gp": "87",  "guadeloupe": "87",  "guadalupe": "87",
  // ── Guam ──────────────────────────────────────────────────
  "gu": "92",  "guam": "92",
  // ── Guatemala ─────────────────────────────────────────────
  "gt": "91",  "guatemala": "91",
  // ── Guayana Francesa ──────────────────────────────────────
  "gf": "81",  "french guiana": "81",  "guayana francesa": "81",
  // ── Guernsey ──────────────────────────────────────────────
  "gg": "74",  "guernsey": "74",
  // ── Guinea ────────────────────────────────────────────────
  "gn": "86",  "guinea": "86",
  // ── Guinea-Bisáu ──────────────────────────────────────────
  "gw": "93",  "guinea-bissau": "93",  "guinea bissau": "93",
  // ── Guinea Ecuatorial ─────────────────────────────────────
  "gq": "88",  "equatorial guinea": "88",  "guinea ecuatorial": "88",
  // ── Guyana ────────────────────────────────────────────────
  "gy": "94",  "guyana": "94",
  // ── Haití ─────────────────────────────────────────────────
  "ht": "99",  "haiti": "99",
  // ── Honduras ──────────────────────────────────────────────
  "hn": "97",  "honduras": "97",
  // ── Hong Kong ─────────────────────────────────────────────
  "hk": "95",  "hong kong": "95",
  // ── Hungría ───────────────────────────────────────────────
  "hu": "100", "hungary": "100",  "hungria": "100",
  // ── India ─────────────────────────────────────────────────
  "in": "104", "india": "104",
  // ── Indonesia ─────────────────────────────────────────────
  "id": "101", "indonesia": "101",
  // ── Irlanda ───────────────────────────────────────────────
  "ie": "102", "ireland": "102",  "irlanda": "102",
  // ── Islandia ──────────────────────────────────────────────
  "is": "108", "iceland": "108",  "islandia": "108",
  // ── Israel ────────────────────────────────────────────────
  "il": "103", "israel": "103",
  // ── Italia ────────────────────────────────────────────────
  "it": "109", "italy": "109",  "italia": "109",
  // ── Jamaica ───────────────────────────────────────────────
  "jm": "110", "jamaica": "110",
  // ── Japón ─────────────────────────────────────────────────
  "jp": "112", "japan": "112",  "japon": "112",
  // ── Jersey ────────────────────────────────────────────────
  "je": "76",  "jersey": "76",
  // ── Jordania ──────────────────────────────────────────────
  "jo": "111", "jordan": "111",  "jordania": "111",
  // ── Kazajistán ────────────────────────────────────────────
  "kz": "123", "kazakhstan": "123",  "kazajstan": "123",
  // ── Kenia ─────────────────────────────────────────────────
  "ke": "113", "kenya": "113",  "kenia": "113",
  // ── Kirguistán ────────────────────────────────────────────
  "kg": "263", "kyrgyzstan": "263",  "kirguistan": "263",
  // ── Kiribati ──────────────────────────────────────────────
  "ki": "116", "kiribati": "116",
  // ── Kosovo ────────────────────────────────────────────────
  "xk": "273", "kosovo": "273",
  // ── Laos ──────────────────────────────────────────────────
  "la": "124", "laos": "124",
  // ── Lesoto ────────────────────────────────────────────────
  "ls": "130", "lesotho": "130",  "lesoto": "130",
  // ── Letonia ───────────────────────────────────────────────
  "lv": "133", "latvia": "133",  "letonia": "133",
  // ── Líbano ────────────────────────────────────────────────
  "lb": "125", "lebanon": "125",  "libano": "125",
  // ── Liberia ───────────────────────────────────────────────
  "lr": "129", "liberia": "129",
  // ── Libia ─────────────────────────────────────────────────
  "ly": "134", "libya": "134",  "libia": "134",
  // ── Liechtenstein ─────────────────────────────────────────
  "li": "127", "liechtenstein": "127",
  // ── Lituania ──────────────────────────────────────────────
  "lt": "131", "lithuania": "131",  "lituania": "131",
  // ── Luxemburgo ────────────────────────────────────────────
  "lu": "132", "luxembourg": "132",  "luxemburgo": "132",
  // ── Macao ─────────────────────────────────────────────────
  "mo": "145", "macao": "145",  "macau": "145",
  // ── Macedonia ─────────────────────────────────────────────
  "mk": "141", "north macedonia": "141",  "macedonia": "141",
  // ── Madagascar ────────────────────────────────────────────
  "mg": "139", "madagascar": "139",
  // ── Madeira ───────────────────────────────────────────────
  "madeira": "171",
  // ── Malasia ───────────────────────────────────────────────
  "my": "155", "malaysia": "155",  "malasia": "155",
  // ── Malaui ────────────────────────────────────────────────
  "mw": "153", "malawi": "153",
  // ── Maldivas ──────────────────────────────────────────────
  "mv": "152", "maldives": "152",  "maldivas": "152",
  // ── Mali ──────────────────────────────────────────────────
  "ml": "142", "mali": "142",
  // ── Malta ─────────────────────────────────────────────────
  "mt": "150", "malta": "150",
  // ── Islas Malvinas ────────────────────────────────────────
  "fk": "69",  "falkland islands": "69",  "malvinas islas": "69",
  // ── Isla de Man ───────────────────────────────────────────
  "im": "75",  "isle of man": "75",  "man isla de": "75",
  // ── Islas Marianas del Norte ──────────────────────────────
  "mp": "146", "northern mariana islands": "146",  "marianas islas": "146",
  // ── Marruecos ─────────────────────────────────────────────
  "ma": "135", "morocco": "135",  "marruecos": "135",
  // ── Islas Marshall ────────────────────────────────────────
  "mh": "140", "marshall islands": "140",  "marshall islas": "140",
  // ── Martinica ─────────────────────────────────────────────
  "mq": "147", "martinique": "147",  "martinica": "147",
  // ── Mauricio ──────────────────────────────────────────────
  "mu": "151", "mauritius": "151",  "mauricio": "151",
  // ── Mauritania ────────────────────────────────────────────
  "mr": "148", "mauritania": "148",
  // ── Mayotte ───────────────────────────────────────────────
  "yt": "242", "mayotte": "242",
  // ── México ────────────────────────────────────────────────
  "mx": "154", "mexico": "154",
  // ── Micronesia ────────────────────────────────────────────
  "fm": "70",  "micronesia": "70",
  // ── Moldavia ──────────────────────────────────────────────
  "md": "137", "moldova": "137",  "moldavia": "137",
  // ── Mónaco ────────────────────────────────────────────────
  "mc": "136", "monaco": "136",
  // ── Mongolia ──────────────────────────────────────────────
  "mn": "144", "mongolia": "144",
  // ── Montenegro ────────────────────────────────────────────
  "me": "138", "montenegro": "138",
  // ── Montserrat ────────────────────────────────────────────
  "ms": "149", "montserrat": "149",
  // ── Mozambique ────────────────────────────────────────────
  "mz": "156", "mozambique": "156",
  // ── Myanmar ───────────────────────────────────────────────
  "mm": "143", "myanmar": "143",  "burma": "143",
  // ── Namibia ───────────────────────────────────────────────
  "na": "157", "namibia": "157",
  // ── Nauru ─────────────────────────────────────────────────
  "nr": "166", "nauru": "166",
  // ── Nepal ─────────────────────────────────────────────────
  "np": "165", "nepal": "165",
  // ── Nicaragua ─────────────────────────────────────────────
  "ni": "162", "nicaragua": "162",
  // ── Níger ─────────────────────────────────────────────────
  "ne": "159", "niger": "159",
  // ── Nigeria ───────────────────────────────────────────────
  "ng": "161", "nigeria": "161",
  // ── Niue ──────────────────────────────────────────────────
  "nu": "167", "niue": "167",
  // ── Isla Norfolk ──────────────────────────────────────────
  "nf": "160", "norfolk island": "160",  "norfolk isla": "160",
  // ── Noruega ───────────────────────────────────────────────
  "no": "164", "norway": "164",  "noruega": "164",
  // ── Nueva Caledonia ───────────────────────────────────────
  "nc": "158", "new caledonia": "158",  "nueva caledonia": "158",
  // ── Nueva Zelanda ─────────────────────────────────────────
  "nz": "168", "new zealand": "168",  "nueva zelanda": "168",
  // ── Omán ──────────────────────────────────────────────────
  "om": "169", "oman": "169",
  // ── Países Bajos ──────────────────────────────────────────
  "nl": "163", "netherlands": "163",  "holland": "163",  "paises bajos": "163",
  // ── Pakistán ──────────────────────────────────────────────
  "pk": "177", "pakistan": "177",
  // ── Palaos ────────────────────────────────────────────────
  "pw": "183", "palau": "183",  "palaos": "183",
  // ── Panamá ────────────────────────────────────────────────
  "pa": "172", "panama": "172",
  // ── Papúa Nueva Guinea ────────────────────────────────────
  "pg": "175", "papua new guinea": "175",  "papua nueva guinea": "175",
  // ── Paraguay ──────────────────────────────────────────────
  "py": "184", "paraguay": "184",
  // ── Perú ──────────────────────────────────────────────────
  "pe": "173", "peru": "173",
  // ── Islas Pitcairn ────────────────────────────────────────
  "pn": "180", "pitcairn islands": "180",  "pitcairn islas": "180",
  // ── Polinesia Francesa ────────────────────────────────────
  "pf": "174", "french polynesia": "174",  "polinesia francesa": "174",
  // ── Polonia ───────────────────────────────────────────────
  "pl": "178", "poland": "178",  "polonia": "178",
  // ── Portugal ──────────────────────────────────────────────
  "pt": "182", "portugal": "182",
  // ── Puerto Rico ───────────────────────────────────────────
  "pr": "181", "puerto rico": "181",
  // ── Qatar ─────────────────────────────────────────────────
  "qa": "185", "qatar": "185",
  // ── Reino Unido ───────────────────────────────────────────
  "gb": "78",  "uk": "78",  "united kingdom": "78",  "reino unido": "78",  "great britain": "78",
  // ── Reunión ───────────────────────────────────────────────
  "re": "186", "reunion": "186",
  // ── Ruanda ────────────────────────────────────────────────
  "rw": "190", "rwanda": "190",  "ruanda": "190",
  // ── Rumanía ───────────────────────────────────────────────
  "ro": "187", "romania": "187",  "rumania": "187",
  // ── Rusia ─────────────────────────────────────────────────
  "ru": "189", "russia": "189",  "rusia": "189",
  // ── Saint Kitts y Nevis ───────────────────────────────────
  "kn": "118", "saint kitts and nevis": "118",  "saint kitts y nevis": "118",
  // ── Islas Salomón ─────────────────────────────────────────
  "sb": "192", "solomon islands": "192",  "salomon islas": "192",
  // ── Samoa ─────────────────────────────────────────────────
  "ws": "240", "samoa": "240",
  // ── Samoa Americana ───────────────────────────────────────
  "as": "12",  "american samoa": "12",  "samoa americana": "12",
  // ── San Marino ────────────────────────────────────────────
  "sm": "202", "san marino": "202",
  // ── San Pedro y Miquelón ──────────────────────────────────
  "pm": "179", "saint pierre and miquelon": "179",  "san pedro y miquelon": "179",
  // ── San Vicente y las Granadinas ──────────────────────────
  "vc": "233", "saint vincent and the grenadines": "233",  "san vicente y granadinas": "233",
  // ── Santa Elena ───────────────────────────────────────────
  "sh": "197", "saint helena": "197",  "santa elena": "197",
  // ── Santa Lucía ───────────────────────────────────────────
  "lc": "126", "saint lucia": "126",  "santa lucia": "126",
  // ── Santo Tomé y Príncipe ─────────────────────────────────
  "st": "206", "sao tome and principe": "206",  "santo tome y principe": "206",
  // ── Senegal ───────────────────────────────────────────────
  "sn": "203", "senegal": "203",
  // ── Serbia ────────────────────────────────────────────────
  "rs": "188", "serbia": "188",
  // ── Seychelles ────────────────────────────────────────────
  "sc": "193", "seychelles": "193",
  // ── Sierra Leona ──────────────────────────────────────────
  "sl": "201", "sierra leone": "201",  "sierra leona": "201",
  // ── Singapur ──────────────────────────────────────────────
  "sg": "196", "singapore": "196",  "singapur": "196",
  // ── Somalia ───────────────────────────────────────────────
  "so": "204", "somalia": "204",
  // ── Sri Lanka ─────────────────────────────────────────────
  "lk": "128", "sri lanka": "128",
  // ── Sudáfrica ─────────────────────────────────────────────
  "za": "244", "south africa": "244",  "sudafrica": "244",
  // ── Sudán ─────────────────────────────────────────────────
  "sd": "194", "sudan": "194",
  // ── Suecia ────────────────────────────────────────────────
  "se": "195", "sweden": "195",  "suecia": "195",
  // ── Suiza ─────────────────────────────────────────────────
  "ch": "41",  "switzerland": "41",  "suiza": "41",
  // ── Surinam ───────────────────────────────────────────────
  "sr": "205", "suriname": "205",  "surinam": "205",
  // ── Suazilandia / Eswatini ────────────────────────────────
  "sz": "209", "eswatini": "209",  "swaziland": "209",  "swazilandia": "209",
  // ── Tailandia ─────────────────────────────────────────────
  "th": "214", "thailand": "214",  "tailandia": "214",
  // ── Taiwán ────────────────────────────────────────────────
  "tw": "224", "taiwan": "224",
  // ── Tanzania ──────────────────────────────────────────────
  "tz": "225", "tanzania": "225",
  // ── Tayikistán ────────────────────────────────────────────
  "tj": "215", "tajikistan": "215",  "tayikistan": "215",
  // ── Territorios Australes Franceses ───────────────────────
  "tf": "212", "french southern territories": "212",  "territorios australes franceses": "212",
  // ── Timor Oriental ────────────────────────────────────────
  "tl": "217", "east timor": "217",  "timor-leste": "217",  "timor oriental": "217",
  // ── Togo ──────────────────────────────────────────────────
  "tg": "213", "togo": "213",
  // ── Tokelau ───────────────────────────────────────────────
  "tk": "216", "tokelau": "216",
  // ── Tonga ─────────────────────────────────────────────────
  "to": "220", "tonga": "220",
  // ── Trinidad y Tobago ─────────────────────────────────────
  "tt": "222", "trinidad and tobago": "222",  "trinidad y tobago": "222",
  // ── Tristán de Acuña ──────────────────────────────────────
  "tristan de acunha": "266",
  // ── Túnez ─────────────────────────────────────────────────
  "tn": "219", "tunisia": "219",  "tunez": "219",
  // ── Islas Turcas y Caicos ─────────────────────────────────
  "tc": "210", "turks and caicos islands": "210",  "turcas y caicos islas": "210",
  // ── Turkmenistán ──────────────────────────────────────────
  "tm": "218", "turkmenistan": "218",
  // ── Turquía ───────────────────────────────────────────────
  "tr": "221", "turkey": "221",  "turquia": "221",
  // ── Tuvalu ────────────────────────────────────────────────
  "tv": "223", "tuvalu": "223",
  // ── Ucrania ───────────────────────────────────────────────
  "ua": "226", "ukraine": "226",  "ucrania": "226",
  // ── Uganda ────────────────────────────────────────────────
  "ug": "227", "uganda": "227",
  // ── Islas Ultramarinas EE.UU. ─────────────────────────────
  "um": "269", "united states minor outlying islands": "269",
  // ── Uruguay ───────────────────────────────────────────────
  "uy": "230", "uruguay": "230",
  // ── Uzbekistán ────────────────────────────────────────────
  "uz": "231", "uzbekistan": "231",
  // ── Vanuatu ───────────────────────────────────────────────
  "vu": "238", "vanuatu": "238",
  // ── Vaticano ──────────────────────────────────────────────
  "va": "232", "vatican": "232",  "holy see": "232",  "vaticano": "232",
  // ── Venezuela ─────────────────────────────────────────────
  "ve": "234", "venezuela": "234",
  // ── Vietnam ───────────────────────────────────────────────
  "vn": "237", "vietnam": "237",
  // ── Islas Vírgenes Británicas ─────────────────────────────
  "vg": "235", "british virgin islands": "235",  "virgenes britanicas islas": "235",
  // ── Wallis y Futuna ───────────────────────────────────────
  "wf": "239", "wallis and futuna": "239",  "wallis y futuna": "239",
  // ── Zambia ────────────────────────────────────────────────
  "zm": "245", "zambia": "245",
  // ── Zimbabue ──────────────────────────────────────────────
  "zw": "246", "zimbabwe": "246",

  // ── España (no aparece en el select internacional) ────────
  "es": "65",  "spain": "65",  "españa": "65",

  // ── Estados de EE.UU. — fallback cuando Shipping Country viene vacío ──
  "alabama": "229",      "alaska": "229",       "arizona": "229",
  "arkansas": "229",     "california": "229",   "colorado": "229",
  "connecticut": "229",  "delaware": "229",     "florida": "229",
  "hawaii": "229",       "idaho": "229",        "illinois": "229",
  "indiana": "229",      "iowa": "229",         "kansas": "229",
  "kentucky": "229",     "louisiana": "229",    "maine": "229",
  "maryland": "229",     "massachusetts": "229","michigan": "229",
  "minnesota": "229",    "mississippi": "229",  "missouri": "229",
  "montana": "229",      "nebraska": "229",     "nevada": "229",
  "new hampshire": "229","new jersey": "229",   "new mexico": "229",
  "new york": "229",     "north carolina": "229","north dakota": "229",
  "ohio": "229",         "oklahoma": "229",     "oregon": "229",
  "pennsylvania": "229", "rhode island": "229", "south carolina": "229",
  "south dakota": "229", "tennessee": "229",    "texas": "229",
  "utah": "229",         "vermont": "229",      "virginia": "229",
  "washington": "229",   "west virginia": "229","wisconsin": "229",
  "wyoming": "229",      "district of columbia": "229", "dc": "229",
};

const COLUMNAS = [
  "Number", "Buyer first name", "Buyer last name", "Buyer email", "Buyer phone number",
  "Date", "Time", "Status", "Payment status", "Transaction ID",
  "Shipping status", "Shipping methods", "Shipping address 1", "Shipping address 2",
  "Shipping city", "Shipping state", "Shipping zip", "Shipping country",
  "Currency", "Items", "Item count", "Item total", "Total price", "Total shipping",
  "Total tax", "Tax remitted by Big Cartel", "Total discount", "Discount code",
  "Source", "Note", "Private notes",
  "Peso", // columna extra opcional — añádela manualmente al final si la necesitas
];

function rellenar(id, valor) {
  const el = document.getElementById(id);
  if (!el) { console.warn("⚠️ Campo no encontrado:", id); return; }
  el.value = valor;
  ['input', 'change', 'blur'].forEach(ev =>
    el.dispatchEvent(new Event(ev, { bubbles: true }))
  );
}

function rellenarMercancia(pesoKg = '0,24', valorNeto) {
  const radioMerc = document.getElementById("myform:chkcontenidoEnvio:1");
  if (!radioMerc) { console.warn("⚠️ Radio 'Mercancías' no encontrado"); return; }
  radioMerc.checked = true;
  radioMerc.dispatchEvent(new Event('change', { bubbles: true }));

  setTimeout(() => {
    rellenar("myform:conhx:0:descMercancia", "Textiles - Algodón");
    rellenar("myform:conhx:0:cantidadPart",  "1");
    rellenar("myform:conhx:0:pesoneto",      pesoKg);
    rellenar("myform:conhx:0:valorneto",     valorNeto);
    rellenar("myform:conhx:0:idPais",        "65");

    const valorContenido = document.getElementById("myform:valorContenido");
    if (valorContenido) {
      valorContenido.removeAttribute("disabled");
      valorContenido.value = valorNeto;
    }

    rellenar("myform:Instruc_noentrega", "1");

    console.log(`📦 Mercancía rellenada — Peso neto: ${pesoKg} kg | Valor neto: ${valorNeto}`);
  }, 500);
}

function procesarCSV(lineaCSV) {
  const valores = lineaCSV.split("\t").map(v => v.trim());
  const fila = Object.fromEntries(COLUMNAS.map((c, i) => [c, valores[i] ?? ""]));

  const codigoPais =
    PAISES[(fila["Shipping country"] || "").toLowerCase().trim()] ||
    PAISES[(fila["Shipping state"]   || "").toLowerCase().trim()] ||
    "229";

  const pesoKg = fila["Peso"] ? (parseFloat(fila["Peso"]) / 1000).toFixed(3) : "";

  const localidad = [fila["Shipping city"], fila["Shipping state"]]
    .filter(Boolean).join(", ");

  rellenar("myform:nombre",                      fila["Buyer first name"]);
  rellenar("myform:apellido",                    fila["Buyer last name"]);
  rellenar("myform:mail",                        fila["Buyer email"]);
  rellenar("myform:telefono",                    fila["Buyer phone number"].replace(/[\s\(\)\-]/g, ""));
  rellenar("myform:direccion_destinatario",      fila["Shipping address 1"]);
  rellenar("myform:dirComplementoInternacional", fila["Shipping address 2"]);
  rellenar("myform:zip",                         fila["Shipping zip"]);
  rellenar("myform:localidadDestInt",            localidad);
  rellenar("myform:selectPaisesInt",             codigoPais);
  rellenar("myform:inputAlto",                   "1");
  rellenar("myform:inputAncho",                  "29");
  rellenar("myform:inputProfundo",               "37");
  rellenar("myform:compDatos_DatoEnv_CampoAdic__5_16", pesoKg ?? '0,24');

  rellenarMercancia(pesoKg ?? '0,24', fila["Item total"]);

  console.log(`✅ Formulario rellenado: ${fila["Buyer first name"]} ${fila["Buyer last name"]}`);
  console.log(`⚖️ Peso introducido: ${pesoKg ? pesoKg + " kg" : "(vacío)"} (${fila["Peso"] || "0"} g)`);
}

function mostrarModal() {
  const overlay = document.createElement("div");
  overlay.style.cssText = `
    position: fixed; inset: 0; background: rgba(0,0,0,0.5);
    z-index: 99998; display: flex; align-items: center; justify-content: center;
  `;

  const modal = document.createElement("div");
  modal.style.cssText = `
    background: white; border-radius: 10px; padding: 24px;
    width: 600px; max-width: 90vw; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    display: flex; flex-direction: column; gap: 12px; z-index: 99999;
  `;

  const titulo = document.createElement("h3");
  titulo.textContent = "📦 Pega la línea del CSV";
  titulo.style.cssText = "margin: 0; font-size: 16px; color: #002d62;";

  const textarea = document.createElement("textarea");
  textarea.placeholder = "Pega aquí la fila del CSV (separada por tabuladores)...";
  textarea.style.cssText = `
    width: 100%; height: 100px; padding: 10px; font-size: 13px;
    border: 1px solid #ccc; border-radius: 6px; resize: vertical;
    font-family: monospace; box-sizing: border-box;
  `;

  const botones = document.createElement("div");
  botones.style.cssText = "display: flex; gap: 10px; justify-content: flex-end;";

  const btnCancelar = document.createElement("button");
  btnCancelar.textContent = "Cancelar";
  btnCancelar.style.cssText = `
    padding: 8px 20px; border-radius: 6px; border: 1px solid #ccc;
    background: white; cursor: pointer; font-size: 14px;
  `;

  const btnAceptar = document.createElement("button");
  btnAceptar.textContent = "Rellenar formulario";
  btnAceptar.style.cssText = `
    padding: 8px 20px; border-radius: 6px; border: none;
    background: #002d62; color: white; cursor: pointer; font-size: 14px;
  `;

  const cerrar = () => document.body.removeChild(overlay);

  btnCancelar.addEventListener("click", cerrar);
  btnAceptar.addEventListener("click", () => {
    const linea = textarea.value.trim();
    if (!linea) { alert("⚠️ El campo está vacío."); return; }
    cerrar();
    procesarCSV(linea);
  });

  document.addEventListener("keydown", function onKey(e) {
    if (e.key === "Escape") { cerrar(); document.removeEventListener("keydown", onKey); }
  });

  botones.appendChild(btnCancelar);
  botones.appendChild(btnAceptar);
  modal.appendChild(titulo);
  modal.appendChild(textarea);
  modal.appendChild(botones);
  overlay.appendChild(modal);
  document.body.appendChild(overlay);

  setTimeout(() => textarea.focus(), 100);
}

window.rellenarEnvio = mostrarModal;

console.log("✅ Listo. Ejecuta rellenarEnvio() para abrir el modal.");
rellenarEnvio();
