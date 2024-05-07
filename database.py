from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

class DatabaseMatriz:
    server = str(os.getenv('DB_HOST_MATRIZ')) + ":" + str(os.getenv('DB_PORT_MATRIZ'))
    database = os.getenv('DB_DATABASE_MATRIZ')
    username = os.getenv('DB_USER_MATRIZ')
    password = os.getenv('DB_PASSWORD_MATRIZ')
    params = ("mysql+mysqlconnector://"+username+":"+password+
              "@"+server+"/"+database)

    engine = create_engine(params, echo=True)

    def connection(self):
        db = sessionmaker(bind=self.engine)
        conn = db()
        return conn

class DatabaseMochis:
    server = str(os.getenv('DB_HOST_MOCHIS')) + ":" + str(os.getenv('DB_PORT_MOCHIS'))
    database = os.getenv('DB_DATABASE_MOCHIS')
    username = os.getenv('DB_USER_MOCHIS')
    password = os.getenv('DB_PASSWORD_MOCHIS')
    params = ("mysql+mysqlconnector://"+username+":"+password+
              "@"+server+"/"+database)

    engine = create_engine(params, echo=True)

    def connection(self):
        db = sessionmaker(bind=self.engine)
        conn = db()
        return conn

class DatabaseMazatlan:
    server = str(os.getenv('DB_HOST_MAZATLAN')) + ":" + str(os.getenv('DB_PORT_MAZATLAN'))
    database = os.getenv('DB_DATABASE_MAZATLAN')
    username = os.getenv('DB_USER_MAZATLAN')
    password = os.getenv('DB_PASSWORD_MAZATLAN')
    params = ("mysql+mysqlconnector://"+username+":"+password+
              "@"+server+"/"+database)

    engine = create_engine(params, echo=True)

    def connection(self):
        db = sessionmaker(bind=self.engine)
        conn = db()
        return conn