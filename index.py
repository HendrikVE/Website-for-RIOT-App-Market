#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb, cgi
import config.db_config as config
import MySQLdb
import textwrap
import logging

db = None
db_cursor = None


def main():
    
    cgitb.enable()
    init_db()
    
    print 'Content-Type: text/html'
    print '\n\r'
    
    print textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">

            {HTML_HEADER}

            <body>

                {HEADER}

                <div class="container">
                {TABS}
                </div>

                {FOOTER}

            </body>
        </html>
    """.format(HTML_HEADER=html_header(),
              HEADER=header(),
              TABS=tabs(),
              FOOTER=footer()))
    
    close_db()


def init_db():
    
    global db
    db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

    # cursor object to execute queries
    global db_cursor
    db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)


def close_db():
    db_cursor.close()
    db.close()


def html_header():
    
    return textwrap.dedent("""
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
    """)


def header():
    
    return textwrap.dedent("""
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
    """)


def tabs():
    
    return textwrap.dedent("""
        <ul class="nav nav-tabs">
            <li class="active"><a data-toggle="tab" href="#tab0">Example applications</a></li>
            <li><a data-toggle="tab" href="#tab1">Your custom RIOT OS</a></li>
        </ul>

        <div class="tab-content">
            <div id="tab0" class="tab-pane fade in active">
                {EXAMPLE_TAB}
            </div>
            
            <div id="tab1" class="tab-pane fade">
                {CUSTOM_TAB}
            </div>
            
        </div>
    """.format(EXAMPLE_TAB=examples_tab(),
               CUSTOM_TAB=custom_tab()))


def custom_tab():

    return textwrap.dedent("""
        {DEVICE_SELECTOR}
        {FILE_UPLOAD}
        {CHECKBOXES}
        <h3>4. Build and flash:</h3>
        <div class="container-fluid">
            <button type="button" class="btn" id="downloadButton" onclick="download()">Compile your personal RIOT OS</button>
            <div class="well" id="cmdOutputCustomTab">
                <div class="progress">
                    <div class="progress-bar progress-bar-striped active" id="progressBarCustomTab" style="width:100%; visibility:hidden"></div>
                </div>
            </div>
        </div>
    """.format(DEVICE_SELECTOR=device_selector("deviceSelectorCustomTab"),
               FILE_UPLOAD=file_upload(),
               CHECKBOXES=checkboxes()))


def examples_tab():
    
    return textwrap.dedent("""
        {DEVICE_SELECTOR}
        {APPLICATIONS}
        <div class="well" id="cmdOutputExamplesTab">
            <div class="progress">
                <div class="progress-bar progress-bar-striped active" id="progressBarExamplesTab" style="width:100%; visibility:hidden"></div>
            </div>
        </div>
    """.format(DEVICE_SELECTOR=device_selector("deviceSelectorExamplesTab"),
              APPLICATIONS=applications()))


# https://www.abeautifulsite.net/whipping-file-inputs-into-shape-with-bootstrap-3
def file_upload():
    
    return textwrap.dedent("""
        <h3>2. Upload your main class file:</h3>
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-6 col-sm-6 col-12">
                    <div class="input-group">
                        <label class="input-group-btn">
                            <span class="btn btn-default">
                                Browse&hellip; <input id="mainFileInput" type="file" style="display: none;">
                            </span>
                        </label>
                        <input type="text" class="form-control" readonly>
                    </div>
                </div>
            </div>
        </div>
    """)


def device_selector(id):
    
    def get_devices():
        
        db_cursor.execute("SELECT * FROM devices ORDER BY display_name")
        return db_cursor.fetchall()
    
    selector_options = ""
    for device in get_devices():
        selector_options += '<option value="{!s}">{!s}</option>'.format(device["internal_name"], device["display_name"])
    
    return textwrap.dedent("""
        <label for="{ID}"><h3>1. Select a device:</h3></label>
        <div class="row">

            <div class="col-md-10">
                <form>
                    <div class="form-group">
                        <div class="container-fluid">
                            <select class="form-control" id="{ID}">
                                {SELECTOR_OPTIONS}
                            </select>
                        </div>
                    </form>
                </div>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-block" id="autodetectButton" onclick="autodetect()">Try autodetect</button>
            </div>
        </div>
    """.format(ID=id, SELECTOR_OPTIONS=selector_options))


def slices(input_list, group_size):
    return [input_list[x:x + group_size] for x in xrange(0, len(input_list), group_size)]


def checkboxes():
    
    def get_checkboxes():
        
        db_cursor.execute("SELECT * FROM modules ORDER BY group_identifier ASC, name ASC")
        return db_cursor.fetchall()
    
    elements_per_row = 4
    # width should add up to 12 per row (bootstrap grid system)
    column_width = int(12 / elements_per_row)
    
    row_template = textwrap.dedent("""
        <div class="row">
            {COLUMNS}
        </div>
    """)
    
    column_template = textwrap.dedent("""
        <div class="col-md-""" + str(column_width) + """">
            <label>
                <input type="checkbox" name="module_checkbox" value="{!s}">
                <div data-toggle="tooltip" data-placement="bottom" title="{!s}">{!s}</div>
            </label>
        </div>
    """)
    
    checkboxes_html = ""
    
    checkboxes = list(get_checkboxes())
    
    checkbox_groups = {}
    
    while len(checkboxes) > 0:
        checkbox = checkboxes.pop(0)
        group = checkbox["group_identifier"]
        
        dict_entry = checkbox_groups.get(group, None)
        if dict_entry is None:
            checkbox_groups[group] = [checkbox]
        else:
            dict_entry.append(checkbox)
            
    for group in sorted(checkbox_groups):
        
        checkboxes_html += '<div class="checkbox well"><h4>' + group + '</h4>'
        
        grouped_checkboxes_slices = slices(checkbox_groups.get(group), elements_per_row)
        
        for grouped_checkboxes in grouped_checkboxes_slices:

            columns = ""
            for checkbox in grouped_checkboxes:

                description = checkbox["description"]
                if description is None:
                    description = ""

                columns += column_template.format(checkbox["id"], cgi.escape(description, True), checkbox["name"])

            checkboxes_html += row_template.format(COLUMNS=columns)
            
        checkboxes_html += '</div>'
    
    return textwrap.dedent("""
        <form>
            <label for="checkboxes_container"><h3>3. Select modules:</h3></label>
            <div class="container-fluid" id="checkboxes_container">
                {ROWS}
            </div>
        </form>
    """.format(ROWS=checkboxes_html))


def applications():
    
    def get_applications():
        
        db_cursor.execute("SELECT * FROM applications ORDER BY name")
        return db_cursor.fetchall()
    
    elements_per_row = 4
    # width should add up to 12 per row (bootstrap grid system)
    column_width = int(12 / elements_per_row)
    
    row_template = textwrap.dedent("""
        <div class="row">
            {COLUMNS}
        </div>
    """)
    
    column_template = textwrap.dedent("""
        <div class="col-md-""" + str(column_width) + """">
            <p>
                <button type="button" class="btn btn-block example-application-button" id="{}" onclick="download_example(this.id)">
                    <div data-toggle="tooltip" data-placement="bottom" title="{}">{}</div>
                </button>
            </p>
        </div>
    """)
    
    grouped_applications_slices = slices(get_applications(), elements_per_row)
    
    applications_html = ""
    for grouped_applications in grouped_applications_slices:
        
        columns = ""
        for application in grouped_applications:

            description = application["description"]
            if description is None:
                description = ""

            columns += column_template.format(application["id"], cgi.escape(description, True), application["name"])
        
        applications_html += row_template.format(COLUMNS=columns)
    
    return textwrap.dedent("""
        <label for="applications_container"><h3>2. Select an application:</h3></label>
            <div class="container-fluid" id="applications_container">
                {ROWS}
            </div>
    """.format(ROWS=applications_html))


def footer():
    
    return textwrap.dedent("""
        <footer class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-sm-8">&copy; Hendrik van Essen, 2017</div>
                    <div class="col-sm-4"><a href="https://github.com/RIOT-OS/RIOT"><img src="/img/riot_logo_footer.png" alt="RIOT logo" height="44" width="81"></img></a></div>
                </div>
            </div>
        </footer>
    """)


if __name__ == "__main__":

    logging.basicConfig(filename="log/index_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
