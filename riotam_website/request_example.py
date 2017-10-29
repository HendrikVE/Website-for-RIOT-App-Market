#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import print_function

import ast
import cgi
import json
import logging
from subprocess import Popen, PIPE, STDOUT

import os

from config import config

build_result = {
    "cmd_output": ""
}

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))

LOGFILE = os.path.join(PROJECT_ROOT_DIR, "log", "request_example.log")


def main():

    form = cgi.FieldStorage()

    application = form.getfirst("application")
    board = form.getfirst("board")

    if not all([application, board]):
        print_error()
        return

    cmd = ["python", "build_example.py",
           "--application", application,
           "--board", board,
           "--caching"]

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd="../../riotam-backend/riotam_backend")
    output = process.communicate()[0]

    # convert string representation of dictionary to "real" dictionary
    build_result = ast.literal_eval(output)
    build_result["cmd_output"] = build_result["cmd_output"].replace("\n", "<br>")

    print_result(json.dumps(build_result))


def print_result(result):

    print ("Content-Type: text/html")
    print ("\n\r")
    print (result)


def print_error():

    print ("Status: 400 Bad Request")
    print ()


if __name__ == "__main__":

    logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        build_result["cmd_output"] = "Something really bad happened on server side: " + str(e)

        print_result(json.dumps(build_result))
