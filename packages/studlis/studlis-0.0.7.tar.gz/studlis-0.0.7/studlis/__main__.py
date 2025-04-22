from studlis.webserver import server as webserv
from studlis.webserv.simplesession import SimpleSessionManager
from studlis.authprovider import NoAuth
from studlis.webserv.pagerequest import global_variants
from studlis.authprovider import AuthPermission
from studlis.projects.project import ProjectManager
from studlis.database import connect_db
import asyncio
import argparse
import os
import sys
import sqlite3
import json
_running = False

appmain = None


class app_main():
    def __init__(self):
        self.webport=8089
        self.dev=False
        self._running=False
        self.session_manager = SimpleSessionManager()
        self.projects={}
    async def run(self):

        self._running=True
        wserver = webserv(self,port=self.webport)
        wserver.dev=self.dev
        self.db=await connect_db(self)


        self.projectmanager = ProjectManager(self)
        await self.projectmanager.refresh_projects()
        from studlis import studlis
        studlis.appmain=self

        #from . import icon

        # Initiate webserver 
        #from studlis import studlis 
        from studlis.studlis import router as studlis_router
        
        wserver.include_router(studlis_router)
        await wserver.start()



        last_expiry_check = asyncio.get_event_loop().time()
        # stay in loop until _running is false
        while self._running:
            await asyncio.sleep(0.1)


        # shut down
        await wserver.stop()
    def exit(self):
        self._running=False
    def has_permission(self,data,permission:AuthPermission):
        session_data=self.session_manager.get_session(data["token"])
        if not session_data:return False # not logged in
        return (session_data["permission"]>=permission.value), session_data
    
   

        






if __name__ == "__main__":
    appmain = app_main()


    # Create the parser
    parser = argparse.ArgumentParser(description='Set the working directory for the script.')

    # Add an argument for the directory path
    parser.add_argument('-path', type=str, help='The path of main database and configuration.')
    parser.add_argument('-dev', action='store_true', help='Set to development mode, disabling cache and enabling debug mode.')
    parser.add_argument('-port', type=int, help='Set the port for the webserver.')
    
    # Parse the arguments
    args = parser.parse_args()

    path = os.getcwd()  # Default to the current working directory

    # Check if the directory argument has been provided
    if args.path:
        path = args.path
        
    if args.dev:
        print(f"Development mode active.")
        appmain.dev=True
    if args.port:
        print(f"Setting port to {args.port}.")
        appmain.webport=args.port
    config_path = os.path.join(path, "studlis.json")
    if os.path.isfile(config_path):
        with open(config_path, 'r') as config_file:
            try:
                appmain.configuration = json.load(config_file)
                appmain.path=path
                if appmain.configuration["auth_provider"] == "none":
                    appmain.auth = NoAuth() # no authentication, user is admin
                elif appmain.configuration["auth_provider"] == "simple":
                    from studlis.authprovider import SimpleAuth
                    appmain.auth = SimpleAuth()
                if "project_roots" in appmain.configuration:
                    appmain.project_roots = appmain.configuration["project_roots"]
                else:
                    print("WARNING: no project root folder set in configuration")


            except json.JSONDecodeError:
                print("Configuration file is not a valid JSON.")
                exit()
    else:
        print("Configuration file does not exist.")
        exit()


# start main async

    #from . import configure
 
    #configure.run_configuration(app)

    
    # Connect to the database using an absolute path
   
    try:
        print("Starting server...")
        asyncio.run(appmain.run())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        appmain._running=False

        print("Server stopped")
        exit()
    except Exception as e:
        appmain._running=False
        raise e
        
        print("Server stopped")
        exit()
    except:
        appmain._running=False

        print("Server stopped")
        exit()


