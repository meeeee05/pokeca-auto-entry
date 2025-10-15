import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def load_config(path="config.json"):
    """設定ファイルを読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    # JSONから設定読み込み
    config = load_config()
    prefs = config["prefectures"]
    start_date = config["start_date"]
    end_date = config["end_date"]

    print("=== 設定内容 ===")
    print(f"都道府県: {prefs}")
    print(f"期間: {start_date} ～ {end_date}")

    # --- Selenium起動 ---
    driver = webdriver.Chrome()  # ChromeDriverが必要
    driver.maximize_window()

    # 仮のURL（ここを後でシティリーグ申込ページに変更）
    driver.get("https://players.pokemon-card.com/event/search?offset=0&order=1")

    # ページが開けるか確認
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("ページを開きました！")

    # --- ここから次のステップで都道府県検索などを実装 ---
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()