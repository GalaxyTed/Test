from database import init_db
from database import db_session
from models import TbTest, Notice
from collections import OrderedDict
from sqlalchemy import desc
from sqlalchemy import func
import datetime

def select_user(email, password=None):
      
  result_data = OrderedDict()
  
  if password!=None :
    queries = db_session.query(TbTest).filter(TbTest.email==email, TbTest.password==password)
  else:
    queries = db_session.query(TbTest).filter(TbTest.email==email)
  
  if(queries.count()>0) :
    result_data["status"] = "0000"
  else :
    result_data["status"] = "0001"
    result_data["description"] = "email 혹은 password가 올바르지 않습니다."
        
  result_data["data"] = [dict(email=q.email, name=q.name) for q in queries]

  
  return result_data
  

def show_tables():  
  queries = db_session.query(TbTest)
  entries = [dict(email=q.email, password=q.password, name=q.name) for q in queries]
  return entries
  
def insert_user(email,password, name):
  result_data = OrderedDict()
  nowDatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
  t = TbTest(email,password, name, nowDatetime)
  db_session.add(t)
  db_session.commit()
  
  if(t != None) :
    result_data["status"] = "0000"
  else :
    result_data["status"] = "0002"
    result_data["description"] = "중복된 회원이 존재합니다."
  
  return result_data
  
def delete_user(email):
  result_data = OrderedDict()
  result=db_session.query(TbTest).filter(TbTest.email==email).delete()
  db_session.commit()
  
  if(result) :
        result_data["status"] = "0000"
  else :
    result_data["status"] = "0003"
    result_data["description"] = "제거 할 회원이 존재 하지 않습니다."
  return result_data
  
def select_notice():
  result_data = OrderedDict()

  queries = db_session.query(Notice).offset(0).limit(5)  
  
  if(queries.count()>0) :
    result_data["status"] = "0000"
  else :
    result_data["status"] = "0005"
    result_data["description"] = "검색된 결과가 없습니다."
        
  result_data["data"] = [dict(symbol=q.symbol, title=q.title, link=q.link, regist_date = str(q.regist_date)) for q in queries]
  return result_data

def main():
  result = select_notice()
  return result
  
if __name__ == "__main__" :
  main()