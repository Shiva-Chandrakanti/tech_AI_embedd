
import psycopg2

class db_connect():

    def __init__(self, config):
        self.config = config
    def postgres_connector(self):
        try:
            conn = psycopg2.connect(
                user=self.config["username"],
                password=self.config["password"],
                host=self.config["host"],
                port=int(self.config["port"]),
                database=self.config["database"]
                # connect_timeout=31536000
            )
            return conn
        except Exception as err:
            print("Unable to connect to the  database \n{}".format(err))
            return "Unable to connect to the  database \n{}".format(err)
        
# conn = psycopg2.connect(
#                 user='administrator',
#                 password='Shiva@223',
#                 host='localhost',
#                 port=int('5432'),
#                 database='postgres',
#                 # connect_timeout=31536000
#             )
# import pandas as pd
# df=pd.read_sql("select * from public.items", con = conn)
# print(df)