#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

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

    cmd = ["python", "build.py"]

    cmd.append("--modules")
    for module in selected_modules:
        cmd.append(module)

    cmd.append("--board")
    cmd.append(board)

    cmd.append("--mainfile")
    cmd.append(main_file_content)

    logging.debug(main_file_content)

    os.chdir("../riotam-backend/")
    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    output = process.communicate()[0]

    json_message = json.loads(output)
    json_message["cmd_output"] = json_message["cmd_output"].replace("\n", "<br>")

    print_result(json.dumps(json_message))


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
