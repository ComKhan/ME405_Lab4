import pyb, micropython
from pyb import Pin, ADC, Timer, ExtInt, SPI
from pyb import repl_uart
import gc
from time import *
import pyb

class stepper():
    def __init__(self, cs, en):
        #this is spiInit
        spi = SPI(2, SPI.CONTROLLER, firstbit = SPI.MSB, baudrate=1000000, polarity=1, phase=1)#SPI latches data on falling edge of clock and CS active low
        # polarity determines idle level for CS, and phase determines whether falling or rising edge of clock latches data from dataline
        self.spi = spi
        self.cs = cs
        self.en = en
        self.en.value(0)
        bits = [0x02, 0x00, 0x00, 0x00]  # setting X_actual & X_target to same position
        self.writeSPI(bytearray(bits))
        bits = [0x00, 0x00, 0x00, 0x00]
        self.writeSPI(bytearray(bits))
        
        #write en_sd high
        bits = [0x68, 0x00, 0x00, 0x20]  # MAKE SWITCHES 0 IN IF_CONFIG PG 34
        self.writeSPI(bytearray(bits))

        #write V_MIN
        bits = [0x04, 0x00, 0x00, 0x0f] 
        self.writeSPI(bytearray(bits))
        
        #write V_MAX
        bits = [0x06, 0x00, 0x00, 0xff]  
        self.writeSPI(bytearray(bits))       
        
        #write pulse_div & ramp_div
        bits = [0x18, 0x00, 0x77, 0x00]  
        self.writeSPI(bytearray(bits))
        
        #calculate pmul & pdiv
        pmul, pdiv = pcalc(1024, 10, 10) # inputs: a_max, pmul, pdiv
        print(pmul, pdiv)
        #write pmul & pdiv
        bits = [0b00010010, 0x01, pmul & 0xff, pdiv & 0x0f]    
        self.writeSPI(bytearray(bits))
        
        #write amax
        bits = [0x0c, 0x00, 0x01, 0x00]    
        self.writeSPI(bytearray(bits))
        
        #write ramp_mode
        bits = [0x14, 0x00, 0x00, 0x00]     #set ramp mode #REF_CONF bits see pg 29?????
        self.writeSPI(bytearray(bits))
        

    def readSPI(self, bits):
        self.cs.value(0)
        ba = bytearray(4)
        self.spi.send_recv(bits, ba, timeout = 500)
        self.cs.value(1)
        return ba

    def writeSPI(self,bits):
        self.cs.value(0)
        self.spi.send(bits)
        self.cs.value(1)
        # MOSI line will maintain voltage of last output bit on write bytearray 
        

def main():
    #initialize clk pin    
    PC7 = Pin(Pin.cpu.C7, mode = Pin.OUT_PP,)
    tim = Timer(3, period = 3, prescaler = 0) #timer3 @ 80MHz
    tim.channel(2, pin = PC7, mode = Timer.PWM, pulse_width = 2)
    
    #initialize cs pins
    PC2 = Pin(Pin.cpu.C2, mode = Pin.OUT_PP, value = 1)  #CS1
    PC3 = Pin(Pin.cpu.C3, mode = Pin.OUT_PP, value = 1)  #CS2
    PC4 = Pin(Pin.cpu.C4, mode = Pin.OUT_PP, value = 1)  #CS1
    PC0 = Pin(Pin.cpu.C0, mode = Pin.OUT_PP, value = 1)  #CS2

    motor1 = stepper(PC2, PC4)
    motor2 = stepper(PC3, PC0)


def pcalc(a_max, ramp_div, pulse_div):  ## is this a motor1.pcalc func now??
    for pmul in range(128,256,1):
        for j in range(14):
            pdiv = 8*(2**j)
            p = a_max/(128*(2**(ramp_div-pulse_div)))
            pd = pmul/pdiv
            q = pd/p
            if(0.95 < q and 1 > q):
                return pmul, j
    return
main()


