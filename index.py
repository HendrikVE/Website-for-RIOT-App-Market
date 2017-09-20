#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import cgi
import cgitb
import logging
import textwrap

from MyDatabase import MyDatabase

BOOTSTRAP_COLUMS_PER_ROW = 12
CFG_APPLICATIONS_PER_ROW = 2
CFG_MODULES_PER_ROW = 4

db = MyDatabase()


def main():
    
    cgitb.enable()
    
    print ('Content-Type: text/html')
    print ('\n\r')
    
    print (textwrap.dedent("""
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
               FOOTER=footer())))


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
                        <img src="/img/riot_logo.png" alt="RIOT logo" height="200" width="445"></img>
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

    boards = fetch_boards()
    modules = fetch_modules()

    board_selector_html = board_selector(boards, "boardSelectorCustomTab", "buttonAutodetectCustomTab")
    modules_html = module_selection(modules)

    return textwrap.dedent("""
        <form id="customTabForm" enctype="multipart/form-data">
            {BOARD_SELECTOR}
            {FILE_UPLOAD}
            {MODULES}
            <h3>4. Build and flash:</h3>
            <div class="container-fluid">
                <button type="button" class="btn btn-primary" id="downloadButton" onclick="download()">Compile your personal RIOT OS</button>
                <div class="well" id="cmdOutputCustomTab">
                    <div class="progress">
                        <div class="progress-bar progress-bar-striped active" id="progressBarCustomTab" style="width:100%; visibility:hidden"></div>
                    </div>
                </div>
            </div>
        </form>
    """.format(BOARD_SELECTOR=board_selector_html,
               FILE_UPLOAD=file_upload_input(),
               MODULES=modules_html))


def examples_tab():

    boards = fetch_boards()
    apps = fetch_applications()

    board_selector_html = board_selector(boards, "boardSelectorExamplesTab", "buttonAutodetectExamplesTab")
    applications_html = application_selection(apps)

    return textwrap.dedent("""
        <form id="examplesTabForm">
            {BOARD_SELECTOR}
            {APPLICATIONS}
        </form>
    """.format(BOARD_SELECTOR=board_selector_html,
               APPLICATIONS=applications_html))


# https://codepen.io/CSWApps/pen/GKtvH
def file_upload_input():
    
    return textwrap.dedent("""
        <h3>2. Upload your main class file:</h3>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-6">
                    <input id="main_file_input" type="file" name="img[]" class="file">
                    <div class="input-group">
                        <input type="text" class="form-control" readonly placeholder="Upload main source file">
                        <span class="input-group-btn">
                            <button class="browse btn btn-primary" type="button"><i class="glyphicon glyphicon-search"></i> Browse</button>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    """)


def board_selector(boards, selector_id, button_id):

    selector_options = ''

    for board in boards:
        selector_options += '<option value="{!s}">{!s}</option>'.format(board["internal_name"], board["display_name"])

    return textwrap.dedent("""
        <label for="{SELECTOR_ID}"><h3>1. Select a board:</h3></label>
        <div class="container-fluid" id="applications_container">
            <div class="row">
                <div class="col-md-10">
                    <div class="form-group">
                        <select class="form-control" id="{SELECTOR_ID}">
                            {SELECTOR_OPTIONS}
                        </select>
                    </div>
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-info btn-block" id="{BUTTON_ID}" onclick="autodetect('{SELECTOR_ID}')">Try autodetect</button>
                </div>
            </div>
        </div>
    """.format(SELECTOR_ID=selector_id,
               SELECTOR_OPTIONS=selector_options,
               BUTTON_ID=button_id))


def slices(input_list, group_size):
    return [input_list[x:x + group_size] for x in xrange(0, len(input_list), group_size)]


def module_selection(modules, elements_per_row=CFG_MODULES_PER_ROW):

    column_width = int(BOOTSTRAP_COLUMS_PER_ROW / elements_per_row)
    
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
    
    checkbox_groups = {}

    for module in modules:

        group = module["group_identifier"]
        checkbox_groups.setdefault(group, []).append(module)

    for group, modules in sorted(checkbox_groups.items()):
        modules = sorted(modules, key=lambda x:x['name'])
        checkboxes_html += '<div class="checkbox well"><h4>' + group + '</h4>'
        
        grouped_checkboxes_slices = slices(modules, elements_per_row)
        
        for grouped_checkboxes in grouped_checkboxes_slices:

            columns = ""
            for checkbox in grouped_checkboxes:
                description = checkbox["description"] or ""
                columns += column_template.format(checkbox["id"], cgi.escape(description, True), checkbox["name"])

            checkboxes_html += row_template.format(COLUMNS=columns)
            
        checkboxes_html += '</div>'
    
    return textwrap.dedent("""
        <label for="checkboxes_container"><h3>3. Select modules:</h3></label>
        <div class="container-fluid" id="checkboxes_container">
            {ROWS}
        </div>
    """.format(ROWS=checkboxes_html))


def application_selection(apps, elements_per_row=CFG_APPLICATIONS_PER_ROW):

    column_width = int(BOOTSTRAP_COLUMS_PER_ROW / elements_per_row)
    
    row_template = textwrap.dedent("""
        <div class="row">
            {COLUMNS}
        </div>
    """)
    
    column_template = textwrap.dedent("""
        <div class="col-md-""" + str(column_width) + """">
            {APPLICATION_PANEL}
        </div>
    """)
    
    grouped_applications_slices = slices(apps, elements_per_row)
    
    applications_html = ""
    for grouped_applications in grouped_applications_slices:
        
        columns = ""
        for application in grouped_applications:

            description = application["description"]
            if not description:
                description = "There is no description yet"

            application_panel = collapsible_panel(application["name"],
                                                  cgi.escape(description, True),
                                                  application["id"],
                                                  "progressDivExampleTab",
                                                  "progressBarExampleTab",
                                                  "panelExampleTab",
                                                  "buttonExampleTab",
                                                  "modalDialogExampleTab")

            columns += column_template.format(APPLICATION_PANEL=application_panel)
        
        applications_html += row_template.format(COLUMNS=columns)
    
    return textwrap.dedent("""
        <label for="applications_container"><h3>2. Select an application:</h3></label>
            <div class="container-fluid" id="applications_container">
                {ROWS}
            </div>
    """.format(ROWS=applications_html))


def collapsible_panel(title, content, application_id, progress_div_id_prefix, progressbar_id_prefix, panel_id_prefix, button_id_prefix, modal_dialog_id_prefix):

    progress_div_id = progress_div_id_prefix + str(application_id)
    progressbar_id = progressbar_id_prefix + str(application_id)
    panel_id = panel_id_prefix + str(application_id)
    button_id = button_id_prefix + str(application_id)

    modal_dialog_id = modal_dialog_id_prefix + str(application_id)
    modal_dialog_html = modal_dialog(modal_dialog_id, "Error log", "")

    return textwrap.dedent("""
        <div id="{PANEL_ID}" class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a class="collapsed" data-toggle="collapse" data-target="#panel_body{APPLICATION_ID}">{TITLE}</a>
                </h4>
            </div>
            <div id="panel_body{APPLICATION_ID}" class="panel-body collapse">
                {CONTENT}
            </div>
            <div class="panel-footer">
                <div class="row">
                    <div class="col-md-4">
                        <button id="{BUTTON_ID}" type="button" class="btn btn-primary" onclick="download_example('{APPLICATION_ID}', '{PROGRESS_DIV_ID}', '{PROGRESSBAR_ID}', '{PANEL_ID}', '{BUTTON_ID}', '{MODAL_DIALOG_ID}')">Download and flash</button>
                    </div>
                    <div class="col-md-8">
                        <div class="progress" id="{PROGRESS_DIV_ID}" style="visibility:hidden">
                            <div class="progress-bar progress-bar-striped active" id="{PROGRESSBAR_ID}" style="width:100%;"></div>
                        </div>                        
                    </div>
                </div>
            </div>
        </div>
        {MODAL_DIALOG}
    """.format(TITLE=title,
               CONTENT=content,
               APPLICATION_ID=application_id,
               PROGRESS_DIV_ID=progress_div_id,
               PROGRESSBAR_ID=progressbar_id,
               PANEL_ID=panel_id,
               BUTTON_ID=button_id,
               MODAL_DIALOG_ID=modal_dialog_id,
               MODAL_DIALOG=modal_dialog_html))


def modal_dialog(dialog_id, title, message):

    return textwrap.dedent("""
        <div class="modal fade" id="{DIALOG_ID}" role="dialog">
            <div class="modal-dialog modal-lg">
            
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <h4 class="modal-title">{TITLE}</h4>
                </div>
                <div class="modal-body">
                    {MESSAGE}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>
            
            </div>
        </div>
    """.format(DIALOG_ID=dialog_id,
               TITLE=title,
               MESSAGE=message))


def footer():
    
    return textwrap.dedent("""
        <footer class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-sm-8">&copy; Hendrik van Essen, 2017</div>
                    <div class="col-sm-4"><a href="https://riot-os.org/"><img src="/img/riot_logo_footer.png" alt="RIOT logo" height="35" width="64"></img></a></div>
                </div>
            </div>
        </footer>
    """)


def fetch_boards():
    db.query("SELECT * FROM boards ORDER BY display_name")
    return db.fetchall()


def fetch_applications():
    db.query("SELECT * FROM applications ORDER BY name")
    return db.fetchall()


def fetch_modules():
    db.query("SELECT * FROM modules ORDER BY group_identifier ASC, name ASC")
    return db.fetchall()


if __name__ == "__main__":

    logging.basicConfig(filename="log/index_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
