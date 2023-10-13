from library import Machine
from library import Part
import library as l
import getinput as gui
import tkinter as tk

#f = l.auto_input()

f = gui.f
l.processingTextFile(f)

'''
Since continuity is no longer a concern, first we schedule the first machining operation
based on the longest machining time of each part. After this, we loop the parts order and 
schedule the part with the lowest machining time each time. When a machining operation is done, it's 
deleted from the part's operations list.
'''

for part in Part.getPartList():
    '''
    For each part, we check how many items there need to be and make new objects of class Part
    '''
    if part.getItems() > 1:
        part.makeCopy(part)

#ordering all the parts by the longest machining time
Part.orderPartList()

last_time = 0

parts_list = Part.copyPartList()

for part in parts_list:
    '''
    Scheduling the first operation for each part. It is taken into consideration that each part has the same first machining operation.
    '''
    first_machine = Machine.getMachineList()[0]
    first_machine_name = first_machine.getName()
    free_machines = first_machine.getCapacity()
    machining_time = part.getOperation(first_machine_name)
    interval = [last_time, last_time + machining_time]
    part.setSchedule(first_machine_name, interval)
    first_machine_busy_times = first_machine.getBusyTimes()
    if [last_time, last_time + machining_time] not in first_machine_busy_times:
        cooldown = first_machine.getCooldown()
        period = [last_time, last_time + machining_time + cooldown]
        first_machine.addToBusyTimes(period)  
    last_time += machining_time
    part.delOperation(first_machine_name)

#Sorting the part list by the longest machining time of each machine
parts_list = sorted(Part.getPartList(), key = lambda part: part.longestOpTime(), reverse = True)

while len(parts_list) != 0:
    '''
    Scheduling all the other operations in the order of which they are finishing their last operation.
    The initial interval for the next machining is starting from the finish time of the last operation and
    ending by adding the machining time.
    Then the interval is checked against the busy times of the machine. If it doesn't intersect with an already occupied 
    interval then it's added to the parts schedule and the machine's busy times. It it does, we add 10 to both ends of the 
    interval and compare again.
    Completed operations are deleted from the list.
    Finished parts are deleted from the list.
    '''
    min = 9999999999999999
    max = 0
    for part in parts_list:
        for interval in part.getSchedule():
            machining_end = interval[1]
            if max < machining_end:
                max = machining_end
        if min > max:
            min = max
            c_part = part
    c_machine_name = c_part.getOperationsMachines()[0]
    next_machine = next((machine for machine in Machine.getMachineList() if machine.getName() == c_machine_name), None)
    next_machine_name = next_machine.getName()
    t_start = min #previous end time
    t_working = c_part.getOperation(next_machine_name)
    t_end = t_start + t_working
    inc = 0
    wrong = 1
    while wrong == 1:
        wrong = 0 
        t_start += inc
        t_end += inc
        next_machine.sortBusyTimes()
        if next_machine.getBusyTimesLen() > 0:
            free_machines = next_machine.getCapacity()
            busy_times = next_machine.getBusyTimes()
            for interval in busy_times:
                if t_start in range(interval[0], interval[1]) or t_end in range(interval[0], interval[1]):
                    if free_machines == 1:
                        wrong = 1
                        inc = 50
                        break
                    else:
                        free_machines -= 1
    busy_times = next_machine.getBusyTimes()
    if [t_start, t_end] not in busy_times:
        cooldown = next_machine.getCooldown()
        period = [t_start, t_end + cooldown]
        next_machine.addToBusyTimes(period)
    c_part.setSchedule(next_machine_name, [t_start, t_end])
    c_part.delOperation(next_machine_name)
    for item in parts_list:
        if item.noOfOperations() == 0:
            del parts_list[parts_list.index(item)]
            
window = tk.Tk()

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results = tk.Text(window, yscrollcommand=scrollbar.set)
results.pack(side=tk.LEFT, fill=tk.BOTH)

#Printing schedule
all_parts = Part.getPartList()
max = 0 #part final time
all_max = 0 #overall final one
for part in all_parts:
    results.insert(tk.END, '{:<10}{}'.format("", part.getName()))
    max = 0
    for interval in part.getSchedule():
        machining_end = interval[1]
        if max < machining_end:
            max = machining_end
    part_schedule = part.getSchedule()
    for interval in part_schedule:
        interval[0] = l.time_format(interval[0])
        interval[1] = l.time_format(interval[1])
    results.insert(tk.END, '\n'.join(map(lambda item: f'\n{item[0]}\n    {item[1]}\n', zip(part.getScheduleMachines(), part_schedule))))
    if all_max < max:
        all_max = max

results.insert(tk.END, "Total time:")
results.insert(tk.END, l.time_format(all_max))

width = 50

results.config(width=width)

window.mainloop()