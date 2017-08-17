#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi, cgitb
import db_config as config
import MySQLdb
import os
import sys
import subprocess
	
def main():
	
	cgitb.enable()

	print "Content-Type: text/html"
	print "\n\r"

	form = cgi.FieldStorage()

	selected_modules = form.getlist("selected_modules")

	for module in selected_modules:
		print module

	os.chdir("../riotam-backend/")
	build_script = subprocess.check_output([sys.executable, "build.py", "here is build.py"])
	
	print build_script

if __name__ == "__main__":
	main()