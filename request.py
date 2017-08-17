#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi, cgitb

cgitb.enable()

print "Content-Type: text/html"
print "\n\r"

form = cgi.FieldStorage()

selected_modules = form.getlist("selected_modules")

for module in selected_modules:
	print module