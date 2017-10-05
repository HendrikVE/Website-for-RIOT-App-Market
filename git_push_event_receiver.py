#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import hashlib
import hmac
import random
import logging

import os
import cgi

import sys

cgi.print_arguments()
cgi.print_environ_usage()


def main():

    print_result("git event handling successfull")

    logging.debug(str(random.randint(0, 9999)) + ": " + str(os.environ["HTTP_X_HUB_SIGNATURE"]))

    secret_key = "riotam"
    request_body = sys.stdin.read()

    is_valid = is_valid_signature(os.environ["HTTP_X_HUB_SIGNATURE"], secret_key, request_body)
    logging.debug("is valid: " + str(is_valid))


def is_valid_signature(signature, secret_key, body):

    #https://stackoverflow.com/questions/28228392/failed-to-verify-github-x-hub-signature-in-my-application
    computed_signature = 'sha1=' + hmac.new(secret_key, body, hashlib.sha1).hexdigest()

    return computed_signature == signature


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