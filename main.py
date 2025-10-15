import tkinter as tk
from tkinter import ttk, messagebox
import json
import subprocess
import sys
import os

root = tk.Tk()
root.title("シティリーグ一括応募ツール")
root.geometry("700x600")

# タイトル
ttk.Label(root, text="シティリーグ一括応募", font=("Meiryo", 14, "bold")).pack(pady=10)

# 都道府県（番号: 名称）
PREFS = {
    1: "北海道", 2: "青森県", 3: "岩手県", 4: "宮城県", 5: "秋田県", 6: "山形県", 7: "福島県",
    8: "茨城県", 9: "栃木県", 10: "群馬県", 11: "埼玉県", 12: "千葉県", 13: "東京都", 14: "神奈川県",
    15: "新潟県", 16: "富山県", 17: "石川県", 18: "福井県", 19: "山梨県", 20: "長野県",
    21: "岐阜県", 22: "静岡県", 23: "愛知県", 24: "三重県",
    25: "滋賀県", 26: "京都府", 27: "大阪府", 28: "兵庫県", 29: "奈良県", 30: "和歌山県",
    31: "鳥取県", 32: "島根県", 33: "岡山県", 34: "広島県", 35: "山口県",
    36: "徳島県", 37: "香川県", 38: "愛媛県", 39: "高知県",
    40: "福岡県", 41: "佐賀県", 42: "長崎県", 43: "熊本県", 44: "大分県", 45: "宮崎県", 46: "鹿児島県", 47: "沖縄県"
}

pref_vars = {num: tk.IntVar() for num in PREFS.keys()}

def layout_checkbuttons():
    for widget in frame_prefs.winfo_children():
        widget.grid_forget()

    width = frame_prefs.winfo_width()
    if width < 200:
        width = 200

    btn_width = 120
    cols = max(1, width // btn_width)

    for i, (num, name) in enumerate(PREFS.items()):
        row, col = divmod(i, cols)
        chk = ttk.Checkbutton(frame_prefs, text=name, variable=pref_vars[num])
        chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)

def submit():
    selected_nums = [num for num, var in pref_vars.items() if var.get()]
    start = start_entry.get()
    end = end_entry.get()

    if not selected_nums:
        messagebox.showwarning("エラー", "少なくとも1つの都道府県を選択してください。")
        return

    # JSONデータ作成
    data = {
        "prefectures": selected_nums,
        "start_date": start,
        "end_date": end
    }

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("保存完了", "設定を config.json に保存しました！")

    # auto_entry.py 実行
    script_path = os.path.join(os.path.dirname(__file__), "auto_entry.py")
    subprocess.Popen([sys.executable, script_path])

# ラベルフレームのスタイル変更
style = ttk.Style()
style.configure("BigLabel.TLabelframe.Label", font=("Meiryo", 12, "bold"))

# 都道府県複数選択
frame_prefs = ttk.LabelFrame(root, text="都道府県を選択（複数可）", padding=10, style="BigLabel.TLabelframe")
frame_prefs.pack(fill="both", expand=True, padx=10, pady=10)

root.update_idletasks()
layout_checkbuttons()
frame_prefs.bind("<Configure>", lambda e: layout_checkbuttons())

# 期間登録
frame_date = ttk.LabelFrame(root, text="期間を選択", padding=10, style="BigLabel.TLabelframe")
frame_date.pack(fill="x", padx=10, pady=10)

ttk.Label(frame_date, text="開始日 :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Label(frame_date, text="例: 2025-10-14", font=("Meiryo", 9), foreground="gray").grid(row=1, column=1, sticky="w", padx=5)
start_entry = ttk.Entry(frame_date, width=15)
start_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_date, text="終了日 :").grid(row=0, column=2, padx=5, pady=5, sticky="e")
end_entry = ttk.Entry(frame_date, width=15)
end_entry.grid(row=0, column=3, padx=5, pady=5)

# 決定ボタン
ttk.Button(root, text="応募する", command=submit).pack(pady=20)

root.mainloop()