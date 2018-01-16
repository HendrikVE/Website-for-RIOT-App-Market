#!/usr/bin/env python

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

db_config = {
    "host": "localhost",
    "user": "riotam_website",
    "passwd": "PASSWORD_WEBSITE",
    "db": "riot_os"
}

GITHUB_SECRET_KEY = "YOUR_SECRET_KEY"

LOGGING_FORMAT = "[%(levelname)s]: %(asctime)s\n"\
                 + "in %(filename)s in %(funcName)s on line %(lineno)d\n"\
                 + "%(message)s\n\n"
