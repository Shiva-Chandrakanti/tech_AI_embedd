
import psycopg2

class db_connect():

    def __init__(self, config):
        self.config = config
    def postgres_connector(self):
        """connects to postgres database"""
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
