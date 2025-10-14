import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

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
    start = start_cal.get_date()
    end = end_cal.get_date()
    if not selected:
        messagebox.showwarning("エラー", "少なくとも1つの都道府県を選択してください。")
        return
    if start > end:
        messagebox.showwarning("エラー", "終了日は開始日以降を選択してください。")
        return
    messagebox.showinfo("設定完了", f"都道府県: {', '.join(selected)}\n期間: {start} ～ {end}")

def layout_checkbuttons():
    """ウィンドウ幅に応じてチェックボックスを再配置"""
    for widget in frame_prefs.winfo_children():
        widget.grid_forget()

    width = frame_prefs.winfo_width()
    if width < 200:
        width = 200

    btn_width = 120  # 1つのチェックボックスの幅目安
    cols = max(1, width // btn_width)

    for i, (pref, var) in enumerate(pref_vars.items()):
        row, col = divmod(i, cols)
        chk = ttk.Checkbutton(frame_prefs, text=pref, variable=var)
        chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)

root = tk.Tk()
root.title("シティリーグ一括応募ツール")
root.geometry("700x600")

# ===== タイトル =====
ttk.Label(root, text="シティリーグ一括応募", font=("Meiryo", 14, "bold")).pack(pady=10)

# ===== ラベルフレームのスタイル変更 =====
style = ttk.Style()
style.configure("BigLabel.TLabelframe.Label", font=("Meiryo", 12, "bold"))

# ===== 都道府県選択エリア =====
frame_prefs = ttk.LabelFrame(root, text="都道府県を選択（複数可）", padding=10, style="BigLabel.TLabelframe")
frame_prefs.pack(fill="both", expand=True, padx=10, pady=10)

pref_vars = {pref: tk.IntVar() for pref in PREFS}

root.update_idletasks()
layout_checkbuttons()

# ウィンドウリサイズ時に再配置
frame_prefs.bind("<Configure>", lambda e: layout_checkbuttons())

# 期間入力
frame_date = ttk.LabelFrame(root, text="期間を選択", padding=10, style="BigLabel.TLabelframe")
frame_date.pack(fill="x", padx=10, pady=10)

ttk.Label(frame_date, text="開始日 :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Label(frame_date, text="例: 2025-10-14", font=("Meiryo", 9), foreground="gray").grid(row=1, column=1, sticky="w", padx=5)
start_entry = ttk.Entry(frame_date, width=15)
start_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_date, text="終了日 :").grid(row=0, column=2, padx=5, pady=5, sticky="e")
ttk.Label(frame_date, text="例: 2025-10-20", font=("Meiryo", 9), foreground="gray").grid(row=1, column=1, sticky="w", padx=5)
end_entry = ttk.Entry(frame_date, width=15)
end_entry.grid(row=0, column=3, padx=5, pady=5)

# ===== 決定ボタン =====
ttk.Button(root, text="応募する", command=submit).pack(pady=20)

root.mainloop()