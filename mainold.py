"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""
import pyb, micropython
from pyb import Pin, ADC, Timer, ExtInt
from pyb import repl_uart
import gc
import pyb
import cotask
import task_share

PC1 = Pin(Pin.cpu.C1, mode = Pin.OUT_PP)
PC0 = Pin(Pin.cpu.C0, mode = Pin.IN)
adc0 = ADC(Pin.cpu.C0)  # PC0 ANALOG INPUT
uart = pyb.UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop = 1)
tim = Timer(6, freq = 1000) #timer6 @ 1kHz

button_int = ExtInt(Pin.cpu.C13, ExtInt.IRQ_FALLING,
                    Pin.PULL_NONE, lambda p: read_ckt())

class drawer():
    def __init__(self):
        self.drawing = 0

def tim_cb(tim):
    if (Time_Vals.num_in() < 999):
        Time_Vals.put(share0.get())
        ADC_Vals.put(adc0.read())
        share0.put(share0.get()+1)
    else:
        share0.put(1)
        tim.callback(None)
    
def read_ckt():
    PC1.value(0 if PC1.value() else 1)
    if (PC1.value() == 0):
        tim.callback(tim_cb)

def TaskComs():
    counter = 0
    while True:
        if (Time_Vals.num_in() == 999):
            counter = Time_Vals.num_in()
        if (counter>0):
            counter-=1
            stuff = ("{:},{:}\r\n".format(Time_Vals.get(), ADC_Vals.get()))
            uart.write(stuff)
        yield (0)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share ('I', thread_protect = False, name = "Share 0")
    Time_Vals = task_share.Queue ('L', 1000, thread_protect = False, overwrite = False,
                           name = "Time Vals")
    ADC_Vals = task_share.Queue ('L', 1000, thread_protect = False, overwrite = False,
                           name = "ADC Vals")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    taskcom = cotask.Task (TaskComs, name = 'Task_1', priority = 2, 
                         period = 1, profile = True, trace = False)
    #cotask.task_list.append (taskbut)
    cotask.task_list.append (taskcom)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()


