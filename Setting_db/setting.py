from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase





class Setting_DB_Table:

    def __init__(self, DATABASE_URL):

        self.DATABASE_URL = DATABASE_URL

        self.engine = None 

        self.session = None



    def CreateEngine(self):

        self.engine = create_engine(
            self.DATABASE_URL,
            connect_args= {"check_same_thread" : False } 
        )

        return self.engine
    


    def Create_session(self):

        self.session = sessionmaker(autoflush="False", bind=self.engine)

        return self.session()
    


settings_db = Setting_DB_Table("sqlite:///./info_users.db")

settings_db.CreateEngine()

settings_db.Create_session()

       
class Base(DeclarativeBase):

    pass
  