import tkinter as tk
from datetime import datetime

def create_time_widget(parent, Roboto, Roboto_small):
    bg_color = "#121212"

    time_label = tk.Label(parent, bg=bg_color)
    time_label.pack(side="right", padx=50, pady=(30,0))

    time = tk.Label(time_label, font= Roboto, bg=bg_color, fg="white")
    time.pack(side="top", padx=20, pady=(10, 0))

    date = tk.Label(time_label, font= Roboto_small, bg=bg_color, fg="white")
    date.pack(side="bottom", padx=10, pady=(0, 10))

    def update_time():
        time.config(text=datetime.now().strftime('%H:%M'))
        time.after(1000, update_time)

    def update_date():
        date.config(text=datetime.now().strftime('%A %d.%m.%Y'))
        date.after(60000, update_date)

    update_time()
    update_date()
