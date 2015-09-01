#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests


VERSION = '0.1'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Validator:
    rest_url = 'https://validator.nu/'

    def __init__(self, file):
        self.file = file

    def validate(self):
        content = ''
        with open(self.file) as file_content:
            content = file_content.read()
        r = requests.post(Validator.rest_url, 
                params={'out': 'gnu'}, 
                headers={'Content-Type': 'text/html; charset=UTF-8'},
                data=content)
        return r.text


def main(argv):
    if len(argv) != 1:
        print 'Invalid number of arguments'
        usage()
        exit(1)

    if argv[0] == '-v':
        version()
        exit(0)

    input_file = argv[len(argv) - 1] # last element is input file

    v = Validator(input_file)
    print 'Validating ' + input_file + '...'
    validation = v.validate()
    if len(validation) > 0:
        print validation
    else:
        print bcolors.OKGREEN + 'No errors or warnings found' + bcolors.ENDC
    print 'Validation complete'


def version():
    print 'html5validator v' + VERSION
    print 'Copyright (C) Erik Sørensen, 2015. All rights reserved.'
    usage()


def usage():
    print 'Usage: html5validator.py file'


if (__name__ == '__main__'):
    main(sys.argv[1:])
