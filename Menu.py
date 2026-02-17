import tkinter as tk
import Time
import MenuWeather
import sys
from PIL import Image, ImageTk
import MenuIcon 
def create_menu(root,canvas,menu_frame_id,weather_frame_id,weather_frame):

    ## SETUP ##
    def kill_process():
        root.destroy()
        sys.exit()

    # Ustawienie boardera wokół okna 
    boarder = Image.open("Image/obramowka.png")
    icon_boarder = ImageTk.PhotoImage(boarder)
    boarder_label = tk.Label(root, image=icon_boarder, borderwidth=0, highlightthickness=0)
    boarder_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Górny Frame
    top_frame = tk.Frame(root, height=156,bg="#121212")
    top_frame.pack(side="top", fill="x",padx=4,pady=(4,0))

    # Środkowy Separator
    middle_frame = tk.Frame(root, height=4,bg="#121212")
    middle_frame.pack(side="top", fill="x",padx=4)

    # Dolny Frame
    bottom_frame = tk.Frame(root, height=272,bg="#121212")
    bottom_frame.pack(fill="both", expand=True,padx=4,pady=(0,4))     

    # Pogoda i zegar na górny frame
    MenuWeather.create_weather_widget(top_frame, 20)
    Time.create_time_widget(top_frame, 72,15)
    # Pasek separatora (700x4) na środku
    MenuIcon.create_separation_widget(middle_frame)

    # Ikony menu na dolnym frame
    empty_space = tk.Frame(bottom_frame, width=55, bg="#121212").pack(side="left",padx=0)
    MenuIcon.create_menu_widget(bottom_frame,"weather-app",18,"Pogoda",canvas,menu_frame_id,weather_frame_id,weather_frame)
    MenuIcon.create_menu_widget(bottom_frame,"schedule",18,"Kalendarz",canvas,menu_frame_id,weather_frame_id,weather_frame)
    MenuIcon.create_menu_widget(bottom_frame,"automation",18,"Automatyka",canvas,menu_frame_id,weather_frame_id,weather_frame)
    MenuIcon.create_menu_widget(bottom_frame,"settings",18,"Ustawienia",canvas,menu_frame_id,weather_frame_id,weather_frame)
