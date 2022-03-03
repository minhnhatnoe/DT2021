'''Interaction with UptimeRobot'''
from threading import Thread
from flask import Flask
app = Flask('')


@app.route('/')
def main():
    '''The returned page'''
    return "Alive"


def run():
    '''Run function that defines host and port'''
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    '''Function to be called by on_ready'''
    server = Thread(target=run)
    server.start()
