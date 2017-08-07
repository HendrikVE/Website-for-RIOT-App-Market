var device;

async function selectDevice() {

    var downloadSection = document.getElementById("downloadSection");

/*
Wenn nicht ander genannt stammen alle vendorid und productid Einträge von:
    http://www.linux-usb.org/usb.ids
*/

    navigator.usb.requestDevice({ filters: [
        
        //{vendorId: 0x0000}, //ARM (family)
        {vendorId: 0x2047},  //MSP430 (family)
        {vendorId: 0x03eb},  //ATmega (family)
        {vendorId: 0x0483},  //MIPS (family)

        {vendorId: 0x0483}, //Nucleo family

        //https://github.com/RIOT-OS/RIOT/wiki/Board%3A-Airfy-Beacon
        {vendorId: 0x0483, productId: 0x3748},  //Airfy Beacon

        {vendorId: 0x2a03, productId: 0x003d},  //Arduino Due (usb2serial)
        {vendorId: 0x2a03, productId: 0x003e},  //Arduino Due

        //https://forum.arduino.cc/index.php?topic=360330.0
        {vendorId: 0x03eb, productId: 0x6121},  //Arduino Zero

        //https://github.com/RIOT-OS/RIOT/wiki/Board%3A-CC2538DK
        {vendorId: 0x0403, productId: 0xa6d1},  //CC2538DK

        {vendorId: 0x0403},  //CC2650STK
        {vendorId: 0x0483},  //LimiFrog-v1
        {vendorId: 0x0d28, productId: 0x0204},  //mbed_lpc1768
        {vendorId: 0x1915},  //micro:bit
        {vendorId: 0x0483},  //MSB-IoT

        //lsusb
        {vendorId: 0x0483, productId: 0x374b},  //Nucleo-F334
        {vendorId: 0x0483, productId: 0x374b},  //Nucleo-F103

        {vendorId: 0x0483},  //Nucleo-F091
        {vendorId: 0x0483},  //Nucleo-F072
        {vendorId: 0x0483},  //Nucleo-F070
        {vendorId: 0x0483},  //Nucleo-F030
        {vendorId: 0x0483},  //Nucleo32-F303
        {vendorId: 0x0483},  //Nucleo32-F042
        {vendorId: 0x0483},  //Nucleo32-F031
        {vendorId: 0x0483},  //NZ32-SC151

        {vendorId: 0x0451},  //OpenMote
        {vendorId: 0x1915},  //PCA1000x (nRF51822 Development Kit)

        //lsusb
        {vendorId: 0x0d28, productId: 0x0204},  //Phytec phyWAVE-KW22

        {vendorId: 0x1915},  //RFduino

        //!different hardware vendors?!?
        {vendorId: 0x03eb},  //SAMD21-xpro
        {vendorId: 0x03eb},  //SAMR21-xpro
        {vendorId: 0x03eb},  //SAML21-xpro

        {vendorId: 0x0d28},  //Seeeduino Arch-Pro
        {vendorId: 0x03eb},  //SODAQ Autonomo

        //https://github.com/RIOT-OS/RIOT/wiki/Board%3A-Spark-Core
        {vendorId: 0x1d50, productId: 0x607f},  //Spark Core

        {vendorId: 0x03eb},  //SparkFun SAMD21 Mini
        {vendorId: 0x0483},  //STM32F0discovery
        {vendorId: 0x0483},  //STM32F3discovery
        {vendorId: 0x0483},  //STM32F4discovery
        {vendorId: 0x1915},  //yunjia-nrf51822
        {vendorId: 0x03eb, productId: 0x0042},  //Arduino Mega2560
        {vendorId: 0x03eb, productId: 0x0043},  //Arduino Uno
        {vendorId: 0x03eb},  //Arduino Duemilanove
        {vendorId: 0x2047},  //MSB-430H
        {vendorId: 0x2047},  //TelosB
        {vendorId: 0x2047},  //WSN430
        {vendorId: 0x2047},  //eZ430-Chronos
        {vendorId: 0x04d8, productId: 0x00e0},  //PIC32-WiFire
        {vendorId: 0x042b},  //Intel Galileo
        {vendorId: 0x8086},  //Intel Galileo
        {vendorId: 0x8087},  //Intel Galileo

        //unknown
        {vendorId: 0x0000, productId: 0x0000},  //HikoB Fox
        {vendorId: 0x0000, productId: 0x0000},  //IoT LAB M3
        {vendorId: 0x0000, productId: 0x0000},  //MSBA2
        {vendorId: 0x0000, productId: 0x0000},  //Mulle
        {vendorId: 0x0000, productId: 0x0000},  //UDOO
        {vendorId: 0x0000, productId: 0x0000},  //Zolertia remote
        {vendorId: 0x0000, productId: 0x0000},  //Zolertia Z1
    ] })
    .then(selectedDevice => {
            device = selectedDevice;
            return device;
     })
    .then(() => {
        printDeviceInfo(device);
        downloadSection.style.visibility = "visible";
        return device;
    })
    .catch(error => { 
        console.log(error);
        downloadSection.style.visibility = "hidden";
    });
}

function printDeviceInfo(device) {

    var infoArray = [
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
    ];

    var infoTable = "<table>";
    for(let i = 0; i < infoArray.length; i++) {

        infoTable += "<tr>";
        infoTable += "<td>" + infoArray[i][0] + ": " + "</td><td>" + infoArray[i][1] + "</td>";
        infoTable += "</tr>";
    }
    infoTable += "</table>";

    document.getElementById("deviceInfo").innerHTML = "<b>Selected Device:</b><br>" + infoTable;
}

function download() {

}