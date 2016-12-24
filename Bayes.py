from __future__ import division
from math import sqrt

__author__ = 'Vasia'

import time
import csv


"""
Once You've calculated the training data, save the arrays to a text file and read in from them
such that you do not have to calculate them each time
preprocess that is
"""



##todolist


        ###########implement hole feature DONE (sort of)#############3
#implement area feature (count of symbols)
#implement thickest row/column feature
    #(i.e. a 1 or 7 is much more likely to have a very thick column and no thick rows, and a number like 5 or 8 (or others)
    #is more likely to have a thick row
#smallish gaps
# identifying gaps will proceed as follows - write a function that determines whether a cell containing a + or # is at the edge of the number
# (meaning that that cell, and its neighbors, have nothing on one side, and a bunch on the other)
# if a cell is an edge cell, look in four rays for 6 cells - look to the top, top left, middle left, bottom left, bottom ( replace
# left with right,bottom, or top if the cell is an edge cell with nothing to the right, bottom, etc.

##0 is for a space (absence of character)
##1 is for the plus +
##2 is for the pound #
cellGeneralProbs1 = [[0 for i in range(28)] for j in range(28)]
cellGeneralProbs2 = [[0 for i in range(28)] for j in range(28)]
cellProbsGivenX0 = [[[0 for i in range(28)] for j in range(28)] for k in range(10)]
cellProbsGivenX1 = [[[0 for i in range(28)] for j in range(28)] for k in range(10)]
cellProbsGivenX2 = [[[0 for i in range(28)] for j in range(28)] for k in range(10)]
cellProbsGivenX0Square = [[[0 for i in range(27)] for j in range(27)] for k in range(10)]
cellProbsGivenX1Square = [[[0 for i in range(27)] for j in range(27)] for k in range(10)]
cellProbsGivenX2Square = [[[0 for i in range(27)] for j in range(27)] for k in range(10)]

precisionDigit = [0 for i in range(10)]


#the maximum amount of holes that a digit has is 7, but I made it 10 in case new data was introduced
#the nth entry in probyholesx is a list for digit n
probYHolesX = [[0 for y in range(10)] for x in range(10)]

probsX = [0 for i in range(10)]
countX = [0 for i in range(10)]

numDataSets = 5000


def countHoles(digitGrid):
    def notVisitedCell(componentMaps,i,j):
        for map in componentMaps:
            if (map.__contains__((i,j))):
                return False
        return True

    componentMaps = []
    holes = []
    for i in range(28):
        for j in range(28):
            if (digitGrid[i][j] == ' '):
                if notVisitedCell(componentMaps,i,j):
                    map = {}
                    DFSTuple = DFSCell(digitGrid,map,i,j,"none")
                    if (DFSTuple[1]):
                        holes.append(DFSTuple[0])
                    componentMaps.append(map)
                    #print(DFSTuple)

    return len(holes)

def DFSCell(digitGrid,map,i,j,prev):
    #if we're in the first row we can look left, down, right (as long as its not the previous cell)
    if (i > 27 or i < 0 or j > 27 or j < 0):
        return [0,False]

    if (digitGrid[i][j] != ' '):
        return [0,True]

    #mark this cell as visited
    map[(i,j)] = True

    #go to other cells, except the previous one
    returnTuple = [0,True]
    if (prev != "up"):
        if ( not map.__contains__((i-1,j))):
            upTuple = DFSCell(digitGrid,map,i-1,j,"down")
            if (not upTuple[1]):
                returnTuple[1] = False
            returnTuple[0] += upTuple[0]

    if (prev != "down"):
        if ( not map.__contains__((i+1,j))):
            downTuple = DFSCell(digitGrid,map,i+1,j,"up")
            if (not downTuple[1]):
                returnTuple[1] = False
            returnTuple[0] += downTuple[0]

    if (prev != "left"):
        if ( not map.__contains__((i,j-1))):
            leftTuple = DFSCell(digitGrid,map,i,j-1,"right")
            if (not leftTuple[1]):
                returnTuple[1] = False
            returnTuple[0] += leftTuple[0]

    if (prev != "right"):
        if ( not map.__contains__((i,j+1))):
            rightTuple = DFSCell(digitGrid,map,i,j+1,"left")
            if (not rightTuple[1]):
                returnTuple[1] = False
            returnTuple[0] += rightTuple[0]

    returnTuple[0] += 1
    return returnTuple





def writeData():
    f = open("bayesprobs.txt",'w')

    for i in range(10):
        if (i != 9):
            f.write(str(probsX[i]) + ",")
        else:
            f.write(str(probsX[i]) + "\n")


    for i in range(28):
        for j in range(28):
            if (j != 27):
                f.write(str(cellGeneralProbs1[i][j]) +",")
            else:
                f.write(str(cellGeneralProbs1[i][j]) + "\n")



    for i in range(28):
        for j in range(28):
            if (j != 27):
                f.write(str(cellGeneralProbs2[i][j]) +",")
            else:
                f.write(str(cellGeneralProbs2[i][j])+"\n")

    for k in range(10):
        for i in range(28):
            for j in range(28):
                if (j != 27):
                    f.write(str(cellProbsGivenX0[k][i][j]) + ",")
                else :
                    f.write(str(cellProbsGivenX0[k][i][j])+"\n")

    for k in range(10):
        for i in range(28):
            for j in range(28):
                if (j != 27):
                    f.write(str(cellProbsGivenX1[k][i][j]) + ",")
                else :
                    f.write(str(cellProbsGivenX1[k][i][j])+"\n")

    for k in range(10):
        for i in range(28):
            for j in range(28):
                if (j != 27):
                    f.write(str(cellProbsGivenX2[k][i][j]) + ",")
                else :
                    f.write(str(cellProbsGivenX2[k][i][j])+"\n")

    for y in range(10):
        for x in range(10):
            if (x!= 9):
                f.write(str(probYHolesX[y][x]) + ",")
            else:
                f.write(str(probYHolesX[y][x])+"\n")

def readPreProcessedTrainingData():
    global probsX
    global cellGeneralProbs1
    global cellGeneralProbs2
    global cellProbsGivenX0
    global cellProbsGivenX1
    global cellProbsGivenX2
    global probYHolesX

    with open('bayesprobs.txt', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        #read probsX
        probsXTemp = reader.next()
        for i in range(10):
            probsX[i] = float(probsXTemp[i])

        #read cellGeneralProbs1
        cellGeneralProbs1Temp = []
        for i in range(28):
            cellGeneralProbs1Temp.append(reader.next())
            for j in range(28):
                cellGeneralProbs1[i][j] = float(cellGeneralProbs1Temp[i][j])

        #read cellGeneralProbs2
        cellGeneralProbs2Temp = []
        for i in range(28):
            cellGeneralProbs2Temp.append(reader.next())
            for j in range(28):
                cellGeneralProbs2[i][j] = float(cellGeneralProbs2Temp[i][j])

        #read cellProbsGivenX0
        cellProbsGivenX0Temp = []
        for k in range(10):
            cellProbsGivenX0Temp.append([])
            for i in range(28):
                cellProbsGivenX0Temp[k].append(reader.next())
                for j in range(28):
                    cellProbsGivenX0[k][i][j] = float(cellProbsGivenX0Temp[k][i][j])


        #read cellProbsGivenX1
        cellProbsGivenX1Temp = []
        for k in range(10):
            cellProbsGivenX1Temp.append([])
            for i in range(28):
                cellProbsGivenX1Temp[k].append(reader.next())
                for j in range(28):
                    cellProbsGivenX1[k][i][j] = float(cellProbsGivenX1Temp[k][i][j])



        #read cellProbsGivenX2
        cellProbsGivenX2Temp = []
        for k in range(10):
            cellProbsGivenX2Temp.append([])
            for i in range(28):
                cellProbsGivenX2Temp[k].append(reader.next())
                for j in range(28):
                    cellProbsGivenX2[k][i][j] = float(cellProbsGivenX2Temp[k][i][j])

        #read probYHolesX
        probYHolesXTemp = []
        for i in range(10):
            probYHolesXTemp.append(reader.next())
            for j in range(10):
                probYHolesX[i][j] = float(probYHolesXTemp[i][j])






def processTrainingData():
    global cellGeneralProbs1
    global cellGeneralProbs2
    global cellProbsGivenX0
    global cellProbsGivenX1
    global cellProbsGivenX2
    global probsX
    global numDataSets
    global probYHolesX



    fimages = open('naivebayes/trainingimages.txt','r')
    flabels = open('naivebayes/traininglabels.txt','r')

    #row will keep track of what line we're up to in the trainingimages document
    #i and j will represent the coordinates of particular cells in seperate 28x28 grids
    #currentDigit refers to digit we're currently collecting data on
    row = 0
    i = 0
    j = 0
    currentDigit = 0

    currentDigitGrid = []

    for line in fimages:

        if (row % 28 == 0):

            if (row != 0):
                #print("Count holes for " + str(currentDigit))
                numHoles = countHoles(currentDigitGrid)
                probYHolesX[currentDigit][numHoles] += 1

            i = 0
            j = 0


            currentDigitGrid = []
            currentDigit = int(flabels.readline())
            probsX[currentDigit] += 1
            #print(currentDigit)

        j = 0
        currentDigitGrid.append([])
        for point in line:
            currentDigitGrid[i].append(point)
            if (point == ' '):
                cellProbsGivenX0[currentDigit][i][j] += 1

            if (point == '+'):
                cellProbsGivenX1[currentDigit][i][j] += 1
                cellGeneralProbs1[i][j] += 1
            if (point == '#'):
                cellProbsGivenX2[currentDigit][i][j] += 1
                cellGeneralProbs2[i][j] += 1

            j+=1




        ##laplace smoothing, add one to the occurence of each featre such that none are zero



        row += 1
        i += 1
        #print(line,end = "")

    for p in range(0,10):
        for q in range(0,28):
            for r in range(0,28):
                cellProbsGivenX0[p][q][r] += 1
                cellProbsGivenX1[p][q][r] += 1
                cellProbsGivenX2[p][q][r] += 1

    for i in range(28):
        line = ""
        for j in range(28):
            cellGeneralProbs1[i][j] /= (numDataSets * 1.0)
            cellGeneralProbs2[i][j] /= (numDataSets * 1.0)

            if (cellGeneralProbs2[i][j] < 0.001):

                line += '      '
            else :
                line += '%2.2f  ' % cellGeneralProbs2[i][j]


        #print(line)

    for k in range(0,10):

        for i in range(0,28):
            line = ""
            for j in range(0,28):
                if (i != 27 and j != 27):
                    cellProbsGivenX0Square[k][i][j] /= probsX[k]

                cellProbsGivenX0[k][i][j] /= probsX[k]
                cellProbsGivenX1[k][i][j] /= probsX[k]
                cellProbsGivenX2[k][i][j] /= probsX[k]

                if (cellProbsGivenX2[k][i][j] < 0.001):
                    line += '      '
                else :
                    line += '%2.2f  ' % cellProbsGivenX2[k][i][j]
            ##print (line)
        ##print("\n")


    for i in range(0,10):
        for j in range(0,10):
            probYHolesX[i][j] /= probsX[i]
        probsX[i] /= 5000

    #print(probYHolesX)
def classifyData():
    global cellGeneralProbs1
    global cellGeneralProbs2
    global cellProbsGivenX0
    global cellProbsGivenX1
    global cellProbsGivenX2
    fimages = open('naivebayes/testimages.txt','r')
    flabels = open('naivebayes/testlabels.txt','r')

    row = 0
    i = 0
    j = 0
    actualDigit = 0
    accuracy = 0

    currentDigitGrid = []

    """
    #probNumerator is numerator of equation that will be iteratively updated -
    # P(A1|X) * ... * P(An|X) * P(B1|X) * ... * P(Bn|X)


    #probDenominator is denominator of equation that will be iteratively updated -
    # P(A1) * ... * P(An) * P(B1) * ... * P(Bn)

    #P(An|X) = cellProbsGivenX1[X][i][j]  for +
    #P(An) = cellGeneralProbs1[i][j]
    #P(Bn|X) = cellProbsGivenX2[X][i][j]  for #
    #P(Bn) = cellGeneralProbs2[i][j]
    """
    probNumerator = [1 for temp in range(10)]
    #probDenominator = [1 for i in range(10)]
    probQuotient = []


    for line in fimages:



        if (row % 28 == 0):
            i = 0
            j = 0


            #if row != 0 and we are here that means we just finished reading test data for at least one digit,
            # we can now multiply probNumerator by P(X) for each X, and then divide numerator and denominator,
            # and then attempt to classify the digit by picking the highest probability in the list
            if (row != 0):

                numHoles = countHoles(currentDigitGrid)
                currentDigitGrid = []









                """
                THIS NEXT LINE THATS no longer COMMENTED OUT
                Adding holes as a feature only increases the accuracy by 0.6%
                """
                for digit in range(10):
                    #########
                    #########

                    probNumerator[digit] *=  (probYHolesX[digit][numHoles])

                    #########
                    #########
                    #########

                    probNumerator[digit] *= probsX[digit]
                    #probQuotient.append(probNumerator[digit] / probDenominator[digit])
                    probQuotient.append(probNumerator[digit])
                    #print("Probability of digit being a " + str(digit) + ": " + str(probQuotient[digit]))


                apparentDigitProbability = max(probQuotient)
                apparentDigit = probQuotient.index(apparentDigitProbability)
                #print("Digit is most likely a " + str(apparentDigit) + " with a probability of " + str(apparentDigitProbability))
                #print("\n")


                countX[actualDigit] += 1
                if (apparentDigit == actualDigit):
                    accuracy += 1

                    precisionDigit[apparentDigit] += 1





            actualDigit = int(flabels.readline())
            probNumerator = [1 for temp in range(10)]
            probQuotient = []

       # if (row == 28 * 5):
           # break

        j = 0
        if (i == 27):
            word = "debug"

        currentDigitGrid.append([])
        for point in line:
            if (point == ' '):
                #for every possible digit, update the numerator of the bayes equation
                for digit in range(10):
                    #if (cellProbsGivenX0[digit][i][j] != 0):
                    probNumerator[digit]   *= (cellProbsGivenX0[digit][i][j])
                    #if (cellGeneralProbs1[i][j] != 0):
                        #probDenominator[digit] *= cellGeneralProbs1[i][j]
                        #print("DIGIT PROBABILITY DENOMINATOR1 FOR " + str(digit)+  " is: " + str(probDenominator[digit]))
                        #print("probability for digit " + str(digit) + " is being multiplied by " + str(cellGeneralProbs1[i][j]))

            if (point == '+'):
                #for every possible digit, update the numerator of the bayes equation
                for digit in range(10):
                    #if (cellProbsGivenX1[digit][i][j] != 0):
                    probNumerator[digit]   *= (cellProbsGivenX1[digit][i][j])
                    #if (cellGeneralProbs1[i][j] != 0):
                        #probDenominator[digit] *= cellGeneralProbs1[i][j]
                        #print("DIGIT PROBABILITY DENOMINATOR1 FOR " + str(digit)+  " is: " + str(probDenominator[digit]))
                        #print("probability for digit " + str(digit) + " is being multiplied by " + str(cellGeneralProbs1[i][j]))

            if (point == '#'):
                for digit in range(10):
                    #if (cellProbsGivenX2[digit][i][j] != 0):
                    probNumerator[digit]   *= (cellProbsGivenX2[digit][i][j])
                    #if (cellGeneralProbs2[i][j] != 0):
                        #probDenominator[digit] *= cellGeneralProbs2[i][j]

            currentDigitGrid[i].append(point)
            j+=1




        row += 1
        i += 1



    print("Total Accuracy:\t\t" + str(  (accuracy / (row / 28)) * 100 ) + "%")
    for l in range(10):
        print("Accuracy of digit " + str(l) + ":\t" + str(   (precisionDigit[l] / countX[l]) * 100  ) + "%")



preProcessed = False

startTime = time.time()
if (preProcessed):
    readPreProcessedTrainingData()



else :
    processTrainingData()
    writeData()

processTime = time.time()

if (preProcessed):
    print("--- %s seconds to read in classifier attributes---" % (time.time() - startTime))

else:
    print("--- %s seconds to proccess training data---" % (time.time() - startTime))

classifyData()

print("--- %s seconds to classify test data---" % (time.time() - processTime))
print("--- %s seconds total---" % (time.time() - startTime))





