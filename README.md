
# Thumby Color Classic API

This is an alternative API for the Thumby Color, designed to be heavily inspired by the original Thumby API to make transitioning easier for those familiar with it. The API provides similar functionality to the original, but with enhancements tailored for the Thumby Color hardware.

## Overview

The Thumby Color Classic API is a hybrid engine/wrapper API. It aims to provide a familiar interface for those who have used the original Thumby API, while leveraging the additional capabilities of the Thumby Color. The API offers utilities for handling graphics, input, audio, and more, just like the original Thumby, but adapted for the more powerful hardware.

The project is still under active development, and several features are yet to be completed. Below is an overview of the current state of the API.

## Features

- **Button Input**  
  Handle all key inputs, including A, B, D-Pad directions, and the bumpers.
  
- **Graphics (RGB565 Color Support)**  
  Draw shapes, bitmaps, and text on the 128x128 screen. The API supports:
  - **Bitmap images** using the `Bitmap` class.
  - **Sprite rendering** similar to the original API.
  - **Font rendering** based on custom font files.

- **Colors**  
  Use a color picker tool (https://rgbcolorpicker.com/565) to define colors. Predefined RGB565 colors are available for convenience.
  - Examples of predefined colors: `BLACK`, `WHITE`, `RED`, `BLUE`, `GREEN`, `YELLOW`, etc.

- **Basic Drawing Commands**
  - `fill()`: Fills the entire screen with a solid color.
  - `setPixel()`: Sets an individual pixel’s color.
  - `drawLine()`, `drawRectangle()`, `drawFilledRectangle()`: Basic shape drawing.

- **Display**  
  Control the screen buffer and easily update the display. The API mimics the behavior of the original Thumby with added color support.

- **Sprites**  
  Create and manipulate sprites with stateful information, such as position, mirroring, and frame animation.

- **Fonts**  
  Load and render custom fonts with support for ASCII character mapping. Fonts follow a custom bitmap format and can include outlines and adjustable gaps between characters.
  - A font must be loaded by the game if text is used, there is no default font.

## Getting Started

  To use the Thumby Color Classic API, you'll need to download only the `thumbyClassic.py` API file and any desired font files from the `fonts` directory. These files should be placed directly into your game folder for use.

1. Download `thumbyClassic.py` [here](https://github.com/demodude4u/Thumby-Classic-API/blob/main/thumbyClassic.py).

2. Download any font files you wish to use from the [fonts directory](https://github.com/demodude4u/Thumby-Classic-API/tree/main/fonts).

3. Import the API into your Thumby Color project:
   ```python
   from thumbyClassic import *
   ```

## Function Mapping from Original Thumby API to Classic API

| **Thumby API**                             | **Classic API**                                  | **Comments**                       |
|--------------------------------------------|--------------------------------------------------|------------------------------------|
| `reset()`                                  | TODO                                             |                                    |
| `buttonX.pressed()`                        | `Button.X.pressed()`                             |                                    |
| `buttonX.justPressed()`                    | `Button.X.justPressed()`                         |                                    |
| `inputPressed()`                           | TODO                                             |                                    |
| `inputJustPressed()`                       | TODO                                             |                                    |
| `dpadPressed()`                            | TODO                                             |                                    |
| `dpadJustPressed()`                        | TODO                                             |                                    |
| `actionPressed()`                          | TODO                                             |                                    |
| `actionJustPressed()`                      | TODO                                             |                                    |
|                                            | `Font(filepath, color=0xFFFF, outline=1, gap=1)` | Load BMP Font files (RGB565)       |
| `display.drawText(text, x, y, color)`      | `Display.drawText(text, x, y)`                   | Color is now set in the `Font` class. |
| `display.setFont(fontFilePath, width, height, space)`|`Display.setFont(font)`                 | Space (Gap) is now set in the `Font` class. |
| `display.width`                            | `WIDTH`                                          |                                    |
| `display.height`                           | `HEIGHT`                                         |                                    |
| `display.update()`                         | `Display.update()`                               |                                    |
| `display.setFPS(fps)`                      | `Display.setFPS(fps)`                            |                                    |
| `display.fill(color)`                      | `Display.fill(color)`                            |                                    |
| `display.brightness(brightness)`           | TODO                                             |                                    |
| `display.setPixel(x, y, color)`            | `Display.setPixel(x, y, color)`                  |                                    |
| `display.getPixel(x, y)`                   | `Display.getPixel(x, y)`                         |                                    |
| `display.drawLine(x1, y1, x2, y2, color)`  | `Display.drawLine(x1, y1, x2, y2, color)`        |                                    |
| `display.drawFilledRectangle(x, y, w, h, color)` | `Display.drawFilledRectangle(x, y, width, height, color)` |                     |
| `display.drawRectangle(x, y, w, h, color)` | `Display.drawRectangle(x, y, width, height, color)` |                                 |
|                                            | `Bitmap(filepath, key=-1, writable=False)`       | Load BMP files (RGB565)            |
| `display.blit(bitmapData, x, y, w, h, key, mirrorX, mirrorY)` | `Display.blit(bitmap, x, y, mirrorX=0, mirrorY=0)` | Key is now set in the `Bitmap` class. |
| `display.blitWithMask(bitmapData, x, y, width, height, key, mirrorX, mirrorY, maskBitmapData)` || Use `Bitmap.key` instead.        |
| `Sprite(width, height, bitmapData, x=0, y=0, key=0  mirrorX=0, mirrorY=0)` | `Sprite(width, height, bitmap, x=0, y=0, mirrorX=0, mirrorY=0, frame=0)` ||
| `Sprite.getFrame`, `Sprite.setFrame(frame)`| `Sprite.frame`                                   |                                    |
| `display.drawSprite(sprite)`               | `Display.drawSprite(sprite)`                     |                                    |
| `display.drawSpriteWithMask(sprite, maskSprite)` |                                            | Use `Bitmap.key` instead.          |
| `audio.play(freq, duration)`               | TODO                                             |                                    |
| `audio.playBlocking(freq, duration)`       | TODO                                             |                                    |
| `audio.stop()`                             | TODO                                             |                                    |
| `audio.setEnabled()`                       | TODO                                             |                                    |
| `audio.set(freq)`                          | TODO                                             |                                    |
| `link.send(data)`                          | TODO                                             |                                    |
| `link.receive()`                           | TODO                                             |                                    |
| `saveData.setName(name)`                   | TODO                                             |                                    |
| `saveData.setItem(key, value)`             | TODO                                             |                                    |
| `saveData.getItem(key)`                    | TODO                                             |                                    |
| `saveData.hasItem(key)`                    | TODO                                             |                                    |
| `saveData.delItem(key)`                    | TODO                                             |                                    |
| `saveData.save()`                          | TODO                                             |                                    |
| `saveData.getName()`                       | TODO                                             |                                    |

## Contributions

Contributions are welcome! If you'd like to help improve the API or add new features, feel free to open an issue or submit a pull request.
