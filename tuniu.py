from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
def tn(set):
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    chrome_options.headless=True#设置浏览器以无界面方式运行
    browser = webdriver.Chrome(options=chrome_options)  # Get local session of Chrome

    browser.get("https://www.tuniu.com/")  # Load page
    time.sleep(3)
    elem = browser.find_element(By.ID, 'keyword-input')  # Find the query box
    elem.clear()
    if set == "london":
        set = 'london2'
        elem.send_keys("伦敦")
    elif set == "newyork":
        set = 'newyork2'
        elem.send_keys("纽约")
    elif set == "san":
        set = 'sanfrancisco2'
        elem.send_keys("旧金山")
    click = browser.find_element(By.ID, 'searchSub').send_keys(Keys.ENTER)
    win_hans = browser.window_handles[::-1]
    browser.switch_to.window(win_hans[0])
    time.sleep(2)
    browser.execute_script("window.scrollTo(0,450)")
    time.sleep(1)
    browser.execute_script("window.scrollTo(0,950)")
    p = browser.find_elements(By.CLASS_NAME, 'main-tit')
    v = browser.find_elements(By.CLASS_NAME, 'tnPrice')
    s = browser.find_elements(By.XPATH, "//*[@id='niuren_list']/div[2]/div[2]/div[1]/div[1]/ul/li[.]/div/a")
    g=browser.find_elements(By.XPATH,"//*[@id='niuren_list']/div[2]/div[2]/div[1]/div[1]/ul/li[.]/div/a/div[1]/div/img")
    d=browser.find_elements(By.XPATH,"//*[@id='niuren_list']/div[2]/div[2]/div[1]/div[1]/ul/li[.]/div/a/dl/dd[2]/span[2]")
    date=[]
    price = []
    name = []
    src = []
    img=[]
    g=g[0:4:1]
    v = v[0:4:1]
    s = s[0:4:1]
    d=d[0:4:1]
    for i in d:
        date.append(i.text)
    for i in g:
        img.append(i.get_attribute("src"))
    for i in s:
        #print(i.get_attribute("href"))
        src.append(i.get_attribute("href"))
    for i in v:
        s = i.text
        s = s.split()
        price.append(s[1])
        #print(s[1])
    p = p[0:4:1]
    for i in p:
        name.append(i.text)
        #print(i.text)

    browser.close()

    import pymysql
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",
                           autocommit=True)
    db_curs = conn.cursor(cursor=pymysql.cursors.DictCursor)
    for name, value, src,img,date in zip(name, price, src,img,date):
        # sql="INSERT INTO `%s` (name) values('%s')"%(place,pl)
        db_curs.execute("INSERT INTO `%s` (name,value,src,img,lai,date) values('%s','%s','%s','%s','%s','%s')" % (set, name, value, src,img,'https://img3.tuniucdn.com/u/mainpic/logo/logo_20170124.png',date))
        # db_curs.execute("select * from %s where name= '%s'   "%(flag,pl))
