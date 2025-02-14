# Your overall code has been rated at 6.45/10
import sys
sys.dont_write_bytecode = True
from pymysql import MySQLError, OperationalError
from utilities import config_reader
from db_service import db_connect
from db_service import execute_query


class dbServiceLauncher():

    def __init__(self,  file_path=None, file_name=None):
        
        self.file_path = file_path
        self.file_name = file_name
        
        
        self.config = config_reader.ConfigRead().config_load(file_path=self.file_path, file_name=self.file_name)
        
       
   
    def check_connection(self,conn_obj):
    
        try:
            if conn_obj.open is True:
                conn = conn_obj
            else:
                conn = self.db_identifier()
        except OperationalError:
            conn = self.db_identifier()
        except Exception as err:
            return "Error while connecting to database : "+str(err)
        return conn
        
    def db_identifier(self):
        
        db_config = self.config["AML_POSTGRES"]
        try:
            # if db_config['db_identifier'] in ["mariadb"]:
            #     conn_class = db_connect.db_connect(db_config).mariadb_connector()
            # if db_config['host']=='mariadb-rds-rre.chzqnfqswu30.us-west-2.rds.amazonaws.com':
            #     print("trying to connect to prod please chesk")
            if db_config['db_identifier'].upper() in ['POSTGRES']:
                conn_class = db_connect.db_connect(db_config).postgres_connector()
            
                
            return conn_class
        except TypeError as typerr:
            print("Type error while connecting to db : ",typerr)
            return "Type error while connecting to db : "+str(typerr)
        except Exception as err:
            print("Exception error while connecting to db : ",err)
            return "Exception error while connecting to db : "+str(err)
    

    def query_execute(self,config=None,q_type=None,query=None,
                        data_dict=None,condition_dict=None,
                        insert_df=None,insert_db=None,insert_table=None,embedding=None
                        ):
        
        data = None
        checked_conn = self.db_identifier()
        if q_type == "select":
            data = execute_query.execute_query(config).select_query(query=query,conn=checked_conn)
      
            data = execute_query.execute_query(config).insert_query(merged_df=insert_df,insert_db=insert_db,
                                                                insert_table=insert_table,conn=checked_conn)
        elif q_type == "embed_insert":
            
            data = execute_query.execute_query(config).insert_embeddings_into_postgres(embedding=embedding,conn=checked_conn,database=insert_db,table_name=insert_table)
        elif q_type=='embed_query':
            data = execute_query.execute_query(config).select_query(query=query,conn=checked_conn)
        checked_conn.close()
        return data

    
    