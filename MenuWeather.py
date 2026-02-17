import tkinter as tk
import requests
from PIL import Image, ImageTk
import threading
from tkinter import font

API_KEY = "b23482a61b0f00b677789afa837d3826"
CITY = "Swidnica"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pl"

def create_weather_widget(parent, font_size):
    bg_color = "#121212"
    Roboto = font.Font(family="Roboto", size=font_size)
    frame = tk.Frame(parent, bg=bg_color)
    frame.pack(side="left", padx=50, pady=(50, 0))

    icon_label = tk.Label(frame, bg=bg_color)
    icon_label.pack(side="left")

     # --- Kolumna z lokalizacją i temperaturą ---
    temp_col = tk.Frame(frame, bg=bg_color)
    temp_col.pack(side="left", padx=(15, 0), pady=(50, 0))

    # Wiersz: ikona lokalizacji + napis
    location_row = tk.Frame(temp_col, bg=bg_color)
    location_row.pack(side="top", pady=(0, 8))

    local_icon_img = Image.open("Image/local.png")
    local_icon_tk = ImageTk.PhotoImage(local_icon_img)
    local_icon_label = tk.Label(location_row, image=local_icon_tk, bg=bg_color)
    local_icon_label.image = local_icon_tk
    local_icon_label.pack(side="left", padx=(0, 5))

    location_label = tk.Label(location_row, text="Świdnica", font=Roboto, bg=bg_color, fg="white")
    location_label.pack(side="left")

    # Ikona temperatury
    temp_icon_img = Image.open("Image/temp.png")
    temp_icon_tk = ImageTk.PhotoImage(temp_icon_img)
    temp_icon_label = tk.Label(temp_col, image=temp_icon_tk, bg=bg_color)
    temp_icon_label.image = temp_icon_tk
    temp_icon_label.pack(side="left", pady=(0, 0))

    # Temperatura
    weather_label = tk.Label(
        temp_col,
        text="Ładowanie...",
        font=Roboto,
        bg=bg_color,
        fg="white"
    )
    weather_label.pack(side="left", padx=(5, 10), pady=(0, 0), anchor="center")

    def fetch_weather():
        try:
            res = requests.get(URL)
            data = res.json()

            if "main" not in data:
                weather_label.config(text=f"Błąd: {data.get('message', 'Nieznany błąd')}")
                return

            temp = data["main"]["temp"]
            icon_id = data["weather"][0]["icon"]
            weather_label.config(text=f"{temp:.1f} °C")

            try:
                image = Image.open(f"Image/weather_icons/{icon_id}.png")
                image_tk = ImageTk.PhotoImage(image)
                icon_label.config(image=image_tk)
                icon_label.image = image_tk
            except Exception as e:
                print(f"Błąd ładowania ikony: {e}")
                weather_label.config(text=f"{temp:.1f} °C")

        except Exception as e:
            print("Błąd pobierania pogody:", e)
            weather_label.config(text="Błąd pobierania")

    def refresh():
        threading.Thread(target=fetch_weather).start()
        frame.after(600000, refresh)  # co 10 minut

    refresh()