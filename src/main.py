import sys
sys.path.append("D:\\Programs\\Python2.7\\Lib\\site-packages\\alglib")
import xalglib as xal

class Pair:
    __index = -1
    __value = -1

    def setParams(self, index, value):
        self.index = index
        self.value = value

    def getIndex(self):
        return self.index

    def getValue(self):
        return self.value

    def toString(self):
        return str(self.index) + ':' + str(self.value)

CONSTANT_TO_COMPARE = 7
# @DESCRIPTION parse date file to array
# @RETURN_VALUE list[]
def parse_date_from_file(file_name):
    file = open(file_name, 'r')
    list = []
    ind = 1
    for line in file:
        tmp = Pair()
        tmp.setParams(ind * 250, (float)(line))
        list.append(tmp)
        ind += 1
    file.close()
    print('--date from file [', file_name, '] parsed successfully')
    return list

# @DESCRIPTION print list[] on console
def print_list(list):
    print('--list values: ')
    for pair in list:
        print(pair.toString())
    print('---------------')

# @DESCRIPTION find top extremum
# @RETURN_VALUE top_dots[]
def find_top_extremum(list):
    top_dots = []
    for i in range(len(list) - 2):
        if (list[i + 1].getValue() > list[i].getValue()):
            if (list[i + 1].getValue() > list[i + 2].getValue()):
                top_dots.append(list[i + 1])
    print('All top extremum was found.')
    return top_dots

# @DESCRIPTION find bot extremum
# @RETURN_VALUE bot_dots[]
def find_bot_extremum(list):
    bot_dots = []
    for i in range(len(list) - 2):
        if (list[i + 1].getValue() < list[i].getValue()):
            if (list[i + 1].getValue() < list[i + 2].getValue()):
                bot_dots.append(list[i + 1])
    print('All bot extremum was found.')
    return bot_dots

# @DESCRIPTION find top interpolation func and values
# @RETURN array with interpolation index and values
def find_interpolant(listExtremum):
    indexes = []
    values = []
    for elem in listExtremum:
        indexes.append(elem.getIndex())
        values.append(elem.getValue())
    ind = indexes[0]
    newIndexes = []
    while ind < indexes[indexes.__len__() - 1]:
        newIndexes.append(ind)
        ind += 50
    newValues = xal.spline1dconvcubic(indexes, values, newIndexes)
    returnArray = []
    for i in xrange(len(newIndexes)):
        tmp = Pair()
        tmp.setParams(newIndexes[i], newValues[i])
        returnArray.append(tmp)
        i += 1
    resultFile = open('D:\ermolaxe\Programming\com.ermolaxe.courseproject\\resources\\result', 'w')
    for elem in returnArray:
        resultFile.write(str(elem.toString()) + '\n')
    resultFile.close()
    return returnArray

# @DESCRIPTION find index by Pair.index
# @RETURN number
def find_index(index, array):
    i = 0
    while index != array[i].getIndex() and i < (array.__len__()-1):
        i += 1
    return i

# @DESCRIPTION find topInterpolant - botInterpolant
# @RETURN array of middle values with step 250
def find_middle_interpolation_values(topExtremum, botExtremum):
    newTopValues = find_interpolant(topExtremum)
    newBotValues = find_interpolant(botExtremum)
    middleDots = []
    if newTopValues[0].getIndex() > newBotValues[0].getIndex() and newTopValues[-1].getIndex() > newBotValues[-1].getIndex():
        botIndex = find_index(newTopValues[0].getIndex(), newBotValues)
        i = 0
        while botIndex < newBotValues.__len__():
            tmp = Pair()
            tmp.setParams(newTopValues[i].getIndex(), (newTopValues[i].getValue() + newBotValues[botIndex].getValue())/2)
            middleDots.append(tmp)
            i += 5
            botIndex += 5
    elif newTopValues[0].getIndex() > newBotValues[0].getIndex() and newTopValues[-1].getIndex() < newBotValues[-1].getIndex():
        botIndex = find_index(newTopValues[0].getIndex(), newBotValues)
        i = 0
        while i < newTopValues.__len__():
            tmp = Pair()
            tmp.setParams(newTopValues[i].getIndex(), (newTopValues[i].getValue() + newBotValues[botIndex].getValue())/2)
            middleDots.append(tmp)
            i += 5
            botIndex += 5
    elif newTopValues[0].getIndex() < newBotValues[0].getIndex() and newTopValues[-1].getIndex() > newBotValues[-1].getIndex():
        topIndex = find_index(newBotValues[0].getIndex(), newTopValues)
        i = 0
        while i < newBotValues.__len__():
            tmp = Pair()
            tmp.setParams(newBotValues[i].getIndex(), (newTopValues[topIndex].getValue() + newBotValues[i].getValue())/2)
            middleDots.append(tmp)
            i += 5
            topIndex += 5
    elif newTopValues[0].getIndex() < newBotValues[0].getIndex() and newTopValues[-1].getIndex() < newBotValues[-1].getIndex():
        topIndex = find_index(newBotValues[0].getIndex(), newTopValues)
        i = 0
        while topIndex < newTopValues.__len__():
            tmp = Pair()
            tmp.setParams(newBotValues[i].getIndex(), (newTopValues[topIndex].getValue() + newBotValues[i].getValue())/2)
            i += 5
            topIndex += 5
    return middleDots

# @DESCRIPTION raznica mezhdu ishodnim i seredinnim signalami
# @RETURN
def find_result(middleDots, prevResults):
    midIndex = 0
    prevIndex = 0
    result = []
    while midIndex < middleDots.__len__():
        if middleDots[midIndex].getIndex() != prevResults[prevIndex].getIndex():
            prevIndex += 1
        elif middleDots[midIndex].getIndex() == prevResults[prevIndex].getIndex():
            tmp = Pair()
            tmp.setParams(middleDots[midIndex].getIndex(), prevResults[prevIndex].getValue() - middleDots[midIndex].getValue())
            result.append(tmp)
            prevIndex += 1
            midIndex += 1
    return result

def is_condition_met(currentSignal, prevSignal, constantToCompare):
    currentSignalIndex = 0
    prevSignalIndex = 0
    chisl = 0
    znam = 0
    while currentSignalIndex < currentSignal.__len__():
        if currentSignal[currentSignal].getIndex() != prevSignal[prevSignalIndex].getValue():
            prevSignalIndex += 1
        else:
            chisl += (prevSignal[prevSignalIndex].getValue() - currentSignal[currentSignalIndex].getValue()) ** 2
    for elem in prevSignal:
        znam += elem.getValue() ** 2
    if constantToCompare < (chisl/znam):
        return True
    else:
        return False

def is_monotonous(signal):
    return find_top_extremum(signal).__len__() == 0 and find_bot_extremum(signal).__len__() == 0


# source code
dataArray = parse_date_from_file('D:\ermolaxe\Programming\com.ermolaxe.courseproject\\resources\\test')

topExtremum = find_top_extremum(dataArray)
print_list(topExtremum)

botExtremum = find_bot_extremum(dataArray)
print_list(botExtremum)

result = find_interpolant(topExtremum)


