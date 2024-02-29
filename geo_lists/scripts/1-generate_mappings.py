import os
import sys

from pprint import PrettyPrinter

from geolocation_enum_list import GEOLOCATION_ENUM_LIST

# loads country code to country name, mapping from country_mapping_raw.csv.
# note: there is currently not a script that creates the country_mapping_raw.csv file, it was created manually.

pp = PrettyPrinter(indent=4).pprint

PATH_SEPARATOR = '\\' if sys.platform == 'win32' else '/'
GEO_DIR: str = '/'.join(os.path.realpath(__file__).split(PATH_SEPARATOR)[:-2])

def sep_print(x): print('-'*32); print(x); print('-'*32)
def sep_wrap(x): s = ['-'*32, x, '-'*32, '']; return '\n'.join(s)


GEO_LIST = set(x.lower() for x in GEOLOCATION_ENUM_LIST)

custom_mapping = {
    'cocos_(keeling)_islands': 'cocos_islands',
    "cote_d'ivoire": 'cote_d_ivoire',
    'guinea-bissau': 'guinea_bissau',
    "korea_(democratic_people's_republic_of)": 'north_korea',
    "democratic_people's_republic_of_korea": 'north_korea',
    'korea_(republic_of)': 'south_korea',
    'republic_of_korea': 'south_korea',
    "lao_people's_democratic_republic": 'laos',
    "palestine, state of": 'palestine',
    'saint_martin_(french_part)': 'saint_martin_french',
    'sint_maarten_(dutch_part)': 'saint_martin_dutch',
    'syrian_arab_republic': 'syria',
    "tanzania, united republic of": 'tanzania',
    'timor-leste': 'timor_leste',
    'united_kingdom_of_great_britain_and_northern_ireland': 'united_kingdom',
    'united_states_minor_outlying_islands': 'us_minor_outlying_islands',
    'united_states_of_america': 'united_states',
    'viet_nam': 'vietnam',
    'virgin_islands_(british)': 'uk_virgin_islands',
    'virgin_islands_(u.s.)': 'us_virgin_islands'
}

def parse_new_collection_for_ccode() -> list[list[str, str]]:

    unique_country_mapping = set()
    ucm_add = unique_country_mapping.add

    with open(f'{GEO_DIR}/new_collection.csv') as f:

        signature_list = f.read().split('\n')

    for line in signature_list:
        try:
            _, _, ccode, country = line.split(',')
        except ValueError:
            _, _, ccode, country, _ = line.split(',')

        ucm_add(f'{ccode},{country.replace(" ", "_").replace("-", "_")}')

    # for mapping in sorted(unique_country_mapping):
    #     print(mapping)
    sep_print(f'{len(unique_country_mapping)} unique country mappings')

    return [x.split(',') for x in sorted(unique_country_mapping)]

def create_dnx_ccode_mapping() -> dict[str, str]:
    unique_country_mapping = parse_new_collection_for_ccode()

    geo_mapping = {'-': 'rfc1918'}

    incompatible_format = []
    incompatible_format_append = incompatible_format.append

    for cty_code, cty_name in unique_country_mapping:

        if cty_name in GEO_LIST:
            geo_mapping[cty_name] = cty_code
            continue

        filtered_name = cty_name.split('(')[0].rstrip('_')  # remove paren and trailing _ if present

        # print(filtered_name)
        if filtered_name in GEO_LIST:
            geo_mapping[filtered_name] = cty_code
            continue

        mapped_name = custom_mapping.get(cty_name, None)
        if mapped_name is not None:
            geo_mapping[mapped_name] = cty_code
            continue

        incompatible_format_append(cty_name)

    pp(f'incompatible format count-> {len(incompatible_format)}, {incompatible_format})')

    return geo_mapping

    # with open(f'{GEO_DIR}/scripts/ccode_to_dnx_auto.csv', 'w') as f:
    #     f.write('\n'.join(sorted(geo_mapping)) + '\n')
    #
    # print(f'total countries mapped->{len(geo_mapping)}')

def generate_dnx_mappings():
    CCODE_TO_DNX_MAP = create_dnx_ccode_mapping()

    CONTINENT_TABLE = {}
    with open(f'{GEO_DIR}/scripts/continent_table.csv') as f:
        continent_table = f.read().replace(' ', '_').replace('-', '_').split('\n')

        for line in continent_table:
            if not line.startswith('#') and line:
                split_line = line.strip().split(',')
                CONTINENT_TABLE[split_line[1]] = split_line[-1]

    # print(f'ccode_to_dnx-> {len(CCODE_TO_DNX_MAP)}, continent_table-> {len(CONTINENT_TABLE)}\n')

    processed_countries = []
    no_dnx_mapping = []
    for cty, continent in CONTINENT_TABLE.items():
        if cty in CCODE_TO_DNX_MAP:
            processed_countries.append(f'{CCODE_TO_DNX_MAP[cty]},{cty},{continent}')

            # remove processed countries so we can manually cross-reference the output
            CCODE_TO_DNX_MAP.pop(cty)
            continue

        no_dnx_mapping.append(f',{cty},{continent}')

    with open(f'{GEO_DIR}/scripts/ccode_to_dnx_auto_generated.csv', 'w') as ccode_to_dnx:
        ccode_to_dnx.write(sep_wrap(f'UNRESOLVED DNXFIREWALL COUNTRIES -> {len(CCODE_TO_DNX_MAP)}'))
        ccode_to_dnx.write('\n'.join(sorted([f'{y},{x}' for x, y in CCODE_TO_DNX_MAP.items()])) + '\n')

        ccode_to_dnx.write(sep_wrap(f'NO DNXFIREWALL MAPPING -> {len(no_dnx_mapping)}'))
        ccode_to_dnx.write('\n'.join(sorted(no_dnx_mapping)) + '\n')

        ccode_to_dnx.write(sep_wrap(f'AUTO GENERATED MAPPING -> {len(processed_countries)}'))
        ccode_to_dnx.write('\n'.join(sorted(processed_countries)))


generate_dnx_mappings()
