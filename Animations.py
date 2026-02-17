import tkinter as tk
import math
from PIL import Image, ImageTk
import time

def crossfade(canvas,frames_source,amount=30,backwards=False):
    frames = []
    for frame in range(amount):
        image = Image.open(f"{frames_source}/frame_{frame:03}.png")
        frames.append(ImageTk.PhotoImage(image))

    def update_frame(index):

        if index < len(frames) and not backwards:
            canvas.delete("all")
            canvas.create_image(0, 0, image=frames[index], anchor="nw")
            canvas.image = frames[index]
            canvas.after(2, lambda: update_frame(index+1))

        if backwards and index > 0:
            canvas.delete("all")
            canvas.create_image(0, 0, image=frames[index], anchor="nw")
            canvas.image = frames[index]
            canvas.after(2, lambda: update_frame(index-1))
    index = 0
    if backwards:
        index = amount-1
    update_frame(index)

def slide2(canvas,frames1_id,frame2_id,time_step,direction,steps,i=0):
    if steps <= 0:
        return
    # Easing: ease-in-out quad
    def ease_in_out_quad(t):
        if t < 0.5:
            return 2 * t * t
        return 1 - pow(-2 * t + 2, 2) / 2

    # Normalizowany postęp
    t = i / steps
    t_prev = (i - 1) / steps if i > 0 else 0.0

    eased = ease_in_out_quad(t)
    eased_prev = ease_in_out_quad(t_prev)

    # Całkowity dystans w pikselach (zgodnie z dotychczasową logiką: 2 px * steps)
    total_distance = 2* steps

    # Przesunięcie dla tego kroku (może być float)
    delta_pixels = (eased - eased_prev) * total_distance

    # Kierunek ruchu
    dx = 0
    dy = 0
    if direction == "left":
        dx = -delta_pixels
    elif direction == "right":
        dx = delta_pixels
    elif direction == "up":
        dy = -delta_pixels
    elif direction == "down":
        dy = delta_pixels

    # Wykonaj przesunięcie
    if dx != 0:
        canvas.move(frames1_id, dx, 0)
        canvas.move(frame2_id, dx, 0)
    if dy != 0:
        canvas.move(frames1_id, 0, dy)
        canvas.move(frame2_id, 0, dy)

    # Dostosuj delay (up/down wcześniej skalowało time_step)
    local_time_step = time_step
    if direction in ("up", "down"):
        local_time_step = int(time_step * 800 / 480)

    # Kontynuuj animację
    if i < steps:
        canvas.after(local_time_step, lambda: slide(canvas, frames1_id, frame2_id, time_step, direction, steps, i+1))


# ...existing code...
def slide(canvas, frames1_id, frame2_id, duration_ms=400, direction="left", fps=60):
    """
    Time-based slide with cubic ease-in-out.
    Backwards-compatible with old signature:
        slide(canvas, id1, id2, time_step, direction, steps)
    where duration_ms should be time_step*steps.
    """
    # Detect legacy call: small duration_ms and very large fps argument => treat as (time_step, steps)
    try:
        if isinstance(duration_ms, (int, float)) and isinstance(fps, (int, float)):
            if duration_ms < 50 and fps > 100:  # heuristic for legacy call
                time_step = float(duration_ms)
                steps = int(fps)
                duration_ms = max(1, int(time_step * steps))
                fps = 60
    except Exception:
        # w razie czego fallback na podane wartości
        pass

    # zabezpieczenie: wymuś aktualizację rozmiarów przed czytaniem
    canvas.update_idletasks()
    # startowe pozycje
    c1 = canvas.coords(frames1_id) or [0, 0]
    c2 = canvas.coords(frame2_id)  or [0, 0]
    sx1, sy1 = float(c1[0]), float(c1[1])
    sx2, sy2 = float(c2[0]), float(c2[1])

    # wymiary canvas (fallback)
    w = canvas.winfo_width() or int(canvas.cget("width") or 800)
    h = canvas.winfo_height() or int(canvas.cget("height") or 480)

    if direction == "left":
        total_dx, total_dy = -float(w), 0.0
    elif direction == "right":
        total_dx, total_dy = float(w), 0.0
    elif direction == "up":
        total_dx, total_dy = 0.0, -float(h)
    else:  # "down"
        total_dx, total_dy = 0.0, float(h)

    # cubic ease-in-out
    def ease_cubic(t):
        if t < 0.5:
            return 4.0 * t * t * t
        return 1.0 - pow(-2.0 * t + 2.0, 3) / 2.0

    frame_interval = max(1, int(1000 / max(1, fps)))
    start_time = time.time() * 1000.0

    def _step():
        now = time.time() * 1000.0
        elapsed = now - start_time
        t = min(max(elapsed / max(1, duration_ms), 0.0), 1.0)
        e = ease_cubic(t)

        nx1 = sx1 + e * total_dx
        ny1 = sy1 + e * total_dy
        nx2 = sx2 + e * total_dx
        ny2 = sy2 + e * total_dy

        canvas.coords(frames1_id, nx1, ny1)
        canvas.coords(frame2_id, nx2, ny2)

        if t < 1.0:
            canvas.after(frame_interval, _step)
        else:
            canvas.coords(frames1_id, sx1 + total_dx, sy1 + total_dy)
            canvas.coords(frame2_id, sx2 + total_dx, sy2 + total_dy)

    _step()
# ...existing code...