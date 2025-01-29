import threading
import os

rows = False
cols = False
grids = False

def checkNums(numLists):
    allowedNums = list(range(1, 10))
    for set in numLists:
        seenNums = []
        for num in set:
            if num in allowedNums and num not in seenNums:
                seenNums.append(num)
            else:
                return False

    return True

def checkRows(rowStrings):
    listOfRows = []
    for i in range(9):
        tempList = []
        for j in range(9):
            tempList.append(int(rowStrings[i][j]))
        listOfRows.append(tempList)

    if checkNums(listOfRows):
        global rows
        rows = True

def checkCols(rowStrings):
    listOfCols = []
    for i in range(9):
        tempList = []
        for j in range(9):
            tempList.append(int(rowStrings[j][i]))
        listOfCols.append(tempList)

    if checkNums(listOfCols):
        global cols
        cols = True

def checkGrids(rowStrings):
    listOfGrids = []
    for i in range(3):
        for j in range(3):
            tempList = []
            for k in range(3):
                for l in range(3):
                    tempList.append(int(rowStrings[k + i * 3][l + j * 3]))
            listOfGrids.append(tempList)

    if checkNums(listOfGrids):
        global grids
        grids = True

def checkPuzzle(puzzleFile):
    replaceMap = {
        '\n': '',
        ' ': ''
    }
    translationTable = str.maketrans(replaceMap)

    sudokuRows = []

    with open(puzzleFile, 'r') as file:
        for line in file:
            if len(line.translate(translationTable)) != 9:
                print("Invalid amount of data in a row was found. Each row must have 9 numbers.")
                return
            for char in line.translate(translationTable):
                if not char.isdigit() or int(char) not in range(1, 10):
                    print(f"Invalid character in solution was found: '{char}'\nOnly numbers 1 - 9 are allowed.")
                    return
            sudokuRows.append(line.translate(translationTable))

    if len(sudokuRows) != 9:
        print("Invalid number of rows of data were found. There must be 9 rows.")
        return
    
    t1 = threading.Thread(checkRows(sudokuRows))
    t2 = threading.Thread(checkCols(sudokuRows))
    t3 = threading.Thread(checkGrids(sudokuRows))
    t1.start()
    t2.start()
    t3.start()

    if __name__ == "__main__":
        print("+-----------------------+")
        for i in range(3):
            for j in range(3):
                print("| ", end='')
                for k in range(3):
                    for l in range(3):
                        print(sudokuRows[j + i * 3][l + k * 3] + ' ', end='')
                    if l + k * 3 != 8:
                        print("| ", end='')
                print("|")
            if j + i * 3 != 8:
                print("+-------+-------+-------+")
        print("+-----------------------+")

    t1.join()
    t2.join()
    t3.join()

    if rows and cols and grids:
        print("This is a valid Sudoku solution!")
    else:
        print("This is an invalid Sudoku solution.")

def main():
    inputFile = input("Please input the name of the file with your Sudoku solution (leave out the \".txt\"): ")
    inputFile = inputFile + ".txt"

    existingFile = False
    while not existingFile:
        if not os.path.exists(inputFile):
            inputFile = input(f"The file '{inputFile}' does not exist. Please try again: ")
            inputFile = inputFile + ".txt"
        else:
            existingFile = True
    
    checkPuzzle(inputFile)

if __name__ == "__main__": main()