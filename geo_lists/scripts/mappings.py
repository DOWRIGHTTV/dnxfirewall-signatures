import os
import sys

from pprint import PrettyPrinter

# loads country code to country name mapping from country_mapping_raw.csv so it can be referenced by the formatter script.
# note: there is currently not a script that that creates the country_mapping_raw.csv file. It was created manually for now.

pp = PrettyPrinter(indent=4).pprint

PATH_SEPARATOR = '\\' if sys.platform == 'win32' else '/'
HOME_DIR: str = '/'.join(os.path.realpath(__file__).split(PATH_SEPARATOR)[:-2])

GEO_LIST = {
    'NONE', 'RFC1918',
    'AFGHANISTAN', 'ALAND_ISLANDS', 'ALBANIA', 'ALGERIA', 'AMERICAN_SAMOA', 'ANDORRA', 'ANGOLA', 'ANGUILLA',
    'ANTIGUA_AND_BARBUDA', 'ARGENTINA', 'ARMENIA', 'ARUBA', 'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN',  # 'ANTARCTICA',
    'BAHAMAS', 'BAHRAIN', 'BANGLADESH', 'BARBADOS', 'BELARUS', 'BELGIUM', 'BELIZE', 'BENIN', 'BERMUDA', 'BHUTAN',
    'BOLIVIA', 'BONAIRE', 'BOSNIA_AND_HERZEGOVINA', 'BOTSWANA', 'BOUVET_ISLAND', 'BRAZIL',
    'BRITISH_INDIAN_OCEAN_TERRITORY', 'BRITISH_VIRGIN_ISLANDS', 'BRUNEI_DARUSSALAM', 'BULGARIA', 'BURKINA_FASO',
    'BURUNDI', 'CABO_VERDE', 'CAMBODIA', 'CAMEROON', 'CANADA', 'CAYMAN_ISLANDS', 'CENTRAL_AFRICAN_REPUBLIC', 'CHAD',
    'CHILE', 'CHINA', 'CHRISTMAS_ISLAND', 'COCOS_ISLANDS', 'COLOMBIA', 'COMOROS', 'CONGO', 'COTE_D_IVOIRE', 'CURACAO',
    'COOK_ISLANDS', 'COSTA_RICA', 'CROATIA', 'CUBA', 'CYPRUS', 'CZECHIA', 'DENMARK', 'DJIBOUTI', 'DOMINICA',
    'DOMINICAN_REPUBLIC', 'ECUADOR', 'EGYPT', 'EL_SALVADOR', 'EQUATORIAL_GUINEA', 'ERITREA', 'ESTONIA', 'ESWATINI',
    'ETHIOPIA', 'FALKLAND_ISLANDS', 'FAROE_ISLANDS', 'FIJI', 'FINLAND', 'FRANCE', 'FRENCH_GUIANA', 'FRENCH_POLYNESIA',
    'GABON', 'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GIBRALTAR', 'GREECE', 'GREENLAND', # 'FRENCH_SOUTHERN_TERRITORIES'
    'GRENADA', 'GUADELOUPE', 'GUAM', 'GUATEMALA', 'GUERNSEY', 'GUINEA', 'GUINEA_BISSAU', 'GUYANA', 'HAITI', 'HOLY_SEE',
    'HONDURAS', 'HONG_KONG', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 'IRAN', 'IRAQ', 'IRELAND', 'ISLE_OF_MAN',
    'ISRAEL', 'ITALY', 'JAMAICA', 'JAPAN', 'JERSEY', 'JORDAN', 'KAZAKHSTAN', 'KENYA', 'KIRIBATI', 'KUWAIT',
    'KYRGYZSTAN', 'LAOS', 'LATVIA', 'LEBANON', 'LESOTHO', 'LIBERIA', 'LIBYA', 'LIECHTENSTEIN', 'LITHUANIA',
    'LUXEMBOURG', 'MACAO', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 'MALDIVES', 'MALI', 'MALTA', 'MARSHALL_ISLANDS',
    'MARTINIQUE', 'MAURITANIA', 'MAURITIUS', 'MAYOTTE', 'MEXICO', 'MICRONESIA', 'MOLDOVA', 'MONACO', 'MONGOLIA',
    'MONTENEGRO', 'MONTSERRAT', 'MOROCCO', 'MOZAMBIQUE', 'MYANMAR', 'NAMIBIA', 'NAURU', 'NEPAL', 'NETHERLANDS',
    'NEW_CALEDONIA', 'NEW_ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA', 'NIUE', 'NORFOLK_ISLAND', 'NORTH_KOREA',
    'NORTH_MACEDONIA', 'NORTHERN_MARIANA_ISLANDS', 'NORWAY', 'OMAN', 'PAKISTAN', 'PALAU', 'PALESTINE', 'PANAMA',
    'PAPUA_NEW_GUINEA', 'PARAGUAY', 'PERU', 'PHILIPPINES', 'PITCAIRN', 'POLAND', 'PORTUGAL', 'PUERTO_RICO', 'QATAR',
    'REUNION', 'ROMANIA', 'RUSSIAN_FEDERATION', 'RWANDA', 'SAINT_BARTHELEMY', 'SAINT_KITTS_AND_NEVIS',  # 'SAINT_HELENA'
    'SAINT_LUCIA', 'SAINT_MARTIN_DUTCH', 'SAINT_MARTIN_FRENCH', 'SAINT_PIERRE_AND_MIQUELON',
    'SAINT_VINCENT_AND_THE_GRENADINES', 'SAMOA', 'SAN_MARINO', 'SAO_TOME_AND_PRINCIPE', 'SAUDI_ARABIA', 'SENEGAL',
    'SERBIA', 'SEYCHELLES', 'SIERRA_LEONE', 'SINGAPORE', 'SLOVAKIA', 'SLOVENIA', 'SOLOMON_ISLANDS', 'SOMALIA',
    'SOUTH_AFRICA', 'SOUTH_KOREA', 'SOUTH_SUDAN', 'SPAIN', 'SRI_LANKA',  # 'SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS'
    'SUDAN', 'SURINAME', 'SWEDEN', 'SWITZERLAND', 'SYRIA', 'TAIWAN', 'TAJIKISTAN', 'TANZANIA', 'THAILAND',
    'TIMOR_LESTE', 'TOGO', 'TOKELAU', 'TONGA', 'TRINIDAD_AND_TOBAGO', 'TUNISIA', 'TURKEY', 'TURKMENISTAN',
    'TURKS_AND_CAICOS_ISLANDS', 'TUVALU', 'UGANDA', 'UKRAINE', 'UK_VIRGIN_ISLANDS', 'UNITED_ARAB_EMIRATES', 'UNITED_KINGDOM',
    'UNITED_STATES', 'URUGUAY', 'US_MINOR_OUTLYING_ISLANDS', 'US_VIRGIN_ISLANDS', 'UZBEKISTAN', 'VANUATU', 'VENEZUELA',
    'VIETNAM', 'WALLIS_AND_FUTUNA', 'WESTERN_SAHARA', 'YEMEN', 'ZAMBIA', 'ZIMBABWE'
}

custom_mapping = {
    'cocos_(keeling)_islands': 'cocos_islands',
    "cote_d'ivoire": 'cote_d_ivoire',
    'guinea-bissau': 'guinea_bissau',
    "korea_(democratic_people's_republic_of)": 'north_korea',
    'korea_(republic_of)': 'south_korea',
    "lao_people's_democratic_republic": 'laos',
    'saint_martin_(french_part)': 'saint_martin_french',
    'sint_maarten_(dutch_part)': 'saint_martin_dutch',
    'syrian_arab_republic': 'syria',
    'timor-leste': 'timor_leste',
    'united_kingdom_of_great_britain_and_northern_ireland': 'united_kingdom',
    'united_states_minor_outlying_islands': 'us_minor_outlying_islands',
    'united_states_of_america': 'united_states',
    'viet_nam': 'vietnam',
    'virgin_islands_(british)': 'uk_virgin_islands',
    'virgin_islands_(u.s.)': 'us_virgin_islands'
}

def create_ccode_mapping():
    with open(f'{HOME_DIR}/scripts/country_mapping_raw.csv') as f:

        unique_set = sorted(list(set(f.read().upper().split('\n'))))

    geo_mapping = {'-,rfc1918'}
    geo_mapping_add = geo_mapping.add

    incompatible_format = []
    incompatible_format_append = incompatible_format.append

    for row in unique_set:
        split_row = row.split(',')

        cty_code = split_row[0]
        cty_name = split_row[1]

        if cty_name in GEO_LIST:
            geo_mapping_add(f'{cty_code},{cty_name}'.lower())
            continue

        filtered_name = cty_name.split('(')[0][:-1]  # remove paren and trailing _ if present

        if filtered_name in GEO_LIST:
            geo_mapping_add(f'{cty_code},{filtered_name}'.lower())
            continue

        mapped_name = custom_mapping.get(cty_name.lower(), None)
        if mapped_name is not None:
            geo_mapping_add(f'{cty_code.lower()},{mapped_name}')
            continue

        incompatible_format_append(split_row[1])

    pp(f'incompatible format count-> {len(incompatible_format)}, {incompatible_format})')

    with open(f'{HOME_DIR}/scripts/ccode_to_dnx_auto.csv', 'w') as f:
        f.write('\n'.join(sorted(geo_mapping)) + '\n')

    print(f'total countries mapped->{len(geo_mapping)}')

def create_continent_mapping():
    with open(f'{HOME_DIR}/scripts/ccode_to_dnx_auto.csv') as ccode_to_dnx:
        CCODE_TO_DNX_MAP = {line.strip().split(',')[1]: line.strip().split(',')[0] for line in ccode_to_dnx}

    with open(f'{HOME_DIR}/scripts/continent_table.csv') as f:
        continent_table = f.read().replace(' ', '_').split('\n')

        CONTINENT_TABLE = {}
        for line in continent_table:
            if not line.startswith('#') and line:
                split_line = line.strip().split(',')
                CONTINENT_TABLE[split_line[1].lower()] = split_line[6].lower()

    print(f'ccode_to_dnx-> {len(CCODE_TO_DNX_MAP)}, continent_table-> {len(CONTINENT_TABLE)}\n')

    processed_countries = []
    count = 0
    for cty, continent in CONTINENT_TABLE.items():
        if cty not in CCODE_TO_DNX_MAP:
            print(cty)
            count += 1

            processed_countries.append(f',{cty},{continent}')

        else:
            processed_countries.append(f'{CCODE_TO_DNX_MAP[cty]},{cty},{continent}')

    with open(f'{HOME_DIR}/scripts/ccode_to_dnx_with_region.csv', 'w') as ccode_to_dnx:
        ccode_to_dnx.write('\n'.join(sorted(processed_countries)))

        print(count)


create_ccode_mapping()
create_continent_mapping()
