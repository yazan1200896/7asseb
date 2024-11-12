import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3307
        self.user = 'root'
        self.password = 'root'
        self.database = 'comp'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Database connection successful")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    def get_cursor(self):
        if self.connection is None:
            self.connect()
        return self.connection.cursor(dictionary=True)

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
