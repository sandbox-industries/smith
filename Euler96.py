# -*- coding: utf-8 -*-
"""
Euler 96
"""
def sudokuFileReader2():
    #reads in file from local disk and creates a dictionary with each key:value pair being a puzzle
    gridNameList=[]
    gridAllOneList=[]
    sudokuTextFile = open(r"/Users/aaronSmith/Documents/p096_sudoku.txt","r") 
    for donuts in range(500):
        x=sudokuTextFile.readline()
        if len(x)==8:
            gridNameList.append(x.strip("\n"))
        else:
            y=[]
            for i in x.strip("\n"):
                y.append(int(i))
            gridAllOneList.append(y)
    sudokuTextFile.close()
    gridLists=[]
    for i in range(0,450,9):
        gridLists.append(gridAllOneList[i:i+9])
    gridDict=dict(zip(gridNameList,gridLists))
    return gridDict

def squareValues(gridArray):
    #returns the values included in the 9 cell squares with s1 being the upper left, s2 the upper middle, .....
    squares={}
    squares["s1"]=gridArray[:3,:3].flatten()
    squares["s2"]=gridArray[:3,3:6].flatten()
    squares["s3"]=gridArray[:3,6:].flatten()
    squares["s4"]=gridArray[3:6,:3].flatten()
    squares["s5"]=gridArray[3:6,3:6].flatten()
    squares["s6"]=gridArray[3:6,6:].flatten()
    squares["s7"]=gridArray[6:,:3].flatten()
    squares["s8"]=gridArray[6:,3:6].flatten()
    squares["s9"]=gridArray[6:,6:].flatten()
    return squares

def solver(gridArray, gridList):
    #fills in all zeros with all possible numbers for each cell
    squares=squareValues(gridArray)
    squareDict=setSquares(gridArray)
    allArray=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        for x in range(len(horRow)):
            if gridArray[y,x]==0:
                vertRow=np.hsplit(gridArray,9)[x]
                vertRow=vertRow.flatten()
                square=squares[squareDict[str(y)+str(x)]]
                allHor=np.setdiff1d(allArray, horRow)
                allHorVert=np.setdiff1d(allHor, vertRow)
                allHorVertSquare=np.setdiff1d(allHorVert, square)
                gridList[y][x]=allHorVertSquare 
    
    #sets places with only one possible to that value
    y=0
    x=-1
    for subList in gridList:
        for item in subList:
            x+=1
            if type(item)==np.ndarray:
                if len(item)==1:
                     gridList[y][x]=item[0]
                else:
                     gridList[y][x]=0    
        y+=1
        x=-1

    gridArray=np.array(gridList)
    print("sum=",gridArray.sum())
    print(gridArray)
    return(gridArray, gridList)       

def extraSolver(gridArray, gridList):
    #fills in all zeros with all possible numbers for each cell
    squares=squareValues(gridArray)
    squareDict=setSquares(gridArray)
    allArray=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        for x in range(len(horRow)):
            if gridArray[y,x]==0:
                vertRow=np.hsplit(gridArray,9)[x]
                vertRow=vertRow.flatten()
                square=squares[squareDict[str(y)+str(x)]]
                allHor=np.setdiff1d(allArray, horRow)
                allHorVert=np.setdiff1d(allHor, vertRow)
                allHorVertSquare=np.setdiff1d(allHorVert, square)
                gridList[y][x]=allHorVertSquare 

    #sets possibles created from above as an np.array and loops through them
    gridArray=np.array(gridList,dtype=object)
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        
        #checks horizontally for possibles that only occur once and sets them
        horArray=np.array([],dtype=int)
        for x in range(len(horRow)):
             if type(gridArray[y,x])==np.ndarray:
                    for item in horRow:
                        if type(item)==np.ndarray:
                            horArray=np.append(horArray,item)
                    vals,count=np.unique(horArray, return_counts=True)
                    vals=vals[count==1]
                    for valItem in vals:
                        horIndexCounter=0
                        for item in horRow:
                            if type(item)==np.ndarray:
                                if len(np.argwhere(item==valItem)) > 0:
                                    gridList[y][horIndexCounter]=valItem    
                            horIndexCounter+=1
     
        #checks vertically for possibles that only occur once and sets them   
        vertArray=np.array([],dtype=int)
        for x in range(len(horRow)):
             if type(gridArray[y,x])==np.ndarray:
                    vertRow=np.hsplit(gridArray,9)[x]
                    vertRow=vertRow.flatten()
                    for item in vertRow:
                        if type(item)==np.ndarray:
                            vertArray=np.append(vertArray,item)
                    vals,count=np.unique(vertArray, return_counts=True)
                    vals=vals[count==1]
                    for valItem in vals:
                        vertIndexCounter=0
                        for item in vertRow:
                            if type(item)==np.ndarray:
                                if len(np.argwhere(item==valItem)) > 0:
                                    gridList[vertIndexCounter][x]=valItem    
                            vertIndexCounter+=1

        #checks 9 cell squares for possibles that only occur once and sets them
        squares=squareValues(gridArray)
        for x in range(len(horRow)):
            squareArray=np.array([],dtype=int)
        if type(gridArray[y,x])==np.ndarray:
            square=squares[squareDict[str(y)+str(x)]]
            for item in square:
                if type(item)==np.ndarray:
                    squareArray=np.append(squareArray,item)
            vals,count=np.unique(squareArray, return_counts=True)
            vals=vals[count==1]
            for valItem in vals:
                if len(np.argwhere(gridArray[y,x]==valItem)) > 0:
                    gridList[y][x]=valItem 
    
    #sets places with only one possible to that value
    y=0
    x=-1
    for subList in gridList:
        for item in subList:
            x+=1
            if type(item)==np.ndarray:
                if len(item)==1:
                     gridList[y][x]=item[0]
                else:
                     gridList[y][x]=0    
        y+=1
        x=-1

    gridArray=np.array(gridList)
    print("sum=",gridArray.sum())
    print(gridArray)
    return(gridArray, gridList) 

def setSquares(gridArray):
    #maps cell y,x coordinates (not the cell values) to greater 9 square s1,s2,s3 and so on 
    squareDict={}
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        for x in range(len(horRow)):
            if y<3:
                if x<3:
                    squareDict[str(y)+str(x)]="s1"
                    continue
                if x>5:
                    squareDict[str(y)+str(x)]="s3"
                    continue
                else:
                    squareDict[str(y)+str(x)]="s2"
                    continue
            if y>5:
                if x<3:
                    squareDict[str(y)+str(x)]="s7"
                    continue
                if x>5:
                    squareDict[str(y)+str(x)]="s9"
                    continue
                else:
                    squareDict[str(y)+str(x)]="s8"
                    continue
            else:
                if x<3:
                    squareDict[str(y)+str(x)]="s4"
                    continue
                if x>5:
                    squareDict[str(y)+str(x)]="s6"
                    continue
                else:
                    squareDict[str(y)+str(x)]="s5"
                    continue
    return squareDict

def runner2():
    #runs all functions, 1st tries solver, then extraSolver
    gridDict=sudokuFileReader2()
#     print("\nData gathered into large dictionary of 50 sudoku puzzles")
    gridArray=np.array(gridDict["Grid 01"])
#     print("\nFirst puzzle read in to set the location of the 9 larger squares")
    squareDict=setSquares(gridArray)
#     print("\nLarger square location set")
    succesfulCounter=0
    for key in gridDict.keys():
        print("\n\n*****Processing",key,"of 50")
#         print("transforming into a list")
        gridList=gridDict[key]
#         print("now to an array")
        gridArray=np.array(gridList)
        numberOfLoops=0
        print("Entering while loop")
        #stays in the solver loop until no new values replace zeros
        while gridArray.sum()!=405:
            lastSum=gridArray.sum()
            numberOfLoops+=1
            print("solver on loop",numberOfLoops,"of",key)
            gridArray, gridList=solver(gridArray, gridList)
            updatedSum=gridArray.sum()
            if updatedSum==405:
                succesfulCounter+=1
                print(key,"solved in",numberOfLoops,"loops!")
                #add code here to capture first 3 values if ever finished
                break
            if updatedSum==lastSum:
                print("FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key,"Time to call in the extraSolver")
                #stays in the extraSolver loop until no new values replace zeros
                while gridArray.sum()!=405:
                    lastSum=gridArray.sum()
                    numberOfLoops+=1
                    print("extraSolver on loop",numberOfLoops,"of",key)
                    gridArray, gridList=extraSolver(gridArray, gridList)
                    updatedSum=gridArray.sum()
                    if updatedSum==lastSum:
                        print("EXTRA FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key)
                        break
                    if updatedSum==405:
                        succesfulCounter+=1
                        print(key,"solved in",numberOfLoops,"loops!")
                        #add code here to capture first 3 values if ever finished
                        break
                break
            continue            
    print("\n****Sudoku puzzle solver finished",succesfulCounter,"of 50 puzzles")
    
import numpy as np
runner2()