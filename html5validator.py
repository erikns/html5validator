#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import json


VERSION = '1.1.1'


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

        num_info = 0
        num_warning = 0
        num_error = 0
        out_lines = []

        for message in messages:
            if message['type'] == 'info':
                out_lines.append(self.__wrap_color(bcolors.OKGREEN, 'I ' + message['message']))
                num_info += 1
            elif message['type'] == 'warning':
                out_lines.append(self.__wrap_color(bcolors.WARNING, 'W' + message['message']))
                num_warning += 1
            elif message['type'] == 'error':
                out_lines.append(self.__wrap_color(bcolors.FAIL, 'E ' + message['message']))
                num_error += 1

        print ''

        if (num_error == 0) and (num_warning == 0):
            print self.__wrap_color(bcolors.OKGREEN, 'Validation OK')
        elif (num_error == 0) and (num_warning > 0):
            print self.__wrap_color(bcolors.WARNING, 'Validation OK with warnings')
        else:
            print self.__wrap_color(bcolors.FAIL, 'Validation FAILED')

        print str(num_error) + ' errors, ' + str(num_warning) + ' warnings, ' + str(num_info) + ' info'
        print 'Issues:'
        for line in out_lines:
            print line

    def __wrap_color(self, color, message):
        return (color + message + bcolors.ENDC)


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
    output.output_stdout(validation)


def version():
    print 'html5validator v' + VERSION
    print 'Copyright (C) Erik Sørensen, 2015. All rights reserved.'
    usage()


def usage():
    print 'Usage: html5validator.py file'


if (__name__ == '__main__'):
    main(sys.argv[1:])
