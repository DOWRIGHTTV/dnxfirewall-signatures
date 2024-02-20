import json
import os
import sys

from geolocation_enum_list import GEOLOCATION_ENUM_LIST

# loads data from new_collection.csv and formats it for use with dnxfirewall.

PATH_SEPARATOR = '\\' if sys.platform == 'win32' else '/'
HOME_DIR: str = '/'.join(os.path.realpath(__file__).split(PATH_SEPARATOR)[:-3])
CFG_DIR: str = f'{HOME_DIR}/configuration'
GEO_DIR: str = f'{HOME_DIR}/geo_lists'

# print(HOME_DIR)

rfc1918 = {'167772160', '2886729728', '3232235520'}

with open(f'{GEO_DIR}/scripts/ccode_to_dnx_final.csv') as ccode_to_dnx:
    CCODE_TO_DNX_MAP = {line.strip().split(',')[0]: line.strip().split(',')[1] for line in ccode_to_dnx if not line.startswith('#')}

def format_ip_and_names():

    modified_lines = []
    modified_lines_append = modified_lines.append

    failed = set()
    with open(f'{GEO_DIR}/new_collection.csv') as f:

        for line in f:
            # at least one country contains a comma in its name
            try:
                net, bcast, ccode, country_name = line.strip().split(',')
            except ValueError:
                net, bcast, ccode, country_name, _ = line.strip().split(',')

            if (country_name == '-'):

                if (net not in rfc1918):
                    continue

            ip_count = int(bcast) - int(net)

            try:
                modified_lines_append(f'{net},{ip_count},{CCODE_TO_DNX_MAP[ccode]}')
            except Exception as e:
                failed.add(ccode)

    print(failed)

    with open(f'{GEO_DIR}/collection_auto_generated.geo', 'w') as f:
        f.write('\n'.join(modified_lines) + '\n')

# loads ccode_to_dnx_final.csv and generates json config file for dnx webui
def generate_geolocation_cfg():
    config = {
        'geolocation': {
            'africa': {'enabled': 1, 'countries': {}},
            'asia': {'enabled': 1, 'countries': {}},
            'europe': {'enabled': 1, 'countries': {}},
            'north_america': {'enabled': 1, 'countries': {}},
            'oceania': {'enabled': 1, 'countries': {}},
            'south_america': {'enabled': 1, 'countries': {}}
        },
        'enum_list': GEOLOCATION_ENUM_LIST
    }

    countries_added = 0
    with open(f'{GEO_DIR}/scripts/ccode_to_dnx_final.csv') as ccode_to_dnx:
        for line in ccode_to_dnx:
            if line.startswith('#'):
                continue

            ccode, cty, continent = line.strip().split(',')
            if continent in config['geolocation']:  # this shouldn't be necessary since the data is pre-filtered
                config['geolocation'][continent]['countries'][cty] = 0  # system default is disabled

                countries_added += 1

            else:
                print(f'continent ({continent}) for {cty} not found')

    print(f'countries added-> {countries_added}')

    # iterating over continents and replacing countries dict with a sorted version
    for continent_data in config['geolocation'].values():
        continent_data['countries'] = dict(sorted(continent_data['countries'].items()))

    with open(f'{CFG_DIR}/geolocation.cfg', 'w') as f:
        json.dump(config, f, indent=4)


if (__name__ == '__main__'):
    # format_ip_and_names()
    generate_geolocation_cfg()
