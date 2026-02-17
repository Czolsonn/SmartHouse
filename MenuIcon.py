import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
import Animations


def create_menu_widget(root, image_name, font_size,label_text,canvas,frame_id_1,frame_id_2,frame_for_next): 
    try:
        image = Image.open(f"Image/{image_name}.png")
    except Exception as e:
        print(f"Błąd pobierania pliku {image_name}.png : {e}")
        return
    
    Roboto = font.Font(family="Roboto",size = font_size)
    photo = ImageTk.PhotoImage(image)

    # Komendy wywoływane po kliknięciu ikony
    def on_click():
        # Ikona weather
        if image_name == "weather-app":
            Animations.slide(canvas,frame_id_1,frame_id_2,2,"left",400)
        if image_name == "schedule":
            pass
        if image_name == "automation":
            pass
        if image_name == "settings":
            pass
        
    
    bg_color = root.cget("bg")
    label = tk.Frame(root, bg=bg_color, width=150, height=180)
    label.pack_propagate(False)  # NIE pozwól ramce zmieniać rozmiaru!
    label.pack(side="left", padx=10, pady=20)

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
        anchor="center",
    )
    button.pack(side="top", padx=0, pady=(10, 0))
    button.image = photo
    button.photo_big = photo_big

    button.bind("<ButtonPress-1>", enlarge)
    button.bind("<ButtonRelease-1>", restore)

    tekst = tk.Label(label, font=Roboto, bg=bg_color, fg="white", text=label_text, width=100, height=1, anchor="center")
    tekst.pack(side="top", padx=0, pady=10)

def create_separation_widget(frame):
    image = Image.open("Image/bialy_pasek_bez_tla.png")
    icon = ImageTk.PhotoImage(image)
    separation_label = tk.Label(frame, image=icon, bg="#121212")
    separation_label.image = icon
    separation_label.pack()

def icon(icon_path,frame,side,padx,pady):
    try:
        img = Image.open(icon_path)
        tk_img = ImageTk.PhotoImage(img)
        icon_label = tk.Label(frame, image=tk_img, bg="#121212")
        icon_label.image = tk_img
        icon_label.pack(side=side, padx=padx, pady=pady)
        return icon_label
    except Exception:
        tk.Label(frame, text="?", fg="white", bg="#121212").pack(side=side, padx=padx, pady=pady)

def row_with_icon(image_path, text, parent,font_size):
    row = tk.Frame(parent, bg="#121212")
    row.pack(side="top", pady=5, anchor="w",padx=(30,0))  # każdy wiersz pod spodem
    Roboto = font.Font(family="Roboto",size = font_size)

    # Ikona
    icon_label = icon(image_path, row, "left", (0,10), (0,0))

    # Tekst
    text_label = tk.Label(
        row,
        font=Roboto,
        text=text,
        fg="white",
        bg="#121212"
    )
    text_label.pack(side="left", padx=(0,0),pady=(3,0))

    return row