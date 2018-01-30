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
import hmac
import hashlib


def github_signature(body, key):
    """Compute github signature for body."""

    # https://developer.github.com/v3/repos/hooks/#create-a-hook
    # https://stackoverflow.com/questions/28228392/failed-to-verify-github-x-hub-signature-in-my-application

    sha1_sig = hmac.new(key, body, hashlib.sha1).hexdigest()
    return 'sha1={sha1}'.format(sha1=sha1_sig)


def check_github_signature(signature, body, key):
    """Verify github signature is correct."""

    sig = github_signature(body, key)
    if signature != sig:
        raise ValueError('Invalid Signature')


def http_forbidden():
    return ('Status: 403 Forbidden\n'
            '\n\r')


def http_result(result):
    return ('Content-Type: text/html\n'
            '\n\r'
            '%s') % result
