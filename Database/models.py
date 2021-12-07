from .database import Base
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
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
class Assets(Base):
  __tablename__ = 'klayswapassets'
  id = Column(String(250), primary_key=True)
  currency =Column(String(250))
  name_kor = Column(String(250))
  price =Column(String(250))
  update_date = Column(DateTime)
  
  def __init__(self, id, currency,name_kor, price, update_date):
    self.id = id
    self.currency =currency
    self.name_kor = name_kor
    self.price = price
    self.update_date = update_date   
class Candles(Base):
  __tablename__ = 'klayswapcandles'
  id = Column(String(250), primary_key=True)
  currency =Column(String(250))
  name_kor = Column(String(250))
  price =Column(String(250))
  create_date = Column(DateTime)
  
  def __init__(self, id, currency,name_kor, price, create_date):
    self.id = id
    self.currency =currency
    self.name_kor = name_kor
    self.price = price
    self.create_date = create_date