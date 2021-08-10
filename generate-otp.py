#!/usr/bin/env python3
# Use this script to generate the one-time pad file for encryption/decryption.

import secrets, sys


def get_group():
    return ''.join([str(secrets.randbelow(10)) for _ in range(5)])


ids = set()

output = sys.argv[1] if len(sys.argv) > 1 else 'otp.txt'

with open(output, 'w') as file:
    for page in range(500):
        # Ensure we have a unique page identifier
        while True:
            id = get_group()
            if id not in ids:
                break
        ids.add(id)
        line = id
        for group in range(19):
            line += ' ' + get_group()
        line += '\n'
        file.write(line)

print('Done')