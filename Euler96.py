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

def solver(gridArray):    
    #fills in all zeros with all possible numbers for each cell
    squares=squareValues(gridArray)
    squareDict=setSquares(gridArray)
    allArray=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    gridList=gridArray.tolist()
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

    gridArray=np.array(gridList)
    #sets places with only one possible to that value
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        for x in range(len(horRow)):
            if type(gridArray[y,x])==np.ndarray:
                if len(gridArray[y,x])==1:
                    gridArray[y,x]=gridArray[y,x][0]
                else:
                    gridArray[y,x]=0
                    
    return gridList

def extraSolver(gridArray):
    #fills in all zeros with all possible numbers for each cell
    squares=squareValues(gridArray)
    squareDict=setSquares(gridArray)
    gridList=gridArray.tolist()
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
    
    gridList=solver(gridArray)

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
    
    gridArray=np.array(gridList)
    #sets places with only one possible to that value
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        for x in range(len(horRow)):
            if type(gridArray[y,x])==np.ndarray:
                if len(gridArray[y,x])==1:
                    gridArray[y,x]=gridArray[y,x][0]
                else:
                    gridArray[y,x]=0    

    print("sum=",gridArray.sum())
    print(gridArray)
    return(gridArray) 

def finalSolver(gridArray):
    squares=squareValues(gridArray)
    squareDict=setSquares(gridArray)
    gridList=gridArray.tolist()
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

    resetGridArray=np.copy(gridArray)
    print("sum of reset array=",resetGridArray.sum())
    print(resetGridArray)
    newGridArray=np.array(gridList)
    for y in range(len(newGridArray)):
        horRow=newGridArray[y]
        for x in range(len(horRow)):
            if type(newGridArray[y,x])==np.ndarray:
                if len(newGridArray[y,x])==2:

                    for index in range(len(newGridArray[y,x])):
                        print("adding in a",newGridArray[y,x][index],"at [y,x]","[",y,x,"]")
                        gridArray[y,x]=newGridArray[y,x][index]
                        print("sum=",gridArray.sum())
                        print(gridArray)
                        while checker(gridArray)==False:
                            lastSum=gridArray.sum()
                            
                            gridArray=extraSolver(gridArray)
                            updatedSum=gridArray.sum()
                            if updatedSum==405:
                                if checker(gridArray)==False:
                                    gridArray=resetGridArray
                                    break
                                else:
                                    return gridArray                                
                            if updatedSum==lastSum:
                                print("trying new value reseting gridArray")
                                gridArray=resetGridArray
                                gridArray[y,x]=0
                                print("sum=",gridArray.sum())
                                print(gridArray)
                                break
                            continue
    print("\n\n\n!!!!!!!!!!!!!!!!!!!******complete failure*****!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
    return gridArray

def finalSolver2(gridArray):
    squares=squareValues(gridArray)
    squareDict=setSquares(gridArray)
    gridList=gridArray.tolist()
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

    resetGridArray=np.copy(gridArray)
    print("sum of reset array=",resetGridArray.sum())
    print(resetGridArray)
    newGridArray=np.array(gridList)
    for y in range(len(newGridArray)):
        horRow=newGridArray[y]
        for x in range(len(horRow)):
            if type(newGridArray[y,x])==np.ndarray:
                if len(newGridArray[y,x])==3:

                    for index in range(len(newGridArray[y,x])):
                        print("adding in a",newGridArray[y,x][index],"at [y,x]","[",y,x,"]")
                        gridArray[y,x]=newGridArray[y,x][index]
                        print("sum=",gridArray.sum())
                        print(gridArray)
                        while checker(gridArray)==False:
                            lastSum=gridArray.sum()
                            
                            gridArray=extraSolver(gridArray)
                            updatedSum=gridArray.sum()
                            if updatedSum==405:
                                if checker(gridArray)==False:
                                    gridArray=resetGridArray
                                    break
                                else:
                                    return gridArray 
                            if updatedSum==lastSum:
                                print("trying new value reseting gridArray")
                                gridArray=resetGridArray
                                gridArray[y,x]=0
                                print("sum=",gridArray.sum())
                                print(gridArray)
                                break
                            continue
    print("\n\n\n!!!!!!!!!!!!!!!!!!!******complete failure*****!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
    return gridArray

def runner3():
    sumList=[]
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
            print("extrSolver on loop",numberOfLoops,"of",key)
            gridArray=extraSolver(gridArray)
            updatedSum=gridArray.sum()
            if updatedSum==405:
                succesfulCounter+=1
                print(key,"solved in",numberOfLoops,"loops!")
                a=""
                for number in gridArray[0,:3].tolist():
                    a=a+str(number)
                sumList.append(int(a))
                break
            if updatedSum==lastSum:
                print("FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key)
                #stays in the extraSolver loop until no new values replace zeros
                gridArray=finalSolver(gridArray)
                updatedSum=gridArray.sum()
                if updatedSum==405:
                    succesfulCounter+=1
                    print(key,"solved in",numberOfLoops,"loops!")
                    b=""
                    for number in gridArray[0,:3].tolist():
                        b=b+str(number)
                    sumList.append(int(b))
                    break                   
                if updatedSum==lastSum:
                    print("FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key)
                    #stays in the extraSolver loop until no new values replace zeros
                    gridArray=finalSolver2(gridArray)
                    updatedSum=gridArray.sum()
                    if updatedSum==405:
                        succesfulCounter+=1
                        print(key,"solved in",numberOfLoops,"loops!")
                        c=""
                        for number in gridArray[0,:3].tolist():
                            c=c+str(number)
                        sumList.append(int(c))
                        break                   
                    if updatedSum==lastSum:
                        print("EXTRA FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key)
                        break
                    break
                break
            continue
    print("\n****Sudoku puzzle solver finished",succesfulCounter,"of 50 puzzles")
    print("sumList has",len(sumList),"values and a sum of",sum(sumList))               
    
def checker(gridArray):
    if gridArray.sum()!=405:
        print("failed total sum")
        return False
    for y in range(len(gridArray)):
        horRow=gridArray[y]
        if horRow.sum()!=45:
            print("horRow failed check")
            return False
    for x in range(len(horRow)):
        vertRow=np.hsplit(gridArray,9)[x]
        vertRow=vertRow.flatten()
        if vertRow.sum()!=45:
            print("vertRow failed check")
            return False
    squares=squareValues(gridArray)
    for k in squares.keys():
        if squares[k].sum()!=45:
            print("square failed check")
            return False
    return True

import numpy as np
runner3()