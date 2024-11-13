import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    def __init__(self, host='127.0.0.1', port=3307, user='root', password='root', database='comp'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            except Error as e:
                raise Exception(f"Error connecting to the database: {e}")

    def get_cursor(self, dictionary=False):
        self.connect()
        return self.connection.cursor(dictionary=dictionary)

    def commit(self):
        if self.connection and self.connection.is_connected():
            self.connection.commit()

    def rollback(self):
        if self.connection and self.connection.is_connected():
            self.connection.rollback()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
