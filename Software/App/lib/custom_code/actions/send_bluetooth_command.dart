// Automatic FlutterFlow imports
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'index.dart'; // Imports other custom actions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:flutter_blue/flutter_blue.dart';

Future<void> sendBluetoothCommand(String command) async {
  // Initialize the Bluetooth instance
  FlutterBlue flutterBlue = FlutterBlue.instance;

  try {
    // Start scanning for devices with a timeout of 4 seconds
    flutterBlue.startScan(timeout: Duration(seconds: 4));

    // Listen to scan results and check for the Raspberry Pi device
    bool deviceFound = false;
    await for (ScanResult result in flutterBlue.scanResults) {
      if (result.device.name == 'electrolock') {
        BluetoothDevice device = result.device;

        // Stop scanning once the device is found
        flutterBlue.stopScan();

        // Connect to the Raspberry Pi device
        await device.connect();
        print("Connected to Raspberry Pi!");

        // Establish an RFCOMM connection (no need for discovering services or characteristics)
        // Simply send data over the RFCOMM channel

        // Send the lock/unlock command as text
        await device.writeData(command.codeUnits);
        print("$command command sent successfully!");

        // Disconnect after the operation
        await device.disconnect();
        deviceFound = true;
        break;
      }
    }

    // If no device was found, print a message
    if (!deviceFound) {
      print("Raspberry Pi device not found.");
    }
  } catch (e) {
    print("Bluetooth error: $e");
  }
}
