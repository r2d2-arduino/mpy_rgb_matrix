from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep
import resources.Tahoma10b as B_FONT
import resources.Verdana10 as C_FONT

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

rgb.fill( COLOR_BLACK )

rgb.text( "Default", 0, 0, COLOR_BLUE )
rgb.set_font( B_FONT )
rgb.draw_text( "TahomaBold", 0, 10, COLOR_YELLOW )
rgb.set_font( C_FONT )
rgb.draw_text( "Verdana10", 0, 20, COLOR_MAGENTA )

try:
    rgb.start()
    sleep(5)
    rgb.stop()
except:
    rgb.stop()