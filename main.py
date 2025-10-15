import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

root = tk.Tk()
root.title("シティリーグ一括応募ツール")
root.geometry("700x600")

#タイトル
ttk.Label(root, text="シティリーグ一括応募", font=("Meiryo", 14, "bold")).pack(pady=10)

#都道府県登録
PREFS = [
    "北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
    "茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
    "新潟県","富山県","石川県","福井県","山梨県","長野県",
    "岐阜県","静岡県","愛知県","三重県",
    "滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県",
    "鳥取県","島根県","岡山県","広島県","山口県",
    "徳島県","香川県","愛媛県","高知県",
    "福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"
]

def submit():
    selected = [pref for pref, var in pref_vars.items() if var.get()]
    start_str = start_entry.get().strip()
    end_str = end_entry.get().strip()

    if not selected:
        messagebox.showwarning("エラー", "少なくとも1つの都道府県を選択してください。")
        return
    if not start_str or not end_str:
        messagebox.showwarning("エラー", "開始日と終了日を入力してください。")
        return

    from datetime import datetime
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("エラー", "日付の形式が不正です。例: 2025-10-14")
        return

    if start_date > end_date:
        messagebox.showwarning("エラー", "終了日は開始日以降を選択してください。")
        return

    data = {
        "prefectures": selected,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }

    import os, json
    filepath = os.path.abspath("config.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("保存完了", f"設定を保存しました！\n保存場所: {filepath}")

def layout_checkbuttons():
    #ウィンドウ幅に応じてチェックボックスを再配置
    for widget in frame_prefs.winfo_children():
        widget.grid_forget()

    width = frame_prefs.winfo_width()
    if width < 200:
        width = 200

    btn_width = 120  #チェックボックスの幅目安
    cols = max(1, width // btn_width)

    for i, (pref, var) in enumerate(pref_vars.items()):
        row, col = divmod(i, cols)
        chk = ttk.Checkbutton(frame_prefs, text=pref, variable=var)
        chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)


# ラベルフレームのスタイル変更
style = ttk.Style()
style.configure("BigLabel.TLabelframe.Label", font=("Meiryo", 12, "bold"))

# 都道府県複数選択
frame_prefs = ttk.LabelFrame(root, text="都道府県を選択（複数可）", padding=10, style="BigLabel.TLabelframe")
frame_prefs.pack(fill="both", expand=True, padx=10, pady=10)

pref_vars = {pref: tk.IntVar() for pref in PREFS}

root.update_idletasks()
layout_checkbuttons()

# ウィンドウリサイズ時に再配置
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