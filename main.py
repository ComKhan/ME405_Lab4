import newtonRaphson
import pen
import math
from pyb import Pin
import stepper

def parseHPGL(filename):
    """Takes input hpgl file and outputs double nested list. First list is lines (only 1), second is instructions"""
    im = open(filename, "r")
    lines = im.readline()
    lines = lines.split(";")  #lines[row] becomes another list instead of str
    
    for point in range(len(lines)): #
        lines[point] = lines[point][0:2] + " " + lines[point][2:]
        lines[point] = lines[point].split(',')
        lines[point] = lines[point][0].split(' ') + lines[point][1:]

    return lines

def draw(listy, plotting):
    """Takes double nested list from parseHPGL function and outputs """

    for instr in listy:
        if instr[0] == 'IN ':
            pass    # will be used ot initialize whole thang
        elif instr[0] == 'SP ':
            pass    # will be used to change colors
        elif instr[0] == 'PU ':
            plotting.drawing = 0
            interpolated_xy_points = interpolate(instrconv(instr)) # converting instruction into points and interpolation of that data
            interpolated_thetas = list(map(lambda point: newtonRaphson.myraph(point), interpolated_xy_points))  # converting target(x,y) -> target(theta1, theta2)
            x_actuals = [[x[0]/2/math.pi*384,(x[1]+x[0])/2/math.pi*384] for x in interpolated_thetas]
            # funtion to raise solenoid
            # loop to move through target locations

        elif instr[0] == 'PD ':
            plotting.drawing = 1
            interpolated_xy_points = interpolate(instrconv(instr),lastloc, 10) # converting instruction into points and interpolation of that data
            interpolated_thetas = list(map(lambda point: newtonRaphson.myraph(point), interpolated_xy_points))  # converting target(x,y) -> target(theta1, theta2)
            x_actuals = [[x[0]/2/math.pi*384,(x[1]+x[0])/2/math.pi*384] for x in interpolated_thetas]
            #interpolate()
            # funcion to drop solenoid
            # loop to move through target locations
            pass

def instrconv(instr):
    """Takes Output of interpolate function as input and outputs corresponding x,y coord for interpolation func. """
    instr = instr[1:]  # cuts off "PU" & "PD"
    i = 0
    target = [0]*2
    motor_in = []
    while(i*2 < len(listy)):
        target[0] = list[i]
        target[1] = list[i+1]
        motor_in.append(target)
        i +=1
    return motor_in

def interpolate(targets, curr_location, resolution):
    """takes a list of targets [[x,y], ...] and current location and returns a new list 
    with as many points to 
    match the desired resolution. Resolution is in dots per inch(dpi)."""
    if len(curr_location) != 2:  # curr_location must be [x,y] 
        print("not a valid current location")
        return None
    interpolated_list = []
    print("\n")
    targets.insert(0, [curr_location[0], curr_location[1]])
    for i in range(len(targets)-1):  # want to interpolate between all items in list
        interpolated_list.append(targets[i])  # always add current target
        x_old, y_old = targets[i][0], targets[i][1]
        x_new, y_new = targets[i+1][0], targets[i+1][1]
        distance_x = x_new - x_old
        distance_y = y_new - y_old
        hyp = math.sqrt(distance_x**2 + distance_y**2)
        num_steps = hyp*resolution
        delta_x = distance_x/(num_steps)
        delta_y = distance_y/(num_steps)
        increment = float(1) / resolution  # increment defines how much our motor should move per point after interpolating
        for i in range(int(num_steps-1)):
                curr_location[0] = curr_location[0] + delta_x
                curr_location[1] = curr_location[1] + delta_y
                interpolated_list.append([curr_location[0], curr_location[1]])
        curr_location = [x_new, y_new]
    interpolated_list.append([targets[-1][0],targets[-1][1]])
    return interpolated_list

def main():
    listy = parseHPGL("drawing.hpgl")
    plotting = pen.drawer()
    draw(listy,plotting)
    
    #initialize clk pin    
    PC7 = Pin(Pin.cpu.C7, mode = Pin.OUT_PP,)  # PC7 configured for GPIO output
    tim = Timer(3, period = 3, prescaler = 0) #timer3 @ 80MHz
    tim.channel(2, pin = PC7, mode = Timer.PWM, pulse_width = 2)  
    # configures PC7 for PWM modulation to act as a clock signal

    #initialize cs and en pins
    PC2 = Pin(Pin.cpu.C2, mode = Pin.OUT_PP, value = 1)  #CS1
    PC3 = Pin(Pin.cpu.C3, mode = Pin.OUT_PP, value = 1)  #CS2
    PC4 = Pin(Pin.cpu.C4, mode = Pin.OUT_PP, value = 1)  #EN1
    PC0 = Pin(Pin.cpu.C0, mode = Pin.OUT_PP, value = 1)  #EN2

    motor1 = stepper(PC2, PC4)
    motor2 = stepper(PC3, PC0)
    
    listy = parseHPGL("drawing.hpgl")
    plotting = pen.drawer()
    draw(listy,plotting)


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
    