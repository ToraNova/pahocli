#!/usr/bin/python3
'''
pahocli is a project based on PahoMQTT-Python https://pypi.org/project/paho-mqtt/ 
in hopes to realize a command line mqtt client

Copyright (C) 2019  Chia Jason

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

@Date June 03 2019
'''
# CONST MACROS
VERSION=0.1

# Imports the paho mqtt client
import paho.mqtt.client as mqtt

# prints the logo
print("PAHOCLI version",str(VERSION))
print()

# prints GNU GPL3
print('''pahocli.py Copyright (C) 2019 Chia Jason
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
''')



