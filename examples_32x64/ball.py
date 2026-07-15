from rgb_matrix_32x64 import RGBMatrix32x64
from time import sleep_us
from random import getrandbits

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
rgb.brightness = 100

rgb.fill(COLOR_BLACK)

radius = 4

x_border = rgb.width - 1
y_border = rgb.height - 1

prev_x = radius
prev_y = radius

x = radius
y = radius

x_speed = 1
y_speed = 1

rgb.start()
color = COLOR_GREEN

try:
    while True:
        color = getrandbits(3) # random color
        if color == 0:
            color = COLOR_GREEN
        #rgb.ellipse( prev_x, prev_y, radius, radius, COLOR_BLACK, True ) # clear previos
        rgb.ellipse(      x,      y, radius, radius, color, True )
        prev_x = x
        prev_y = y
        
        x += x_speed
        y += y_speed
        
        if x + radius > x_border or x - radius < 0:
            x_speed = -x_speed
            
        if y + radius > y_border or y - radius < 0:
            y_speed = -y_speed    

        sleep_us(100)
        
except:
    # Turn off display cleanly
    rgb.stop()
    print("Stopped.")
    




    

