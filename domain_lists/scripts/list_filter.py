#!/usr/bin/env python3

import sys
import argparse
import datetime

from collections import Counter

# building a unique filename based on the current time
current_time = datetime.datetime.now().strftime('%I-%H-%M.%S%p')
FILENAME_SEED = f'{current_time}-filtered'

parser = argparse.ArgumentParser(description='filters dns-resolve results in various ways.')
parser.add_argument('filename', help='input file with list of results', type=argparse.FileType('r'))
parser.add_argument('--resource', help='removes hostnames without a valid (A) record', action='store_true')
parser.add_argument('--authority', help='removes hostnames without a valid (NS) record', action='store_true')
parser.add_argument('-d', metavar='[1-9]', help='filter consecutive dashes (-)', choices=range(1, 10), type=int)
parser.add_argument('-e', metavar='sub-string', help='List of sub-strings to filter', type=str, default=[], nargs='+')
parser.add_argument('-k', help='keeps excluded data in a corresponding output file', action='store_true')
parser.add_argument('-m', help='counts number of occurrences of listed sub-strings and prints results',
    type=str, default=[], nargs='+')

args = parser.parse_args(sys.argv[1:])

RESULTS_FILE = args.filename
FILTER_RESOURCE = args.resource
FILTER_AUTHORITY = args.authority
DASH_CT = args.d
USER_EXCLUDE = args.e
KEEP_EXCLUDED = args.k
USER_MATCH = args.m

if (DASH_CT):
    USER_EXCLUDE.append('-' * DASH_CT)
    USER_MATCH.append('-' * DASH_CT)

filtered_data = []
filtered_data_append = filtered_data.append

excluded_data = []
excluded_data_append = excluded_data.append

user_matches = Counter()

errors = 0
for line in RESULTS_FILE:

    host = line.strip().split(',')
    try:
        domain_name = host[0]
        resource  = int(host[1])
        authority = int(host[2])
    except:
        errors += 1
        continue

    for sub_string in USER_MATCH:
        if sub_string in domain_name:
            user_matches[sub_string] += 1


    if (FILTER_RESOURCE and not resource):
        excluded_data_append(line)

    elif (FILTER_AUTHORITY and not authority):
        excluded_data_append(line)

    elif (not USER_EXCLUDE):
        filtered_data_append(domain_name)

    elif (USER_EXCLUDE):

        for sub_string in USER_EXCLUDE:

            if (sub_string not in domain_name):
                continue

            excluded_data_append(line)

            break

        else:
            filtered_data_append(domain_name)

with open(f'{FILENAME_SEED}.txt', 'w') as outfile:
    outfile.write('\n'.join(filtered_data))

print(f'done. filtered: {len(excluded_data)}, remaining: {len(filtered_data)}, errors: {errors}.')

if (KEEP_EXCLUDED):
    with open(f'{FILENAME_SEED}-excluded.txt', 'w') as outfile:
        outfile.write(''.join(excluded_data))

if (user_matches):
    max_len = 0
    for k in user_matches:
        if len(k) > max_len: max_len = len(k)

    print(f'domain{" " * (max_len)}counts')

    for sub_string, ct in user_matches.most_common():
        print(f'{sub_string.ljust(max_len)}      {ct}')
