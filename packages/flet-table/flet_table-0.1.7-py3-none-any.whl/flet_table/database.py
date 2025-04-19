'''this moduel in delevop -> please check readme and also call the contr
    need to add alembic version for migration 
'''

import pymysql


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host='youtlocalhost',
                user='youuser',
                password='',
                database='db',
                charset='utf8mb4'
            )
            return self.connection
        except pymysql.Error as e:
            print(f"Error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

def get_db_connection(connection_args : dict) -> pymysql.connect:
    '''
    example -> 
    {
        'user' : 'root',
        'host' : 'localhost',
        'password' : 'root',
        'database' : 'database'
    }
    '''
    return pymysql.connect(**connection_args)