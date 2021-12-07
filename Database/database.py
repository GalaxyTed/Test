# database.py
#!/usr/bin/python

#########################################
#     python 2.7.3
#########################################

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote  

engine = create_engine('mysql+pymysql://root:%s@localhost:3306/qmacro?charset=utf8' % quote('Rbdlf1749!@#'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  Base.metadata.create_all(engine)