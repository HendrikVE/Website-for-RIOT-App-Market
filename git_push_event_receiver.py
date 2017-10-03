#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import random
import logging
import cgitb

cgitb.enable()

print ("Status: 403 Forbidden")
print ("\n\r")

logging.basicConfig(filename="log/git_push_event_receiver_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

logging.debug(random.randint(0, 9999))
