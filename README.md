# mpy_rgb_matrix
Micropython library for RGB Matrix 32x64 and 64x64.

![Photo of gc9a01 display](/../main/photos/matrix32x64.jpg)

## Hub75 connection:
### For 32x64 RGB Matrix:
![Photo of gc9a01 display](/../main/photos/hub75_32x64.png)
### For 64x64 RGB Matrix:
![Photo of gc9a01 display](/../main/photos/hub75_64x64.png)

## File Structure:
* **examples_32x64/** - a set of examples for the Matrix 32x64.
* **examples_64x64/** - a set of examples for the Matrix 64x64.
* **resources/** - files related to examples.
* **draw_fb_g8.py** - Graphical library based on Micropython Framebuffer.
* **rgb_matrix_32x64.py** - Main library for the Matrix 32x64.
* **rgb_matrix_64x64.py** - Main library for the Matrix 64x64.

## Minimum code to run:
```python
from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep

# Pinout for Esp32 (d1)
rgb = RGBMatrix32x64( r1 = 25, g1 = 26, b1 = 27,
                      r2 = 21, g2 = 22, b2 = 23,
                      clk = 15, lat = 19, oe = 5,
                      a = 12, b = 16, c = 17, d = 18 )

rgb.fill( 0 )
rgb.text( "Matrix", 0, 0, 1 )

rgb.start()
sleep(5)
rgb.stop()
```

## Display functions:
* **refresh_matrix ( )** - Resresh the Matrix once.
* **start ( )** - Start loop of refreshing the matrix in 2nd core (for this function, it is better to use a 2-core controller).
* **stop ( )** - Stop loop of refreshing the matrix in 2nd core (for this function, it is better to use a 2-core controller).
* **show ( )** - Copy backbuffer to framebuffer (when 2nd buffer enabled only).

# 2nd Buffer
The second buffer is used if the graphics portion of frame generation takes a long time. While matrix refreshing takes 1-2 ms, the frame buffer generation process can take 20-100 ms. To avoid interference on the matrix, the frame is first generated in the back buffer, then copied to the main buffer—the one being refreshed.

## Example of using 2nd buffer:
```python
from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep

rgb = RGBMatrix32x64( r1 = 25, g1 = 26, b1 = 27,
                      r2 = 21, g2 = 22, b2 = 23,
                      clk = 15, lat = 19, oe = 5,
                      a = 12, b = 16, c = 17, d = 18,
                      add2ndBuffer = True )

rgb.fill( 0 )
rgb.text( "Matrix", 0, 0, 1 )
rgb.show() # <- Use when add2ndBuffer is True

rgb.start()
sleep(5)
rgb.stop()
```
# Using with a 1-core controller:
A method for updating the matrix for a single-core controller without **start( )** and **stop( )** functions
```python
from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep, sleep_ms

# Pinout for Esp32 (d1)
rgb = RGBMatrix32x64( r1 = 25, g1 = 26, b1 = 27,
                      r2 = 21, g2 = 22, b2 = 23,
                      clk = 15, lat = 19, oe = 5,
                      a = 12, b = 16, c = 17, d = 18 )

rgb.fill( 0 )
rgb.text( "Matrix", 0, 0, 1 )

try:
    while True:
        rgb.refresh_matrix()
        sleep_ms(1) # Gives the processor a rest
except:
    rgb.oe.on() # Turn off matrix cleanly
    print("Stopped.")
rgb.oe.on()
```

