# Orange Pi Fan Controller

PINE Rock64 fan controller.

## Description

This repository provides scripts that can be run on the PINE Rock64 that will
monitor the core temperature and start the fan when the temperature reaches
a certain threshold.

To use this code, you'll have to install a fan.

The instructions for do that you can be found on this guide for RPi: [Control Your Raspberry Pi Fan (and Temperature) with Python](https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python).

**<u>THIS SCRIPT IS SET TO CONTROL FAN WITH PIN 15 and 16 (Tested on board: PINE Rock64 v2.0)</u>**

## Requirements

**This script use [Rock64-R64.GPIO](https://github.com/Leapo/Rock64-R64.GPIO) library.**

## Install


sudo update-rc.d fancontrol.sh defaults