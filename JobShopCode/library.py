class Machine:
    '''
    A class for creating machine objects. All machine objects have a name, capacity and a cooldown time.
    Also, each machine object has a list that keeps track of all the intervals in which the machine is 
    occupied.
        Syntax:
        self.busy_times = [[t1, t2]]
    '''
    all_machines = []
    '''
    A list of all the Machine class objects. Every time an object is created, it's added
    to this list.
    '''

    def __init__(self, name):
        self.name = name
        self.capacity = 0
        self.cooldown = 0
        self.busy_times = []
        Machine.all_machines.append(self)

    def getName(self):
        return self.name
    
    def setCapacity(self, capacity):
        self.capacity = capacity

    def getCapacity(self):
        return self.capacity
    
    def setCooldown(self, cooldown):
        self.cooldown = cooldown

    def getCooldown(self):
        return self.cooldown
    
    def addToBusyTimes(self, interval):
        self.busy_times.append(interval)

    def getBusyTimes(self):
        return self.busy_times
    
    def sortBusyTimes(self):
        self.busy_times.sort(key = lambda x: x[-1])
    
    def getBusyTimesLen(self):
        return len(self.busy_times)
    
    def getMachineList():
        return Machine.all_machines


class Part:
    '''
    A class for creating part objects. All part objects have a name, a number of items, a dictionary
    for all the operations for that part and one for the machining schedule of each part.
    Syntax:
        self.operations = {Machine: machining time}
        self.schedule = {Machine: [start time, end time]}
    '''
    all_parts = []
    '''
    A list of all the Part class objects. Every time an object is created, it's added
    to this list.
    '''

    def __init__(self, name):
        self.name = name
        self.items = 0
        self.operations = dict()
        self.schedule = dict()
        Part.all_parts.append(self)

    def longestSchTime(self):
        max = 0
        for interval in self.schedule.values():
            machining_end = interval[1]
            if max < machining_end:
                max = machining_end
        return max
    
    def longestOpTime(self):
        max = 0
        for machine in self.operations.keys():
            time = self.operations[machine]
            if max < time:
                max = time
        return max
    
    def makeCopy(self, part):
        for i in range(1, part.items):
            new_part_name = part.name + " " + str(i)
            new_part = Part(new_part_name)
            new_part.items = 0
            new_part.operations = part.operations.copy()
            new_part.schedule = part.schedule.copy()
    
    def getName(self):
        return self.name
    
    def setItems(self):
        return self.items

    def getItems(self):
        return self.items
    
    def setOperation(self, machine, value):
        self.operations[machine] = value

    def getOperation(self, machine):
        return self.operations[machine]
    
    def getOperationsMachines(self):
        return list(self.operations.keys())
    
    def noOfOperations(self):
        return len(self.operations.keys())
    
    def delOperation(self, machine):
        del self.operations[machine]
    
    def setSchedule(self, machine, interval):
        self.schedule[machine] = interval

    def getSchedule(self):
        return self.schedule.values()
    
    def getScheduleMachines(self):
        return self.schedule.keys()
    
    def getPartList():
        return Part.all_parts
    
    def copyPartList():
        return Part.all_parts.copy()
    
    def orderPartList():
        Part.all_parts.sort(key = lambda part: part.longestOpTime(), reverse = True)

    def orderStageTwo():
        Part.all_parts.sort(key = lambda x: (0 in x, max(x)), reverse=True)

def get_int(line):
    '''
    Extracting numbers from lines.
    '''
    i = 0
    for char in line:
        if char.isdigit():
            i = i * 10 + int(char)
    return i

def time_format(seconds):
    '''
    Formatting seconds into hours:minutes:seconds format
    '''
    result = "{:02d}:{:02d}:{:02d}".format(seconds // 3600, (seconds % 3600) // 60, (seconds % 60))
    return result

def auto_input():
    '''
    For testing the code without manually entering the file path 
    '''
    input_file = r'D:\facultate\2023_Internship_Challenge_Software\Input_Two.txt'
    f = open(input_file, "r")
    return f

def manual_input():
    '''
    For testing with manual entry of the file path.
    '''
    while True:
        try:
            input_file = input("Please insert the file path: ")
            f = open(input_file, "r")
            break
        except FileNotFoundError:
            print("The path given doesn't return any document. Please check the location of your file or the format of the path and try again")
        except OSError:
            print("Invalid path.")
        except:
            print("Invalid argument.")
    return f

def spelling_check(control, line):
    '''
    In order to take spelling errors into consideration, first both the machine name saved
    in machine_list and the one from the line are each converted to lowercase and saved in a set.
    Then, we take the number of different characters from each set, turn it into a percentage
    by dividing it with then length of the set machine_name and the lower the percentage,
    the closer the 2 values are. 0.1 is chosen as treshold to take into consideration matches.
    When a match is found, it's added to parts_processing.
    This method compares all the characters in the 2 names only once, and deduces a similarity percentage.
    The loop iterates through all the machine names until the match is found.
    '''
    control = set(control.lower())
    line = set(line[6:].split(":")[0].lower())
    match = control.symmetric_difference(line)
    match_pct = len(match) / len(control)
    if match_pct < 0.1:
        return True
    else:
        return False
    
def processingTextFile(f):
    for line in f:
        '''
        The loop goes through each line of the file, looking for key phrases that mark the sections of the document
        '''
        if "Available machines" in line:
            '''
            If "Available machines" is found, then for the next lines extract the names of the machines and create Machine class objects.
            Based on the formatting in the file, the name of the machine is extracted by splitting each row at ". ", taking the part after
            the splitting string, eliminating the automatic new line character at the end and saving it in the placeholder variable aux.
            Then, through aux, each name of the machine is added as a key in the machines_charact dict and as an element to the
            machines_list list.
            When the splitting string ". " is no longer found in the line, then the loop exits.
            '''
            for line in f:
                if ". " in line:
                    aux = line.split(". ")[1].strip("\n")
                    machine = Machine(aux)
                else:
                    if "#" in line:
                        continue
                    else:
                        break
        elif "Machine features" in line:
            '''
            If "Machine features" is found, then from the next line onward the presence of a feature is checked by the presence of the
            character ":".
            '''
            index = 0
            for machine in Machine.getMachineList():
                for line in f:
                    if ":" in line:
                        if " one " in line:
                            machine.setCapacity(1)
                        elif " two " in line:
                            machine.setCapacity(2)
                        elif "no limit" in line:
                            machine.setCapacity(-1)    
                        elif "second" in line:
                            sec = get_int(line)
                            machine.setCooldown(sec)
                        elif "none" in line:
                            machine.setCooldown(0)
                    else:
                        break
        elif "Part list" in line:
            '''
        If "Part list" is found, then from the next line onward if it finds a ". " then considers that the line contains a part name.
        When ". " is not found and a "#" is not present, the loop breaks
        The splitting string ". " is used to separate the number order and " - " to separate the name from the item.
        A Part class object is created for each new part. The number of items is saved in the item attribute.
        '''
            for line in f:
                if ". " in line:
                    aux = line.split(". ")[1]
                    name = aux.split(" - ")[0]
                    items = aux.split(" - ")[1]
                    items = items.split(" item")[0].strip("\n")

                    part = Part(name)
                    #Part.part_types.append(name)
                    part.items = get_int(items)
                else:
                    if "#" in line:
                        continue
                    else:
                        break
        elif "Part operations" in line:
            '''
            If the phrase "Part operations" is found, then the next lines checked for the piece and its operations.
            The start of the operations list for each part is identified by looking for ":". 
            '''
            for part in Part.all_parts:
                for line in f:
                    if ":" in line:
                        machine_list = Machine.getMachineList()
                        for machine in machine_list:
                            machine_name = machine.getName()
                            if line != "\n":
                                if spelling_check(machine_name, line):
                                    aux = get_int(line.split(" - ")[1])
                                    part.setOperation(machine_name, aux)
                                    break
                    else:
                        break