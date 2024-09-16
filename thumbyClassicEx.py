import engine
import engine_io
import engine_draw

import math
import array

WIDTH = const(128)
"""Width of the screen, in pixels."""
HEIGHT = const(128)
"""Height of the screen, in pixels."""

class DisplayEx:
    
    _fb = engine_draw.back_fb()
    _fbData = engine_draw.back_fb_data()
    
    _sin_f10 = array.array('h',[int(math.sin(math.radians(x)) * 1024)+1024 for x in range(-90, 91)])
    _tan_f10 = array.array('h',[int(math.tan(math.radians(x / 2)) * 1024)+1024 for x in range(-90, 91)])
    
    @micropython.viper
    def blitRotate(bitmap, angle: int, x: int, y: int, pivotX: int, pivotY: int):
        
        buf = ptr16(DisplayEx._fbData)
        bmpW = int(bitmap.width)
        bmpH = int(bitmap.height)
        bmp = ptr16(bitmap.data)
        key = int(bitmap.key)
        
        sinLookup = ptr16(DisplayEx._sin_f10)
        tanLookup = ptr16(DisplayEx._tan_f10)

        if angle < 90:
            ra, flip = angle, 0
        elif angle <= 270:
            ra, flip = 180 - angle, 1
            x -= 2 * ((bmpW >> 1) - pivotX)
        else:
            ra, flip = angle - 360, 0

        # Determine rendering mode
        if ra == 0:
            rmode = 1
        elif ra == 90:
            rmode = 2
        elif ra == -90:
            rmode = 3
        else:
            rmode = 0
            shx_f10 = -(tanLookup[ra + 90]-1024)
            shy_f10 = sinLookup[ra + 90]-1024

        si = 0
        for srcY in range(bmpH):
            if flip:
                srcY = bmpH - 1 - srcY
            
            for srcX in range(bmpW):
                c = bmp[si] & 0xFFFF
                
                if c == key:
                    si += 1
                    continue

                if rmode == 0:  # Shear-based rotation for larger angles
                    dx = srcX - pivotX
                    dy = srcY - pivotY

                    h_shear_x = dx + ((dy * shx_f10) >> 10)
                    ry = dy + ((h_shear_x * shy_f10) >> 10)
                    rx = h_shear_x + ((ry * shx_f10) >> 10)

                    rx += pivotX
                    ry += pivotY

                elif rmode == 1:  # No rotation
                    rx = srcX
                    ry = srcY

                elif rmode == 2:  # Quick rotate 90
                    rx = pivotX - srcY + pivotY
                    ry = pivotY + srcX - pivotX

                elif rmode == 3:  # Quick rotate -90
                    rx = pivotX + srcY - pivotY
                    ry = pivotY - srcX + pivotX

                if flip:
                    dstX = x + (bmpW - rx)
                else:
                    dstX = x + rx
                dstY = y + ry

                if 0 <= dstX < WIDTH and 0 <= dstY < HEIGHT:
                    buf[dstY*WIDTH+dstX] = c
                    
                si += 1