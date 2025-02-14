


import pandas as pd
import numpy as np



class execute_query():

    def __init__(self,config=None):
        self.config = config

    def select_query(self, query=None, conn=None):
        """
        :param query: user can call this function by specifying the query directly
                    if Null / None, code will look for the details from config file
        :param conn: connection object
        :return: select query
        """
        if query is None:
            try:
                db_name = self.config["db_name"]
                table_name = self.config["table_name"]
                columns = self.config["columns"]
                filter = self.config["filter"]
                dedupe = self.config["dedupe"]
            except KeyError as e:
                raise "Key not found {}".format(str(e))
            except Exception as e:
                raise e

            if columns == ['*'] or columns == '*' or columns is None or columns == "":
                column_list = '*'
            else:
                column_list = ",".join(columns)

            if filter == "" or filter is None:
                where_cond = ""
            else:
                where_cond = "where "+ filter
            if dedupe == True or dedupe == "True":
                select_query = "select Distinct {} from {}.{} {}".format(column_list,db_name,table_name,where_cond)

            else:
                select_query = "select {} from {}.{} {}".format(column_list,db_name,table_name, where_cond)
        else:
            select_query = query
        try:
            df = pd.read_sql(select_query, con = conn)
            data_result = df.to_dict(orient="records")
            return data_result
        except Exception as e:
            raise e

    def insert_query(self,merged_df,insert_db=None,insert_table=None,conn=None):
        def build_query_for_record(db_name, table, columns, values_l):
            columns_string = f"({','.join(columns)})"
            values_string = f"({','.join(['%s'] * len(columns))})"
            values_string = f"{','.join([values_string] * len(values_l))}"
            cleaned_values_l = []
            for values in values_l:
                values = [str(v) for v in values]
                for v in values:
                    if v in ('nan','','None','null','NULL','NONE',' ',np.nan,np.NaN,np.NAN,'NaN','NAN'):
                        v = None
                    cleaned_values_l.append(v)

            duplicate_key_updates = ",".join(["{}=VALUES({})".format(column, column) for column in columns])
            query = "INSERT INTO {}.{} {} VALUES {} ON DUPLICATE KEY UPDATE {}".format(db_name, table, columns_string,
                                                                                         values_string,
                                                                                         duplicate_key_updates)
            return query, cleaned_values_l
        if insert_table is None:
            db_config = self.config
            table_name = db_config["table_name"]
            database = db_config["db_name"]
            BATCH_SIZE = db_config["batch_size"]
        else:
            table_name = insert_table
            database = insert_db
            

        # Iterated over rows of merged data and insert.
        columns = merged_df.columns.tolist()
        values_l = []
        for idx, row in merged_df.iterrows():
            values = [row[col] for col in columns]
            values_l.append(values)
        # Sampling 1000 batch
        while (values_l):
            if insert_table is None:
                batched_data = values_l[:BATCH_SIZE]
                values_l = values_l[BATCH_SIZE:]
            else:
                batched_data = values_l
            query, cleaned_values = build_query_for_record(database,table_name, columns, batched_data)
            try:
                with conn.cursor() as cur:
                    cur.execute(query, tuple(cleaned_values))
                    conn.commit()
            except Exception as e:
                print('ERROR persisting data: ', str(e))
            else:
                break

        print('Successfully entered data.')
        return "Successfully entered data."

        
    def insert_embeddings_into_postgres(self,embedding,conn,table_name,database,conn_str=None):
        # PostgreSQL connection
        
        cursor = conn.cursor()

        # Convert embedding to a Postgres-compatible format (list of floats or a NumPy array)
        embedding = np.array(embedding, dtype=np.float32).tolist()

        # Insert the embedding into the database
    
        cursor.execute(
            "INSERT INTO {} (item_name, embedding) VALUES ('Sample content', '{}')".format(table_name, embedding)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
