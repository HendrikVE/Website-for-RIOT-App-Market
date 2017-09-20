var board = null;

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
        /*var infoArray = [
            ["manufacturerName", device.manufacturerName],
            ["vendorId", device.vendorId.toString(16)],
            ["productName", device.productName],
            ["productId", device.productId.toString(16)],
            ["serialNumber", device.serialNumber],
            ["usbVersionMajor", device.usbVersionMajor],
            ["usbVersionMinor", device.usbVersionMinor],
            ["usbVersionSubminor", device.usbVersionSubminor],
            ["deviceClass", device.deviceClass],
            ["deviceSubclass", device.deviceSubclass],
            ["deviceProtocol", device.deviceProtocol],
            ["deviceVersionMajor", device.deviceVersionMajor],
            ["deviceVersionMinor", device.deviceVersionMinor],
            ["deviceVersionSubminor", device.deviceVersionSubminor],
            ["configuration", device.configuration],
            ["configurations", device.configurations],
            ["opened", device.opened]
        ];*/

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
    
    //https://stackoverflow.com/questions/8563240/how-to-get-all-checked-checkboxes
    var checkboxes = document.getElementsByName("module_checkbox");
    var checkboxesChecked = [];
    
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            // add the IDs (retrieved from the database) to the array
            checkboxesChecked.push(checkboxes[i].value);
        }
    }

    var board = document.getElementById("boardSelectorCustomTab").value;
    var main_file = document.getElementById("main_file_input").files[0];
    
    if (checkboxesChecked.length == 0) {

        alert("You need to select at least one module")
    }
    else if (main_file == null) {

        alert("You have to upload your main source file for your project!")
    }
    else {
        
        var downloadButton = document.getElementById("downloadButton");
        var progressBar = document.getElementById("progressBarCustomTab");
        
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
                alert(thrownError);
            },
            success: function(response) {

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
                document.getElementById("cmdOutputCustomTab").innerHTML = jsonResponse.cmd_output;


                //talk to the riotam chrome extension
                var extensionId = "knldjmfmopnpolahpmmgbagdohdnhkik";

                // Make a simple request:
                chrome.runtime.sendMessage(extensionId, jsonResponse,
                    function() {
                        if(chrome.runtime.lastError.message == "Could not establish connection. Receiving end does not exist.") {
                            alert("You need to install the RIOT OS AppMarket Extension");
                        }
                    }
                );
            }
        });
    }
}


function download_example(applicationID, progressDivID, progressBarID, panelID) {
    
    var buttons = document.getElementsByClassName("example-application-button");
    var progressDiv = document.getElementById(progressDivID);
    var progressBar = document.getElementById(progressBarID);
    var panel = document.getElementById(panelID);

    progressDiv.style.visibility = "visible";
    progressBar.style.visibility = "visible";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            
            document.getElementById("cmdOutputExamplesTab").innerHTML = this.responseText

            var jsonResponse = null;
            try {
                jsonResponse = JSON.parse(this.responseText);
            }
            catch(e) {
                alert("Server sent broken JSON");
                return;
            }

            if(jsonResponse == null || jsonResponse.output_file != null) {
                panel.className = "panel panel-success";
            }
            else {
                panel.className = "panel panel-danger";
            }

            //this.responseText has to be a json string
            document.getElementById("cmdOutputExamplesTab").innerHTML = jsonResponse.cmd_output;


            //talk to the riotam chrome extension
            var extensionId = "knldjmfmopnpolahpmmgbagdohdnhkik";

            // Make a simple request:
            chrome.runtime.sendMessage(extensionId, jsonResponse,
                function() {
                    if(chrome.runtime.lastError.message == "Could not establish connection. Receiving end does not exist.") {
                        alert("You need to install the RIOT OS AppMarket Extension");
                    }
                }
            );
       }
    };

    xhttp.open("POST", "/request_example.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    params = "";
    params += "application=" + applicationID;
    params += "&";
    params += "board=" + document.getElementById("boardSelectorExamplesTab").value;

    xhttp.send(params);
}


https://wiki.selfhtml.org/wiki/JavaScript/File_Upload
function dateiupload(evt) {

    var files = evt.target.files;
    var file = files[0];

    if (!f.type.match('text/plain')) {
        return;
    }

    var reader = new FileReader();

    var senddata = new Object();
    senddata.name = file.name;
    senddata.date = file.lastModified;
    senddata.size = file.size;
    senddata.type = file.type;

    reader.onload = function(fileContent) {
        senddata.fileData = fileContent.target.result;

        /*
        Code für AJAX-Request hier einfügen
        */
    }

    // Die Datei einlesen und in eine Data-URL konvertieren
    reader.readAsDataURL(file);
}

// https://codepen.io/CSWApps/pen/GKtvH
$(document).on('click', '.browse', function(){
    var file = $(this).parent().parent().parent().find('.file');
    file.trigger('click');
});
$(document).on('change', '.file', function(){
    $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});
