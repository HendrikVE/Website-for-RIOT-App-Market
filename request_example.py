#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi, cgitb
from subprocess import Popen, PIPE, STDOUT
import os
import logging
import json

build_result = {
    "cmd_output": "",
    "board": None,
    "application_name": "application",
    "output_file": None,
    "output_file_extension": None,
    "output_archive": None,
    "output_archive_extension": None
}


def main():

    cgitb.enable()

    form = cgi.FieldStorage()

    application = form.getfirst("application")
    board = form.getfirst("board")

    if all(v is not None for v in [application, board]):
        build_result["cmd_output"] = "missing parameters for request!"
        build_result["cmd_output"] += "application = " + str(application)
        build_result["cmd_output"] += "board = " + str(board)
        print_result(json.dumps(build_result))
        return

    os.chdir("../riotam-backend/")
    proc = Popen(["python build_example.py --application " + application + " --board " + board], stdout=PIPE, stderr=STDOUT, shell=True)
    output = proc.communicate()[0]

    print_result(output)


def print_result(result):

    print "Content-Type: text/html"
    print "\n\r"
    print result


if __name__ == "__main__":

    logging.basicConfig(filename="log/request_example_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        build_result["cmd_output"] = "Something really bad happened on server side: " + str(e)

        print_result(json.dumps(build_result))
