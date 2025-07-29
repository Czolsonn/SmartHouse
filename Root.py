import tkinter as tk
from tkinter import font
import Time
import Weather
import sys
from PIL import Image, ImageTk
import CalendarIcon
import WeatherIcon
import CameraIcon

def create_root():
    def enter_fullscreen():
        root.overrideredirect(True)
        #root.attributes("-fullscreen", True)
        root.focus_force()

    def kill_process():
        root.destroy()
        sys.exit()

    root = tk.Tk()
    root.title("Smart House – Test")
    root.configure(bg="#121212")
    root.geometry("800x480")  # dopasowane do ekranu

    # GÓRNA CZĘŚĆ
    top_frame = tk.Frame(root, height=160, bg="#121212")
    top_frame.pack(side="top", fill="x")

    # ŚRODKOWY SEPARATOR
    middle_frame = tk.Frame(root, height=4, bg="#121212")
    middle_frame.pack(side="top", fill="x")

    # DOLNY PANEL
    bottom_frame = tk.Frame(root, height=276, bg="#121212")
    bottom_frame.pack(fill="both", expand=True)

    # Czcionka
    Roboto_small = font.Font(family="Roboto",size=12)
    Roboto_medium = font.Font(family="Roboto",size= 24)
    Roboto_big = font.Font(family="Roboto",size = 72)        

    # Pogoda i zegar
    Weather.create_weather_widget(top_frame, Roboto_medium)
    Time.create_time_widget(top_frame, Roboto_big,Roboto_small)

    # Pasek separatora (700x4)
    image = Image.open("Image/bialy_pasek_bez_tla.png")
    icon = ImageTk.PhotoImage(image)
    separation_label = tk.Label(middle_frame, image=icon, bg="#121212")
    separation_label.image = icon
    separation_label.pack()

    # DOLNE KAFELKI
    CalendarIcon.create_calendar_widget(bottom_frame,Roboto_small)
    WeatherIcon.create_weather_widget(bottom_frame,Roboto_small)
    CameraIcon.create_camera_widget(bottom_frame,Roboto_small)

    # Przycisk wyjścia
    kill_button = tk.Button(root, text="Zamknij", font=("Arial", 10), command=kill_process, bg="red", fg="white")
    kill_button.pack(side="bottom", pady=5)

    root.after(50, enter_fullscreen)
    root.mainloop()

if __name__ == "__main__":
    create_root()
