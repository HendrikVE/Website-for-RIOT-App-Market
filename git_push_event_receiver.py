#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import hashlib
import hmac
import json
import logging
import os
import subprocess
import sys


#enum
class PushedRepo:
    Website, Backend = range(2)


PATH_RIOTAM_BACKEND = "/var/www/riotam-backend"
PATH_RIOTAM_WEBSITE = "/var/www/riotam-website"


def main():

    secret_key = "riotam"
    request_body = sys.stdin.read()
    is_valid = is_valid_signature(os.environ["HTTP_X_HUB_SIGNATURE"], secret_key, request_body)

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

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    return process.communicate()[0]


def update_website():
    output = execute_command(["git", "-C", PATH_RIOTAM_WEBSITE, "pull"])
    logging.debug("PULL WEBSITE REPO:\n" + output)


def update_backend():
    output = execute_command(["git", "-C", PATH_RIOTAM_BACKEND, "pull"])
    logging.debug("PULL BACKEND REPO:\n" + output)

    output = execute_command(["python", "db_update.py"], PATH_RIOTAM_BACKEND)
    logging.debug("DB_UPDATE:\n" + output)

    output = execute_command(["python", "strip_riot_repo.py"], PATH_RIOTAM_BACKEND)
    logging.debug("STRIP_RIOT_REPO.py:\n" + output)


def get_repo_type(name):

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

    logging.basicConfig(filename="log/git_push_event_receiver_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)