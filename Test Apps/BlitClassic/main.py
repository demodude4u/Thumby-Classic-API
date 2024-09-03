from thumbyClassic import Display, Bitmap, Color, WIDTH, HEIGHT

key = Color.MAGENTA
bmpIcon = Bitmap("icon.bmp")
bmpBG = Bitmap("bg.bmp")

x, y = 0, 0
dx, dy = 0.8, 1
mx, my = 0, 0
while True:
    Display.blit(bmpBG, 0, 0)
    
    x += dx
    y += dy
    if x < 0:
        x, dx, mx = 0, abs(dx), 0
    if y < 0:
        y, dy, my = 0, abs(dy), 0
    if x + bmpIcon.width > WIDTH:
        x, dx, mx = WIDTH - bmpIcon.width, -abs(dx), 1
    if y + bmpIcon.height > HEIGHT:
        y, dy, my = HEIGHT - bmpIcon.height, -abs(dy), 1
        
    Display.blit(bmpIcon, x, y, key, mx, my)
    
    Display.update()