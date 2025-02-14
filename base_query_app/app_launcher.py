from utilities import config_reader
from db_service import db_connect,execute_query
from modules import insert_data
from modules import gpt_connect


class LaunchApp():
    def __init__(self,db_launch,file_name=None,file_path=None):
        """initilizes all the required objects"""
        self.db_launch=db_launch
        self.config= config_reader.ConfigRead().config_load(file_name=file_name,file_path=file_path)
        # self.conn=db_connect.db_connect(config=self.config).postgres_connector()

    def insert_data(self):
        """calls function that used to insert file"""
        data=insert_data.inser_data_db(db_launch=self.db_launch,config=self.config).upload_file()
        return data

    def get_response(self):
        """connects to gpt and gets queried data"""
        data =gpt_connect.ChatGPT(api_key=self.config['api_token']['api_secret_key'],model=self.config['api_token']['model'],config=self.config,db_launch=self.db_launch)
        return data