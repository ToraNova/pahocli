# PAHOCLI
pahocli is a project based on PahoMQTT-Python [paho-mqtt](https://pypi.org/project/paho-mqtt/) in hopes to realize a command line mqtt client.
The client is designed to be simple and lightweight for easy modifications as well as use.

### Dependencies:

	pacman -S python-virtualenv

### Setup and usage:

Setting up virtual-env

	./envsetup

Usage:

	. bin/activate
	./pahocli.py

### Lazy use
If you do not want to use virtual-env, then simply do the following after paho-mqtt is installed with pip3 without virtual-env

	pip3 install paho-mqtt

use with:

	python3 pahocli.py

#### Using packages:
* paho-mqtt

