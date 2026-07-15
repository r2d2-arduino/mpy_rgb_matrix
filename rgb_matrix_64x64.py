"""
RGBMatrix64x64 v 0.2.1
Library for RGB Matrix 64x64

Color: 8 colors
 
Project path: https://github.com/r2d2-arduino/mpy_rgb_matrix
MIT License

Author: Arthur Derkach 
"""
from draw_fb_g8 import DRAW_FB_G8
from machine import Pin
from time import sleep_ms, sleep_us
import array
from _thread import start_new_thread

class RGBMatrix64x64( DRAW_FB_G8 ):
    # Define screen dimensions
    WIDTH  = const(64)
    HEIGHT = const(64)
    LOOP_DELAY = const(1000) # delay in us: 100..2000

    def __init__( self, r1, g1, b1, r2, g2, b2, clk, lat, oe, a, b, c, d, e,
                  controller = '', add2ndBuffer = False ):
        ''' Main constructor
        r1 (int): Number of pin R1
        g1 (int): Number of pin G1
        b1 (int): Number of pin B1
        r2 (int): Number of pin R2
        g2 (int): Number of pin G2
        b2 (int): Number of pin B2
        clk (int): Number of pin CLK
        lat (int): Number of pin LAT
        oe (int): Number of pin OE
        a (int): Number of pin A
        b (int): Number of pin B
        c (int): Number of pin C
        d (int): Number of pin D
        controller (str): Controller name: RP2, ESP32, ESP32-S3, ESP32-C3,...
        '''
        # Security check for register mode
        for p in (r1, g1, b1, r2, g2, b2, clk, lat, oe, a, b, c, d, e):
            if p > 31:
                raise ValueError(f"Pin {p} is > 31! Data & CLK pins must be between 0 and 31 for direct memory access.")
            
        # Initialize data pins (Upper half)
        self.r1 = Pin( r1, Pin.OUT )
        self.g1 = Pin( g1, Pin.OUT )
        self.b1 = Pin( b1, Pin.OUT )

        # Initialize data pins (Lower half)
        self.r2 = Pin( r2, Pin.OUT )
        self.g2 = Pin( g2, Pin.OUT )
        self.b2 = Pin( b2, Pin.OUT )

        # Initialize control pins
        self.clk = Pin( clk, Pin.OUT )
        self.lat = Pin( lat, Pin.OUT )
        self.oe  = Pin(  oe, Pin.OUT )

        # Initialize row address pins
        self.a = Pin( a, Pin.OUT )
        self.b = Pin( b, Pin.OUT )
        self.c = Pin( c, Pin.OUT )
        self.d = Pin( d, Pin.OUT )
        self.e = Pin( e, Pin.OUT )
        
        # Saving bit positions for registers
        self.clk_bit = 1 << clk
        self.lat_bit = 1 << lat
        self.oe_bit  = 1 << oe
        
        # Init Draw Library
        super().__init__( WIDTH, HEIGHT )
        
        self.add2ndBuffer = add2ndBuffer
        #Init front buffer (for matrix update)
        if add2ndBuffer:
            self.fbuffer = bytearray( self.buffsize )
        
        self.brightness = 100 # Default
        self.running = False # 2nd-core refresh matrix running
        
        # Trying to get controller
        if controller == '':
            controller = self.read_controller_name() 
        self.controller_name = controller
        
        # 00-31 pin-output registers only
        if controller in ('ESP32-S3', 'ESP32-C3'):
            self.GPIO_OUT_W1TS  = 0x60004008 
            self.GPIO_OUT_W1TC  = 0x6000400C # + bit
        elif controller in ('ESP32-C5', 'ESP32-C6'):
            self.GPIO_OUT_W1TS = 0x60091008
            self.GPIO_OUT_W1TC = 0x6009100C
        elif controller == 'RP2': #Raspberry Pi Pico
            self.GPIO_OUT_W1TS = 0xD0000014
            self.GPIO_OUT_W1TC = 0xD0000018
        else: # ESP32
            self.GPIO_OUT_W1TS = 0x3FF44008
            self.GPIO_OUT_W1TC = 0x3FF4400C
        
        # Preparing Lookup Table (LUT) ---
        self.color_lut = array.array('I', [0] * 64)
        
        self.color_mask = (1 << r1) | (1 << r2) | (1 << g1) | (1 << g2) | (1 << b1) | (1 << b2)
        
        for v1 in range(8):
            # Mask for R1(25), G1(26), B1(27)
            m1 = ((1<<r1) if v1&4 else 0) | ((1<<g1) if v1&2 else 0) | ((1<<b1) if v1&1 else 0)
            for v2 in range(8):
                # Mask for R2(21), G2(22), B2(23)
                m2 = ((1<<r2) if v2&4 else 0) | ((1<<g2) if v2&2 else 0) | ((1<<b2) if v2&1 else 0)
                # Index in range 0..63
                self.color_lut[(v1 << 3) | v2] = m1 | m2

        # --- Preparing Address LUT ---
        self.row_mask_on = array.array('I', [0] * 32)
        self.row_mask_off = array.array('I', [0] * 32)
        
        for r in range(32):
            on_mask = 0
            off_mask = 0
            
            if r & 1: on_mask |= (1 << a)
            else: off_mask |= (1 << a)
            if r & 2: on_mask |= (1 << b)
            else: off_mask |= (1 << b)
            if r & 4: on_mask |= (1 << c)
            else: off_mask |= (1 << c)
            if r & 8: on_mask |= (1 << d)
            else: off_mask |= (1 << d)
            if r & 16: on_mask |= (1 << e)
            else: off_mask |= (1 << e)
            
            self.row_mask_on[r] = on_mask
            self.row_mask_off[r] = off_mask
            
    @staticmethod
    def read_controller_name():
        """ Reading controller name """
        from os import uname
        
        info = uname()
        sysname = info.sysname

        controller = 'Undefined'
        if sysname == 'esp32':
            if 'ESP32S3' in info.machine:
                controller = 'ESP32-S3'
            elif 'ESP32C3' in info.machine:
                controller = 'ESP32-C3'
            elif 'ESP32C5' in info.machine:
                controller = 'ESP32-C5'
            elif 'ESP32C6' in info.machine:
                controller = 'ESP32-C6'                
            else:
                controller = 'ESP32'
        elif sysname == 'rp2':
            controller = 'RP2'

        return controller
    
    @micropython.viper
    def refresh_matrix(self):
        '''
        Resresh of Matrix
        '''
        if int(self.add2ndBuffer) == 1:
            buf = ptr8(self.fbuffer) # framebuffer
        else:
            buf = ptr8(self.buffer) # framebuffer
            
        brightness = int(self.brightness)
        lut = ptr32(self.color_lut)
        
        # Registers for 0..31 pins
        W1TS = ptr32(self.GPIO_OUT_W1TS) # Set to 1
        W1TC = ptr32(self.GPIO_OUT_W1TC) # Set to 0
        
        # Mask of all color pins
        color_mask = int(self.color_mask) 
        
        # Adress mask
        row_on  = ptr32(self.row_mask_on)
        row_off = ptr32(self.row_mask_off)
        
        # Mask of other pins 
        clk_mask = int(self.clk_bit)
        lat_mask = int(self.lat_bit)
        oe_mask  = int(self.oe_bit)
        
        for row in range(32):
            idx1 = int(row << 6)
            idx2 = int(idx1 + 2048)
            
            for col in range(64):
                val1 = int(buf[idx1])
                val2 = int(buf[idx2])
                idx1 += 1
                idx2 += 1
                
                # Turn off all 6 color pins at once
                W1TC[0] = color_mask 
                
                # Turn on the choosed colors, taking the finished mask from LUT
                W1TS[0] = lut[(val1 << 3) | val2]
                
                # Pulse clock to push data into shift registers
                W1TS[0] = clk_mask
                W1TC[0] = clk_mask
            
            # Pulse latch to move data from shift registers to output buffers
            W1TS[0] = lat_mask
            W1TC[0] = lat_mask

            # Set row address (A, B, C, D)
            W1TS[0] = row_on[row]
            W1TC[0] = row_off[row]
            
            # --- Brightness setting ---
            W1TC[0] = oe_mask # Matrix on
            
            for _ in range(brightness):
                pass
            
            W1TS[0] = oe_mask # Matrix off  
    
    def show(self):
        ''' Send back buffer to front '''
        if self.add2ndBuffer:
            self.fbuffer[:] = self.buffer
        else:
            print('Show method disabbled for 1 buffer mode')
    
    def start(self):
        """ Launching the 2nd core """
        if not self.running:
            self.running = True
            start_new_thread(self._render_loop, ())
            
    def stop(self):
        """ Safely stop the thread """
        self.running = False
        # Waiting for the thread to finish.
        sleep_ms(10)
        # Matrix off
        self.oe.on() 

    def _render_loop(self):
        """ Loop for 2nd core """
        refresh_matrix = self.refresh_matrix
        while self.running:
            # Draw 1 frame
            refresh_matrix()
            
            # It is CRITICAL that there is a pause
            sleep_us(LOOP_DELAY)
            
