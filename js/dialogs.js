/*
 * Copyright (C) 2017-2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

function showAlertDownloadProcessRunning() {
    alert("Another process is already running, please wait until it's finished.");
}


function showAlertNoExtension() {
    alert("You need to install the RAPstore extension and then reload this page. See https://github.com/riot-appstore/rapstore-browser-integration");
}


function showAlertNoNativeMessagingHost() {
    alert("You need to install the Native Messaging Host along with the RAPstore extension and then reload this page. See https://github.com/riot-appstore/rapstore-browser-integration");
}
