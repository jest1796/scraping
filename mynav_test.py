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

    # 検索後のページでもアンケート用小ウインドウが１つまたは２つ開く場合があるので
    # ２秒待機後にクリックを２回行ってそれらを消す
    sleep(2)
    pag.click(200,200)
    sleep(2)
    pag.click(200,200)

    # １ページ内の会社名をまとめて取得。
    co_names = driver.find_elements(By.XPATH,'//h3[contains(@class,"cassetteRecruit")]')

    # 1ページ内の会社詳細へのリンクをまとめて取得
    co_links = driver.find_elements(By.XPATH,'//a[@class="js__ga--setCookieOccName"]')


    # １ページ内の会社名を収納するための空リストを準備
    page_names = []

    for co_name in co_names:
        page_names.append(co_name.text)
        print(co_name.text + "\n")       #取得できたかの確認のため表示
        
    # 既にリスト形式で取得した会社名 names に 新たなページで取得した page_names を加える
    names += page_names    

    # １ページ内の会社詳細へのリンクを収納するための空リストを準備
    page_urls = []

    for co_link in co_links:
        page_urls.append(co_link.get_attribute)
        print(co_link.get_attribute('href') + "\n")
        driver.execute_script('arguments[0].click();', co_link)

        # 会社詳細を開くたびに新たなタブが開くので、変数handle_arrayにタブ操作のためのドライバを入れる
        handle_array = driver.window_handles

        # 一番最後に開いたタブ（取得したい会社の詳細ページ）を指定するため、handle_arrayの[-1]を指定
        driver.switch_to.window(handle_array[-1])

        sleep(5)
        try:
            info_page_link = driver.find_element(By.XPATH,'//li[@class="tabNaviRecruit__item blue" and contains(.,"求人情報")]/a')
            print("メッセージページです")
            driver.execute_script('arguments[0].click();',info_page_link)
            print("求人情報ページへ移動します")
        except:
            print("求人情報ページのためこのまま続行")

        try:
            work_late = driver.find_element(By.XPATH,'//div[contains(.,"固定残業") or contains(.,"みなし残業") or contains(.,"見込み残業")]')
            # print(work_late.text)
            conpany_name = driver.find_element(By.XPATH,'//span[@class="companyName"]')
            print(conpany_name.text + "　残業条件注意　　")
        except:
            print("なし")
      
        # 上記のtry except文で要素が取得できなかった場合でも会社詳細を検索出来ているかをチェックするため社名を表示
        conpany_name = driver.find_element(By.XPATH,'//span[@class="companyName"]')
        print(conpany_name.text)

        # 検索結果一覧のページに戻るためにhandle_array[0]を指定
        driver.switch_to.window(handle_array[0])

    # 既にリスト形式で取得した会社詳細リンク url に 新たなページで取得した page_urls を加える   
    urls += page_urls
    sleep(3)


    # 次ページへのリンクを取得する。　　もし取得できない場合は最後のページなのでexcept以降の処理へ
    try:
        next_link = driver.find_element(By.XPATH,'(//li/a[@class ="iconFont--arrowLeft"])[2]')
        driver.execute_script('arguments[0].click();', next_link)
        # print('次のページをスクレイピング開始')
        
        sleep(2)
        # scrape(names,urls)
        scrape(urls,names)
    except:
        #namesとurlsのタイプを確認
    #    print(type(names))
    #    print(type(urls))

    #    print(names)
        # 会社名をリスト型で表示
    #    print(urls)
        # リンクをリスト型で表示
       print("取得会社数    "  + str(len(names)))
       print("取得リンク数  " + str(len(urls)))
       print(str(id(urls)) + "  戻す直前")    
        

# namesとurlsという空のリストを作成し、scrape関数に渡し、返り値を受け取る
def main():
    names =[]
        # 会社名のリスト
    urls =[]
        # 詳細へのリンクのリスト
    print(str(id(urls)) + "  最初")    
        

    # scrape(names,urls)
    scrape(urls,names)
        # ２つの空リストをscrape関数に渡す

    # print(type(names))    #namesとurlsのタイプを確認
    # print(type(urls))
    
    # print(names)
        # 会社名をリスト型で表示
    # print(urls)
        # リンクをリスト型で表示
    print(str(id(urls)) + "  最後" )

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
