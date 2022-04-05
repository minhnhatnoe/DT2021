'''Interaction with UptimeRobot'''
import logging
import sys
from threading import Thread
from flask import Flask
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
app = Flask('')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def main():
    '''The returned page'''
    return "Alive"


def run():
    '''Run function that defines host and port'''
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    '''Function to be called by main'''
    server = Thread(target=run)
    server.daemon = True
    server.start()
