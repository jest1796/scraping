from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyautogui as pag

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://tenshoku.mynavi.jp/')

search_bar = driver.find_element(By.XPATH,'//input[@class="topSearch__text"]')
search_bar.send_keys("札幌　ITエンジニア　未経験")

sleep(2)

pag.click(50,200)
pag.click(50,200)


# search_btn = driver.find_element(By.XPATH,'//div[@class="karte-widget__container')
# search_btn.click()
search_btn = driver.find_element(By.XPATH,'//button[@class="topSearch__button js__searchRecruitTop"]')
search_btn.click()
# search_btn = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div/div[2]/a[1]')
# search_btn.click()

sleep(10)
driver.quit()

# //input[@class="topSearch__text"] 検索窓のXpath 