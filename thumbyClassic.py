import engine_main

import engine
import engine_io
import engine_draw

from engine_resources import TextureResource

import framebuf

class Button:
    #TODO access pin directly instead through engine
    def __init__(self,btn):
        self.btn = btn
    @micropython.native
    def pressed(self) -> bool:
        return self.btn.is_pressed
    @micropython.native
    def justPressed(self) -> bool:
        return self.btn.is_just_pressed
Button.A = Button(engine_io.A)
Button.B = Button(engine_io.B)
Button.U = Button(engine_io.UP)
Button.D = Button(engine_io.DOWN)
Button.L = Button(engine_io.LEFT)
Button.R = Button(engine_io.RIGHT)
Button.LB = Button(engine_io.LB)
Button.RB = Button(engine_io.RB)
Button.MENU = Button(engine_io.MENU)

class Color:
    BLACK = const(0x0000)
    NAVY = const(0x000F)
    DARKGREEN = const(0x03E0)
    DARKCYAN = const(0x03EF)
    MAROON = const(0x7800)
    PURPLE = const(0x780F)
    OLIVE = const(0x7BE0)
    LIGHTGREY = const(0xD69A)
    DARKGREY = const(0x7BEF)
    BLUE = const(0x001F)
    GREEN = const(0x07E0)
    CYAN = const(0x07FF)
    RED = const(0xF800)
    MAGENTA = const(0xF81F)
    YELLOW = const(0xFFE0)
    WHITE = const(0xFFFF)
    ORANGE = const(0xFDA0)
    GREENYELLOW = const(0xB7E0)
    PINK = const(0xFE19)
    BROWN = const(0x9A60)
    GOLD = const(0xFEA0)
    SILVER = const(0xC618)
    SKYBLUE = const(0x867D)
    VIOLET = const(0x915C)

class Bitmap(TextureResource):
    @micropython.native
    def __init__(self, filepath, writable=False):
        super().__init__(self, filepath, writable)

class Font(TextureResource):
    @micropython.native
    def __init__(self, filepath, width:int, height:int, gap:int=1):
        super().__init__(self, filepath, False)
        self.width = width
        self.height = height
        self.gap = gap

class Sprite:
    @micropython.native
    def __init__(self, width:int, height:int, bitmap, 
                 x:int=0, y:int=0, key:int=-1, mirrorX:int=0, mirrorY:int=0, 
                 frame:int=0):
        self.width = width
        self.height = height
        self.bitmap = bitmap
        self.x = x
        self.y = y
        self.key = key
        self.mirrorX = mirrorX 
        self.mirrorY = mirrorY 
        self.frame = frame

WIDTH = const(128)
HEIGHT = const(128)

class Display:
    _fb = engine_draw.back_fb()
    _fbData = engine_draw.back_fb_data()

    @micropython.viper
    def setFPS(fps):
        engine.fps_limit(fps)

    @micropython.viper
    def setFont(font):
        pass #TODO
    @micropython.viper
    def drawText(string, x:int, y:int, color:int):
        pass #TODO

    @micropython.viper
    def fill(color:int):
        buf32 = ptr32(Display._fbData)
        v32 = (color<<16) | color
        for i in range((WIDTH*HEIGHT)//2):
            buf32[i] = v32

    @micropython.viper
    def setPixel(x:int, y:int, color:int):
        buf = ptr16(Display._fbData)
        buf[y*WIDTH+x] = color
    @micropython.viper
    def getPixel(x:int, y:int) -> int:
        buf = ptr16(Display._fbData)
        return buf[y*WIDTH+x]

    @micropython.native
    def drawLine(x1:int, y1:int, x2:int, y2:int, color:int):
        Display._fb.line(x1, y1, x2, y2, color)
    @micropython.native
    def drawFilledRectangle(x:int, y:int, w:int, h:int, color:int):
        Display._fb.rect(x, y, w, h, color, True)
    @micropython.native
    def drawRectangle(x:int, y:int, w:int, h:int, color:int):
        Display._fb.rect(x, y, w, h, color, False)

    @micropython.viper
    def blit(bitmap, x:int, y:int, key:int=-1, mirrorX:int=0, mirrorY:int=0):
        buf = ptr16(_fbData)
        width = int(bitmap.width)
        height = int(bitmap.height)
        bitmap = ptr16(bitmap.data)

        if x >= WIDTH or (x+width) <= 0 or \
                y >= HEIGHT or (y+height) <= 0:
            return
        
        srcX = 0
        srcY = 0
        dstX = x
        dstY = y

        if x < 0:
            srcX -= x
            dstX -= x
            width += x
        if (x+width) >= WIDTH:
            width -= (x+width) - WIDTH
        if y < 0:
            srcY -= y
            dstY -= y
            height += y
        if (y+height) >= HEIGHT:
            height -= (y+height) - HEIGHT
        
        if mirrorY > 0:
            si = (srcY+height-1) * width + srcX
            srcGap = -width*2
        else:
            si = srcY * width + srcX
            srcGap = 0
        if mirrorX > 0:
            si += width-1
            sdi = -1
        else:
            sdi = 1
        di = dstY * WIDTH + dstX
        dstGap = WIDTH - width        
        for _ in range(height):
            for _ in range(width):
                c = bitmap[si] & 0xFFFF
                if c != key:
                    buf[di] = c
                si += sdi
                di += 1
            si += srcGap
            di += dstGap
    
    @micropython.viper
    def drawSprite(sprite):
        buf = ptr16(Display._fbData)
        width = int(sprite.width)
        height = int(sprite.height)
        bitmap = ptr16(sprite.bitmap.data)
        bitmapWidth = int(sprite.bitmap.width)
        x = int(sprite.x)
        y = int(sprite.y)
        key = int(sprite.key)
        mirrorX = int(sprite.mirrorX)
        mirrorY = int(sprite.mirrorY) 
        frame = int(sprite.frame)

        if x >= WIDTH or (x+width) <= 0 or \
                y >= HEIGHT or (y+height) <= 0:
            return
        
        if frame > 0:
            span = bitmapWidth // width
            row = frame // span
            col = frame % span
            srcX = col * width
            srcY = row * height
        else:
            srcX = 0
            srcY = 0
        dstX = x
        dstY = y

        if x < 0:
            srcX -= x
            dstX -= x
            width += x
        if (x+width) >= WIDTH:
            width -= (x+width) - WIDTH
        if y < 0:
            srcY -= y
            dstY -= y
            height += y
        if (y+height) >= HEIGHT:
            height -= (y+height) - HEIGHT
        
        if mirrorY > 0:
            si = (srcY+height-1) * bitmapWidth + srcX
            srcGap = width - bitmapWidth
        else:
            si = srcY * bitmapWidth + srcX
            srcGap = bitmapWidth - width
        if mirrorX > 0:
            si += width-1
            sdi = -1
        else:
            sdi = 1
        di = dstY * WIDTH + dstX
        dstGap = WIDTH - width        
        for _ in range(height):
            for _ in range(width):
                c = bitmap[si] & 0xFFFF
                if c != key:
                    buf[di] = c
                si += sdi
                di += 1
            si += srcGap
            di += dstGap
            
    @micropython.native
    def update():
        while not engine.tick():
            pass

class Audio:
    @micropython.native
    def play(freq, duration):
        pass #TODO
    @micropython.native
    def playBlocking(freq, duration):
        pass #TODO
    @micropython.native
    def stop():
        pass #TODO
    @micropython.native
    def enable(setting):
        pass #TODO

class Link:
    @micropython.native
    def send(data):
        pass #TODO
    @micropython.native
    def receive():
        pass #TODO

class SaveData:
    @micropython.native
    def setName(subDirectoryName):
        pass #TODO
    @micropython.native
    def getName():
        pass #TODO
    @micropython.native
    def setItem(key, value):
        pass #TODO
    @micropython.native
    def getItem(key):
        pass #TODO
    @micropython.native
    def hasItem(key):
        pass #TODO
    @micropython.native
    def delItem(key):
        pass #TODO
    @micropython.native
    def save():
        pass #TODO