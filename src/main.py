# -*- encoding: utf-8 -*-

import sys
sys.path.append("D:\\Programs\\Python2.7\\Lib\\site-packages\\alglib")
import xalglib as xal
from Tkinter import *
import tkFileDialog
import matplotlib.pyplot as ptl

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

filename = ""
imagenumb = 0
firstclickflag = True

def parse_data_from_file(file_name):
    file = open(file_name, 'r')
    list = []
    ind = 1
    for line in file:
        tmp = Pair()
        tmp.setParams(ind * 250, (float)(line))
        list.append(tmp)
        ind += 1
    file.close()
    return list

def parse_mid_result_file(file_name):
    file = open(file_name, 'r')
    list = []
    for line in file:
        words = line.split(":")
        tmp = Pair()
        tmp.setParams(float(words[0]), float(words[1]))
        list.append(tmp)
    file.close()
    return list

def find_top_extremum(list):
    t_max = []
    for i in range(1, len(list) - 2):
        if list[i].getValue() > list[i - 1].getValue() and list[i].getValue() >= list[i + 1].getValue():
            t_max.append(list[i])
    return t_max

def find_bot_extremum(list):
    t_min_1 = []
    for i in range(1, len(list) - 2):
        if list[i].getValue() <= list[i - 1].getValue() and list[i].getValue() < list[i + 1].getValue():
            t_min_1.append(list[i])
    return t_min_1

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
    return returnArray

def find_index(index, array):
    i = 0
    while index != array[i].getIndex() and i < (array.__len__() - 1):
        i += 1
    return i

def find_middle_interpolation_values(topExtremum, botExtremum):
    newTopValues = find_interpolant(topExtremum)
    newBotValues = find_interpolant(botExtremum)
    middleDots = []
    if newTopValues[0].getIndex() > newBotValues[0].getIndex() and newTopValues[-1].getIndex() > newBotValues[-1].getIndex():
        botIndex = find_index(newTopValues[0].getIndex(), newBotValues)
        i = 0
        while botIndex < newBotValues.__len__():
            tmp = Pair()
            tmp.setParams(newTopValues[i].getIndex(), (newTopValues[i].getValue() + newBotValues[botIndex].getValue()) / 2)
            middleDots.append(tmp)
            i += 5
            botIndex += 5
    elif newTopValues[0].getIndex() > newBotValues[0].getIndex() and newTopValues[-1].getIndex() < newBotValues[-1].getIndex():
        botIndex = find_index(newTopValues[0].getIndex(), newBotValues)
        i = 0
        while i < newTopValues.__len__():
            tmp = Pair()
            tmp.setParams(newTopValues[i].getIndex(), (newTopValues[i].getValue() + newBotValues[botIndex].getValue()) / 2)
            middleDots.append(tmp)
            i += 5
            botIndex += 5
    elif newTopValues[0].getIndex() < newBotValues[0].getIndex() and newTopValues[-1].getIndex() > newBotValues[-1].getIndex():
        topIndex = find_index(newBotValues[0].getIndex(), newTopValues)
        i = 0
        while i < newBotValues.__len__():
            tmp = Pair()
            tmp.setParams(newBotValues[i].getIndex(), (newTopValues[topIndex].getValue() + newBotValues[i].getValue()) / 2)
            middleDots.append(tmp)
            i += 5
            topIndex += 5
    elif newTopValues[0].getIndex() < newBotValues[0].getIndex() and newTopValues[-1].getIndex() < newBotValues[-1].getIndex():
        topIndex = find_index(newBotValues[0].getIndex(), newTopValues)
        i = 0
        while topIndex < newTopValues.__len__():
            tmp = Pair()
            tmp.setParams(newBotValues[i].getIndex(), (newTopValues[topIndex].getValue() + newBotValues[i].getValue()) / 2)
            i += 5
            topIndex += 5
    return middleDots


def find_result(middleDots, prevResults):
    midIndex = 0
    prevIndex = 0
    result = []
    while midIndex < middleDots.__len__():
        if middleDots[midIndex].getIndex() != prevResults[prevIndex].getIndex():
            prevIndex += 1
        elif middleDots[midIndex].getIndex() == prevResults[prevIndex].getIndex():
            tmp = Pair()
            tmp.setParams(middleDots[midIndex].getIndex(),
                          prevResults[prevIndex].getValue() - middleDots[midIndex].getValue())
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
        if currentSignal[currentSignalIndex].getIndex() != prevSignal[prevSignalIndex].getIndex():
            prevSignalIndex += 1
        else:
            chisl += (prevSignal[prevSignalIndex].getValue() - currentSignal[currentSignalIndex].getValue()) ** 2
            currentSignalIndex += 1
    for elem in prevSignal:
        znam += elem.getValue() ** 2
    if constantToCompare > (chisl / znam):
        return True
    else:
        return False

def is_monotonous(signal):
    return find_top_extremum(signal).__len__() == 0 and find_bot_extremum(signal).__len__() == 0

def choose_file():
    global filename
    filename = tkFileDialog.askopenfilename()

def one_step():
    global firstclickflag
    global filename
    global imagenumb
    if firstclickflag:
        firstclickflag = False
        data = parse_data_from_file(filename)
        indexlist = []
        valuelist = []
        i = 0
        while i < data.__len__()-2:
            indexlist.append(data[i].getIndex())
            valuelist.append(data[i].getValue())
            i += 1
        ptl.plot(indexlist, valuelist)
        ptl.savefig('D:\ermolaxe\Programming\com.ermolaxe.courseproject\image\stepalgorithm\\startdata.png')
        file = open('D:\ermolaxe\Programming\com.ermolaxe.courseproject\\resources\middleresult.txt', 'w')
        for i in data:
            file.write(str(i.toString()+'\n'))
        file.close()
        filename = 'D:\ermolaxe\Programming\com.ermolaxe.courseproject\\resources\middleresult.txt'
        ptl.show()
    else:
        data = parse_mid_result_file(filename)
        epsilon = float(coeff.get())
        notFinalResult = inner_alg(data)
        isConditionMet = is_condition_met(notFinalResult, data, epsilon)
        newNotFinalResult = notFinalResult
        while not isConditionMet:
            newNotFinalResult = inner_alg(notFinalResult)
            isConditionMet = is_condition_met(newNotFinalResult, notFinalResult, epsilon)
            notFinalResult = newNotFinalResult
        indexlist = []
        valuelist = []
        i = 0
        while i < newNotFinalResult.__len__() - 2:
            indexlist.append(newNotFinalResult[i].getIndex())
            valuelist.append(newNotFinalResult[i].getValue())
            i += 1
        ptl.plot(indexlist, valuelist)
        ptl.savefig('D:\ermolaxe\Programming\com.ermolaxe.courseproject\image\stepalgorithm\\moda' + str(imagenumb) + '.png')
        imagenumb += 1
        if not is_monotonous(newNotFinalResult):
            newSignal = find_result(newNotFinalResult, data)
            file = open('D:\ermolaxe\Programming\com.ermolaxe.courseproject\\resources\middleresult.txt', 'w')
            for i in newSignal:
                file.write(str(i.toString() + '\n'))
            file.close()
        ptl.show()
        ptl.clf()

def full_alg():
    data = parse_data_from_file(filename)
    epsilon = float(coeff.get())
    indexlist = []
    valuelist = []
    i = 0
    while i < data.__len__()-2:
        indexlist.append(data[i].getIndex())
        valuelist.append(data[i].getValue())
        i += 1
    ptl.plot(indexlist, valuelist)
    ptl.savefig('D:\ermolaxe\Programming\com.ermolaxe.courseproject\image\\fullalgorithm\\startdata.png')
    ptl.show()
    ptl.clf()
    result = process_alg(data, epsilon)
    isMonotonous = is_monotonous(result)
    while not isMonotonous:
        result = process_alg(result, epsilon)
        isMonotonous = is_monotonous(result)
    return result

def process_alg(data, epsilon):
    global imagenumb
    notFinalResult = inner_alg(data)
    isConditionMet = is_condition_met(notFinalResult, data, epsilon)
    newNotFinalResult = notFinalResult
    while not isConditionMet:
        newNotFinalResult = inner_alg(notFinalResult)
        isConditionMet = is_condition_met(newNotFinalResult, notFinalResult, epsilon)
        notFinalResult = newNotFinalResult
    indexlist = []
    valuelist = []
    i = 0
    while i < newNotFinalResult.__len__() - 2:
        indexlist.append(newNotFinalResult[i].getIndex())
        valuelist.append(newNotFinalResult[i].getValue())
        i += 1
    ptl.plot(indexlist, valuelist)
    ptl.savefig('D:\ermolaxe\Programming\com.ermolaxe.courseproject\image\\fullalgorithm\\moda'+str(imagenumb)+'.png')
    imagenumb += 1
    ptl.clf()
    result = find_result(newNotFinalResult, data)
    return result

def inner_alg(data):
    topExtremum = find_top_extremum(data)
    botExtremum = find_bot_extremum(data)
    if topExtremum.__len__() >= 2 and botExtremum.__len__() >= 2:
        middleDots = find_middle_interpolation_values(topExtremum, botExtremum)
        notFinalResult = find_result(middleDots, data)
        return notFinalResult
    else:
        return data

# user interface
root = Tk()
root.title("Эмпирическая декомпозиция мод")
root.geometry("460x100")
root.config(background="#D3F8B0")

choose_file_btn = Button(root, text='Выбрать файл', background="#9DD06D", foreground="#27292B", padx=3, pady=3,
                         command=choose_file).place(x=20, y=10, width=100, height=50)
one_step_btn = Button(root, text='Один шаг алгоритма', background="#9DD06D", foreground="#27292B", padx=3, pady=3,
                      command=one_step).place(x=130, y=10, width=140, height=50)
full_alg_btn = Button(root, text='Выполнить весь алгоритм', background="#9DD06D", foreground="#27292B", padx=3, pady=3,
                      command=full_alg).place(x=280, y=10, width=160, height=50)

radioNumber = IntVar()
radioNumber.set(1)
lab = Label(root, bg="#D3F8B0", text='Коэффициент для сравнения нормированного квадрата разностей')
lab.place(x=10, y=72)
coeff = Entry(root, width=10, bd=2)
coeff.place(x=385, y=72)

root.mainloop()