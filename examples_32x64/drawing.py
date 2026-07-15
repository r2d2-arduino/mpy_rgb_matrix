from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep

COLOR_BLACK   = const(0)
COLOR_BLUE    = const(1)
COLOR_GREEN   = const(2)
COLOR_CYAN    = const(3)
COLOR_RED     = const(4)
COLOR_MAGENTA = const(5)
COLOR_YELLOW  = const(6)
COLOR_WHITE   = const(7)

rgb = RGBMatrix32x64( r1 = 25, g1 = 26, b1 = 27, r2 = 21, g2 = 22, b2 = 23,
                      clk = 15, lat = 19, oe = 5,
                      a = 12, b = 16, c = 17, d = 18 )
rgb.brightness = 100 # 0..1000

rgb.fill(COLOR_BLACK)

rgb.rect(0, 0, 64, 32, COLOR_WHITE)

rgb.fill_rect(4, 4, 10, 10, COLOR_RED) 
rgb.fill_rect(16, 4, 10, 10, COLOR_GREEN)
rgb.fill_rect(28, 4, 10, 10, COLOR_BLUE) 

rgb.ellipse(44, 8, 5, 5, COLOR_CYAN)
rgb.ellipse(56, 8, 5, 5, COLOR_YELLOW, True)

rgb.pixel(25, 16, COLOR_RED)

rgb.line(0, 0, rgb.width - 1, rgb.height - 1, COLOR_YELLOW)

rgb.text("Matrix", 2, 20, COLOR_MAGENTA)

try:
    rgb.start()
    sleep(5)
    rgb.stop()
except:
    rgb.stop()