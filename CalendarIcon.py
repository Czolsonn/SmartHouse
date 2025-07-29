import tkinter as tk
from PIL import Image, ImageTk
import os

def create_calendar_widget(root,Roboto): 
    try:
        image = Image.open("Image/schedule.png").resize((100,100))
    except Exception as e:
        print(f"Błąd pobierania pliku schedule.png : {e}")
        return

    photo = ImageTk.PhotoImage(image)

    def on_click():
        print("Wciśnięty przycisk Kalendarza")
    
    bg_color = root.cget("bg")

    button = tk.Button(
        root, 
        text="\nKalendarz",
        compound="top",  # <-- tekst pod obrazkiem
        image = photo,
        command=on_click,
        font = Roboto, 
        borderwidth=0,
        relief="flat",         # płaski styl (bez wciśnięcia)
        bg = bg_color,            # tło
        activebackground= bg_color,
        fg="white",            # <--- kolor tekstu
        activeforeground="white",# tło po najechaniu (hover)
    )
    button.pack(side = "left" , expand= "true" ,padx=20,pady=20)
    button.image = photo
    