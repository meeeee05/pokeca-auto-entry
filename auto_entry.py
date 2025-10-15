import json
import webbrowser

# JSON読み込み
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

pref_nums = config["prefectures"]
start_date = config["start_date"].replace("-", "/")
end_date = config["end_date"].replace("-", "/")

# ベースURLと固定パラメータ
BASE_URL = "https://players.pokemon-card.com/event/search"
FIXED_PARAMS = "&event_type=3:2&league_type=1&offset=0&accepting=true&order=1"

# --- 🔹 都道府県番号をカンマ区切りでまとめる ---
pref_str = ",".join(str(num) for num in pref_nums)

# --- 🔹 URL生成（1本にまとめる） ---
url = (
    f"{BASE_URL}?start_date={start_date}"
    f"&end_date={end_date}"
    f"&prefecture={pref_str}"
    f"{FIXED_PARAMS}"
)

# 出力
print("=== 生成されたURL ===")
print(url)

# --- 🔹 ブラウザで開く ---
webbrowser.open(url)