#!/usr/bin/env python3

from __future__ import annotations

import os
import pprint
import sys
import hashlib

WRITE_MANIFEST = True
WRITE_VALIDATION = True
# WRITE_MANIFEST = False
# WRITE_VALIDATION = False

PATH_SEPARATOR = '\\' if sys.platform == 'win32' else '/'
HOME_DIR: str = '/'.join(os.path.realpath(__file__).split(PATH_SEPARATOR)[:-2])

LIST_FOLDERS = ('domain_lists', 'geo_lists', 'ip_lists')

pp = pprint.PrettyPrinter(indent=4, width=120).pprint


# hashing in a way that is compatible with linux file systems
# todo: comments are causing hashing issues. tshoot and resolve.
def get_hash(file_path: str) -> str:
    # hashing file with all comments removed
    with open(file_path, 'rb') as file:
        file = b'\n'.join([line for line in file.read().splitlines() if not line.startswith(b'#')])

        file += b'\n'

        file_hash = hashlib.sha256(file).hexdigest()

    return file_hash

def build_manifest() -> list[str]:
    manifest = []

    # signature files
    for folder in LIST_FOLDERS:

        with open(f'{HOME_DIR}/{folder}/SIGNATURE_LIST', 'r') as sig_file:
            signature_list = sig_file.read().splitlines()

        for file in signature_list:
            file_path = f'{folder}/{file}'

            file_hash = get_hash(f'{HOME_DIR}/{file_path}')

            manifest.append(f'{file_path} {file_hash}')

    # webui geolocation config file
    # webui_cfg_file_path = 'webui/geolocation_config.json'
    # webui_cfg_hash = get_hash(f'{HOME_DIR}/webui/geolocation.cfg')
    # manifest.append(f'webui/geolocation_config.json {get_hash(f"{HOME_DIR}/webui/geolocation.cfg")}')

    return manifest

def write_manifest(manifest: list[str]) -> None:
    with open(f'{HOME_DIR}/SIGNATURE_MANIFEST', 'w') as manifest_file:
        manifest_file.write('\n'.join(manifest))

        manifest_file.write('\n')

def build_validation() -> list[str]:
    file_validation = [
        f'COMPATIBLE_VERSION {get_hash(f"{HOME_DIR}/COMPATIBLE_VERSION")}',
        f'SIGNATURE_MANIFEST {get_hash(f"{HOME_DIR}/SIGNATURE_MANIFEST")}'
    ]

    return file_validation

def write_validation(file_validation: list[str]) -> None:
    with open(f'{HOME_DIR}/FILE_VALIDATION', 'w') as validation_file:
        validation_file.write('\n'.join(file_validation))

        validation_file.write('\n')


if (__name__ == '__main__'):
    manifest = build_manifest()
    if (WRITE_MANIFEST):
        write_manifest(manifest)

    validation = build_validation()
    if (WRITE_VALIDATION):
        write_validation(validation)

    pp(manifest)
    pp(validation)
