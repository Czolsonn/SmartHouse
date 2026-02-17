import tkinter as tk
import Menu
import Weather
import WeatherCollections


def create_root():
    # Wejście w tryb boarder_less
    def enter_fullscreen():
        root.overrideredirect(True)
        root.focus_force()


    # Utworzenie głównego okna
    root = tk.Tk()
    root.title("Smart House")
    root.configure(bg="#121212") # Ustawienie koloru tła
    root.geometry("800x480")  # Wymiary ekranu
    # Canvas do nakładania elementów Menu w celu animacji
    canvas = tk.Canvas(root, width=800, height=480, bg="#121212", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    menu_frame = tk.Frame(canvas, bg="#121212", width=800, height=480)
    menu_frame_id = canvas.create_window(0, 0, anchor="nw", window=menu_frame, width=800, height=480)

    weather_frame = tk.Frame(canvas, bg="#121212", width=800, height=480)
    weather_frame_id = canvas.create_window(800, 0, anchor="nw", window=weather_frame, width=800, height=480)

    Menu.create_menu(menu_frame,canvas,menu_frame_id,weather_frame_id,weather_frame)

    def fetch_and_update():
        new_data = WeatherCollections.read_data_from_server()
        if new_data is None:
            # jeśli błąd, spróbuj ponownie później
            root.after(600_000, fetch_and_update)
            return
        # wyczyść poprzednie widgety wewnątrz weather_frame
        for w in weather_frame.winfo_children():
            w.destroy()
        # zbuduj UI na nowo z nowymi danymi
        Weather.create_weather_menu(weather_frame, new_data,canvas,weather_frame_id,menu_frame_id)
        # zaplanuj kolejne odświeżenie za 10 minut (600000 ms)
        root.after(600_000, fetch_and_update)

    root.after(0,fetch_and_update)

    root.after(50, enter_fullscreen)
    root.mainloop()

if __name__ == "__main__":
    create_root()
