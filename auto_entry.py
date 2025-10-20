import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Json読み込み
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

pref_nums = config["prefectures"]
start_date = config["start_date"].replace("-", "/")
end_date = config["end_date"].replace("-", "/")

#可変URL生成 
#クエリパラメータとしてJsonの内容をURLに挿入
BASE_URL = "https://players.pokemon-card.com/event/search"
FIXED_PARAMS = "&event_type=3:2&league_type=1&offset=0&accepting=true&order=1"
pref_str = ",".join(map(str, pref_nums))
target_url = f"{BASE_URL}?start_date={start_date}&end_date={end_date}&prefecture={pref_str}{FIXED_PARAMS}"
#print(f"アクセスURL: {target_url}")

#Selenium起動
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.get(target_url)
print("ページを読み込み中...")
time.sleep(4)    # JS描画待ち

#Userログイン待ち
print("\n 必要に応じて手動でログインしてください。")
input("ログインが完了したら return を押してください。")

#ログイン後に、再度検索URLを開く
print("\n 検索ページ再読み込み中...")
driver.get(target_url)
time.sleep(4)
#print("ログイン完了を確認、大会一覧を再取得中...")


#大会タイトル取得XPath
title_xpath = (
    "//div[contains(@class,'right') and not(ancestor::div[contains(@class,'right')])]"
    "/div[contains(@class,'title')]"
)

#現在の一覧ページから大会タイトル要素を取得
def get_title_elements():
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
        elems = driver.find_elements(By.XPATH, title_xpath)
        visible = [e for e in elems if e.is_displayed() and e.text.strip()]
        return visible
    except Exception:
        return []

#大会タイトルを表示
titles = get_title_elements()
print(f"検出された大会タイトル数: {len(titles)}")
for i, t in enumerate(titles, start=1):
    print(f"  {i}: {t.text.strip()}")

if not titles:
    print("大会タイトルが見つかりませんでした。")
    driver.quit()
    exit()



#応募処理ループ
for idx in range(len(titles)):
    titles = get_title_elements()
    if idx >= len(titles):
        print(f"インデックス {idx} は現在のタイトル数を超えています。終了します。")
        break

    title_elem = titles[idx]
    title_text = title_elem.text.strip()
    print(f"\n[{idx+1}] '{title_text}' をクリックして大会に申し込みます...")

    try:
        #大会タイトルクリック
        driver.execute_script("arguments[0].scrollIntoView(true);", title_elem)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", title_elem)

        # 詳細ページロード待機
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.c-btn.c-btn-primary")))
        time.sleep(1)
        #print("大会詳細ページを開きました。")

        #「イベント応募へ」押下
        try:
            entry_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'イベント応募へ')]"))
            )
            driver.execute_script("arguments[0].click();", entry_btn)
            print("「イベント応募へ」をクリックしました。")
        except Exception as e:
            print("「イベント応募へ」が見つかりませんでした（スキップ）:", e)
            driver.get(target_url)
            time.sleep(2)
            continue

        #「利用規約」にチェック（input or label）
        try:
            try:
                agree = wait.until(EC.element_to_be_clickable((By.ID, "agreement2")))
                driver.execute_script("arguments[0].click();", agree)
                label_id = label_elem.get_attribute("id")
                print("利用規約に同意しました。（inputクリック）: {label_id}")
            except Exception:
                label_elem = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'利用規約に同意する')]"))
                )
                driver.execute_script("arguments[0].click();", label_elem)
                print("利用規約に同意しました。（ラベルクリック）")
            time.sleep(0.5)
        except Exception as e:
            print("利用規約チェックボックスが見つかりません（スキップ）:", e)
            driver.get(target_url)
            time.sleep(2)
            continue

        #「応募する」押下
        try:
            apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'応募する')]")))
            driver.execute_script("arguments[0].click();", apply_btn)
            print("「応募する」をクリックしました。")
        except Exception as e:
            print("「応募する」が見つかりません（スキップ）:", e)
            driver.get(target_url)
            time.sleep(2)
            continue

        time.sleep(2)
        print(f"[{idx+1}] '{title_text}' に応募しました。")

        # 一覧に戻る
        driver.get(target_url)
        time.sleep(3)

    except Exception as e:
        print(f"[{idx+1}] 処理中にエラーが発生しました: {e}")
        driver.get(target_url)
        time.sleep(3)
        continue

print("\n全処理完了。ブラウザを閉じます。")
driver.quit()