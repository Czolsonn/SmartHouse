import tkinter as tk
import requests
from PIL import Image, ImageTk
import threading

API_KEY = "b23482a61b0f00b677789afa837d3826"
CITY = "Swidnica"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pl"

def create_weather_widget(parent, Roboto):
    bg_color = "#121212"

    frame = tk.Frame(parent, bg=bg_color)
    frame.pack(side="left", padx=50, pady=(50,0))

    icon_label = tk.Label(frame, bg=bg_color)
    icon_label.pack(side="left")

    weather_label = tk.Label(
        frame,
        text="Ładowanie...",
        font=Roboto,
        bg=bg_color,
        fg="white"
    )
    weather_label.pack(side="right", padx=(15, 10),pady=(70,0))

    def fetch_weather():
        try:
            res = requests.get(URL)
            data = res.json()
            print("Odpowiedź z API:", data)

            if "main" not in data:
                weather_label.config(text=f"Błąd: {data.get('message', 'Nieznany błąd')}")
                return

            temp = data["main"]["temp"]
            icon_id = data["weather"][0]["icon"]
            weather_label.config(text=f"{temp:.1f} °C")

            try:
                image = Image.open(f"Image/weather_icons/{icon_id}.png").resize((164, 164))
                icon = ImageTk.PhotoImage(image)
                icon_label.config(image=icon)
                icon_label.image = icon
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
