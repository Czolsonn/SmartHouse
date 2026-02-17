import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from WeatherCollections import get_5day_forecast,get_current_weather, get_current_date, unix_to_time, get_hourly_forecast
from MenuIcon import create_separation_widget,icon,row_with_icon
import sys
from Animations import crossfade,slide

clicked_hourly = False

def create_weather_menu(root,weather_data,canvas,weather_frame_id,menu_frame_id):
    ## SETUP ##

    # upewnij się, że ramka ma zadany rozmiar i nie zmienia go automatycznie
    root.config(width=800, height=480)
    root.pack_propagate(False)

    # Funkcja zamykająca aplikację
    def kill_process():
        root.destroy()
        sys.exit()

    # Ustawienia czcionki
    Roboto = font.Font(family="Roboto",size = 12)
    
    ## GUI -  OBRAMÓWKA, AKTUALNA POGODA, PRZEWIDYWANA POGODA ##
    # Tworzymy obramówkę 
    boarder = Image.open("Image/obramowka.png")
    icon_boarder = ImageTk.PhotoImage(boarder)
    boarder_label = tk.Label(root, image=icon_boarder, borderwidth=0, highlightthickness=0)
    boarder_label.image = icon_boarder
    boarder_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Ramka na menu pogody
    forecast_frame = tk.Frame(root, bg="#121212")
    forecast_frame.pack(fill="both", padx=4, pady=4,expand=True)  # TO JEST OK!

    top_frame = tk.Frame(forecast_frame, height=316,bg="#121212")
    top_frame.pack(side="top", fill="x")
    top_frame.pack_propagate(False)  # NIE pozwól ramce zmieniać rozmiaru!

    separation_frame = tk.Frame(forecast_frame, height=4,bg="#121212")
    separation_frame.pack(side="top", fill="x")
    separation_frame.pack_propagate(False)  # NIE pozwól ramce zmieniać rozmiaru!

    bottom_frame = tk.Frame(forecast_frame, height=160,bg="#121212")
    bottom_frame.pack(side="bottom", fill="x")
    bottom_frame.pack_propagate(False)  # NIE pozwól ramce zmieniać rozmiaru!

    # Aktualna pogoda
    create_current_weather_widget(top_frame,bottom_frame,12,16, 20,28,weather_data,canvas,weather_frame_id,menu_frame_id)
    # Przewidywana pogoda forecast daily
    create_forecast_weather_widget(bottom_frame,12,weather_data,canvas,weather_frame_id,menu_frame_id)
    create_separation_widget(separation_frame)
   
#Funkcja tworząca widget z aktualną pogodą zawierającą:
# - ikonę pogody
# - lokalizację
# - datę
# - aktualną temperaturę
# - odczuwalną temperaturę
# - dane dodatkowe (wilgotność, ciśnienie, wiatr)
def create_current_weather_widget(frame,bottom_frame, font_size_3 ,font_size_2, font_size_1, font_size,weather_data,canvas,weather_frame_id,menu_frame_id):
    ## SETUP ##
    # Ustawienia czcionki
    Roboto = font.Font(family="Roboto", size=font_size,weight="bold")
    font_1 = font.Font(family="Roboto", size=font_size_1, weight="bold")
    font_2 = font.Font(family="Roboto", size=font_size_2)
    font_3 = font.Font(family="Roboto", size=font_size_3)

    # Wczytywanie danych pogody z WeatherCollections
    day_results = get_current_weather(weather_data)

    ## PRAWA STRONA WIDGETU - LOKALIZACJA, DATA, TEMPERATURA AKTUALNA##
    # Główny kontener dla lewej kolumny
    left_column = tk.Frame(frame, bg="#121212")
    left_column.pack(side="left", padx=(20,0), pady=20)

    # Lokalizacja i Data Frame
    location_frame = tk.Frame(left_column, bg="#121212", width=220, height=170)
    location_frame.pack(side="top", pady=(0,20))
    location_frame.pack_propagate(False)

    # Ikona Lokalizacji
    location_icon_label = icon("Image/local.png",location_frame,"left",(10,0),(0,136))

    # Ramka na teksty (nazwa + data)
    text_frame = tk.Frame(location_frame, bg="#121212")
    text_frame.pack(side="left", padx=10, pady=(0,20))

    # Nazwa Lokalizacji
    location_label = tk.Label(text_frame, font=font_1, text="Świdnica", fg="white", bg="#121212")    
    location_label.pack(anchor="w",pady=(0,0))  # góra w ramce

    # Data
    current_date = get_current_date()
    date_label = tk.Label(text_frame,font=font_2,text=f"{current_date['day_number']} {current_date['month_name']}\n{current_date['day_name']}",fg="white",bg="#121212")
    date_label.pack(anchor="w",pady= (20,50))  # pod nazwą

    temp_frame = tk.Frame(left_column, bg="#121212", width=250, height=100)
    temp_frame.pack(side="top")
    temp_frame.pack_propagate(False)
    
    # Ikona temperatury
    temp_icon_label = icon("Image/temp_64p.png",temp_frame,"left",(20,0),0) 

    # Ramka na wartości temperatury
    temp_number_frame = tk.Frame(temp_frame, bg="#121212")
    temp_number_frame.pack(side="left", padx=(20,0))

    # Temperatura aktualna
    temp_label = tk.Label(temp_number_frame,font=Roboto,text=f"{day_results[0]['temp']:.0f}°",fg="white",bg="#121212")
    temp_label.pack(side="top", padx=(0,76), pady=(8,0))

    # Temperatura odczuwalna
    feels_like_label = tk.Label(temp_number_frame,font=font_3,text=f"Odczuwalna {day_results[0]['feels_like']:.0f}°",fg="gray",bg="#121212")
    feels_like_label.pack(side="top", padx=(0,24), pady=(0,8))

    ## ŚRODKOWA STRONA WIDGETU - IKONA POGODY##
    # Główny kontener dla środkowej kolumny
    middle_column = tk.Frame(frame, bg="#121212", width=300, height=340)
    middle_column.pack(side="left", padx=0, pady=(10,0))
    middle_column.pack_propagate(False)

    # Ikona pogody
    icon(f"Image/weather_icons/256p/{day_results[0]['icon']}.png",middle_column,"top",0,0)
    create_switch_forecast_widget(middle_column,bottom_frame,weather_data,canvas,weather_frame_id,menu_frame_id)

    ## PRAWA STRONA WIDGETU - OPIS I DANE DODATKOWE POGODY ##
    # Prawa kolumna - opis pogody i dane dodatkowe
    right_column = tk.Frame(frame, bg="#121212")
    right_column.pack(side="left", padx=(0,20), pady=20)

    # Tworzymy wiersze po kolei
    row_with_icon("Image/sunrise.png",   f"{unix_to_time(day_results[0]['sunrise'])}",   right_column, font_size_2)
    row_with_icon("Image/sunset.png",    f"{unix_to_time(day_results[0]['sunset'])}",    right_column, font_size_2)
    row_with_icon("Image/humidity.png",  f"{day_results[0]['humidity']} %", right_column, font_size_2)
    row_with_icon("Image/windy.png",     f"{day_results[0]['wind_speed']} m/s", right_column, font_size_2)
    row_with_icon("Image/barometer.png", f"{day_results[0]['pressure']} hPa",  right_column, font_size_2)





# Funkcja tworząca widget z prognozą pogody na 5 dni zawierającą:
# - dzień tygodnia
# - temperaturę maksymalną i minimalną
# - ikonę pogody
def create_forecast_weather_widget(frame, font_size,weather_data,canvas,weather_frame_id,menu_frame_id):

    ## SETUP ##
    # Ustawienia czcionki
    Roboto = font.Font(family="Roboto", size=font_size)

    # Wczytywanie danych pogody z WeatherCollections
    five_day_results = get_5day_forecast(weather_data)

    ## FORECAST NASTĘPNYCH DNI - LEWE PRAWE WYPEŁNIENIE, 5 DNI POGODY WCZYTYWANE##
    # Dodaj przycisk powrotu
    exit_button_image = ImageTk.PhotoImage(Image.open("Image/back-button.png"))
    exit_button = tk.Canvas(frame, bg="#121212", width=exit_button_image.width(), height=exit_button_image.height(), highlightthickness=0, bd=0)
    exit_button.pack(side="left", pady=(80,10),padx=(20,10))
    exit_button.create_image(0,0,image=exit_button_image,anchor="nw")
    exit_button.image = exit_button_image
    exit_button.bind("<Button-1>", lambda e: slide(canvas, weather_frame_id, menu_frame_id, 2, "right", 400))

    # Iteracja po wynikach pogody i tworzenie widgetów
    for day in five_day_results:
        # Ramka dla każdego dnia
        day_frame = tk.Frame(frame, bg="#121212")
        day_frame.pack(side="left", padx=0, pady=10)

        # Ikona pogody
        icon_label = icon(f"Image/weather_icons/64p/{day['icon_id']}.png",day_frame,"top",0,(10,0))

        # Dzień tygodnia
        tk.Label(day_frame, font=Roboto, text=day["day"], fg="white", bg="#121212").pack()
        # Maksymalna temperatura
        tk.Label(day_frame, font=Roboto, text=f"{day['max_temp']:.0f}°", fg="white", bg="#121212").pack(side="left",padx=(40,0))
        # Minimalna temperatura
        tk.Label(day_frame, font=Roboto, text=f"{day['min_temp']:.0f}°", fg="gray", bg="#121212").pack(side="right",padx=(0,40))

    # Dodaj pustą ramkę po prawej, która się rozszerza
    tk.Frame(frame, bg="#121212").pack(side="left", fill="both", expand=True)

# Funkcja tworząca widget z przełącznikiem między prognozą 5 dniową a prognozą godzinową
# Składa się z dwóch przycisków z ikonami "24" i "3"
def create_switch_forecast_widget(frame,bottom_frame,weather_data,canvas,weather_frame_id,menu_frame_id):
    ## SETUP ##
    switch_frame = tk.Frame(frame, bg="#121212")
    switch_frame.pack(side="top")

    # Wczytywanie obrazków przycisków
    daily_image = Image.open("Image/number-24.png")
    daily_image_tk = ImageTk.PhotoImage(daily_image)
    hourly_image = Image.open("Image/num_3.png")
    hourly_image_tk = ImageTk.PhotoImage(hourly_image)

    # Tworzenie przycisków
    # Przycisk 3-godzinny
    hourly_button = tk.Canvas(switch_frame, width=hourly_image.width, height=hourly_image.height, highlightthickness=0, bd=0, bg="#121212")
    hourly_button.pack(side="left", padx=(0,70),pady=(0,10))
    hourly_button.create_image(0, 0, image=hourly_image_tk, anchor="nw")
    hourly_button.image = hourly_image_tk

    # Przycisk 24-godzinny
    daily_button = tk.Canvas(switch_frame, width=daily_image.width, height=daily_image.height, highlightthickness=0, bd=0, bg="#121212")
    daily_button.pack(side="right", padx=(0,45),pady=(0,10))
    daily_button.create_image(0, 0, image=daily_image_tk, anchor="nw")
    daily_button.image = daily_image_tk

    # Event kliknięcia przycisku 3-godzinnego
    def on_hourly_click(event):
        global clicked_hourly
        if clicked_hourly:
            return
        crossfade(hourly_button, "Animations/Number_3",30)
        crossfade(daily_button, "Animations/Number_24",30,backwards=True)
        clicked_hourly = True
        update_forecast_widgets(bottom_frame,weather_data,canvas,weather_frame_id,menu_frame_id)

    # Event kliknięcia przycisku 24-godzinnego
    def on_daily_click(event):
        global clicked_hourly
        if not clicked_hourly:
            return
        crossfade(daily_button, "Animations/Number_24",30)
        crossfade(hourly_button, "Animations/Number_3",30,backwards=True)
        clicked_hourly = False
        update_forecast_widgets(bottom_frame,weather_data,canvas,weather_frame_id,menu_frame_id)

    # Podpinamy eventy do przycisków
    hourly_button.bind("<Button-1>", on_hourly_click)
    daily_button.bind("<Button-1>", on_daily_click)

# Funkcja tworząca widget z prognozą pogody na najbliższe godziny zawierającą:
# - godzinę
# - temperaturę maksymalną i minimalną
# - ikonę pogody
def create_hourly_forecast_widget(frame,font_size,weather_data,canvas,weather_frame_id,menu_frame_id):

    ## SETUP ##
    # Ustawienia czcionki
    Roboto = font.Font(family="Roboto", size=font_size)

    # Wczytywanie danych pogody z WeatherCollections
    hourly_result = get_hourly_forecast(weather_data)

    ## FORECAST NASTĘPNYCH GODZIN - LEWE PRAWE WYPEŁNIENIE, 5 DNI POGODY WCZYTYWANE##
    # Dodaj pustą ramkę po lewej, która się rozszerza
    exit_button_image = ImageTk.PhotoImage(Image.open("Image/back-button.png"))
    exit_button = tk.Canvas(frame, bg="#121212", width=exit_button_image.width(), height=exit_button_image.height(), highlightthickness=0, bd=0)
    exit_button.pack(side="left", pady=(80,10),padx=(20,10))
    exit_button.create_image(0,0,image=exit_button_image,anchor="nw")
    exit_button.image = exit_button_image
    exit_button.bind("<Button-1>", lambda e: slide(canvas, weather_frame_id, menu_frame_id, 2, "right", 400))
   

    # Iteracja po wynikach pogody i tworzenie widgetów
    for hours in hourly_result[:5]:
        # Ramka dla każdego 3 godzinnego okresu
        hours_frame = tk.Frame(frame, bg="#121212")
        hours_frame.pack(side="left", padx=0, pady=10)

        # Ikona pogody
        icon_label = icon(f"Image/weather_icons/64p/{hours['icon_id']}.png",hours_frame,"top",0,(10,0))

        # Godzinny timestamp
        tk.Label(hours_frame, font=Roboto, text=hours["time"], fg="white", bg="#121212").pack()
        # Maksymalna temperatura
        tk.Label(hours_frame, font=Roboto, text=f"{hours['temp_max']:.0f}°", fg="white", bg="#121212").pack(side="left",padx=(40,0))
        # Minimalna temperatura
        tk.Label(hours_frame, font=Roboto, text=f"{hours['temp_min']:.0f}°", fg="gray", bg="#121212").pack(side="right",padx=(0,40))

    # Dodaj pustą ramkę po prawej, która się rozszerza
    tk.Frame(frame, bg="#121212").pack(side="left", fill="both", expand=True)

# Przejście między widokiem prognozy 5 dniowej a prognozą godzinową
def update_forecast_widgets(bottom_frame,weather_data,canvas,weather_frame_id,menu_frame_id):
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    
    if clicked_hourly:
        create_hourly_forecast_widget(bottom_frame,12,weather_data,canvas,weather_frame_id,menu_frame_id)
    else:
        create_forecast_weather_widget(bottom_frame,12,weather_data,canvas,weather_frame_id,menu_frame_id)