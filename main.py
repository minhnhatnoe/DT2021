'''Master Bot code'''
from sys import argv
from src import app


if __name__ == "__main__":
    if len(argv) == 1:
        print("Local mode")
        app.local()
    elif len(argv) == 2:
        if argv[1] == "deploy":
            print("Deployment mode. Make sure bot has no other instance")
            app.deploy()
        else:
            print('Run with argument "deploy" to run in deployment mode')
    else:
        print("Too many arguments")
