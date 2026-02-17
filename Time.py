import tkinter as tk
from datetime import datetime
from tkinter import font

def create_time_widget(parent, font_size_BIG, font_size_SMALL):
    bg_color = "#121212"

    Roboto = font.Font(family="Roboto",size= font_size_BIG)
    Roboto_small = font.Font(family="Roboto",size= font_size_SMALL)

    time_label = tk.Label(parent, bg=bg_color)
    time_label.pack(side="right", padx=50, pady=(30,0))

    time = tk.Label(time_label, font= Roboto, bg=bg_color, fg="white")
    time.pack(side="top", padx=20, pady=(10, 0))

    date = tk.Label(time_label, font= Roboto_small, bg=bg_color, fg="white")
    date.pack(side="bottom", padx=10, pady=(0, 10))

    def update_time():
        time.config(text=datetime.now().strftime('%H:%M'))
        time.after(100, update_time)

    def update_date():
        date.config(text=datetime.now().strftime('%A %d.%m.%Y'))
        date.after(100, update_date)

    update_time()
    update_date()
