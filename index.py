from app import app, server
from routes import render_page_content

from environment.settings import APP_DEBUG, DEV_TOOLS_PROPS_CHECK #, APP_HOST, APP_PORT


if __name__ == "__main__":
    app.run_server(
        #host=APP_HOST,
        #port=APP_PORT,
        debug=False,
        dev_tools_props_check=False,
    )