"""
A hybrid engine/wrapper API that is designed similarly to the original Thumby API.

Authors:
    Demod
Version:
    0.0.0 (TBD)
    
Conversion notes from Thumby API to Classic API:
    (TODO)

"""

import engine_main

import engine
import engine_io
import engine_draw

from engine_resources import TextureResource

import framebuf

class Button:
    """Buttons are A, B, UP, DOWN, LEFT, RIGHT, LB, RB, and MENU."""
    
    #Initialized later
    A = None
    """A Button - Far right button."""
    B = None
    """B Button - Inside right button."""
    UP = None
    """Up Button - Up on the d-pad."""
    DOWN = None
    """Down Button - Down on the d-pad."""
    LEFT = None
    """Left Button - Left on the d-pad."""
    RIGHT = None
    """Right Button - Right on the d-pad."""
    LB = None
    """Left Bumper Button - Top left button."""
    RB = None
    """Right Bumper Button - Top right button."""
    MENU = None
    """Menu Button - Bottom left button."""
    
    def __init__(self,btn):
        """DO NOT USE -- instead please use:<br><br>
        Button.A<br>
        Button.B<br>
        Button.UP<br>
        Button.DOWN<br>
        Button.LEFT<br>
        Button.RIGHT<br>
        Button.LB<br>
        Button.RB<br>
        Button.MENU<br>
        """
        self.btn = btn
        
    @micropython.native
    def pressed(self) -> bool:
        """Checks if the button is currently pressed.

        Returns:
            bool: True if pressed, otherwise False.
        """
        return self.btn.is_pressed
    
    @micropython.native
    def justPressed(self) -> bool:
        """Checks if the button was first pressed this frame.

        Returns:
            bool: True if this is the first frame pressed, otherwise False.
        """
        return self.btn.is_just_pressed
Button.A = Button(engine_io.A)
Button.B = Button(engine_io.B)
Button.UP = Button(engine_io.UP)
Button.DOWN = Button(engine_io.DOWN)
Button.LEFT = Button(engine_io.LEFT)
Button.RIGHT = Button(engine_io.RIGHT)
Button.LB = Button(engine_io.LB)
Button.RB = Button(engine_io.RB)
Button.MENU = Button(engine_io.MENU)

class Color:
    """Hard-coded colors for easy reference, in RGB565. If you desire to pick your own colors, use a RGB565 picker tool such as https://rgbcolorpicker.com/565"""
    
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

class Bitmap():
    """Wrapper class around TextureResource, for loading images."""
    
    @micropython.native
    def __init__(self, filepath, key=-1, writable=False):
        """Loads a bitmap from file.

        Args:
            filepath (string): Relative or absolute path to the bitmap file. It must be a BMP image, preferrably in RGB565 format.
            key (int, optional): Transparency color mask, in RGB565. Defaults to -1.
            writable (bool, optional): Set the bitmap data in RAM to be editable by the program, otherwise it will be stored in flash scratch. Defaults to False.
        """
        self.tex = TextureResource(filepath, writable)
        self.width = self.tex.width
        self.height = self.tex.height
        self.data = self.tex.data
        self.key = key

class Font():
    """Wrapper class around TextureResource, for loading fonts. Fonts in Classic API are not the same as in the Thumby Color engine, they more closely resemble fonts in the original Thumby API. Sample fonts are provided in the repository."""
    
    @micropython.native
    def __init__(self, filepath, color:int=0xFFFF, outline:int=1, gap:int=1):
        """Loads a font from file.

        Font bitmaps follow a special format:
             - Exactly 16 columns and 6 rows, monospaced
             - White pixels are colored
             - Black pixels are outline
             - Magenta pixels are transparency
             - Characters are in ASCII order, starting at code 32

        Attributes such as color, outline, and gap can be changed later.

        Args:
            filepath (string): Relative or absolute path to the bitmap file. It must be a BMP image, preferrably in RGB565 format.
            width (int): _description_
            height (int): _description_
            color (int, optional): In RGB565. See `Color` class for example colors. Defaults to white.
            outline (int, optional): Shows black outline if set to 1. Defaults to 1.
            gap (int, optional): Spacing between characters, ignoring the outside outline. Defaults to 1.
        """
        self.tex = TextureResource(filepath, False)
        self.width = self.tex.width // 16
        self.height = self.tex.height // 6
        self.data = self.tex.data
        self.color = color
        self.outline = outline
        self.gap = gap

    @micropython.native
    def widthString(self, str):
        """Calculate the pixel width of a string using this font.

        Args:
            str (string): A text string.

        Returns:
            int: The width in pixels.
        """
        count = len(str)
        if count == 0:
            return 0
        return count * (self.width + self.gap - 2) - self.gap + 2

class Sprite:
    """Bitmap wrapper class with stateful information, similar to the Thumby API Sprite class."""
    
    @micropython.native
    def __init__(self, width:int, height:int, bitmap, 
                 x:int=0, y:int=0, mirrorX:int=0, mirrorY:int=0, 
                 frame:int=0):
        """Creates a new sprite.

        Args:
            width (int): The width of the sprite/frame.
            height (int): The height of the sprite/frame.
            bitmap (Bitmap): The bitmap of the sprite or spritesheet.
            x (int, optional): Initial X position. Defaults to 0.
            y (int, optional): Initial Y position. Defaults to 0.
            mirrorX (int, optional): Flips sprite horizontally if set to 1. Defaults to 0.
            mirrorY (int, optional): Flips sprite vertically if set to 1. Defaults to 0.
            frame (int, optional): The frame in the spritesheet, starting at 0 from left to right, top to bottom. Defaults to 0.
        """
        self.width = width
        self.height = height
        self.bitmap = bitmap
        self.x = x
        self.y = y
        self.mirrorX = mirrorX 
        self.mirrorY = mirrorY 
        self.frame = frame

WIDTH = const(128)
"""Width of the screen, in pixels."""
HEIGHT = const(128)
"""Height of the screen, in pixels."""

class Display:
    """Graphical calls for updating the screen with shapes and images."""
    
    _fb = engine_draw.back_fb()
    _fbData = engine_draw.back_fb_data()
    
    _font = None

    @micropython.viper
    def setFPS(fps):
        """Sets the framerate of the engine.

        Args:
            fps (int): Target framerate, otherwise 0 for unlimited framerate.
        """
        engine.fps_limit(fps)

    @micropython.viper
    def fill(color:int):
        """Fills the entire screen with a solid color.

        Args:
            color (int): In RGB565. See `Color` class for example colors.
        """
        buf32 = ptr32(Display._fbData)
        v32 = (color<<16) | color
        for i in range((WIDTH*HEIGHT)//2):
            buf32[i] = v32

    @micropython.viper
    def setPixel(x:int, y:int, color:int):
        """Sets a single pixel on the screen.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            color (int): In RGB565. See `Color` class for example colors.
        """
        buf = ptr16(Display._fbData)
        buf[y*WIDTH+x] = color
    @micropython.viper
    def getPixel(x:int, y:int) -> int:
        """Checks a single pixel on the screen that is already drawn.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            int: The current color, in RGB565.
        """
        buf = ptr16(Display._fbData)
        return buf[y*WIDTH+x]

    @micropython.native
    def drawLine(x1:int, y1:int, x2:int, y2:int, color:int):
        """Draws a single line on the screen.

        Args:
            x1 (int): Starting X coordinate.
            y1 (int): Starting Y coordinate.
            x2 (int): Ending X coordinate.
            y2 (int): Ending Y coordinate.
            color (int): In RGB565. See `Color` class for example colors.
        """
        Display._fb.line(x1, y1, x2, y2, color)
    @micropython.native
    def drawFilledRectangle(x:int, y:int, w:int, h:int, color:int):
        """Draws a filled rectangle on the screen.

        Args:
            x (int): Top-left X coordinate.
            y (int): Top-left Y coordinate.
            w (int): Width of rectangle.
            h (int): Height of rectangle.
            color (int): In RGB565. See `Color` class for example colors.
        """
        Display._fb.rect(x, y, w, h, color, True)
    @micropython.native
    def drawRectangle(x:int, y:int, w:int, h:int, color:int):
        """Draws a rectangle outline on the screen.

        Args:
            x (int): Top-left X coordinate.
            y (int): Top-left Y coordinate.
            w (int): Width of rectangle.
            h (int): Height of rectangle.
            color (int): In RGB565. See `Color` class for example colors.
        """
        Display._fb.rect(x, y, w, h, color, False)

    @micropython.viper
    def blit(bitmap, x:int, y:int, mirrorX:int=0, mirrorY:int=0):
        """Draws a bitmap on the screen.

        Args:
            bitmap (Bitmap): The bitmap.
            x (int): Top-left X coordinate.
            y (int): Top-left Y coordinate.
            mirrorX (int, optional): Flips bitmap horizontally if set to 1. Defaults to 0.
            mirrorY (int, optional): Flips bitmap vertically if set to 1. Defaults to 0.
        """
        buf = ptr16(Display._fbData)
        bmpW = int(bitmap.width)
        bmpH = int(bitmap.height)
        bmp = ptr16(bitmap.data)
        key = int(bitmap.key)

        w, h = bmpW, bmpH

        if x >= WIDTH or (x+w) <= 0 or y >= HEIGHT or (y+h) <= 0:
            return
        
        srcX = 0
        srcY = 0
        dstX = x
        dstY = y

        if x < 0:
            srcX -= x
            dstX -= x
            w += x
        if (x+w) >= WIDTH:
            w -= (x+w) - WIDTH
        if y < 0:
            srcY -= y
            dstY -= y
            h += y
        if (y+h) >= HEIGHT:
            h -= (y+h) - HEIGHT

        if mirrorX and mirrorY:
            srcX = bmpW - srcX - w
            srcY = bmpH - srcY - h
            si = (srcY+h-1) * bmpW + srcX + w - 1
            srcGap = w - bmpW
            dx = -1
        elif mirrorX:
            srcX = bmpW - srcX - w
            si = srcY * bmpW + srcX + w - 1
            srcGap = bmpW + w
            dx = -1
        elif mirrorY:
            srcY = bmpH - srcY - h
            si = (srcY+h-1) * bmpW + srcX
            srcGap = -bmpW - w
            dx = 1
        else:
            si = srcY * bmpW + srcX
            srcGap = bmpW - w
            dx = 1        

        di = dstY * WIDTH + dstX
        dstGap = WIDTH - w        
        for _ in range(h):
            for _ in range(w):
                c = bmp[si] & 0xFFFF
                if c != key:
                    buf[di] = c
                si += dx
                di += 1
            si += srcGap
            di += dstGap
    
    @micropython.viper
    def drawSprite(sprite):
        """Draws a sprite on the screen. This can be called multpile times for the same sprite.

        Args:
            sprite (Sprite): The sprite.
        """
        buf = ptr16(Display._fbData)
        sprW = int(sprite.width)
        sprH = int(sprite.height)
        bmp = ptr16(sprite.bitmap.data)
        bmpW = int(sprite.bitmap.width)
        bmpH = int(sprite.bitmap.height)
        key = int(sprite.bitmap.key)
        x = int(sprite.x)
        y = int(sprite.y)
        mirrorX = int(sprite.mirrorX)
        mirrorY = int(sprite.mirrorY) 
        frame = int(sprite.frame)

        w, h = sprW, sprH

        if x >= WIDTH or (x+w) <= 0 or y >= HEIGHT or (y+h) <= 0:
            return
        
        if frame > 0:
            cols = bmpW // sprW
            row = frame // cols
            col = frame % cols
            sprX = col * sprW
            sprY = row * sprH
        else:
            sprX = 0
            sprY = 0

        srcX = sprX
        srcY = sprY
        dstX = x
        dstY = y

        if x < 0:
            srcX -= x
            dstX -= x
            w += x
        if (x+w) >= WIDTH:
            w -= (x+w) - WIDTH
        if y < 0:
            srcY -= y
            dstY -= y
            h += y
        if (y+h) >= HEIGHT:
            h -= (y+h) - HEIGHT
        
        if mirrorX and mirrorY:
            srcX = (sprX + sprW) - (srcX - sprX) - w
            srcY = (sprY + sprH) - (srcY - sprY) - h
            si = (srcY+h-1) * bmpW + srcX + w - 1
            srcGap = w - bmpW
            dx = -1
        elif mirrorX:
            srcX = (sprX + sprW) - (srcX - sprX) - w
            si = srcY * bmpW + srcX + w - 1
            srcGap = bmpW + w
            dx = -1
        elif mirrorY:
            srcY = (sprY + sprH) - (srcY - sprY) - h
            si = (srcY+h-1) * bmpW + srcX
            srcGap = -bmpW - w
            dx = 1
        else:
            si = srcY * bmpW + srcX
            srcGap = bmpW - w
            dx = 1        

        di = dstY * WIDTH + dstX
        dstGap = WIDTH - w        
        for _ in range(h):
            for _ in range(w):
                c = bmp[si] & 0xFFFF
                if c != key:
                    buf[di] = c
                si += dx
                di += 1
            si += srcGap
            di += dstGap

    @micropython.native
    def setFont(font):
        """Set the font to be used by `Display.drawText`. Attributes such as color, outline, and gap are set in `font`.

        Args:
            font (Font): The font to use.
        """
        Display._font = font
    @micropython.viper
    def drawText(text, x:int, y:int):
        """Draw text on the screen. Set the font with `Display.setFont`. Attributes such as color, outline, and gap are set in the font.

        Args:
            text (string): The text to show on the screen.
            x (int): Top-left X coordinate.
            y (int): Top-left Y coordinate.
        """
        buf = ptr16(Display._fbData)
        font = Display._font
        sprW = int(font.width)
        sprH = int(font.height)
        bmp = ptr16(font.data)
        bmpW = int(font.tex.width)
        bmpH = int(font.tex.height)
        alphaKey = int(Color.MAGENTA)
        colorKey = int(Color.WHITE)
        outlineKey = int(Color.BLACK)
        x1 = int(x)
        y1 = int(y)
        color = int(font.color)
        outline = int(font.outline)
        gap = int(font.gap) - 2

        if color == colorKey:
            colorKey = -1
        if outline != 0:
            outlineKey = -1

        if int(len(text)) == 0:
            return

        if y1 > HEIGHT or (y1+sprH) <= 0:
            return

        for char in text:
            if x1 >= WIDTH or (x1+sprW) <= 0:
                x1 += sprW + gap
                continue
        
            x, y = x1, y1
            w, h = sprW, sprH

            frame = int(ord(char)) - 32
            row = frame >> 4
            col = frame & 0xF
            sprX = col * sprW
            sprY = row * sprH

            srcX = sprX
            srcY = sprY
            dstX = x
            dstY = y

            if x < 0:
                srcX -= x
                dstX -= x
                w += x
            if (x+w) >= WIDTH:
                w -= (x+w) - WIDTH
            if y < 0:
                srcY -= y
                dstY -= y
                h += y
            if (y+h) >= HEIGHT:
                h -= (y+h) - HEIGHT
            
            si = srcY * bmpW + srcX
            srcGap = bmpW - w
            dx = 1        

            di = dstY * WIDTH + dstX
            dstGap = WIDTH - w        
            for _ in range(h):
                for _ in range(w):
                    c = bmp[si] & 0xFFFF
                    if c != alphaKey and c != outlineKey:
                        if c == colorKey:
                            c = color
                        buf[di] = c
                    si += dx
                    di += 1
                si += srcGap
                di += dstGap

            x1 += sprW + gap
            
    @micropython.native
    def update():
        """Updates the screen and waits for the next frame.
        """
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