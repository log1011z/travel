from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
def ly(set):
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    chrome_options.headless = True  # 设置浏览器以无界面方式运行
    browser = webdriver.Chrome(options=chrome_options)  # Get local session of Chrome

    browser.get("https://www.ly.com/")  # Load page
    elem = browser.find_element(By.ID, 'pt__search_text')  # Find the query box
    elem.clear()
    if set=="london":
        set='london2'
        elem.send_keys("伦敦")
    elif set=="newyork":
        set = 'newyork2'
        elem.send_keys("纽约")
    elif set=="san":
        set = 'sanfrancisco2'
        elem.send_keys("旧金山")
    time.sleep(0.5)
    click = browser.find_element(By.ID, 'pt__search_btn').click()

    win_hans = browser.window_handles[::-1]
    browser.switch_to.window(win_hans[0])
    time.sleep(3)
    n=browser.find_elements(By.XPATH,"/html/body/div[3]/div[4]/div[1]/div[2]/div[3]/ul/li[.]/div/a/h3")
    v = browser.find_elements(By.XPATH, "/html/body/div[3]/div[4]/div[1]/div[2]/div[3]/ul/li[.]/div/div[3]/p/span")
    s = browser.find_elements(By.XPATH, "/html/body/div[3]/div[4]/div[1]/div[2]/div[3]/ul/li[.]/div/a")
    p=browser.find_elements(By.XPATH,"/html/body/div[3]/div[4]/div[1]/div[2]/div[3]/ul/li[.]/a/img")
    d=browser.find_elements(By.CLASS_NAME,'info_detail')
    date=[]
    name = []
    value = []
    src = []
    img=[]
    v = v[0:3:1]
    n=n[0:3:1]
    s = s[0:3:1]
    p=p[0:3:1]
    d=d[0:3:1]
    for i in d:
        date.append(i.text)
    for i in p:
        img.append(i.get_attribute("src"))
    for i in s:
        #print(i.get_attribute("href"))
        src.append(i.get_attribute("href"))
    for i in v:
        value.append(i.text)
        #print(i[0], i[2][1:-1])
    for i in n:
        name.append(i.text)

    browser.close()

    import pymysql
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",
                           autocommit=True)
    db_curs = conn.cursor(cursor=pymysql.cursors.DictCursor)
    for name, value, src,img,date in zip(name, value, src,img,date):
        # sql="INSERT INTO `%s` (name) values('%s')"%(place,pl)
        db_curs.execute("INSERT INTO `%s` (name,value,src,img,lai,date) values('%s','%s','%s','%s','%s','%s')" % (set, name, value, src,img,'https://pic5.40017.cn/i/ori/PS2lfS0492.jpg',date))
        # db_curs.execute("select * from %s where name= '%s'   "%(flag,pl))

    conn.close()