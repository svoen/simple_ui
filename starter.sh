#!/bin/sh

echo off
sudo rmmod dvb_usb_rtl28xxu rtl2832
cd /home/pi/dump1090
./dump1090 --interactive --net --net-ro-size 500 --net-ro-rate 5
