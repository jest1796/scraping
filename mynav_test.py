# 要インストール
#  selenium
#  pyautogui

# googlechromeのバージョンに対応したwebdriverをダウンロードの上、当ファイルと同じディレクトリに置くこと

from contextlib import nullcontext
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyautogui as pag

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://tenshoku.mynavi.jp/')


def scrape(urls,names):
# def scrape(names,urls):

    # 検索後のページでもアンケート用小ウインドウが１つまたは２つ開く場合があるので
    # ２秒待機後にクリックを２回行ってそれらを消す
    sleep(2)
    pag.click(200,200)
    sleep(2)
    pag.click(200,200)


    co_names = driver.find_elements(By.XPATH,'//h3')
    co_links = driver.find_elements(By.XPATH,'//a[@class="js__ga--setCookieOccName"]')

    page_names = []
    for co_name in co_names:
        page_names.append(co_name.text)
        # print(co_name.text + "\n")
    names += page_names    
    
    page_urls = []
    for co_link in co_links:
        page_urls.append(co_link.get_attribute)
        # print(co_link.get_attribute('href') + "\n")
    urls += page_urls
    sleep(3)


    # 次ページへのリンクを取得　取得できない場合は最後のページなのでexcept以降の処理へ
    try:
        next_link = driver.find_element(By.XPATH,'(//li/a[@class ="iconFont--arrowLeft"])[2]')
        driver.execute_script('arguments[0].click();', next_link)
        print('次のページをスクレイピング開始')
        
        sleep(2)
        # scrape(names,urls)
        scrape(urls,names)
    except:
        #namesとurlsのタイプを確認
       print(type(names))
       print(type(urls))

       print(names)
        # 会社名をリスト型で表示
       print(urls)
        # リンクをリスト型で表示
       print("取得会社数    "  + str(len(names)))
       print("取得リンク数  " + str(len(urls)))    
        
    # return [urls]

# namesとurlsという空のリストを作成し、scrape関数に渡し、返り値を受け取る
def main():
    names =[]
        # 会社名のリスト
    urls =[]
        # 詳細へのリンクのリスト
        

    # scrape(names,urls)
    scrape(urls,names)
        # ２つの空リストをscrape関数に渡す

    # print(type(names))    #namesとurlsのタイプを確認
    print(type(urls))
    print(type(names))    
    
    print(names)
        # 会社名をリスト型で表示
    print(urls)
        # リンクをリスト型で表示


    print("取得会社数    "  + str(len(names)))
    print("取得リンク数  " + str(len(urls)))    
            # 最終的に取得できた会社数とリンク数を表示
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
main()

sleep(5)
driver.quit()

# //input[@class="topSearch__text"] 検索窓のXpath 

# (//p[@class="result__num"]/em)[1]/text() 検索する求人票の数

# //p[@class="main_title"] 会社名
# //h3[@class="cassetteRecruit__name"] 会社名こちらかも？

# //a[@class="link entry_click entry3"]　詳細へのリンク
# //a[@class="js__ga--setCookieOccName"] 詳細へのリンクこちらかも？

# //a[@class="iconFont--arrowLeft"] 次のページへのリンク
# //li[@class="pager__next"]/a

# print("\n" + "スクレイピングを実行しますか？　（Y / N)")
# Y_N = input()
# if Y_N=="y":
#     print("スクレイピング実行\n"+"UNDER CONSTRUCTION")
#     main()
# else:
#     print("中止します。")