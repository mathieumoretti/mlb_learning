from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


class DatabaseFactory:
    Base = declarative_base()

#class Database:
#    __instance = None

   

#    def initialize(self):
#        self.engine = create_engine(self.db_uri)

#    def get_instance(self):
#        if __instance:
#            return __instance
#        return self.initialize

            