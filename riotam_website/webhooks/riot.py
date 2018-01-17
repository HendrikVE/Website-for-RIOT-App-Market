#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *                    Gaëtan Harter <gaetan.harter@fu-berlin.de
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import print_function

import os
import sys
import logging
import subprocess

# I have issue to import 'config' as its not a package
sys.path.append('../')
from config import config
from webhooks import common

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.join(CUR_DIR, os.pardir, os.pardir)

BACKEND_DIR = os.path.join(PROJECT_ROOT_DIR, os.pardir,
                           'riotam-backend', 'riotam_backend')
LOGFILE = os.path.join(PROJECT_ROOT_DIR, 'log', 'webhook_riot.log')


def _process_update_request(request_body):
    """Verify body signature and update backend if valid."""

    try:
        request_sig = os.environ.get('HTTP_X_HUB_SIGNATURE', '')
        secret_key = config.GITHUB_SECRET_KEY
        common.check_github_signature(request_sig, request_body, secret_key)

        update_backend(BACKEND_DIR)

        return common.http_result('webhook handled successfully')
    except ValueError:
        return common.http_forbidden()


def update_backend(backend_dir):
    """Update backend repositories, database and scripts."""
    cmd = ['python', 'push_webhook_handler.py']

    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                     cwd=backend_dir)
    logging.debug(output)


def main():
    request_body = sys.stdin.read()
    http_ret = _process_update_request(request_body)
    print(http_ret)


if __name__ == "__main__":

    logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()
    except Exception as err:
        logging.error(str(err), exc_info=True)
        exit(1)
