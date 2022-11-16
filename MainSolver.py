from collections import OrderedDict, deque


board = [[3, 1, 6, 5, 7, 8, 4, 9, 2 ],
          [ 5, 2, 9, 1, 3, 4, 7, 6, 8 ],
          [ 4, 8, 7, 6, 2, 9, 5, 3, 1 ],
          [ 2, 6, 3, 0, 1, 5, 9, 8, 7 ],
          [ 9, 7, 4, 8, 6, 0, 1, 2, 5 ],
          [ 8, 5, 1, 7, 9, 2, 6, 4, 3 ],
          [ 1, 3, 8, 0, 4, 7, 2, 0, 6 ],
          [ 6, 9, 2, 3, 5, 1, 8, 7, 4 ],
          [ 7, 4, 5, 0, 8, 6, 3, 1, 0]]

columns = []
column = []
box = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
numbersToCheck = []

checkedValue = ""
blankSpaceArray = []


def columnCreator():
    i = 0
    while i < 9:
        for row in board:
            column.append(row[i])
        columns.append(column.copy())
        column.clear()
        i += 1


def boxCreator():
    rowIndex = 0
    columnIndex = 0
    boxNumber = 1
    for x in board:
        if 0 <= rowIndex <= 2:
            boxNumber = 1
        if 3 <= rowIndex <= 5:
            boxNumber = 4
        if 6 <= rowIndex <= 9:
            boxNumber = 7
        for y in range(0, 3):
            box[boxNumber].append(x[columnIndex])
            columnIndex += 1
        boxNumber += 1
        for y in range(3, 6):
            box[boxNumber].append(x[columnIndex])
            columnIndex += 1
        boxNumber += 1
        for y in range(6, 9):
            box[boxNumber].append(x[columnIndex])
            columnIndex += 1
        boxNumber += 1
        columnIndex = 0
        rowIndex += 1


def checkBoxWithCoordinates(rowIndex, columnIndex):
    boxNumber = 0
    if rowIndex < 3 and columnIndex < 3:
        boxNumber = 1
    elif rowIndex < 3 and 2 < columnIndex < 6:
        boxNumber = 2
    elif rowIndex < 3 and columnIndex > 5:
        boxNumber = 3
    elif 2 < rowIndex < 6 and columnIndex < 3:
        boxNumber = 4
    elif 2 < rowIndex < 6 and 2 < columnIndex < 6:
        boxNumber = 5
    elif 2 < rowIndex < 6 and columnIndex > 5:
        boxNumber = 6
    elif 5 < rowIndex and columnIndex < 3:
        boxNumber = 7
    elif 5 < rowIndex and 2 < columnIndex < 6:
        boxNumber = 8
    elif rowIndex > 5 and columnIndex > 5:
        boxNumber = 9

    return boxNumber


def checkRowColumn(rowIndex, columnIndex):
    possibilities = []
    for number in range(1, 10):
        check = number not in board[rowIndex] and number not in columns[columnIndex] and number not in box[
            checkBoxWithCoordinates(rowIndex, columnIndex)]
        if check is True:
            possibilities.append(number)
    return possibilities

def fillBox(row, column, numberToFill):
    boxNr = checkBoxWithCoordinates(row, column)
    rowAdjustor = 0
    columnAdjustor = 0
    boxIndex = 0
    if boxNr in [2, 5, 8]:
        columnAdjustor = -3
    elif boxNr in [3, 6, 9]:
        columnAdjustor = -6
    if 3 < boxNr < 7:
        rowAdjustor = -3
    elif 6 < boxNr < 10:
        rowAdjustor = -6
    boxIndex = ((row + rowAdjustor) * 3) + (column + columnAdjustor)
    box[boxNr][boxIndex] = numberToFill

def getAllBlankSpacePossibilities(rowIndex, columnIndex):
    if columnIndex == 8:
        rowIndex += 1
        columnIndex = 0
    else:
        columnIndex += 1
    for row in board[rowIndex:]:
        for num in row[columnIndex:]:
            if num == 0:
                blankSpaceArray.append([[rowIndex, columnIndex], checkRowColumn(rowIndex, columnIndex), 9])
            columnIndex += 1
            if columnIndex > 8:
                columnIndex = 0
                rowIndex += 1
                if rowIndex > 8:
                    break
                continue



def fillPositionInBoard(numOfBlankSpace, pointer):
    #put number in board
    board[blankSpaceArray[numOfBlankSpace][0][0]][blankSpaceArray[numOfBlankSpace][0][1]] = \
        (blankSpaceArray[numOfBlankSpace][1][pointer])
    rowIndex = blankSpaceArray[numOfBlankSpace][0][0]
    columnIndex = blankSpaceArray[numOfBlankSpace][0][1]
    #put number in box
    fillBox(rowIndex, columnIndex, blankSpaceArray[numOfBlankSpace][1][pointer])
    #put number in column
    columns.clear()
    columnCreator()
    keepPreviousPossibilities = numOfBlankSpace + 1
    del blankSpaceArray[keepPreviousPossibilities:]
    getAllBlankSpacePossibilities(rowIndex, columnIndex)

# possible room for optimization: dont calculate all possibilites for all original blankspaces
def bruteforce():
    numOfBlankSpace = 0
    while numOfBlankSpace < len(blankSpaceArray):
        # No possibilites
        if len(blankSpaceArray[numOfBlankSpace][1]) == 0:
            # We go one position back
            numOfBlankSpace -= 1
            # If pointer exceeds the end of array len we reset pointer and repeat
            while blankSpaceArray[numOfBlankSpace][2] == (len(blankSpaceArray[numOfBlankSpace][1]) - 1):
                #remove impossible value from board
                board[blankSpaceArray[numOfBlankSpace][0][0]][blankSpaceArray[numOfBlankSpace][0][1]] = 0
                #remove impossible value from box
                fillBox(blankSpaceArray[numOfBlankSpace][0][0], blankSpaceArray[numOfBlankSpace][0][1], 0)
                #refresh columns
                columns.clear()
                columnCreator()
                blankSpaceArray[numOfBlankSpace][2] = 0
                numOfBlankSpace -= 1
            if blankSpaceArray[numOfBlankSpace][2] < (len(blankSpaceArray[numOfBlankSpace][1]) - 1):
                blankSpaceArray[numOfBlankSpace][2] += 1
                fillPositionInBoard(numOfBlankSpace, blankSpaceArray[numOfBlankSpace][2])
                numOfBlankSpace += 1
    # Filling Position with value for the first time
        elif blankSpaceArray[numOfBlankSpace][2] == 9:
            blankSpaceArray[numOfBlankSpace][2] = 0
            fillPositionInBoard(numOfBlankSpace, blankSpaceArray[numOfBlankSpace][2])
            numOfBlankSpace += 1

        else:
            fillPositionInBoard(numOfBlankSpace, blankSpaceArray[numOfBlankSpace][2])
            numOfBlankSpace += 1

boxCreator()
columnCreator()
getAllBlankSpacePossibilities(0, -1)
bruteforce()
print(board)
