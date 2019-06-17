import random
from selenium import webdriver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

Chromedriver_path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
]


def create_chrome(proxy_ip=0, headless=0):
    ua_set = 'user-agent=' + random.choice(USER_AGENTS)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(ua_set)
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    if proxy_ip:
        print('使用的代理ip为 ', proxy_ip)
        chrome_options.add_argument('--proxy-server=%s' % proxy_ip)
    driver = webdriver.Chrome(Chromedriver_path, options=chrome_options)
    return driver


def get_proxy_ip():
    proxy_ip = requests.get(
        'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=90cd4ea1565ae6a78fd6304e070cd045&orderNo=GL201905221916298fF1cDGV&count=1&isTxt=1&proxyType=1').content.decode()[
               0:-2]
    print('生成了一个新的代理ip', proxy_ip)
    return proxy_ip


def selenium_wait(driver, xpath, time=30):
    element = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    return element


def selenium_wait_tagname(driver, tagname, time_wait=30):
    WebDriverWait(driver, time_wait).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, tagname)))
    element = driver.find_elements_by_tag_name(tagname)
    return element


def selenium_click(driver, xpath, wait_time=30):
    WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))).click()
    time.sleep(2)
