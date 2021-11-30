from Database.database import init_db
from Database.database import db_session
from Database.models import Notice
from collections import OrderedDict
import datetime
import uuid

def insert_notice(symbol ,title, link ,date):
  id = uuid.uuid1()
  now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
  notice = Notice(id,symbol,title, link, date, now_date)
  db_session.add(notice)
  db_session.commit()
  return

def select_notice(symbol, title, date): 
  queries = db_session.query(Notice).filter(Notice.symbol==symbol, Notice.title==title, Notice.regist_date==date)
  return queries

  
def main():
  result = insert_notice("123","123","123","123","123","1990-11-11 00:00:00")
  return result
  
if __name__ == "__main__" :
  main()