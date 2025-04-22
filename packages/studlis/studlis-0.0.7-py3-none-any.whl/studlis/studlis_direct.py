import os

class Studlis():
    def __init__(self, *args, **kwargs):
        if "path" in kwargs:
            config_path = kwargs["path"]
        else:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")

            
        if os.path.isfile(config_path):
            with open(config_path, 'r') as config_file:
                try:
                    appmain.configuration = json.load(config_file)
        
                    if appmain.configuration["auth_provider"] == "none":
                        appmain.auth = NoAuth() # no authentication, user is admin
                    if "project_roots" in appmain.configuration:
                        appmain.project_roots = appmain.configuration["project_roots"]
                    else:
                        print("WARNING: no project root folder set in configuration")


                except json.JSONDecodeError:
                    print("Configuration file is not a valid JSON.")
                    exit()