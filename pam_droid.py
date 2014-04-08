#Made for bitcamp 2014
#David Morris, Ken Sawyer
#Authenticates using a droid and speech.
#avoid databases, use port 1999
CERT="Server.crt"
IP="10.1.35.135"

#libraries
import ssl
import socket
from subprocess import check_output
import threading
from time import sleep
import simplejson as json
#from flask import Flask, request
#of zeroth importance, exit if this hangs!
#def guarantee()

#first, we need to confirm that we have a connection. Otherwise, why do anything else?
def pam_sm_authenticate(pamh, flags, argv):
    sock = socket.socket()
    try:
        sock.connect(IP,1999)
    except:
        return pamh.PAM_IGNORE #if I can't find the phone, pretend I never tried to use this auth system.

    #now that we have a connection, we must verify that the phone we connected to holds the cert,
    #and we establish a secure connection.

    try:
        sock = ssl.wrap_socket(sock,
                #cert_reqs=ssl.CERT_REQUIRED,
                #ca_certs = CERT
                )
    except:
        return pamh.PAM_AUTHTOK_ERR #if the cert failed, assume the worst!
    #
    #app = Flask(__name__)
    #
    #@app.route('/', methods=['POST'])
    #def hello_world():
    #    return 'Hello World!'
    #
    #if __name__ == '__main__':
    #    app.run(port=1999)

    #Send a request and wait for its response in a new thread.
    sock.send("START")
    #class phonethread (threading.Thread):
    #    def __init__(self, threadID, name, counter):
    #        threading.Thread.__init__(self)
    #        self.threadID = threadID
    #        self.name = name
    #        self.counter = counter
    #    def run(self):
    def phonefunc():
        def read_socket():
            return sock.recv(1024)
        return  b''.join(iter(read_socket, b'')).decode('utf-8')
    phonethread = Thread(target = phonefunc )

    def pcfunc():
        localstr = check_output(["speech.sh"])
        return localstr[14:]
    pcthread = Thread(target = pcfunc)
    sock.flush()
    strphone = phonethread.start()
    sleep(1)
    strpc = pcthread.start()

    phonethread.join()
    pcthread.join()
    phonedicts = json.loads(strphone)['result'][0]['alternative']
    pcdicts = json.loads(strpc)['result'][0]['alternative']
    phonel = list()
    pcl = list()
    for d in phonedicts:
        phonel.append(d['transcript'])
    for d in pcdicts:
        pcl.append(d['transcript'])

    #now we act on our lists.
    if 'kill' in phonel:
        return pamh.PAM_AUTH_ERR

    if 'sign in' in phonel:
        if 'sign in' in pcl:
            return pamh.PAM_SUCCESS

    return pamh.PAM_IGNORE
