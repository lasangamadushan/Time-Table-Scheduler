import argparse

subjects = []
rooms = []
slots = {}
assignments = []

def readInput(name):        #read input file and store in subjects array and in rooms array
    global subjects
    global rooms
    inp =  open(name, 'r')
    data = inp.read()
    lines = data.split('\n')
    inputValues = []
    for line in lines:
        inputValues.append(line.split(','))
    subjects = inputValues[:-1]
    rooms = inputValues[-1]

def writeOutput(fileName): #write output file using completed assigned array
    outp = open(fileName, 'w')
    line = ""
    data = ""
    for r in assignments:
        for c in r:
            if(c):
                line += str(c) + ','
        line = line[:-1]+"\n"
        data += line
        line = ""
    outp.write(data)
            

def assign(subjects,selection): #assign timeslots and rooms using minimum remaining values and forward checking
    global assignments
    result = False
    if(len(subjects)==0):
        return True
    else:
        unmodifiedSub = subjects
        remainings = sortByLength(subjects)     #sort by number of remaining options
        if(remainings[0][1]=='c'):              #get the subject with minimum remaining values
            for i in range(len(assignments)):
                if(assignments[i][0]==remainings[0][0]):
                    assignments[i][1]=remainings[0][selection]
                    timeslot = remainings[0][selection]
                    for j in range(len(subjects)):              #keep track remaining legal values for unassigned subjects
                        if timeslot in subjects[j]:
                            if len(subjects[j])>3:              #check whether subject has at least one legal value
                                subjects[j].remove(timeslot)
                            else:
                                return False
                    result = assign(subjects[1:], selection)    #check the result of forward assignings
                    
        elif(remainings[0][1]=='o'):            #get the subject with minimum remaining values
            for i in range(len(assignments)):
                if(assignments[i][0]==remainings[0][0]):
                    assignments[i][1]=remainings[0][selection]
                    timeslot = remainings[0][selection]
                    for j in range(len(subjects)):              #keep track remaining legal values for unassigned subjects
                        if timeslot in subjects[j]:
                            if (subjects[j][1]=='c'):
                                if len(subjects[j])>3:          #check whether subject has at least one legal value
                                    subjects[j].remove(timeslot)
                                else:
                                    return False
                            elif (subjects[j][1]=='o'):         #assign any room if all rooms are available
                                if (slots[timeslot] ==0):
                                    assignments[i][2]=rooms[0]
                                    slots[timeslot] = [rooms[0]]
                                else:
                                    for room in rooms:
                                        if(room not in slots[timeslot]):    #check available rooms and assign
                                            assignments[i][2]=room
                                            slots[timeslot].append(room)
                                            
                                
                    result = assign(subjects[1:], selection)    #check the result of forward assignings

                    
        if (result == False):                       #if current selection is not suitable, do it again with another selection
            return assign(unmodifiedSub, selection+1)
                          

def main(inputFile, outputFile):
    readInput(inputFile)        #read input file
    for subject in subjects:
        for slot in subject[2:]:
            if (slot not in slots):     #initialize all slots as free and available
                slots[slot]= 0
        assignments.append([subject[0], 0, 0])  #initialize the assignment array
    assign(subjects,2)          # do assignments
    writeOutput(outputFile)     #write to the outputfile
            
def sortByLength(L):            #sort array by length of its elements
    for i in range(len(L)):
        for j in range(1,len(L)-i):
            if(len(L[j-1])>len(L[j])):
                temp = L[j-1]
                L[j-1] = L[j]
                L[j] = temp
    return L


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Input File Name")    #Enter input file name
    parser.add_argument("outputFile", help="Output File Name")  #Enter output file name
    args = parser.parse_args()
    main(args.inputFile, args.outputFile)                       #call main function with two arguments
