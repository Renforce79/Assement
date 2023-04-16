import psycopg2

class connections:
    def __init__(self):
        pass
    
    def posgres_conn(self):
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres",
            port=5433
        )
        
        return conn