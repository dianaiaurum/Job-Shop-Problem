def get_int(line):
    i = 0
    for char in line:
        if char.isdigit():
            i = i * 10 + int(char)
    return i

def time_format(seconds):
    result = "{:02d}:{:02d}:{:02d}".format(seconds // 3600, (seconds % 3600) // 60, (seconds % 60))
    return result

#For testing the code without manually entering the file path 
def auto_input():
    input_file = r'D:\facultate\2023_Internship_Challenge_Software\Input_One.txt'
    f = open(input_file, "r")
    return f


#For testing with manual entry of the file path
def manual_input():
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

f = manual_input()

'''
We assume that all the part operations are written in the order that the machines were presented.
The order in which the parts are machined is first based on the longest machining time, then the number
of machines in part operations. This order is saved as a list in parts_order.
Variables:
machines_charact
        type: dictionary
        structure: {Machine Name : {"Capacity" : capacity, "Cooldown time" : cooldown time}}           
machines_list - contains all the names of the machines
    type: list
parts_processing
    type: dictionary
    structure: {Part Name : {"Item" : no. of items to process, First machine : time to spend on that machine, Second machine : time to spend on that machine}}
parts_list - contains all the names of the parts
    type: list
c_part_schedule - the machining schedule of the part currenty being processed
    type: dictionary
    structure: {Machine name : [machining start, machining end]}
parts_schedule - dictionary in which the entire machining schedule is saved
    typr: dict()
    structure: {Part name : {Machine name : [machining start, machining end]}}
aux - used as placeholder
    type: string
index - used for indexing
    type: int
'''

machines_charact = {}
machines_list = []

parts_processing = {}
parts_list = []

c_part_schedule = dict(zip(machines_list, map(lambda x: [], machines_list)))
parts_schedule = dict()
cooldown_times = dict()

for line in f:
    '''
    Variables:
    c_machine = current machine
    c_part = current part
    '''
    if "Available machines" in line:
        for line in f:
            if ". " in line:
                aux = line.split(". ")[1].strip("\n")
                machines_charact[aux] = ""
                machines_list.append(aux)
            else:
                if "#" in line:
                    continue
                else:
                    break
    elif "Machine features" in line:
        index = 0
        for line in f:
            if line.count(":") == 2:
                c_machine = machines_list[index]
                machines_charact[c_machine] = []
            if ":" in line:
                if " one " in line:
                    machines_charact[c_machine].append(1)
                elif "second" in line:
                    sec = get_int(line)
                    machines_charact[c_machine].append(sec)
                elif "none" in line:
                    machines_charact[c_machine].append(0)
            if line.count(":") == 1:
                index+=1
            if index == len(machines_charact):
                break
    elif "Part list" in line:
        for line in f:
            if ". " in line:
                aux = line.split(". ")[1]
                c_part = aux.split(" - ")[0]
                value = aux.split(" - ")[1]
                value = value.split(" item")[0].strip("\n")

                parts_processing[c_part] = list()
                parts_processing[c_part].append(get_int(value))
                parts_list.append(c_part)
            else:
                if "#" in line:
                    continue
                else:
                    break
    elif "Part operations" in line:
        index_part = -1
        index_machine = 0
        for line in f:
            if line.count(":") == 2:
                index_part += 1
                index_machine = 0
            for machine in machines_list:
                if machine in line:
                    c_part = parts_list[index_part]
                    aux = get_int(line.split("-")[1])
                    parts_processing[c_part].append(aux)
                    line = f.readline()
                else:
                    parts_processing[c_part].append(0)


parts_processing_copy = parts_processing.copy()

#For each part, we check how many items there need to be and add them as different parts to part_order
for key in parts_processing_copy.keys():
    if parts_processing[key][0] > 1:
        new_key = key + "+"
        parts_processing[new_key] = parts_processing[key][1:]
    parts_processing[key] = parts_processing[key][1:]

parts_order = sorted(parts_processing.values(), key = lambda x: (0 in x, max(x)), reverse=True)

for list in parts_order:
    for key, value in parts_processing.items():
        if value == list:
            parts_schedule[key] = None

#adding to memory all the machines with cooldown times and the cooldown time
for machine in machines_charact.keys():
    if machines_charact[machine][1] > 0:
        cooldown_times[machine] = machines_charact[machine][1]

machine_schedule = dict((key, None) for key in machines_list)

for part in parts_order:
    '''
    Based on the order in parts_order, each part is taken, its machining interval for each machine
    is computed and added to part_schedule. For each part, the list of machines machine_list is 
    iterated.
    Computing the machining time is done by 
    Variable:
    c_part_schedule - holds the machining schedule for the current part 
        type: dict
        structure: {Machine name : [start processing time, end processing time]}
    last_time - holds the value of the time at which the last machining operation ended for the 
                current part
        type: int
    '''
    last_time = 0
    c_part_schedule = dict(zip(machines_list, map(lambda x: [0, 0], machines_list)))
    if parts_order.index(part) == 0:
        '''
        For the first machining of the first part in order, the start time is 0 and the end time
        is the machining time for the first machining operation, and after the start time is the end time
        of the previus machining operation and the end time is the start time + the machining time
        last_time takes the value of the end time of this machining operation
        '''
        for machine, parts_time in zip(c_part_schedule.keys(), part):
            if parts_time != 0:
                c_part_schedule[machine][0] = last_time    #machining start time
                c_part_schedule[machine][1] = parts_time + last_time   #machining end time
                last_time = c_part_schedule[machine][1]       
    else:
        '''
        For all the other parts, for each machine for which the machining time is not 0 we compute an intitial interval by taking the 
        time at which the previous machining ended and adding to it the machining time.
        If its the first machining, then the starting time is 0.
        After that, we check for each machining time if its outside the working intervals of its machine. If it is, then it is saved in
        parts_schedule. If not, then all the intervals of that part are pushed up by 50, as to not lose continuity, and the check is done again
        until all the intervals are in a free slot. 
        After adding the parts schedule to parts_schedule, the cooling time is added to the intervals.
        '''
        wrong = 1
        max = 0
        for key in parts_schedule.keys():
            if parts_schedule[key] != None:
                m = machines_list[0]
                if max < parts_schedule[key][m][1]:
                    max = parts_schedule[key][m][1]
        while wrong == 1:
            wrong = 0
            for machine, parts_time in zip(c_part_schedule.keys(), part):
                if parts_time != 0:
                    if part.index(parts_time) == 0:
                        c_part_schedule[machine][0] = max
                        c_part_schedule[machine][1] = max + parts_time
                    else:
                        c_part_schedule[machine][1] = parts_time + last_time
                        c_part_schedule[machine][0] = last_time
                    last_time = c_part_schedule[machine][1]
            for key in parts_list:
                for machine in machines_list:
                    if parts_schedule[key] != None and parts_schedule[key][machine] != [0, 0] and c_part_schedule[machine] != [0, 0]:
                        if parts_schedule[key][machine][0] >= c_part_schedule[machine][1] or parts_schedule[key][machine][1] <= c_part_schedule[machine][0]:
                            continue
                        else:
                            wrong = 1
                            max += 50
                            break
                if wrong == 1:
                    break
    for key, val in parts_processing.items():
        if val == part:
            parts_schedule[key] = c_part_schedule
            break
    del parts_processing[key]
    if cooldown_times:
        for machine in cooldown_times.keys():
            c_part_schedule[machine][1] += cooldown_times[machine]


#transforming all the intervals into the 00:00:00 format
for value in parts_schedule.values():
    for interval in value.values():
        interval[0] = time_format(interval[0])
        interval[1] = time_format(interval[1])

final_time = 0

#printing final schedule
for part_name in parts_list:
    print('{:<10}{}'.format("", part_name))
    index = 1
    for part, process in parts_schedule.items():
        if part_name in part:
            print(index, ".")
            for machine, interval in process.items():
                print('{:<30}{}'.format(machine, interval))
                final_time = interval[1]
            index += 1

print("Total process time", final_time)

