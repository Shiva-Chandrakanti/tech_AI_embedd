import sys
import re
sys.dont_write_bytecode = True
from api_services import api
import app_launcher
from datetime import datetime
import sys,os
from datetime import datetime
import db_service_launcher

CONFIG_FILE_PATH = "/Users/administrator/Documents/tech_ai_embeddings/tech_AI_embedd/base_query_app/config"
CONFIG_FILE_NAME = 'config_file'
CON_ENVIRONMENT = 'DEVELOPMENT'

db_launch=db_service_launcher.dbServiceLauncher(file_path=CONFIG_FILE_PATH,file_name=CONFIG_FILE_NAME)
# initilising database object, that can passed to the modules for querying base.

app_launch = app_launcher.LaunchApp(db_launch=db_launch,file_name=CONFIG_FILE_NAME,file_path=CONFIG_FILE_PATH)
# initiliasing app launcher, can be called for modules for inserting, gopt connect

my_api = api.FlaskApp(app_name='query bot',port_number=5004,allowed_origin='*')
app = my_api.app

@app.route("/query_base",methods=['POST'])
def bot():
    """end point for taking query and the query fed to gpt"""
    requested_payload = my_api.request_maker(method='POST')
    question= requested_payload['query']
    data = app_launch.get_response(query=question)
    app_response = my_api.json_response(data=data)
    
    return app_response

@app.route("/insert_new_data",methods=['POST'])
def insert_data():
    """takes csv pdf txt files as payload, converts to embedding and inserts to vector base"""
    # payload=my_api.request_maker(method='POST')
    data = app_launch.insert_data()
    app_response = my_api.json_response(data=data)
    
    return app_response

if __name__ == '__main__':
    my_api.flash_server_start(debug=True) 
    