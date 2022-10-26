# 要インストール
#  selenium
#  pyautogui

# googlechromeのバージョンに対応したwebdriverをダウンロードの上、当ファイルと同じディレクトリに置くこと

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyautogui as pag

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://tenshoku.mynavi.jp/')

def scrape():
    sleep(3)
    pag.click(200,200)
    # test = driver.find_element(By.XPATH,'//h1')
    co_name = driver.find_element(By.XPATH,'//h3')
    co_link = driver.find_element(By.XPATH,'//a[@class="js__ga--setCookieOccName"]').get_attribute('href')
    # print(test.text)
    print(co_name.text)
    print(co_link)

    return()

search_bar = driver.find_element(By.XPATH,'//input[@class="topSearch__text"]')
search_bar.send_keys("大阪市　ITエンジニア　未経験")

# ポップアップ画面二つ（アンケートや事前確認）が確実に現れてから次の処理に移るために2秒待機
sleep(3)

# ポップアップ画面を消して「検索ボタン」を押すために、画面上の適当な点を２回クリックする
pag.click(200,200)
pag.click(200,200)

search_btn = driver.find_element(By.XPATH,'//button[@class="topSearch__button js__searchRecruitTop"]')
search_btn.click()

sleep(2)

number_recrute = driver.find_element(By.XPATH,('//p[@class="result__num"]/em')).text
print("\n" + "検索数は"+ number_recrute +"です。")
# print("\n" + "スクレイピングを実行しますか？　（Y / N)")
# Y_N = input()
# if Y_N=="y":
#     print("スクレイピング実行\n"+"UNDER CONSTRUCTION")
    # scrape()
# else:
#     print("中止します。")

scrape()



sleep(5)
driver.quit()

# //input[@class="topSearch__text"] 検索窓のXpath 

# (//p[@class="result__num"]/em)[1]/text() 検索する求人票の数

# //p[@class="main_title"] 会社名
# //h3[@class="cassetteRecruit__name"] 会社名こちらかも？

# //a[@class="link entry_click entry3"]　詳細へのリンク
# //a[@class="js__ga--setCookieOccName"] 詳細へのリンクこちらかも？

# //a[@class="iconFont--arrowLeft"] 次のページへのリンク