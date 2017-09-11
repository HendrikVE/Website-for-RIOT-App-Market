#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, cgi
import config.db_config as config
import MySQLdb
#import logging

def main():
    
    cgitb.enable()
    
    #logging.basicConfig(filename = "log/index_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    print 'Content-Type: text/html'
    print '\n\r'
    
    print '<!DOCTYPE html>'
    print '<html lang="en">'
    
    print_html_header()
    
    print '<body>'

    # print '<button type="button" id="selectButton" onclick="selectDevice()">Select Device</button>'

    # print '<p><div id="deviceInfo" style="white-space: pre"></div></p>'
    
    print_header()
    
    print '<div class="container">'
    print_tabs()
    print '</div>'
    
    print_footer()
    
    print '</body></html>'
    
def print_html_header():
    
    print 
    print """
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <link rel="stylesheet" href="/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="/css/custom.css" />
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="/js/bootstrap.min.js"></script>

        <script src="/js/main.js"></script>
        <title>RIOT OS App Market</title>
        <!-- Origin Trial Token, feature = WebUSB (For Chrome M57+), origin = https://www.vanappsteer.de, expires = 2017-09-05 -->
        <meta http-equiv="origin-trial" data-feature="WebUSB (For Chrome M57+)" data-expires="2017-09-05" content="AkyHUtyQc2+ctDNdGbCJpuTTdTmkZM1U0cxMhvwvgkGdfX4vB28BwYm/8Z3OJTVfGD1r8OIiS7QwazYx97rZ1QIAAABTeyJvcmlnaW4iOiJodHRwczovL3d3dy52YW5hcHBzdGVlci5kZTo0NDMiLCJmZWF0dXJlIjoiV2ViVVNCMiIsImV4cGlyeSI6MTUwNDU2OTYwMH0=">
        </head>
    """
    print 
    
def print_header():
    
    print """
        <div class="jumbotron">
            <div class="container">
                <div class="row">

                    <div class="col-sm-8">
                        <h1>RIOT OS AppMarket</h1>
                        <p>Let us build your custom RIOT OS according to your needs</p>
                    </div>

                    <div class="col-sm-4">
                        <img src="/img/riot_logo.png" alt="RIOT logo" height="200" width="200"></img>
                    </div>

                </div>
            </div>
        </div>
    """
    
def print_tabs():
    
    print '<ul class="nav nav-tabs">'
    print '<li class="active"><a data-toggle="tab" href="#tab0">Example applications</a></li>'
    print '<li><a data-toggle="tab" href="#tab1">Your custom RIOT OS</a></li>'
    print '</ul>'
    
    print '<div class="tab-content">'
    
    print '<div id="tab0" class="tab-pane fade in active">'
    print_examples_tab()
    print '</div>'
    
    print '<div id="tab1" class="tab-pane fade">'
    print_custom_tab()
    print '</div>'
    
    print '</div>'
    
def print_custom_tab():
    
    print_device_selector()
    
    print_file_upload()
    
    print_checkboxes()

    print '<h3>4. Build and flash:</h3>'
    
    print '<div class="container-fluid">'
    print '<button type="button" class="btn" id="downloadButton" onclick="download()">Compile your personal RIOT OS</button>'
    print '<div class="well" id="cmdOutput">'
    
    print '<div class="progress">'
    print '<div class="progress-bar progress-bar-striped active" id="progressBar" style="width:100%; visibility:hidden">'
    print '</div></div>'
    
    print '</div>'
    print '</div>'
    
def print_examples_tab():
    
    print_device_selector()
    
    print_applications()
    
# https://www.abeautifulsite.net/whipping-file-inputs-into-shape-with-bootstrap-3
def print_file_upload():
    
    print '<h3>2. Upload your main.c:</h3>'
    print '<div class="container-fluid">'
    print """
        <div class="col-lg-6 col-sm-6 col-12">
            <div class="input-group">
                <label class="input-group-btn">
                    <span class="btn btn-default">
                        Browse&hellip; <input type="file" style="display: none;" multiple>
                    </span>
                </label>
                <input type="text" class="form-control" readonly>
            </div>
        </div>
        """
    print '</div>'
    
def print_device_selector():
    
    db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

    # cursor object to execute queries
    db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    db_cursor.execute("SELECT * FROM devices ORDER BY display_name")
    results = db_cursor.fetchall()
    
    print '<label for="device_selector"><h3>1. Select a device:</h3></label>'
    print '<div class="row">'
    
    print '<div class="col-md-10">'
    print '<form>'
    print '<div class="form-group">'
    print '<div class="container-fluid">'
    print '<select class="form-control" id="device_selector">'
    
    for row in results:
        print '<option value="{!s}">{!s}</option>'.format(row["internal_name"], row["display_name"])
        
    print '</select></div></form></div>'
    
    db_cursor.close()
    db.close()
    print '</div>'
    
    print '<div class="col-md-2">'
    print '<button type="button" class="btn" id="autodetectButton" onclick="autodetect()">Try autodetect</button>'
    print '</div>'
    
    print '</div>'
    
def print_checkboxes():
    
    db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

    # cursor object to execute queries
    db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    db_cursor.execute("SELECT * FROM modules ORDER BY group_identifier ASC, name ASC")
    results = db_cursor.fetchall()
    
    # width should add up to 12 per row (bootstrap grid system)
    column_width = 3
    current_width_taken = 0
    
    string_to_fill = '<div class="col-md-' + str(column_width) + '"><label><input type="checkbox" name="module_checkbox" value="{!s}"><div data-toggle="tooltip" data-placement="bottom" title="{!s}">{!s}</div></label></div>'
    
    print '<form>'
    print '<label for="checkboxes_container"><h3>3. Select modules:</h3></label>'
    print '<div class="container-fluid" id="checkboxes_container">'
    
    last_group_identifier = None
    group_left_open = False
    row_left_open = False
    new_row = True
    
    for row in results:
        
        group_identifier_changed = last_group_identifier != row["group_identifier"]
        if last_group_identifier == None or group_identifier_changed:
            
            if group_left_open:
                # close group
                print '</div>'
                
            if row_left_open:
                current_width_taken = 0
                new_row = True
                
                # close row
                print '</div>'
                row_left_open = False
            
            # open new group
            print '<div class="checkbox well"><h4>' + row["group_identifier"] + '</h4>'
            group_left_open = True
        
        if new_row:
            
            if last_group_identifier != None and not group_identifier_changed:
                # close the current row. if last_group_identifier is None, there was no row before
                print '</div>'
                
            # open new row
            print '<div class="row">'
            row_left_open = True
            
            current_width_taken = 0
            new_row = False
        
        description = row["description"]
        if description is None:
            description = ""
        
        print string_to_fill.format(row["id"], cgi.escape(description, True), row["name"])
        
        current_width_taken += column_width
        new_row = current_width_taken >= 12
        last_group_identifier = row["group_identifier"]

    if row_left_open:
        print '</div>'
        
    if group_left_open:
        print '</div>'
        
    # close the container
    print '</div>'
    
    print '</form>'
        
    db_cursor.close()
    db.close()
    
def print_applications():
    
    db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

    # cursor object to execute queries
    db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    
    db_cursor.execute("SELECT * FROM applications ORDER BY name")
    results = db_cursor.fetchall()
    
    # width should add up to 12 per row (bootstrap grid system)
    column_width = 3
    current_width_taken = 0
    
    string_to_fill = '<div class="col-md-' + str(column_width) + '"><p><button type="button" class="btn btn-block" id="{!s}" onclick="download()"><div data-toggle="tooltip" data-placement="bottom" title="{!s}">{!s}</div></button></p></div>'
    
    print '<label for="applications_container"><h3>2. Select an application:</h3></label>'
    print '<div class="container-fluid" id="applications_container">'
    
    row_left_open = False
    new_row = True
    
    for row in results:
        
        if new_row:
            
            if row_left_open:
                print '</div>'
                
            # open new row
            print '<div class="row">'
            row_left_open = True
            
            current_width_taken = 0
            new_row = False
        
        description = row["description"]
        if description is None:
            description = ""
        
        print string_to_fill.format(row["id"], cgi.escape(description, True), row["name"])
        
        current_width_taken += column_width
        new_row = current_width_taken >= 12

    if row_left_open:
        print '</div>'
        
    # close the container
    print '</div>'
    
def print_footer():
    
    print '<footer class="footer">'
    print '<div class="container">'
    print '<div class="row">'
    print '<div class="col-sm-8">&copy; Hendrik van Essen, 2017</div>'
    print '<div class="col-sm-4"><a href="https://github.com/RIOT-OS/RIOT"><img src="/img/riot_logo_footer.png" alt="RIOT logo" height="44" width="81"></img></a></div>'
    print '</div>'
    print '</div>'
    print '</footer>'
    
if __name__ == "__main__":
    main()