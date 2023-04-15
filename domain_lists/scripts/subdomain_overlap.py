from pprint import PrettyPrinter
from ipaddress import IPv4Address

ALL_FILES = False
WRITE_TO_FILE = True

pp = PrettyPrinter().pprint

# =========================
# FILENAME TO FILTER
FILE_TO_PARSE = 'drug'
FILES_TO_PARSE = [
    'ads', 'crypto_miner', 'downloads', 'drugs', 'dynamic_dns', 'fraud', 'gambling', 'malicious', 'mature', 'p2p',
    'piracy', 'pornography', 'purchases', 'ransomware', 'remote_login', 'scam', 'social_media', 'stream_video',
    'suspicious', 'telemetry', 'trackers', 'video_games', 'vpn', 'weapons'
]
if (not ALL_FILES):
    FILES_TO_PARSE.clear()
    FILES_TO_PARSE.append(FILE_TO_PARSE)
# =========================

FILEPATH = f'C:/Users/Freedom/PycharmProjects/dnxfirewall-signatures/domain_lists'

def run_script():
    global FILES_TO_PARSE

    for file in FILES_TO_PARSE:
        loaded_signatures = load_signatures(file)

        iter_filter_ip_addresses(loaded_signatures)

        iter_filter_www(loaded_signatures)

        iter_ddup_signatures(loaded_signatures)

        # iter_combine_sub_domains(loaded_signatures)

        if (WRITE_TO_FILE):
            write_signatures(file, loaded_signatures)

def load_signatures(file: str) -> dict[str, list[str]]:
    SIGNATURE_FILE = f'{FILEPATH}/{file}.domains'

    with open(SIGNATURE_FILE, 'r') as sig_file:
        raw_signatures: dict[str, list[str]] = {}

        # initialization values
        current_section = ''
        current_section_append = [].append

        for sig in sig_file.read().splitlines():

            if not sig.strip():
                continue

            # separators will be silently ignored, but placed back in output file
            if sig.startswith('#'):

                if ('section:' in sig):

                    # slicing off pound
                    current_section = sig[2:]
                    raw_signatures[current_section] = []

                    # performance tweak
                    current_section_append = raw_signatures[current_section].append

            else:
                current_section_append(sig.split()[0])

    return raw_signatures

def filter_ip_addresses(signature_list: list[str]) -> None:
    ''' inplace filter
    '''
    filtered_list = []

    for signature in signature_list:

        try:
            IPv4Address(signature)
        except:
            filtered_list.append(signature)

    signature_list.clear()
    signature_list.extend(filtered_list)

def write_signatures(file: str, processed_signatures: dict[str, list[str]]) -> None:
    OUTPUT_FILE = f'{FILEPATH}/{file}.new'

    with open(OUTPUT_FILE, 'w') as output_file:

        for section, signatures in processed_signatures.items():

            output_file.write(f'# {"="*32}\n')
            output_file.write(f'# {section}\n')
            output_file.write(f'# {"="*32}\n')

            signatures_with_categories = [f'{x} {file}' for x in sorted(signatures)]

            output_file.write('\n'.join(sorted(signatures_with_categories)))

            output_file.write('\n')

def filter_www(signature_list: list[str]) -> None:
    ''' inplace filter
    '''
    filtered_list = []

    for signature in signature_list:

        if signature.startswith('www.'):
            signature = signature[4:]

        filtered_list.append(signature.lower())

    signature_list.clear()
    signature_list.extend(filtered_list)

def ddup_signatures(signature_list: list[str]) -> None:
    ''' inplace filter
    '''
    dduped_signatures = set(signature_list)

    signature_list.clear()
    signature_list.extend(dduped_signatures)

def combine_sub_domains(signature_list: list[str]) -> None:
    ''' inplace filter
    '''
    with open(f'{FILEPATH}/data/second_level.domains', 'r') as sld:
        second_level_domains = set([d.split()[0] for d in sld if d.strip()])

    with open(f'{FILEPATH}/data/cdn.domains', 'r') as sld:
        cdns = set([d.split()[0] for d in sld if d.strip()])

    existing_primary_domains = set()
    signatures = []

    for signature in signature_list:

        sliced_sig = '.'.join(signature.split('.')[-2:])
        if (sliced_sig in second_level_domains):
            sliced_sig = '.'.join(signature.split('.')[-3:])

        if (sliced_sig in existing_primary_domains):
            continue

        # if cdn detected, full domain will be added to the list
        if (sliced_sig in cdns):
            signatures.append(signature)
            continue

        existing_primary_domains.add(sliced_sig)
        signatures.append(sliced_sig)

    signature_list.clear()
    signature_list.extend(signatures)

def iter_filter_ip_addresses(loaded_signatures: dict[str, list[str]]) -> None:
    original_count = 0
    filtered_count = 0

    for section, signatures in loaded_signatures.items():
        # pre-processing count
        original_count += len(signatures)

        filter_ip_addresses(signatures)

        # post in place swap of filtered data
        filtered_count += len(signatures)

    print(f'{"ip filter ->".ljust(20)}orig: {original_count}, reduced: {filtered_count}')

def iter_filter_www(loaded_signatures: dict[str, list[str]]) -> None:
    original_count = 0
    filtered_count = 0

    for section, signatures in loaded_signatures.items():

        # pre-processing count
        original_count += len(signatures)

        filter_www(signatures)

        # post in place swap of filtered data
        filtered_count += len(signatures)

    print(f'{"www filter ->".ljust(20)}orig: {original_count}, reduced: {filtered_count}')

def iter_ddup_signatures(loaded_signatures: dict[str, list[str]]) -> None:
    original_count = 0
    filtered_count = 0

    for section, signatures in loaded_signatures.items():
        # pre-processing count
        original_count += len(signatures)

        ddup_signatures(signatures)

        # post in place swap of filtered data
        filtered_count += len(signatures)

    print(f'{"ddup ->".ljust(20)}orig: {original_count}, reduced: {filtered_count}')

def iter_combine_sub_domains(loaded_signatures: dict[str, list[str]]) -> None:
    original_count = 0
    filtered_count = 0

    for section, signatures in loaded_signatures.items():
        # pre-processing count
        original_count += len(signatures)

        combine_sub_domains(signatures)

        # post in place swap of filtered data
        filtered_count += len(signatures)

    print(f'{"containment ->".ljust(20)}orig: {original_count}, reduced: {filtered_count}')


if (__name__ == '__main__'):
    run_script()
