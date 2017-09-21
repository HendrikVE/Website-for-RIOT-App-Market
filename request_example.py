#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import cgi, cgitb
from subprocess import Popen, PIPE, STDOUT
import os
import logging
import json

build_result = {
    "cmd_output": ""
}


def main():

    cgitb.enable()

    form = cgi.FieldStorage()

    application = form.getfirst("application")
    board = form.getfirst("board")

    if not all([application, board]):
        print_error()
        """build_result["cmd_output"] = "missing parameters for request!"
        build_result["cmd_output"] += "application = " + str(application)
        build_result["cmd_output"] += "board = " + str(board)
        print_result(json.dumps(build_result))"""
        return

    os.chdir("../riotam-backend/")
    proc = Popen(["python build_example.py --application " + application + " --board " + board], stdout=PIPE, stderr=STDOUT, shell=True)
    output = proc.communicate()[0]

    json_message = json.loads(output)
    json_message["cmd_output"] = json_message["cmd_output"].replace("\n", "<br>")

    print_result(json.dumps(json_message))


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
