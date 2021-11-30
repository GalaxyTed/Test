from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class TbTest(Base):
  __tablename__ = 'user'
  email = Column(String(250), primary_key=True)
  password = Column(String(250))
  name =Column(String(250))
  create_date = Column(DateTime)
  
  def __init__(self, email, password, name, create_date):
    self.email = email;
    self.password = password
    self.name = name
    self.create_date = create_date
    
  def __repr__(self):
    return "<TbTest('%d', '%s', '%s'>" %(self.id, str(self.datetime), self.string)

class Notice(Base):
  __tablename__ = 'xanglenotice'
  id = Column(String(250), primary_key=True)
  symbol =Column(String(250))
  title = Column(String(250))
  link = Column(String(250))
  regist_date = Column(DateTime)
  create_date = Column(DateTime)
  
  def __init__(self, id, symbol, title, link ,regist_date, create_date):
    self.id = id
    self.symbol =symbol
    self.title = title
    self.link = link
    self.regist_date = regist_date
    self.create_date = create_date