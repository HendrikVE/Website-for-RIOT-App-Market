#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import db_config as config
import MySQLdb

def main():
	
	cgitb.enable()

	print "Content-Type: text/html"
	print "\n\r"

	print "<!DOCTYPE html>"
	print "<html>"
	print "<head>"
	print "<title>RIOT OS App Market</title>"
	print "<link rel=""stylesheet"" href=""styles.css"">"
	print "<!-- Origin Trial Token, feature = WebUSB (For Chrome M57+), origin = https://www.vanappsteer.de, expires = 2017-08-23 -->"
	print "<meta http-equiv=""origin-trial"" data-feature=""WebUSB (For Chrome M57+)"" data-expires=""2017-08-23"" content=""AuMsLNMamUdtrJmHYTJ+0qNNi3rEKeAfbeQcVT8ZvAcdz9QJHhHk9l4kHIAPaHsMEkOGLGBYsfDOCL8BBkocHgEAAABTeyJvcmlnaW4iOiJodHRwczovL3d3dy52YW5hcHBzdGVlci5kZTo0NDMiLCJmZWF0dXJlIjoiV2ViVVNCMiIsImV4cGlyeSI6MTUwMzUxNzQxMX0="">"
	print "</head>"
	print
	print "<body>"

	print "<button type=""button"" id=""selectButton"" onclick=""selectDevice()"">Select Device</button>"

	print "<p><div id=""deviceInfo"" style=""white-space: pre""></div></p>"

	print "<div id=""downloadSection"" style=""visibility: hidden;"">"
	
	print_checkboxes()

	print "<br><button type=""button"" id=""downloadButton"" onclick=""download()"">Download your personal RIOT OS</button></div><script src=""main.js""></script>"

	print "</body>"
	print "</html>"

def print_checkboxes():
	
	db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

	# cursor object to execute queries
	db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

	db_cursor.execute("SELECT * FROM modules ORDER BY group_identifier")
	results = db_cursor.fetchall()
	
	string_to_fill = "<li><label><input type=""checkbox"" name=""{!s}"" value=""{!s}"">{!s}</label></li>"

	print "<form><h3>Select modules:</h3><fieldset>"
	
	last_group_identifier = None
	group_left_open = False
	
	for row in results:
		
		group_identifier_changed = last_group_identifier != row["group_identifier"]
		if last_group_identifier == None or group_identifier_changed:
			
			if group_left_open:
				print "</ul>"
			
			# open new group
			print "<p>" + row["group_identifier"] + "</p><ul>"
			group_left_open = True
			
		last_group_identifier = row["group_identifier"]
		
		print string_to_fill.format(row["group_identifier"], row["id"], row["name"])

	if group_left_open:
		print "</ul>"
		
	print "</fieldset></form>"
		
	db_cursor.close()
	db.close()
	
if __name__ == '__main__':
	main()