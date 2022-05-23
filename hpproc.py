def instrconv(instr):
    """Takes Output of interpolate function as input and outputs corresponding x,y coord for interpolation func. """
    instr = instr[1:]  # cuts off "PU" & "PD"
    i = 0
    target = [0]*2
    motor_in = []
    while(i < len(instr)):
        target[0] = int(instr[i])
        target[1] = int(instr[i+1])
        motor_in.append([target[0], target[1]])
        i += 2
    return motor_in

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

def interpolate(targets, curr_location, resolution = 1):
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
