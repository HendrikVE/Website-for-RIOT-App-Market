#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import db_config as config
import MySQLdb

def main():
	
	cgitb.enable()

	print 'Content-Type: text/html'
	print '\n\r'

	print '<!DOCTYPE html>'
	print '<html>'
	print '<head>'
	print '<meta charset=""utf-8"">'
	print '<meta name="viewport" content="width=device-width, initial-scale=1">'
	print '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
	print '<link rel="stylesheet" type="text/css" href="/css/custom.css" />'
	print '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>'
	print '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>'
	print '<script src="main.js"></script>'
	print '<title>RIOT OS App Market</title>'
	print '<!-- Origin Trial Token, feature = WebUSB (For Chrome M57+), origin = https://www.vanappsteer.de, expires = 2017-09-05 -->'
	print '<meta http-equiv="origin-trial" data-feature="WebUSB (For Chrome M57+)" data-expires="2017-09-05" content="AkyHUtyQc2+ctDNdGbCJpuTTdTmkZM1U0cxMhvwvgkGdfX4vB28BwYm/8Z3OJTVfGD1r8OIiS7QwazYx97rZ1QIAAABTeyJvcmlnaW4iOiJodHRwczovL3d3dy52YW5hcHBzdGVlci5kZTo0NDMiLCJmZWF0dXJlIjoiV2ViVVNCMiIsImV4cGlyeSI6MTUwNDU2OTYwMH0=">'
	print '</head>'
	print
	print '<body>'
	print '<div class="container">'

	# print '<button type="button" id="selectButton" onclick="selectDevice()">Select Device</button>'

	# print '<p><div id="deviceInfo" style="white-space: pre"></div></p>'

	# print '<div id="downloadSection" style="visibility: hidden;">'
	
	print_jumbotron()
	
	print_device_selector()
	
	print_checkboxes()

	print '<br><button type="button" id="downloadButton" onclick="download()">Download your personal RIOT OS</button>'
	# print '</div>'
	print '<div id="demo">NULL</div>'

	print '</div></body></html>'
	
def print_jumbotron():
	
	print '<div class="jumbotron">'
	print '<h1>RIOT AppMarket</h1>'
	print '<p>Let us compile your custom RIOT OS</p>'
	print '</div>'
	
def print_checkboxes():
	
	db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

	# cursor object to execute queries
	db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

	db_cursor.execute("SELECT * FROM modules ORDER BY group_identifier")
	results = db_cursor.fetchall()
	
	string_to_fill = '<li><label><input type="checkbox" name="module_checkbox" value="{!s}">{!s}</label></li>'
	
	print '<form><h3>Select modules:</h3>'
	
	last_group_identifier = None
	group_left_open = False
	
	for row in results:
		
		group_identifier_changed = last_group_identifier != row["group_identifier"]
		if last_group_identifier == None or group_identifier_changed:
			
			if group_left_open:
				print '</ul></fieldset>'
			
			# open new group
			print '<fieldset><legend>' + row["group_identifier"] + '</legend><ul>'
			group_left_open = True
			
		last_group_identifier = row["group_identifier"]
		
		print string_to_fill.format(row["id"], row["name"])

	if group_left_open:
		print '</ul></fieldset>'
		
	print '</form>'
		
	db_cursor.close()
	db.close()
	
def print_device_selector():
	
	db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

	# cursor object to execute queries
	db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	
	db_cursor.execute("SELECT * FROM devices ORDER BY display_name")
	results = db_cursor.fetchall()
	
	print '<form>'
	print '<div class="form-group">'
	print '<label for="device_selector">Select a device:</label>'
	print '<select class="form-control" id="device_selector">'
	
	for row in results:
		print '<option value="{!s}">{!s}</option>'.format(row["internal_name"], row["display_name"])
		
	print '</select></div></form>'
	
	db_cursor.close()
	db.close()
	
if __name__ == "__main__":
	main()