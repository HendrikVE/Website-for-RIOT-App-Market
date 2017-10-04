#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import random
import logging

import os


def main():

    print_result("git event handling successfull")

    logging.debug(str(random.randint(0, 9999)) + ": " + str(os.environ["X-Hub-Signature"]))


def print_result(result):

    print ("Content-Type: text/html")
    print ("\n\r")
    print (result)


def print_error():

    print ("Status: 403 Forbidden")
    print ("\n\r")


if __name__ == "__main__":

    logging.basicConfig(filename="log/git_push_event_receiver_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)