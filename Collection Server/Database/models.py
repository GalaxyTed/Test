from Database.database import Base
from sqlalchemy import Column, Integer, String, DateTime

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