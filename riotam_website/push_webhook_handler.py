#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import hashlib
import hmac
import json
import logging
import os
import sys
from subprocess import Popen, PIPE, STDOUT

from config import config

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, ".."))

LOGFILE = os.path.join(PROJECT_ROOT_DIR, "log", "push_webhook_handler_log.txt")


#enum
class PushedRepo:
    Website, Backend = range(2)


def main():

    request_body = sys.stdin.read()
    is_valid = is_valid_signature(os.environ["HTTP_X_HUB_SIGNATURE"], config.GITHUB_SECRET_KEY, request_body)

    json_message = json.loads(request_body)
    repo_name = json_message["repository"]["full_name"]

    if is_valid:
        repo_to_update = get_repo_type(repo_name)

        if repo_to_update == PushedRepo.Website:
            update_website()

        elif repo_to_update == PushedRepo.Backend:
            update_backend()

        else:
            print_error()
            logging.error("script called by unconfigured repository " + repo_name)
            return

        print_result("webhook handled successfully")

    else:
        print_error()


def execute_command(cmd, cwd=None):
    """
    Execute command with Popen

    Parameters
    ----------
    cmd: array_like
        List of strings of the command to execute. Needs to be split on spaces
    cwd: string
        working directory to change to (default is None)

    Returns
    -------
    string
        Commandline output

    """

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd=cwd)
    return process.communicate()[0]


def update_website():
    """
    Update git repository of frontend (website)

    """
    output = execute_command(["git", "-C", PATH_RIOTAM_WEBSITE, "pull"])
    logging.debug("PULL WEBSITE REPO:\n" + output)


def update_backend():
    """
    Update git repository of backend and run some scripts to update database or the backend itself

    """
    wd = os.path.normpath(os.path.join(PATH_RIOTAM_WEBSITE, "..", "riotam-backend", "riotam_backend"))
    output = execute_command(["python", "push_webhook_handler.py"], cwd=wd)
    logging.debug(output)


def get_repo_type(name):
    """
    Determine repository type by name

    Parameters
    ----------
    name: string
        Name of the repository

    Returns
    -------
    PushedRepo
        Recognized repository type, None if nothing has matched

    """
    if name.endswith("riotam-website"):
        return PushedRepo.Website

    elif name.endswith("riotam-backend"):
        return PushedRepo.Backend

    else:
        return None


def is_valid_signature(signature, secret_key, body):

    #https://developer.github.com/v3/repos/hooks/#create-a-hook
    #https://stackoverflow.com/questions/28228392/failed-to-verify-github-x-hub-signature-in-my-application
    computed_signature = "sha1=" + hmac.new(secret_key, body, hashlib.sha1).hexdigest()

    return computed_signature == signature


def print_result(result):

    print ("Content-Type: text/html")
    print ("\n\r")
    print (result)


def print_error():

    print ("Status: 403 Forbidden")
    print ("\n\r")


if __name__ == "__main__":

    logging.basicConfig(filename=LOGFILE, format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)