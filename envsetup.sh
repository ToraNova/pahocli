#!/bin/bash

echo "Setting up virtualenv"
virtualenv .

. bin/activate
pip3 install paho-mqtt

deactivate
