#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import json


VERSION = '1.0.1'


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
                params={'out': 'json'}, 
                headers={'Content-Type': 'text/html; charset=UTF-8'},
                data=content)
        if r.status_code == 200:
            return r.text
        else:
            return ''


class ValidationOutputFormatter:
    def __init__(self):
        pass

    def output_stdout(self, validation):
        validation_json = json.loads(validation)
        # print validation_json

        messages = validation_json['messages']
        for message in messages:
            if message['type'] == 'info':
                print bcolors.OKGREEN + 'Info:\t' + message['message'] + bcolors.ENDC
            elif message['type'] == 'warning':
                print bcolors.WARNING + 'Warning:\t' + message['message'] + bcolors.ENDC
            elif message['type'] == 'error':
                print bcolors.FAIL + 'Error:\t' + message['message'] + bcolors.ENDC

    def output_stdout_old(self, validation):
        if len(validation) > 0:
            print bcolors.FAIL + 'Found something:' + bcolors.ENDC
            print validation
        else:
            print bcolors.OKGREEN + 'No errors or warnings found' + bcolors.ENDC
        print 'Validation complete'


def main(argv):
    if len(argv) != 1:
        print 'Invalid number of arguments'
        usage()
        exit(1)

    if argv[0] == '-v':
        version()
        exit(0)

    input_file = argv[len(argv) - 1] # last element is input file
    do_validation(input_file)


def do_validation(input_file):
    v = Validator(input_file)
    print 'Validating ' + input_file + '...'
    validation = v.validate()
    output = ValidationOutputFormatter()
    # output.output_stdout_old(validation)
    output.output_stdout(validation)


def version():
    print 'html5validator v' + VERSION
    print 'Copyright (C) Erik Sørensen, 2015. All rights reserved.'
    usage()


def usage():
    print 'Usage: html5validator.py file'


if (__name__ == '__main__'):
    main(sys.argv[1:])
