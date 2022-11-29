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
import pandas as pd
import datetime

print("検索したい単語をスペース区切りで入力してください\n")
print("(市町村名、職種、未経験など））\n")
words = input()

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(options = options)
driver.implicitly_wait(10)
driver.get('https://tenshoku.mynavi.jp/')


  

def scrape(urls,names,df):
    
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
        link = co_link.get_attribute('href')
        print(link)
        # print(co_link.get_attribute('href') + "\n")
        driver.execute_script('arguments[0].click();', co_link)

        # 会社詳細を開くたびに新たなタブが開くので、変数handle_arrayにタブ操作のためのドライバを入れる
        handle_array = driver.window_handles

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
            #求人情報ページ内に「固定残業」「みなし残業」「見込み残業」の文字列どれかがあれば 変数work_lateに格納。なければ獲得失敗となりexcept以降の処理へ飛ぶ
            
            work_late = driver.find_element(By.XPATH,'//div[contains(.,"固定残業") or contains(.,"みなし残業") or contains(.,"見込み残業")]')
            conpany_name = driver.find_element(By.XPATH,'//span[@class="companyName"]').text
            print(conpany_name+ "　残業条件注意　　")
            overtime = "有り"    #固定残業等
        except:
            overtime = "なし"
            print(overtime)
      
        # 上記のtry except文で要素が取得できなかった場合でも会社詳細を検索出来ているかをチェックするため社名を表示
        company_name = driver.find_element(By.XPATH,'//span[@class="companyName"]').text
        print(company_name)
        # link = co_link.get_attribute('href') #会社求人情報ページへのURL
        company_data = pd.Series([company_name,overtime,link],index=df.columns)
        print(company_data)
        df = df.append(company_data,ignore_index=True)
      
        # 検索結果一覧のページに戻るためにhandle_array[0]を指定
        driver.switch_to.window(handle_array[0])

    # 既にリスト形式で取得した会社詳細リンク url に 新たなページで取得した page_urls を加える   
    urls += page_urls
    sleep(3)


    # 次ページへのリンクを取得する。　　もし取得できない場合は最後のページなのでexcept以降の処理へ
    try:
        next_link = driver.find_element(By.XPATH,'(//li/a[@class ="iconFont--arrowLeft"])[2]')
        driver.execute_script('arguments[0].click();', next_link)
        print('次のページをスクレイピング開始')
        
        sleep(2)
    
        scrape(urls,names,df)
    except:
       
       print("取得会社数    "  + str(len(names)))
       print("取得リンク数  " + str(len(urls)))
       
    #    print(df.drop[0])
       dt = datetime.datetime.now()
       dt = dt.strftime('%Y-%m-%d_%H%M%S')
       df = df.dropna()
       df.to_csv(dt + "_data.csv",index=False)
       
       return(df)    
        

# namesとurlsという空のリストを作成し、scrape関数に渡し、返り値を受け取る
def main():
    names =[]
        # 会社名のリスト
    urls =[]
        # 詳細へのリンクのリスト
    df = pd.DataFrame(columns=['会社名','みなし残業等','URL'],index=[0])  

    print(str(id(urls)) + "  最初")    
        

    scrape(urls,names,df)
        # 2つの空リストとデータフレーム1つをscrape関数に渡す

    print("取得会社数    "  + str(len(names)))
    print("取得リンク数  " + str(len(urls)))    
            # 最終的に取得できた会社数とリンク数を表示
    
    return(df)


search_bar = driver.find_element(By.XPATH,'//input[@class="topSearch__text"]')
search_bar.send_keys(words)

# ポップアップ画面二つ（アンケートや事前確認）が確実に現れてから次の処理に移るために3秒待機
sleep(3)

# ポップアップ画面を消して「検索ボタン」を押すために、画面上の適当な点を２回クリックする
pag.click(200,200)
pag.click(200,200)

search_btn = driver.find_element(By.XPATH,'//button[@class="topSearch__button js__searchRecruitTop"]')
search_btn.click()

sleep(2)

number_recrute = driver.find_element(By.XPATH,('//p[@class="result__num"]/em')).text
print("\n" + "検索数は"+ number_recrute +"です。")
print("実行しますか？（検索数に比例して時間がかかります）")
print("スクレイピング開始＞＞1を押してください\n中止　　　　　　　＞＞2を押してください")
a = int(input())
if a==1:
    print("GO!")
    main()

driver.quit()


