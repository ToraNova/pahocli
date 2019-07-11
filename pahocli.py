#!bin/python3
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
VERSION="0.1.3"

# Imports the paho mqtt client
import paho.mqtt.client as mqtt
from argparse import ArgumentParser
import sys, time, json

#=================================================
# ANSI ESCAPE SEQUENCE FOR COLOR CODING
#=================================================
class Eseq:

    normtext = "\033[m" # native color

    # bright color sequences
    # prepends these for color sequences
    defred = "\033[0;31m"        # bright red
    defgrn = "\033[0;32m"        # bright green
    defyel = "\033[0;33m"        # bright yellow
    defblu = "\033[0;34m"        # bright blue
    defmag = "\033[0;35m"        # bright magenta
    defcya = "\033[0;36m"        # bright cyan
    defwht = "\033[0;37m"        # use this to go back to normal text

    bolred = "\033[1;31m"        # bold red
    bolgrn = "\033[1;32m"        # bold green

    whtred = "\033[1;31;40m"    # pure red ?
    whtgrn = "\033[1;32;40m"    # pure green ?

def on_connect( client, userdata, flags, rc):
    try:
        print(Eseq.defgrn+"Connected"+Eseq.normtext,"with result code",str(rc))
        if( len(client.topicls) > 0):
            for t in client.topicls:
                client.subscribe(t)
                print(">"+Eseq.defgrn+"Re-Subscribing"+\
                    Eseq.normtext+" to topic:"+\
                    Eseq.defblu+subtopic+Eseq.normtext)
        print(">",end="")
        sys.stdout.flush()
    except Exception as e:
        print("Exception has occurred:",str(e))

def on_disconnect( client, userdata, rc):
    print(Eseq.defred+"Disconnected"+Eseq.normtext,"with result code",str(rc))
    print(">",end="")
    sys.stdout.flush()

def on_message( client, userdata, msg):
    msgstr = msg.payload.decode('utf-8') #don't forget this baby
    try:
        msgd = json.loads(msgstr)
        print("On Message["+Eseq.defblu+msg.topic+Eseq.normtext+"]:",\
                Eseq.defyel+str(msgd)+Eseq.normtext)
    except Exception as e:
        print("On Message["+Eseq.defblu+msg.topic+Eseq.normtext+"]:",\
                Eseq.defcya+msgstr+Eseq.normtext)
    print(">",end="")
    sys.stdout.flush()

#def on_subscribe(client, userdata, mid, granted_qos):

def showHelp():
    print(Eseq.defmag+"PAHOCLI version",VERSION,Eseq.normtext)
    print("sub <topic>     -- subscribes to <topic>")
    print("pub <topic>     -- changes publish to <topic>")
    print("uns <topic>     -- unsubs from <topic> (* for all)")
    print("ls              -- list all currently subscribed topics")
    print("p <msg>         -- sends msg to topic set under pub")
    print("r               -- repeats last message")
    print("j <msg>         -- test serializing with json format of msg")
    print("help/?          -- show this help")
    print("exit quit q   -- exit the program")

if __name__ == "__main__":

    # prints the logo
    print("PAHOCLI version",VERSION," June 2019")
    # prints GNU GPL3
    print(
'''
pahocli.py Copyright (C) 2019 Chia Jason
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions;''')
    print(
'''
===========================================================\\
        /------------------\\
        +                  |                         *
        + -----------------/
        |/
        | -------\\  |    | /-----\\            *
        |       |]  |    | |     |
        | ----=/ ]  |----| |     |
        | |      ]  |    | |     |
        | \\------/  |    | \\-----/ .... CommandlineXFACE
===========================================================/
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

    c.topicls = []
    c.on_connect = on_connect
    c.on_disconnect = on_disconnect
    c.on_message = on_message
    #c.on_subscribe = on_subscribe

    while True:
        try:
            c.connect( args.broker, args.port, 60)
            break
        except ConnectionRefusedError:
            print("Connection refused.",args.broker, args.port)
            time.sleep(3)
        except Exception as e:
            print("Unknown exception",str(e))
            exit(1)

    c.loop_start()

    prevpub = None
    selpub = None
    mode = "str"
    try:
        while True:

            uin = input(">")
            time.sleep(0.1)
            if( len(uin) == 0 ):
                # Do nothing here.
                continue
            else:
                #-----------------------------------------------------------
                # Main SWITCH block
                #-----------------------------------------------------------
                if( uin.startswith("sub ") ):
                    # Subscribe
                    subtopic = uin[len("sub "):]
                    print("Subscribing to topic:"\
                            +Eseq.defblu+subtopic+Eseq.normtext,end="")
                    res = c.subscribe( subtopic )
                    if(res[0] == 0):
                        print("...OK")
                        c.topicls.append( subtopic )
                    else:
                        print("...ER",res)

                elif( uin.startswith("uns ") ):
                    subtopic = uin[len("uns "):]
                    if subtopic == "*":
                        print("Unsubscribing all topic(s):"\
                                +Eseq.defblu,c.topicls,Eseq.normtext,end="")
                        for t in c.topicls:
                            res = c.unsubscribe( t )
                            if(res[0] == 0):
                                print("..."+Eseq.defgrn+"OK"+Eseq.normtext)
                            else:
                                print("..."+Eseq.defred+"ER"+Eseq.normtext)
                            c.topicls = []

                    elif subtopic in c.topicls:
                        print("Unsubscribing from topic:"\
                                +Eseq.defblu+subtopic+Eseq.normtext,end="")
                        res = c.unsubscribe( subtopic )
                        if(res[0] == 0):
                            print("..."+Eseq.defgrn+"OK"+Eseq.normtext)
                            del c.topicls[ c.topicls.index( subtopic) ]
                        else:
                            print("..."+Eseq.defred+"ER"+Eseq.normtext)
                    else:
                        print("Not subscribed to",subtopic)

                elif( uin == "ls" ):
                    print("Currently subscribed to the following topics:")
                    for t in c.topicls:
                        print(">    *",Eseq.defblu+t+Eseq.normtext)

                elif( uin.startswith("pub ") ):
                    # Set publish
                    pubtopic = uin[len("pub "):]
                    print("Publishing to topic:"+Eseq.defblu+pubtopic+Eseq.normtext)
                    selpub = pubtopic

                elif( uin.startswith("p ") ):
                    # Publish msg
                    msg = uin[len("p "):]
                    if( selpub is None ):
                        print("Please specify publishing topic with pub first")
                    else:
                        c.publish( selpub, msg )
                        prevpub = (selpub,msg)

                elif( uin.startswith("j") ):
                    msg = uin[len("j "):]
                    try:
                        tjs = json.loads(msg)
                        print("Test Serialize"+Eseq.defyel,tjs
                                ,Eseq.normtext)
                    except Exception as e:
                        print(Eseq.defred+"Exception has occurred:"+\
                            Eseq.normtext,str(e))

                elif( uin == "r" ):
                    # Repeat
                    if( prevpub is None):
                        print("No history. please publish with p first.")
                    else:
                        c.publish( prevpub[0], prevpub[1] )

                elif( uin == "help" or uin == "?" ):
                    # Help
                    showHelp()

                elif( uin == "exit" or uin == "quit" or uin == "q" ):
                    # Exit
                    exit(0)

                else:
                    # Unknown command
                    print("Unknown command. type help for more information")

    except KeyboardInterrupt:
        print("Keyboard Exit")
        exit(0)
    except Exception as e:
        print("Exception has occurred",str(e))
        exit(1)







