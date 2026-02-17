from PIL import Image

img1 = Image.open("num_24.png")
img2 = Image.open("number-24.png")

frames = 30  # liczba klatek przejścia
for i in range(frames+1):
    alpha = i / frames
    blended = Image.blend(img1, img2, alpha)
    blended.save(f"Number_24/frame_{i:03d}.png")