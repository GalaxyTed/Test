import sys, os, time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from collections import OrderedDict
from Database import dao


#WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

def initial_webdriver():
    #BackGround로 실행할지에 대한 Option 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("headless")

    #webdriver 생성
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options) #driverManger에서 생성
    #driver = webdriver.Chrome('C:/Users/Qpang/Desktop/test/chromedriver',options=options) #driver Path를 지정하여 생성
    return driver

def xangle(driver):
    while True :
        if len(driver.window_handles) > 1 :
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            
        driver.execute_script('window.open("about:blank", "_blank");')
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://xangle.io/disclosure-feed?exchange=all')

        symbol = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/span[1]").text.split('\n')     
        title =driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[2]").text
        date =driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[3]").text
                
        #URL 확인하기 위한 작업 진행
        driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div/div[2]/button").click()
        driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div").click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.implicitly_wait(20)
                
        link =driver.current_url
        #link = "test"        
        # 현재 탭 닫기
        driver.close()

        # 맨 처음 탭으로 변경(0번 탭)
        driver.switch_to.window(driver.window_handles[1])
        
        notices = dao.select_notice(symbol,title,date)
        if notices.count() == 0:
            dao.insert_notice(symbol,title,link,date)
        time.sleep(10)
    return

def klayswap(driver):
    driver.get('https://klayswap.com/assets')
    driver.implicitly_wait(20)
    
    while True :
        #0초에 시작한다
        while datetime.now().second!=0:
            time.sleep(0.1)
            
        coininfo_list = driver.find_elements(By.CSS_SELECTOR , '#app > main > div > section > article.asset-page__list__content > div > div')
        for item in coininfo_list:
            coininfo = item.text.split('\n')
            dao.insert_assets(coininfo[1],coininfo[0],coininfo[5].split(' ')[1])
            dao.insert_candles(coininfo[1],coininfo[0],coininfo[5].split(' ')[1])
        time.sleep(40)
        driver.refresh()
        driver.implicitly_wait(20)
    return

def test():
    while True :
        result_data = dao.insert_tradeHistory("user","trigger","order","exchange","currency",1,10000)
        result_data
    
if __name__ == "__main__":
    test()
    #klayswap(initial_webdriver())
