from utilities import config_reader
from db_service import db_connect,execute_query
from modules import insert_data


class LaunchApp():
    def __init__(self,db_launch,file_name=None,file_path=None):
        self.db_launch=db_launch
        self.config= config_reader.ConfigRead().config_load(file_name=file_name,file_path=file_path)
        # self.conn=db_connect.db_connect(config=self.config).postgres_connector()

    def insert_data(self):
        data=insert_data.inser_data_db(db_launch=self.db_launch,config=self.config).upload_file()
        return data

    def get_response(self):
        return "x"