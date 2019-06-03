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
from argparse import ArgumentParser
import sys, time


def on_connect( client, userdata, flags, rc):
    print("Connected with result code",str(rc))
    print(">",end="")
    sys.stdout.flush()

def on_disconnect( client, userdata, rc):
    print("Disconnected with result code",str(rc))
    print(">",end="")
    sys.stdout.flush()

def on_message( client, userdata, msg):
    print("On Message[{}]".format(msg.topic),":",msg.payload)
    print(">",end="")
    sys.stdout.flush()

#def on_subscribe(client, userdata, mid, granted_qos):

def showHelp():
    print("PAHOCLI version",str(VERSION))
    print("/sub:<topic> subscribes to <topic>")
    print("/pub:<topic> changes publish to <topic>")
    print("/p <msg> sends msg to topic set under /pub")
    print("/r repeats last message")
    print("/help show this help")
    print("/exit /quit exit the program")

if __name__ == "__main__":

    # prints the logo
    print("PAHOCLI version",str(VERSION))
    print()

    # prints GNU GPL3
    print('''pahocli.py Copyright (C) 2019 Chia Jason
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    ''')

    ap = ArgumentParser()
    ap.add_argument("-b","--broker",type=str,\
            help="The broker address (127.0.0.1)",default='127.0.0.1')
    ap.add_argument("-p","--port",type=int,\
            help="The broker port (1883)",default=1883)
    ap.add_argument("-u","--username",type=str,\
            help="Use username")
    ap.add_argument("-P","--password",type=str,\
            help="Use password")
    ap.add_argument("--cafile",type=str,\
            help="Specify this for TLS connection (the CA file)")

    args = ap.parse_args()

    c = mqtt.Client()

    if( args.username is not None and args.password is not None ):
        c.username_pw_set(username=args.username, password=args.password)
    if( args.cafile is not None):
        import ssl
        c.tls_set( ca_certs = args.cafile, cert_reqs = ssl.CERT_REQUIRED,\
                tls_version = ssl.PROTOCOL_TLS)

    c.on_connect = on_connect
    c.on_disconnect = on_disconnect
    c.on_message = on_message
    #c.on_subscribe = on_subscribe

    c.connect( args.broker, args.port, 60)
    c.loop_start()

    prevpub = None
    selpub = None
    try:
        while True:

            uin = input(">")
            time.sleep(0.1)
            if( len(uin) == 0 ):
                continue
            else:
                if( uin.startswith("/sub ") ):
                    # Subscribe
                    subtopic = uin[len("/sub "):]
                    print("Subscribing to topic:"+subtopic,end="")
                    res = c.subscribe( subtopic )
                    if(res[0] == 0):
                        print("...OK")
                    else:
                        print("...ER")

                elif( uin.startswith("/pub ") ):
                    # Set publish
                    pubtopic = uin[len("/pub "):]
                    print("Publishing to topic:"+pubtopic)
                    selpub = pubtopic

                elif( uin.startswith("/p ") ):
                    # Publish msg
                    msg = uin[len("/p "):]
                    if( selpub is None ):
                        print("Please specify publishing topic with /pub first")
                    else:
                        c.publish( selpub, msg )
                        prevpub = (selpub,msg)

                elif( uin == "/r" ):
                    # Repeat
                    if( prevpub is None):
                        print("No history. please publish with /p first.")
                    else:
                        c.publish( prevpub[0], prevpub[1] )

                elif( uin == "/help" ):
                    # Help
                    showHelp()

                elif( uin == "/exit" or uin == "/quit" ):
                    # exit
                    exit(0)

                else:
                    # Unknown command
                    print("Unknown command. type /help for more information")
            
    except KeyboardInterrupt:
        print("Keyboard Exit")
        exit(0)
    except Exception as e:            
        print("Exception has occurred",str(e))
        exit(1)
        





    



