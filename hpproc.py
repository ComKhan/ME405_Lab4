import newtonRaphson
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

def draw(listy: list) -> list:
    """Takes double nested list from parseHPGL function and outputs """

    for instr in listy:
        if instr[0] == 'IN ':
            pass    # will be used ot initialize whole thang
        elif instr[0] == 'SP ':
            pass    # will be used to change colors
        elif instr[0] == 'PU ':
            interpolated_xy_points = interpolate(instrconv(instr))
            interpolated_thetas = list(map(lambda point: newtonRaphson.myraph(point), interpolated_xy_points))
            # funtion to raise solenoid
            # loop to move through target locations

        elif instr[0] == 'PD ':
            #interpolate()
            # funcion to drop solenoid
            # loop to move through target locations
            pass

def instrconv(listy: list) -> list:
    """Takes Output of interpolate function as input and outputs corresponding theta values in list to spin motor. """
    i = 0
    target = [0]*2
    motor_in = []
    while(i*2 < len(listy)):
        target[0] = list[i]
        target[1] = list[i+1]
        motor_in.append(target)
        i +=1
    return motor_in
    
def main():
    print(parseHPGL("drawing.hpgl"))
    

main()


def interpolate(targets: list, curr_location: list, resolution: int) -> None:
    """takes a list of targets [[x,y], ...] and current location and returns a new list 
    with as many points to 
    match the desired resolution. Resolution is in dots per inch(dpi).
    wrote by hayden"""
    pass
