import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# JSON読み込み
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

pref_nums = config["prefectures"]
start_date = config["start_date"]
end_date = config["end_date"]

print(f"対象都道府県番号: {pref_nums}")
print(f"期間: {start_date} ～ {end_date}")

# Chrome起動
driver = webdriver.Chrome()
driver.get("https://players.pokemon-card.com/event/search?offset=0&order=1")

# ---- ここからサイトに応じた操作を記述 ----
time.sleep(2)

# 仮に、都道府県選択がセレクトボックスの場合：
for pref_num in pref_nums:
    print(f"都道府県 {pref_num} のイベントを検索します...")
    # driver.find_element(By.CSS_SELECTOR, f"option[value='{pref_num}']").click()
    # 検索ボタンなどをクリックする処理をここに書く
    time.sleep(1)

driver.quit()