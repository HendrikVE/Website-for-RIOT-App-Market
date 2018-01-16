/*
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var board = null;
var downloadIsRunning = false;

var extensionAvailable = false;
var nativeMessagingHostAvailable = false;

var chromeExtensionId = "knldjmfmopnpolahpmmgbagdohdnhkik";

$(window).on("load", function() {

    $body = $('body');

    // waiting for async operations of extension to finish before continue
    setTimeout(checkBrowserIntegration, 1 * 1000);

    return extensionAvailable && nativeMessagingHostAvailable;
});

function checkBrowserIntegration() {

    var containsExtensionTag = document.body.classList.contains("rapstore_extension_installed");
    var containsNativeMessagingHostTag = document.body.classList.contains("rapstore_native_messaging_host_installed");

    if (!containsExtensionTag) {
        showAlertNoExtension();
    }
    else if (!containsNativeMessagingHostTag) {
        showAlertNoNativeMessagingHost();
    }

    extensionAvailable = containsExtensionTag;
    nativeMessagingHostAvailable = containsNativeMessagingHostTag;
}


// return true if everything went fine, false in case of failure
function do_prechecks() {

    // first check: is another download already running?
    if(downloadIsRunning) {
        showAlertDownloadProcessRunning();
        return false;
    }
    // second check: is the extension itself installed/ activated
    else if (!extensionAvailable) {
        showAlertNoExtension();
        return false;
    }
    // third check: check if the extension was able to connect to native messaging host
    else if (!nativeMessagingHostAvailable) {
        showAlertNoNativeMessagingHost();
        return false;
    }

    // all tests passed successfully
    return true;
}


function showAlertDownloadProcessRunning() {
    alert("Another process is already running, please wait until it's finished.");
}


function showAlertNoExtension() {
    alert("You need to install the RAPstore extension and then reload this page. See https://github.com/riot-appstore/riotam-browser-integration");
}

function showAlertNoNativeMessagingHost() {
    alert("You need to install the Native Messaging Host along with the RAPstore extension and then reload this page. See https://github.com/riot-appstore/riotam-browser-integration");
}

// show pop up, before closing tab by running download
// https://stackoverflow.com/questions/6966319/javascript-confirm-dialog-box-before-close-browser-window
window.onbeforeunload = function (event) {

    if (downloadIsRunning) {

        var message = "Download is still running. Are you sure you want to leave?";
        if (typeof event == "undefined") {
            event = window.event;
        }
        if (event && downloadIsRunning) {
            event.returnValue = message;
        }
        return message;
    }
    else {
        // dont show a dialog when no download is running
        return null;
    }
}

// https://stackoverflow.com/questions/38241480/detect-macos-ios-windows-android-and-linux-os-with-js
function getOS() {

    var userAgent = window.navigator.userAgent,
    platform = window.navigator.platform,
    macosPlatforms = ["Macintosh", "MacIntel", "MacPPC", "Mac68K"],
    windowsPlatforms = ["Win32", "Win64", "Windows", "WinCE"],
    iosPlatforms = ["iPhone", "iPad", "iPod"],
    os = null;

    if (macosPlatforms.indexOf(platform) !== -1) {
        os = "Mac OS";
    }
    else if (iosPlatforms.indexOf(platform) !== -1) {
        os = "iOS";
    }
    else if (windowsPlatforms.indexOf(platform) !== -1) {
        os = "Windows";
    }
    else if (/Android/.test(userAgent)) {
        os = "Android";
    }
    else if (!os && /Linux/.test(platform)) {
        os = "Linux";
    }

    return os;
}

filterRules = [
    //all values are mandatory, even if they are null
    //vendorId and productId are used for WebUSB API, boardInternalName is ignored by it
    {vendorId: 0x0d28, productId: 0x0204, boardInternalName: "pba-d-01-kw2x"},              //Phytec phyWAVE-KW22
    {vendorId: 0x0483, productId: 0x374b, boardInternalName: "nucleo-f103"},                //Nucleo-F103
    {vendorId: 0x0483, productId: 0x374b, boardInternalName: "nucleo-f334"},                //Nucleo-F334
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f091"},                //Nucleo-F091
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f072"},                //Nucleo-F072
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f070"},                //Nucleo-F070
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f030"},                //Nucleo-F030
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo32-f303"},              //Nucleo32-F303
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo32-f042"},              //Nucleo32-F042
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo32-f031"},              //Nucleo32-F031
    {vendorId: 0x2047, productId: null  , boardInternalName: "MSP430 (family)"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "ATmega (family)"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "MIPS (family)"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "Nucleo family"},
    {vendorId: 0x0483, productId: 0x3748, boardInternalName: "Airfy Beacon"},
    {vendorId: 0x2a03, productId: 0x003d, boardInternalName: "Arduino Due (usb2serial)"},
    {vendorId: 0x2a03, productId: 0x003e, boardInternalName: "Arduino Due"},
    {vendorId: 0x03eb, productId: 0x6121, boardInternalName: "Arduino Zero"},
    {vendorId: 0x0403, productId: null  , boardInternalName: "CC2650STK"},
    {vendorId: 0x0403, productId: 0xa6d1, boardInternalName: "CC2538DK"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "LimiFrog-v1"},
    {vendorId: 0x0d28, productId: 0x0204, boardInternalName: "mbed_lpc1768"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "micro:bit"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "MSB-IoT"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "NZ32-SC151"},
    {vendorId: 0x0451, productId: null  , boardInternalName: "OpenMote"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "PCA1000x (nRF51822 Development Kit)"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "RFduino"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "SAMD21-xpro"},
    {vendorId: 0x0d28, productId: null  , boardInternalName: "Seeeduino Arch-Pro"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "SODAQ Autonomo"},
    {vendorId: 0x1d50, productId: 0x607f, boardInternalName: "Spark Core"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "SparkFun SAMD21 Mini"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "STM32F0discovery"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "STM32F3discovery"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "STM32F4discovery"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "yunjia-nrf51822"},
    {vendorId: 0x03eb, productId: 0x0042, boardInternalName: "Arduino Mega2560"},
    {vendorId: 0x03eb, productId: 0x0043, boardInternalName: "Arduino Uno"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "Arduino Duemilanove"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "MSB-430H"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "TelosB"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "WSN430"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "eZ430-Chronos"},
    {vendorId: 0x04d8, productId: 0x00e0, boardInternalName: "PIC32-WiFire"},
    {vendorId: 0x042b, productId: null  , boardInternalName: "Intel Galileo"},
    {vendorId: 0x8086, productId: null  , boardInternalName: "Intel Galileo"},
    {vendorId: 0x8087, productId: null  , boardInternalName: "Intel Galileo"},
    {vendorId: null  , productId: null  , boardInternalName: "HikoB Fox"},
    {vendorId: null  , productId: null  , boardInternalName: "IoT LAB M3"},
    {vendorId: null  , productId: null  , boardInternalName: "MSBA2"},
    {vendorId: null  , productId: null  , boardInternalName: "Mulle"},
    {vendorId: null  , productId: null  , boardInternalName: "UDOO"},
    {vendorId: null  , productId: null  , boardInternalName: "Zolertia remote"},
    {vendorId: null  , productId: null  , boardInternalName: "Zolertia Z1"},
]

async function autodetect(selectorID) {

/*
unless otherwise specified, following vendorid and productid entries are coming from:
    http://www.linux-usb.org/usb.ids
*/

    navigator.usb.requestDevice({filters: filterRules})
    .then(selectedDevice => {
            device = selectedDevice;
            return device;
     })
    .then(() => {

        selectedRule = null;
        //first rule which fits is taken by this algorithm
        for (var i = 0; i < filterRules.length; i++) {
            rule = filterRules[i];

            if (rule.vendorId != null && rule.productId != null) {
                if (rule.vendorId == device.vendorId && rule.productId == device.productId) {
                    selectedRule = rule;
                    break;
                }
            }
            else if (rule.vendorId != null) {
                if (rule.vendorId == device.vendorId) {
                    selectedRule = rule;
                    break;
                }
            }
        }

        if (selectedRule == null) {
            alert("Sorry, your board could not be recognized :(");
        }
        else {
            console.log(selectedRule.boardInternalName);
            document.getElementById(selectorID).value = selectedRule.boardInternalName;
        }

        return device;
    })
    .catch(error => { 
        console.log(error);
    });

}


function download() {

    if (do_prechecks()) {
        download_post();
    }
}


function download_post() {

    //https://stackoverflow.com/questions/8563240/how-to-get-all-checked-checkboxes
    var checkboxes = document.getElementsByName("module_checkbox");
    var checkboxesChecked = [];

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            // add the IDs (retrieved from the database) to the array
            checkboxesChecked.push(checkboxes[i].value);
        }
    }

    var board = document.getElementById("customTab_boardSelector").value;
    var main_file = document.getElementById("customTab_main_file_input").files[0];

    if (checkboxesChecked.length == 0) {

        alert("You need to select at least one module");
    }
    else if (main_file == null) {

        alert("You have to upload your main source file for your project!");
    }
    else {

        downloadIsRunning = true;
        setNavigationEnabled(false);

        var downloadButton = document.getElementById("customTab_downloadButton");
        var progressBar = document.getElementById("customTab_progressBar");

        downloadButton.disabled = true;
        progressBar.style.visibility = "visible";

        var formData = new FormData();
        for (var i = 0; i < checkboxesChecked.length; i++) {
            formData.append('selected_modules[]', checkboxesChecked[i]);
        }
        formData.append("board", board);
        formData.append("main_file_content", main_file, "main.c");

        // https://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously
        $.ajax({
            url: "/request.py",
            type: "POST",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,

            error: function (xhr, ajaxOptions, thrownError) {

                downloadIsRunning = false;
                setNavigationEnabled(true);
                alert(thrownError);
            },
            success: function(response) {

                downloadIsRunning = false;
                setNavigationEnabled(true);

                var jsonResponse = null;
                try {
                    jsonResponse = JSON.parse(response);
                }
                catch(e) {
                    alert("Server sent broken JSON");
                    return;
                }

                if(jsonResponse != null && jsonResponse.output_archive != null) {
                    downloadButton.className = "btn btn-success";
                    downloadButton.innerHTML = "Download"

                    messageExtension("rapstore", jsonResponse);
                }
                else {
                    downloadButton.className = "btn btn-danger";
                    downloadButton.innerHTML = "Something went wrong"
                }

                //this.responseText has to be a json string
                document.getElementById("customTab_cmdOutput").innerHTML = jsonResponse.cmd_output;
            }
        });
    }
}


function download_example(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID) {

    if (do_prechecks()) {
        download_example_post(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID);
    }
}


function download_example_post(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID) {

    downloadIsRunning = true;
    setNavigationEnabled(false);

    var progressDiv = document.getElementById(progressDivID);
    var progressBar = document.getElementById(progressBarID);
    var panel = document.getElementById(panelID);
    var button = document.getElementById(buttonID);

    var modalDialog = document.getElementById(modalDialogID);
    var modalDialogBody = modalDialog.getElementsByClassName("modal-body")[0];
    var modalDialogFooter = modalDialog.getElementsByClassName("modal-footer")[0];

    progressDiv.style.visibility = "visible";
    progressBar.style.visibility = "visible";

    // reset
    panel.className = "panel panel-default";
    button.className = "btn btn-primary"

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {

        if (this.readyState == 4) {
            downloadIsRunning = false;
            setNavigationEnabled(true);
        }

        if (this.readyState == 4 && this.status == 200) {

            var jsonResponse = null;
            try {
                jsonResponse = JSON.parse(this.responseText);
            }
            catch(e) {
                alert("Server sent broken JSON");
                progressDiv.style.visibility = "hidden";
                progressBar.style.visibility = "hidden";
                return;
            }

            if(jsonResponse != null && jsonResponse.output_archive != null) {
                panel.className = "panel panel-success";

                button.className = "btn btn-success"

                messageExtension("rapstore", jsonResponse);
            }
            else {
                panel.className = "panel panel-danger";

                button.className = "btn btn-danger"
                button.innerHTML = "Show error log";

                modalDialogBody.innerHTML = "<p>" + jsonResponse.cmd_output + "</p>"
                modalDialogFooter.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal" onclick="sendMailToSupport(\'' + modalDialogID + '\')">Send log to support</button>' + modalDialogFooter.innerHTML;

                $('#' + modalDialogID + '').modal('show');
                button.onclick = function() {
                    $('#' + modalDialogID + '').modal('show');
                }
            }

            progressDiv.style.visibility = "hidden";
            progressBar.style.visibility = "hidden";
       }
    };

    xhttp.open("POST", "/request_example.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    params = "";
    params += "application=" + applicationID;
    params += "&";
    params += "board=" + document.getElementById("examplesTab_boardSelector").value;

    xhttp.send(params);
}


function messageExtension(givenAction, givenMessage="") {

    var isFirefox = typeof InstallTrigger !== 'undefined';
    var isChrome = !!window.chrome && !!window.chrome.webstore;

    if (isFirefox || isChrome) {
        window.postMessage({
            action: givenAction,
            message: givenMessage
        },
        "*");
    }
    else {
        alert("Browser not supported yet, sry!");
    }
}


function sendMailToSupport(modalDialogID) {

    var modalDialog = document.getElementById(modalDialogID);
    var modalDialogBody = modalDialog.getElementsByClassName("modal-body")[0];

    window.open("mailto:hendrikve@zedat.fu-berlin.de?subject=riotam&body=" + encodeURIComponent(modalDialogBody.innerHTML) + "");
}


function setNavigationEnabled(enabled) {

    // https://stackoverflow.com/questions/20668880/bootstrap-tabs-pills-disabling-and-with-jquery
    if (enabled) {
        $(".nav li").removeClass('disabled');
        $(".nav li").find("a").attr("data-toggle","tab");
    }
    else {
        $(".nav li").addClass('disabled');
        $(".nav li").find("a").removeAttr("data-toggle");
    }
}


// https://codepen.io/CSWApps/pen/GKtvH
$(document).on('click', '.browse', function(){
    var file = $(this).parent().parent().parent().find('.file');
    file.trigger('click');
});
$(document).on('change', '.file', function(){
    $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});
