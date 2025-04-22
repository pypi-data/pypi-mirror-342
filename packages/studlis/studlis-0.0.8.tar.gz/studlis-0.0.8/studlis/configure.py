import os
import socket
import sys
# Check if the "worklists" folder exists

def run_configuration(app):

    # Print welcoming information
    print(" --- ")


    # Check if port is free to use

    #try:
    #    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #        s.bind(("localhost", app.webport))
    #        
    #except OSError:
    #    print("\033[91m" + f"[ERROR] Port {app.webport} is already in use. Server cannot start. Use -port to assign another port." + "\033[0m")
    #   sys.exit()




    print("Press CTRL+C to stop the server.")
    print(" --- ")

