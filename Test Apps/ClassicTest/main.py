from thumbyClassic import *

bmpBG = Bitmap("bg.bmp")
bmpLogo = Bitmap("logo.bmp", Color.MAGENTA)
bmpTankBtm = Bitmap("tankBtm.bmp", Color.MAGENTA)
bmpTankTop = Bitmap("tankTop.bmp", Color.MAGENTA)

sprTankBtm = Sprite(24, 24, bmpTankBtm)
sprTankTop = Sprite(24, 24, bmpTankTop)

#
#   Test Blit
#
def test_blit():
    x, y = 0, 0
    dx, dy = 0.85, 1
    mx, my = 0, 0
    
    while True:
        # Next test
        if Button.MENU.justPressed():
            break
        
        # Bounce around the screen
        x += dx
        y += dy
        if x < 0:
            x, dx, mx = 0, abs(dx), 0
        if y < 0:
            y, dy, my = 0, abs(dy), 0
        if x > WIDTH:
            x, dx, mx = WIDTH, -abs(dx), 1
        if y > HEIGHT:
            y, dy, my = HEIGHT, -abs(dy), 1

        Display.blit(bmpBG, 0, 0, 0, 0)
        Display.blit(bmpLogo, int(x)-24, int(y)-24, mx, my)
        Display.update()
        
#
#   Test Sprite
#
def test_sprite():
    x, y = 64, 64
    animBtm = 0
    aim = 0
    animTop = 0
   
    # Tables to convert aiming/moving into sprite states
    frameBtmLookup = [# dx, dy -> frame, mx, my
        [(2,1,1),(0,1,0),(2,1,0)], # -1
        [(4,0,1),(0,0,0),(4,0,0)], # 0
        [(2,0,1),(0,0,0),(2,0,0)] # 1
    ]
    frameTopLookup = [# aim -> frame, mx, my
        (0,0,0), # 0
        (3,0,0), # 1
        (6,0,0), # 2
        (3,1,0), # 3
        (0,1,0), # 4
        (3,1,1), # 5
        (6,0,1), # 6
        (3,0,1) # 7
    ]
   
    while True:
        # Next test
        if Button.MENU.justPressed():
            break
        
        # Player controls
        dx = 1 if Button.RIGHT.pressed() else -1 if Button.LEFT.pressed() else 0
        dy = 1 if Button.DOWN.pressed() else -1 if Button.UP.pressed() else 0
        daim = 1 if Button.RB.justPressed() else -1 if Button.LB.justPressed() else 0
        fire = Button.A.justPressed()
        
        # Screen boundaries
        x = max(0, min(WIDTH, x + dx))
        y = max(0, min(HEIGHT, y + dy))

        # Turret aiming
        aim = (aim + daim + 8) % 8
        
        # Bottom sprite
        if dx != 0 or dy != 0:
            sprTankBtm.frame, sprTankBtm.mirrorX, sprTankBtm.mirrorY = frameBtmLookup[dx+1][dy+1]
            animBtm = (animBtm + 1) % 2
            sprTankBtm.frame += animBtm
        sprTankBtm.x = x - 12
        sprTankBtm.y = y - 12
        
        # Top sprite
        sprTankTop.frame, sprTankTop.mirrorX, sprTankTop.mirrorY = frameTopLookup[aim]
        if fire:
            animTop = 5
        elif animTop > 0:
            animTop -= 1
        sprTankTop.frame += animTop//2
        sprTankTop.x = x - 12
        sprTankTop.y = y - 12
        
        Display.fill(Color.BROWN)
        Display.drawSprite(sprTankBtm)
        Display.drawSprite(sprTankTop)
        Display.update()
            
#
#   Test Font
#
def test_font():
    pass # TODO

#
#   Test Shapes
#
def test_shapes():
    pass # TODO
       
tests = [
    test_blit,
    test_sprite,
    test_font,
    test_shapes,
]

Display.setFPS(30)
while True:
    for test in tests:
        test()
        Display.update()