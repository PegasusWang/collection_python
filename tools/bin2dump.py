#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function
import sys
import binascii

READ_BLOCKSIZE = 16

is_py3 = sys.version_info[0] == 3


def main(argv):
    if len(argv) < 3:
        print('Usage: {0} input_file output_file'.format(argv[0]))
        sys.exit(1)
    with open(argv[1], 'rb') as file_inp, open(argv[2], 'w') as file_out:
        while True:
            byte_s = file_inp.read(READ_BLOCKSIZE)
            if not byte_s: break
            hex_char_repr = binascii.hexlify(byte_s)
            hex_char_repr = str(hex_char_repr, encoding='utf-8') if is_py3 else hex_char_repr
            file_out.write(hex_char_repr)
            file_out.write("\n")


if __name__ == '__main__':
    main(sys.argv)
