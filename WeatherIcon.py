import tkinter as tk
from PIL import Image, ImageTk
import os

def create_weather_widget(root,Roboto): 
    try:
        image = Image.open("Image/weather-app.png").resize((100,100))
    except Exception as e:
        print(f"Błąd pobierania pliku weather-app.png : {e}")
        return

    photo = ImageTk.PhotoImage(image)

    def on_click():
        print("Wciśnięty przycisk Pogody")
    
    bg_color = root.cget("bg")
    label = tk.Frame(root, bg=bg_color, width=200, height=180)
    label.pack_propagate(False)  # NIE pozwól ramce zmieniać rozmiaru!
    label.pack(side="left", padx=20, pady=20)

    photo_big = ImageTk.PhotoImage(image.resize((110, 110)))

    def enlarge(event):
        button.config(image=photo_big)
        #tekst.pack_configure(pady=18)  # większy odstęp

    def restore(event):
        button.config(image=photo)
        #tekst.pack_configure(pady=10)  # mniejszy odstęp

    button = tk.Button(
        label,
        image=photo,
        command=on_click,
        borderwidth=0,
        relief="flat",
        bg=bg_color,
        activebackground=bg_color,
        activeforeground="white",
        width=120,
        height=120,
        anchor="center"
    )
    button.pack(side="top", padx=0, pady=(10, 0))
    button.image = photo
    button.photo_big = photo_big

    button.bind("<ButtonPress-1>", enlarge)
    button.bind("<ButtonRelease-1>", restore)

    tekst = tk.Label(label, font=Roboto, bg=bg_color, fg="white", text="Pogoda", width=100, height=1, anchor="center")
    tekst.pack(side="top", padx=0, pady=10)