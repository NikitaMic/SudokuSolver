from collections import OrderedDict, deque

board = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]
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
        check = number not in board[rowIndex] and number not in columns[columnIndex] and number not in box[checkBoxWithCoordinates(rowIndex, columnIndex)]
        if check is True:
            possibilities.append(number)
    return possibilities


def blankSpaceOptions():
    rowIndex = 0
    for row in board:
        columnIndex = 0
        for num in row:
            if num == 0:
                blankSpaceArray.append([[rowIndex, columnIndex], checkRowColumn(rowIndex, columnIndex), 0])
            columnIndex += 1
        rowIndex += 1

def bruteforce():
    board[blankSpaceArray[0][0][0]][blankSpaceArray[0][0][1]] = (blankSpaceArray[0][1][0])

boxCreator()
columnCreator()
blankSpaceOptions()
print(board)
bruteforce()
print(board)