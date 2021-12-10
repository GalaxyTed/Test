from sqlalchemy.sql.expression import text
from .database import init_db
from .database import db_session
from .models import Notice, TradeHistory
from .models import Assets
from .models import User
from .models import Candles
from collections import OrderedDict
from sqlalchemy import distinct, func
import datetime
import uuid

#User Table
def insert_user(email,password, name):
  result_data = OrderedDict()
  nowDatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
  user = User(email,password, name, nowDatetime)
  db_session.add(user)
  db_session.commit()
  
  if(user != None) :
    result_data["status"] = "0000"
  else :
    result_data["status"] = "0002"
    result_data["description"] = "중복된 회원이 존재합니다."
  
  return result_data

def select_user(email, password=None):
  result_data = OrderedDict()
  db_session.close()
  if password!=None :
    queries = db_session.query(User).filter(User.email==email, User.password==password)
  else:
    queries = db_session.query(User).filter(User.email==email)
  
  if(queries.count()>0) :
    result_data["status"] = "0000"
  else :
    result_data["status"] = "0001"
    result_data["description"] = "email 혹은 password가 올바르지 않습니다."
        
  result_data["data"] = [dict(email=q.email, name=q.name) for q in queries]
  
  return result_data

def delete_user(email):
  result_data = OrderedDict()
  result=db_session.query(User).filter(User.email==email).delete()
  db_session.commit()
  
  if(result) :
        result_data["status"] = "0000"
  else :
    result_data["status"] = "0003"
    result_data["description"] = "제거 할 회원이 존재 하지 않습니다."
    
  return result_data
  

#Notice Table
def insert_notice(symbol ,title, link ,date):
  id = uuid.uuid1()
  now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
  notice = Notice(id,symbol,title, link, date, now_date)
  db_session.add(notice)
  db_session.commit()
  
  return

def select_notice():
  result_data = OrderedDict()
  db_session.close()
  queries = db_session.query(Notice).order_by(Notice.create_date.desc()).offset(0).limit(5)
  db_session.commit()
  
  if(queries.count()>0) :
    result_data["status"] = "0000"
  else :
    result_data["status"] = "0005"
    result_data["description"] = "검색된 결과가 없습니다."
        
  result_data["data"] = [dict(symbol=q.symbol, title=q.title, link=q.link, regist_date = str(q.regist_date)) for q in queries]
  
  return result_data  

def select_notice(symbol, title, date): 
  queries = db_session.query(Notice).filter(Notice.symbol==symbol, Notice.title==title, Notice.regist_date==date)
  return queries

#Assets Table
def insert_assets(currency, name, price): 
  id = uuid.uuid1()
  now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
  notice = Assets(id,currency,name,price,now_date)
  
  item = db_session.query(Assets).filter(Assets.currency==currency).first()
  if item == None: 
    db_session.add(notice) 
  else:
    item.price = price
    item.update_date = now_date

  db_session.commit()
  return

def select_assets(currency=None):
  result_data = OrderedDict()
  db_session.close()
  
  if currency!=None :
    queries=db_session.query(Assets).filter(Assets.currency==currency)
  else:
    queries=db_session.query(Assets).order_by(Assets.update_date.desc())
  
  result_data["status"] = "0000"
  result_data["data"] = [dict(currency=q.currency, name_kor=q.name_kor, price=q.price, update_date = str(q.update_date)) for q in queries]
  
  
  return result_data

#Candles Table
def select_candles(currency="KSP", count=1, interval_type="MIN", interval=1):
  result_data = OrderedDict()
  db_session.close()
  
  if interval_type == "MIN":
    queries=db_session.query(Candles).filter(func.substr(Candles.create_date, 15, 2)%interval == 0, Candles.currency==currency).order_by(Candles.create_date.desc()).offset(0).limit(count)
  elif interval_type == "HOUR":
    queries=db_session.query(Candles).filter(func.substr(Candles.create_date, 12, 2)%interval == 0, Candles.currency==currency).order_by(Candles.create_date.desc()).offset(0).limit(count)
  elif interval_type == "DAY":
    queries=db_session.query(Candles).filter(func.substr(Candles.create_date, 12, 2) == 0,func.substr(Candles.create_date, 15, 2) == 0, Candles.currency==currency).order_by(Candles.create_date.desc()).offset(0).limit(count)  
  
  result_data["status"] = "0000"
  result_data["data"] = [dict(currency=q.currency, name_kor=q.name_kor, price=q.price, create_date = str(q.create_date)) for q in queries]
  
  
  return result_data

def insert_candles(currency, name, price): 
  id = uuid.uuid1()
  now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  candles = Candles(id,currency,name,price,now_date)
  db_session.add(candles)
  db_session.commit()
  return

#Trade History
def insert_tradeHistory(user_name,trigger_name, order_type, exchange_name, currency, unit, price):
  id = uuid.uuid1()
  now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  tradeHistory = TradeHistory(id,user_name,trigger_name, order_type, exchange_name, currency, unit, price,now_date)
  db_session.add(tradeHistory)
  db_session.commit()
  
  result_data = OrderedDict() 
  result_data["status"] = "0000"
  result_data["data"] = dict(id=tradeHistory.id, user_name=tradeHistory.user_name, trigger_name=tradeHistory.trigger_name, order_type=tradeHistory.order_type, exchange_name=tradeHistory.exchange_name, currency=tradeHistory.currency, unit=str(tradeHistory.unit), price=str(tradeHistory.price), create_date = str(tradeHistory.create_date))
  
  return result_data