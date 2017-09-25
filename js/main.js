var board = null;
var downloadIsRunning = false;

var extensionId = "knldjmfmopnpolahpmmgbagdohdnhkik";

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

async function autodetect(selectorID) {

/*
Wenn nicht anders genannt stammen alle vendorid und productid Einträge von:
    http://www.linux-usb.org/usb.ids
*/

    navigator.usb.requestDevice({ filters: [

/*
see riotam-backend/js_update.py for details
*/
/* begin of replacement */
{vendorId: 0x0d28, productId: 0x0204}, //Phytec phyWAVE-KW22
{vendorId: 0x2047}, //MSP430 (family)
{vendorId: 0x03eb}, //ATmega (family)
{vendorId: 0x0483}, //MIPS (family)
{vendorId: 0x0483}, //Nucleo family
{vendorId: 0x0483, productId: 0x3748}, //Airfy Beacon
{vendorId: 0x2a03, productId: 0x003d}, //Arduino Due (usb2serial)
{vendorId: 0x2a03, productId: 0x003e}, //Arduino Due
{vendorId: 0x03eb, productId: 0x6121}, //Arduino Zero
{vendorId: 0x0403}, //CC2650STK
{vendorId: 0x0403, productId: 0xa6d1}, //CC2538DK
{vendorId: 0x0483}, //LimiFrog-v1
{vendorId: 0x0d28, productId: 0x0204}, //mbed_lpc1768
{vendorId: 0x1915}, //micro:bit
{vendorId: 0x0483}, //MSB-IoT
{vendorId: 0x0483, productId: 0x374b}, //Nucleo-F334
{vendorId: 0x0483, productId: 0x374b}, //Nucleo-F103
{vendorId: 0x0483}, //Nucleo-F091
{vendorId: 0x0483}, //Nucleo-F072
{vendorId: 0x0483}, //Nucleo-F070
{vendorId: 0x0483}, //Nucleo-F030
{vendorId: 0x0483}, //Nucleo32-F303
{vendorId: 0x0483}, //Nucleo32-F042
{vendorId: 0x0483}, //Nucleo32-F031
{vendorId: 0x0483}, //NZ32-SC151
{vendorId: 0x0451}, //OpenMote
{vendorId: 0x1915}, //PCA1000x (nRF51822 Development Kit)
{vendorId: 0x1915}, //RFduino
{vendorId: 0x03eb}, //SAMD21-xpro
{vendorId: 0x0d28}, //Seeeduino Arch-Pro
{vendorId: 0x03eb}, //SODAQ Autonomo
{vendorId: 0x1d50, productId: 0x607f}, //Spark Core
{vendorId: 0x03eb}, //SparkFun SAMD21 Mini
{vendorId: 0x0483}, //STM32F0discovery
{vendorId: 0x0483}, //STM32F3discovery
{vendorId: 0x0483}, //STM32F4discovery
{vendorId: 0x1915}, //yunjia-nrf51822
{vendorId: 0x03eb, productId: 0x0042}, //Arduino Mega2560
{vendorId: 0x03eb, productId: 0x0043}, //Arduino Uno
{vendorId: 0x03eb}, //Arduino Duemilanove
{vendorId: 0x2047}, //MSB-430H
{vendorId: 0x2047}, //TelosB
{vendorId: 0x2047}, //WSN430
{vendorId: 0x2047}, //eZ430-Chronos
{vendorId: 0x04d8, productId: 0x00e0}, //PIC32-WiFire
{vendorId: 0x042b}, //Intel Galileo
{vendorId: 0x8086}, //Intel Galileo
{vendorId: 0x8087}, //Intel Galileo
{vendorId: 0x0000}, //HikoB Fox
{vendorId: 0x0000}, //IoT LAB M3
{vendorId: 0x0000}, //MSBA2
{vendorId: 0x0000}, //Mulle
{vendorId: 0x0000}, //UDOO
{vendorId: 0x0000}, //Zolertia remote
{vendorId: 0x0000}, //Zolertia Z1
/* end of replacement */
        
    ] })
    .then(selectedDevice => {
            device = selectedDevice;
            return device;
     })
    .then(() => {

        var boardDictionary = {};
        boardDictionary["MBED CMSIS-DAP"] = "pba-d-01-kw2x";

        productName = device.productName;
        if (boardDictionary[productName] === undefined) {
            alert("Sorry, your board could not be recognized :(");
        }
        else {
            document.getElementById(selectorID).value = boardDictionary[productName];
        }

        return device;
    })
    .catch(error => { 
        console.log(error);
    });

}


function download() {

    chrome.runtime.sendMessage(extensionId, {request: "native_messaging_host_accessible"},
        function(response) {

            //first check: is the extension itself installed/ activated
            if (chrome.runtime.lastError) {
                if (chrome.runtime.lastError.message == "Could not establish connection. Receiving end does not exist.") {
                    alert("You need to install the RIOT OS AppMarket Extension");
                    return;
                }
            }

            //second check: look in to the response if the extension was able to connect to native messaging host
            if(!response.success) {
                alert("You need to install the riotam Native Messaging Host provided in riotam-chrome-integration/native-messaging-host/");
                return;
            }

            //third check: is another download already running?
            if(downloadIsRunning) {
                alert("Another process is already running, please wait until it is finished.");
                return;
            }

            download_post();
        }
    );
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

        alert("You need to select at least one module")
    }
    else if (main_file == null) {

        alert("You have to upload your main source file for your project!")
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

                if(jsonResponse == null || jsonResponse.output_file != null) {
                    downloadButton.className = "btn btn-success";
                    downloadButton.innerHTML = "Download"
                }
                else {
                    downloadButton.className = "btn btn-danger";
                    downloadButton.innerHTML = "Something went wrong"
                }

                //this.responseText has to be a json string
                document.getElementById("customTab_cmdOutput").innerHTML = jsonResponse.cmd_output;

                chrome.runtime.sendMessage(extensionId, jsonResponse);
            }
        });
    }
}


function download_example(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID) {

    chrome.runtime.sendMessage(extensionId, {request: "native_messaging_host_accessible"},
        function(response) {

            //first check: is the extension itself installed/ activated
            if (chrome.runtime.lastError) {
                if (chrome.runtime.lastError.message == "Could not establish connection. Receiving end does not exist.") {
                    alert("You need to install the RIOT OS AppMarket Extension");
                    return;
                }
            }

            //second check: look in to the response if the extension was able to connect to native messaging host
            if(!response.success) {
                alert("You need to install the riotam Native Messaging Host provided in riotam-chrome-integration/native-messaging-host/");
                return;
            }

            //third check: is another download already running?
            if(downloadIsRunning) {
                alert("Another process is already running, please wait until it is finished.");
                return;
            }

            download_example_post(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID);
        }
    );
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

            if(jsonResponse == null || jsonResponse.output_file != null) {
                panel.className = "panel panel-success";

                button.className = "btn btn-success"
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

            chrome.runtime.sendMessage(extensionId, jsonResponse);
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

function sendMailToSupport(modalDialogID) {

    var modalDialog = document.getElementById(modalDialogID);
    var modalDialogBody = modalDialog.getElementsByClassName("modal-body")[0];

    window.open("mailto:support@vanappsteer.de?subject=riotam&body=" + encodeURIComponent(modalDialogBody.innerHTML) + "");
}


function setNavigationEnabled(enabled) {

    // https://stackoverflow.com/questions/20668880/bootstrap-tabs-pills-disabling-and-with-jquery
    if (enabled) {
        $(".nav li").removeClass('disabled');
        $(".nav li").find("a").attr("data-toggle","tab")
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
