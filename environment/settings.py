"""
The module creates the logic to read different configurations based on the environment
"""

#import os
#from os.path import join, dirname
#from dotenv import load_dotenv

#dotenv_path = join(dirname(__file__), os.getenv("ENVIRONMENT_FILE"))
#load_dotenv(dotenv_path=dotenv_path, override=True)

# APP_HOST = os.environ.get("HOST")
# APP_PORT = int(os.environ.get("PORT"))
APP_DEBUG = True # bool(os.environ.get("DEBUG"))
DEV_TOOLS_PROPS_CHECK = True # bool(os.environ.get("DEV_TOOLS_PROPS_CHECK"))