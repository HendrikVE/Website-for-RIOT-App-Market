#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import ast
import cgi
from subprocess import Popen, PIPE, STDOUT
import os
import logging
import json

build_result = {
    "cmd_output": ""
}


def main():

    form = cgi.FieldStorage()

    application = form.getfirst("application")
    board = form.getfirst("board")

    if not all([application, board]):
        print_error()
        return

    cmd = ["python", "build_example.py",
           "--application", application,
           "--board", board]

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd="../riotam-backend/riotam_backend")
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

    logging.basicConfig(filename="log/request_example_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        build_result["cmd_output"] = "Something really bad happened on server side: " + str(e)

        print_result(json.dumps(build_result))
