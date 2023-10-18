from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
def xc(set):
    chrome_options = Options()
    chrome_options.headless=True#设置浏览器以无界面方式运行
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203')  # 修改User-Agent
    chrome_options.page_load_strategy = 'eager'
    browser = webdriver.Chrome(options=chrome_options)  # Get local session of Chrome

    browser.get("https://www.ctrip.com/")  # Load page
    elem = browser.find_element(By.ID, '_allSearchKeyword')  # Find the query box
    if set == "london":
        set='london3'
        elem.send_keys("伦敦")
    elif set == "newyork":
        set = 'newyork3'
        elem.send_keys("纽约")
    elif set == "san":
        set = 'sanfrancisco3'
        elem.send_keys("旧金山")
    time.sleep(1)
    # elem.send_keys(Keys.ENTER)
    click = browser.find_element(By.ID, 'search_button_global').send_keys(Keys.ENTER)
    # time.sleep(20) # Let the page load, will be added to the API

    win_hans = browser.window_handles[::-1]
    browser.switch_to.window(win_hans[0])
    time.sleep(3)
    url = []
    name = []
    intro = []
    na = browser.find_elements(By.CLASS_NAME, 'title')
    for i in na:
        name.append(i.text)
        #print(i.text)
    img = browser.find_elements(By.CLASS_NAME, 'guide-main-item-top')

    for i in img:
        s = i.get_attribute('style')
        s = s.split('"')
        url.append(s[1])
        #print(s[1])
    introduction = browser.find_elements(By.CLASS_NAME, 'txt')
    for i in introduction:
        intro.append(i.text)
        #print(i.text)
    browser.close()

    import pymysql
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",
                           autocommit=True)
    db_curs = conn.cursor(cursor=pymysql.cursors.DictCursor)
    for name, value, src in zip(name, intro, url):
        # sql="INSERT INTO `%s` (name) values('%s')"%(place,pl)
        db_curs.execute(
            "INSERT INTO `%s` (name,introduction,img) values('%s','%s','%s')" % (set, name, value, src))
