#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi, cgitb
import os
from subprocess import Popen, PIPE
	
def main():

    cgitb.enable()

    print "Content-Type: text/html"
    print "\n\r"

    form = cgi.FieldStorage()

    application = form.getfirst("application")
    device = form.getfirst("device")
    
    os.chdir("../riotam-backend/")
    proc = Popen(["python", "build_example.py", "--application " + application + " --device " + device], stdout=PIPE)
    output = proc.communicate()[0]
    print output
	
if __name__ == "__main__":
    
    main()