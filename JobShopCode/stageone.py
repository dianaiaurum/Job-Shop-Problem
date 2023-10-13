'''
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
    aux - used as placeholder
        type: string
    index - used for indexing
        type: int
'''


'''
#For testing the code without manually entering the file path 
input_file = r'D:\facultate\2023_Internship_Challenge_Software\Input_One.txt'
f = open(input_file, "r")
'''

#For testing with manual entry of the file path
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

machines_charact = {}
machines_list = []

parts_processing = {}
parts_list = []

for line in f:
    '''
    The loop goes through each line of the file, looking for key phrases that mark the sections of the document
    '''
    if "Available machines" in line:
        '''
        If "Available machines" is found, then for the next lines extract the names of the machines and store them in machines_charact
        and machine_lists.
        Based on the formatting in the file, the name of the machine is extracted by splitting each row at ". ", taking the part after
        the splitting string, eliminating the automatic new line character at the end and saving it in the placeholder variable aux.
        Then, through aux, each name of the machine is added as a key in the machines_charact dict and as an element to the
        machines_list list.
        When the splitting string ". " is no longer found in the line, then the loop exits.
        '''
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
        '''
        If "Machine features" is found, then from the next line onward the presence of a feature is checked by the presence of the
        character ":".
        Based on the structure of the document, the machines are put in order, so using an index starting from 0, the machines_list
        is used to add the characteristics into the machines_charact. The index increases when only one ":" is found, because all
        machines have only 2 features. When the index is equal to the number of machines, the loop exits.
        The features are split from their order number by the splitting string "- ". Then the name of the feature and the value is split
        using the splitting string ": ".
        '''
        index = 0
        for line in f:
            if ":" in line:
                aux = line.split("- ")[1].strip("\n")
                machines_charact[machines_list[index]] = {aux.split(": ")[0] : aux.split(": ")[1]}
            if line.count(":") == 1:
                index+=1
            if index == len(machines_charact):
                break
    elif "Part list" in line:
        '''
        If "Part list" is found, then from the next line onward if it finds a ". " then considers that the line contains a part name.
        When ". " is not found and a "#" is not present, the loop breaks
        Aux and key are used as placeholder values in order to contain the number of items and the name of the item respectively. 
        The splitting string ". " is used to separate the number order and " - " to separate the name from the item.
        The name of the item is saved in both the parts_processing as key and parts_list, and the number of items is saved for each
        item name key as a dictionary with the structure {"Item": no.}
        '''
        for line in f:
            if ". " in line:
                aux = line.split(". ")[1]
                key = aux.split(" - ")[0]
                value = aux.split(" - ")[1]
                value = value.split(" item")[0].strip("\n")
                dict = "Item"

                parts_processing[key] = {dict : value}
                parts_list.append(key)
            else:
                if "#" in line:
                    continue
                else:
                    break
    elif "Part operations" in line:
        '''
        If the phrase "Part operations" is found, then the next lines checked for the piece and its operations.
        The start of the operations list for each part is identified by looking for two ":". When it's found, the index marks
        the number of the piece the current line is at (which is why index starts from -1). Then, for each part, it goes throught
        the list of machines and if it is found, then it is added to the dictionary with its processing time.
        '''
        index_part = -1
        for line in f:
            if line.count(":") == 2:
                index_part += 1
            for machine in machines_list:
                if machine in line:
                    parts_processing[parts_list[index_part]][machine] = line.split(machine)[1].strip("\n").strip(": ")

'''
Formatting the console output
'''
print("Parts")    
for part in parts_processing.keys():
    print(part)
    for key in parts_processing[part].keys():
        print('{:<10}{:<20}{}'.format("", key, parts_processing[part][key]))

