import websocket
import thread
import time
import sys

import threading
import sys, itertools
import json
from termcolor import colored
import logging

class Loading(threading.Thread):

    def __init__(self, num):
        threading.Thread.__init__(self) 

        self.num = num
        self.signal = True
        self.spinner = itertools.cycle(
                    [
                        '|*      |',
                        '| *     |',
                        '|  *    |',
                        '|   *   |',
                        '|    *  |',
                        '|     * |',
                        '|      *|',
                        '|     * |',
                        '|    *  |',
                        '|   *   |',
                        '|  *    |',
                        '| *     |',
                    ])
        self.spin_len = len(self.spinner.next())
        self.colspinner = itertools.cycle(['red','cyan','green','yellow','magenta'])
    def run(self):
        while self.signal:
            try:
                spin = colored(self.spinner.next(), self.colspinner.next())
                sys.stdout.write(spin)
                sys.stdout.flush()
                sys.stdout.write('\b'*self.spin_len)
                time.sleep(0.2)
            except KeyboardInterrupt, e:
                break


loading = Loading(1)
def on_message(ws, message):

    try:
        d = json.loads(message)
        created = int(d['created'])
        msg = d['message']
        level = d['levelname']
        levelno = d['levelno']
        module = d['module']
        myfuncName = str(d['funcName'])
        exc_info = d['exc_info']
        lineno = str(d['lineno'])

        color = 'green'
        if levelno >= logging.CRITICAL:
            color = 'red'
        elif levelno >= logging.ERROR:
            color = 'magenta'
        elif levelno >= logging.WARNING:
            color = 'yellow'

#        t = "%s%s%s.py:%s:%s #%s" %(
        s1 = '{0} {1}:{2}:{3}{4} {5} {6}'.format(
                colored('{:>12}'.format(created), 'magenta'),
                colored("%s.py"%module, 'green'),
                colored(myfuncName, 'cyan'),
                colored("#", 'magenta'),
                colored(lineno, 'yellow'),
                colored(">", 'magenta'),
                colored(msg, 'yellow'))
        s2 = colored('{:11}'.format("[%s]"%level), color)
        print '%s%s' %(s2,s1)
    except Exception, e:
        print e


def on_error(ws, error):
    print "error:", error


def on_close(ws):
    print("### CLOSED ###")
    loading.signal=False


def on_open(ws):
    def run(*args):
        loading.signal=False
        import time
        print"CONNECTED"
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt, e:
                break

        ws.close()
        print("Thread terminating...")

    thread.start_new_thread(run, ())
if __name__ == "__main__":
    if len(sys.argv) < 2:
        host = "ws://localhost:8889/ws"
    else:
        host = sys.argv[1]
    msg = "### WS connecting to %s ###" %host
    print colored(msg, 'yellow')
    loading.start()
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
