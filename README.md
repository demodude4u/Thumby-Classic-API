
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
  Predefined RGB565 colors are available for convenience, and you can define custom colors if needed.  
  Examples of predefined colors:
  - `BLACK`, `WHITE`, `RED`, `BLUE`, `GREEN`, `YELLOW`, etc.

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

- **Audio (TODO)**  
  A placeholder for playing audio. The functionality is currently under development.

- **Link and Save Data (TODO)**  
  Networking and persistent save data are in progress.

## Getting Started

  To use the Thumby Color Classic API, you'll need to download only the `thumbyClassic.py` API file and any desired font files from the `fonts` directory. These files should be placed directly into your game folder for use.

1. Download `thumbyClassic.py` [here](https://github.com/demodude4u/Thumby-Classic-API/blob/main/thumbyClassic.py).

2. Download any font files you wish to use from the [fonts directory](https://github.com/demodude4u/Thumby-Classic-API/tree/main/fonts).

3. Import the API into your Thumby Color project:
   ```python
   from thumbyClassic import *
   ```

## Differences from the Original Thumby API

While the Thumby Color Classic API attempts to stay as close as possible to the original Thumby API, there are some key differences due to hardware capabilities and optimizations:
- Full RGB565 color support for graphics and text.
- Different handling of fonts and sprites, with a focus on better customization.
- New functionality for networking and persistent data (still in development).

A detailed conversion guide from the original Thumby API to the Classic API will be provided soon.

## Roadmap

- Complete audio support
- Implement networking (Link class)
- Finalize persistent save data (SaveData class)
- Add more graphical primitives and optimizations

## Contributions

Contributions are welcome! If you'd like to help improve the API or add new features, feel free to open an issue or submit a pull request.
