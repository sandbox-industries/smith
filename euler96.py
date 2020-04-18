#!/usr/bin/env python
# coding: utf-8

# ![Screen%20Shot%202020-04-16%20at%201.05.47%20PM.png](attachment:Screen%20Shot%202020-04-16%20at%201.05.47%20PM.png)

# In[1]:


def sudokuFileReader2():
    gridNameList=[]
    gridAllOneList=[]
    sudokuTextFile = open(r"/Users/aaronSmith/Documents/p096_sudoku.txt","r") 
    for i in range(500):
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


# In[2]:


def squareValues(gridArray):
    #break array in squares with s1 being the upper left, s2 the upper middle, .....
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


# In[3]:


def solver(gridArray, gridList):
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
#     print(gridArray)
    return(gridArray, gridList)       
        


# In[4]:


def setSquares(gridArray):
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


# In[5]:


def runner2():
    print("Starting data gathering")
    gridDict=sudokuFileReader2()
    print("\nData gathered into large dictionary of 50 sudoku puzzles")
    gridArray=np.array(gridDict["Grid 01"])
    print("\nFirst puzzle read in to set the location of the 9 larger squares")
    squareDict=setSquares(gridArray)
    print("\nLarger square location set")
    succesfulCounter=0
    for key in gridDict.keys():
        print("\n\n*****Processing",key,"of 50")
#         print("transforming into a list")
        gridList=gridDict[key]
#         print("now to an array")
        gridArray=np.array(gridList)
        numberOfLoops=0
        print("Entering while loop")
        while gridArray.sum()<405:
            lastSum=gridArray.sum()
#             print("current sum=",gridArray.sum())
            numberOfLoops+=1
            print("solver on loop",numberOfLoops,"of",key)
            gridArray, gridList=solver(gridArray, gridList)
            updatedSum=gridArray.sum()
            if updatedSum==lastSum:
                print("FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key)
                break 
            if updatedSum==405:
                succesfulCounter+=1
                print(key,"solved in",numberOfLoops,"loops!")
    print("sudoku puzzle solver finished",succesfulCounter,"of 50 puzzles")


# In[6]:


import numpy as np
runner2()

