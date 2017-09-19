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

    selected_modules = form.getlist("selected_modules[]")
    board = form.getfirst("board")
    main_file_content = form.getfirst("main_file_content")

    if not all([selected_modules, board, main_file_content]):
        print_error()
        """build_result["cmd_output"] = "missing parameters for request!<br>"
        build_result["cmd_output"] += "selected_modules = {}<br>".format(str(selected_modules))
        build_result["cmd_output"] += "board = {}<br>".format(str(board))
        build_result["cmd_output"] += "main_file_content = {}<br>".format(str(main_file_content))
        print_result(json.dumps(build_result))"""
        return

    argument_modules = ["--modules"]
    for module in selected_modules:
        argument_modules.append(" " + module)

    arguments = "".join(argument_modules) + " " + "--board " + board

    os.chdir("../riotam-backend/")
    proc = Popen(["python build.py " + arguments], stdout=PIPE, stderr=STDOUT, shell=True)
    output = proc.communicate()[0]

    print_result(output)


def print_result(result):

    print ("Content-Type: text/html")
    print ("\n\r")
    print (result)


def print_error():

    print ("Status: 403 Forbidden")
    print ("\n\r")


if __name__ == "__main__":

    logging.basicConfig(filename="log/request_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        build_result["cmd_output"] = "Something really bad happened on server side: " + str(e)

        print_result(json.dumps(build_result))
