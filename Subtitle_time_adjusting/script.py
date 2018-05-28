import re
import os

#fileName = input("Enter the input file name: ")
print(os.name)
print(os.getcwd())
ls = os.listdir('.')
print(ls[1])

print("Hello World!!")

def timeInUnits(time):
    timeUnits = dict()
    mileSecond = time%1000
    timeUnits["mileSecond"] = mileSecond
    second = time//1000
    timeUnits["second"] = second
    timeUnits["minute"] = 0
    if second > 60:
        minute = second // 60
        timeUnits["minute"] = minute
        second = second % 60
        timeUnits["second"] = second
    return timeUnits

'''
System.out.format("%02d\n", i)
'''

def timeShiftForward(timer, timeUnits):
    timer = timer.split(',')
    mileSecondCarry = 0
    
    mileTimer = int(timer[1]) + timeUnits["mileSecond"]
    mileSecondCarry = mileTimer // 1000
    mileTimer = str(mileTimer % 1000).zfill(3)

    timer = timer[0].split(':')

    secondTimer = int(timer[2]) + timeUnits["second"] + mileSecondCarry
    secondTimerCarry = secondTimer // 60
    secondTimer = str(secondTimer).zfill(2)

    minuteTimer = str(int(timer[1]) + timeUnits["minute"] + secondTimerCarry).zfill(2)
    # No need of carry adding

    timer = timer[0] + ":" + minuteTimer + ":" + secondTimer + "," + mileTimer
    #print(timer)
    return timer


fileName = "Input_subtitle.srt"
file = open(fileName,'r')

#time = int(input("Enter the in mileSecond you want to start time of subtitle: "))
time = 71500
timeUnits = timeInUnits(time)
print(timeUnits)

outputFile = open('Output_subtitle.srt', 'a')

for line in file:
    line = line.strip()
    if re.search(' --> ', line):
        timer = line.split(' --> ')
        print(timer)
        
        startTimer = timer[0]
        endTimer = timer[1]
        
        startTimerShifted = timeShiftForward(startTimer, timeUnits)
        endTimerShifted = timeShiftForward(endTimer, timeUnits)

        timer = [startTimerShifted, endTimerShifted]
        
        print(timer,"\n")

        line = timer[0] + " --> " + timer[1]
    outputFile.write(line)
    outputFile.write('\n')

outputFile.close()
file.close()
