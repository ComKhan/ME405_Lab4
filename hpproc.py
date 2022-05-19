from matplotlib.pyplot import plot
import newtonRaphson
import pen
import math
def parseHPGL(filename: str) -> list:
    """Takes input hpgl file and outputs double nested list. First list is lines (only 1), second is instructions"""
    im = open(filename, "r")
    lines = im.readline()
    lines = lines.split(";")  #lines[row] becomes another list instead of str
    
    for point in range(len(lines)): #
        lines[point] = lines[point][0:2] + " " + lines[point][2:]
        lines[point] = lines[point].split(',')
        lines[point] = lines[point][0].split(' ') + lines[point][1:]

    return lines

def draw(listy: list, plotting: pen.drawer) -> list:
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
            # funtion to raise solenoid
            # loop to move through target locations

        elif instr[0] == 'PD ':
            plotting.drawing = 1
            interpolated_xy_points = interpolate(instrconv(instr)) # converting instruction into points and interpolation of that data
            interpolated_thetas = list(map(lambda point: newtonRaphson.myraph(point), interpolated_xy_points))  # converting target(x,y) -> target(theta1, theta2)
            #interpolate()
            # funcion to drop solenoid
            # loop to move through target locations
            pass

def instrconv(instr: list) -> list:
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

def createframe(point: list,plot: int):
    

    
def main():
    instrList = parseHPGL('drawing.hpgl')
    draw(instrList)
    

main()


def interpolate(targets: list, curr_location: list, resolution: int) -> None:
    """takes a list of targets [[x,y], ...] and current location and returns a new list 
    with as many points to 
    match the desired resolution. Resolution is in dots per inch(dpi).
    wrote by hayden"""
    if len(curr_location) != 2:  # curr_location must be x,y 
        return None
    interpolated_list = []
    for i in range(len(targets)-1):  # want to interpolate between all items in list
        interpolated_list.append(targets[i])  # always add current target
        x_old, y_old = targets[i][0], targets[i][1]
        x_new, y_new = targets[i+1][0], targets[i+1][1]
        distance = math.sqrt((x_new - y_old)**2 + (y_new - y_old)**2)
        increment = float(1) / resolution  # increment defines how much our motor should move per point after interpolating
        
        pass
    interpolated_list.append(targets[-1])  # get last target position
    pass
