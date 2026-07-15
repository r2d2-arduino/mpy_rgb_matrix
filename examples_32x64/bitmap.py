from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep
from resources.bitmaps import sun, suncloud, cloud, rain, rainlight, snowman

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
                      a = 12, b = 16, c = 17, d = 18,
                      add2ndBuffer = True )
rgb.brightness = 100 # 0..1000

bitmaps = [sun, suncloud, cloud, rain, rainlight, snowman]
colors = [COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_MAGENTA, COLOR_WHITE ]
size = 16

try:
    rgb.start()

    for i in range( len( bitmaps ) ):
        rgb.fill(COLOR_BLACK) # clear
        bitmap = bitmaps[ i ]
        color = colors[i]
        
        for x in range( rgb.width // size ):
            for y in range( rgb.height // size ):
                rgb.draw_bitmap( bitmap, x * size, y * size, color )
        
        rgb.show() # Use when add2ndBuffer is True
        sleep( 1 )

    rgb.stop()
except:
    rgb.stop()