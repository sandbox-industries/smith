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
    print("sum=",gridArray.sum())
    print(gridArray)
    return(gridArray, gridList)       
        


# In[10]:


from pprint import pprint
import numpy as np
gridDict=sudokuFileReader2()
gridList=gridDict["Grid 06"]
gridArray=np.array(gridList)
squareDict=setSquares(gridArray)
pprint(gridList)
print("\n\n")
pprint(gridArray)


# In[93]:


gridArray, gridList=solver(gridArray, gridList)


# In[84]:


gridArray, gridList=extraSolver(gridArray, gridList)


# In[ ]:


vertArray=np.array([],dtype=int)
a=np.array([1, 4, 5, 7, 9])
b=np.array([5, 7, 9])
c=np.array([4, 9])
d=np.array([1, 4, 9])
e=np.array([1, 5, 7])
f=np.array([1, 5, 6, 7])


# In[ ]:


testList=[a,b,c,d,e,f]


# In[ ]:


vals


# In[ ]:


x=np.argwhere(f==vals)
len(x)


# In[ ]:


for item in testList:
    vertArray=np.append(vertArray,item)
vals,count=np.unique(vertArray, return_counts=True)
vals=vals[count==1]
for item in testList:
    x=np.argwhere(item==vals)
    if len(x) > 0:
        print(item, "to set to",vals)


# In[ ]:


vertArray


# In[ ]:


vals,count=np.unique(vertArray, return_counts=True)
vals=vals[count==1]
print(vals)


# In[ ]:


arr = np.array([1, 2, 3, 4, 5, 4, 4])

x = np.where(arr == 8)

print(len(x[0]))
print(type(x))


# In[75]:


def extraSolver(gridArray, gridList):
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

#     print(gridList)
    
    
    gridArray=np.array(gridList,dtype=object)
#     print("\nThe Array has", len(gridArray),"rows")
    for y in range(len(gridArray)):
#         print("\nrow #",y,"\n")
        horRow=gridArray[y]
#         print(horRow)
        horArray=np.array([],dtype=int)
        for x in range(len(horRow)):
             if type(gridArray[y,x])==np.ndarray:
#                     print("np arrays only",gridArray[y,x])
                    for item in horRow:
#                         print(type(item))
                        if type(item)==np.ndarray:
                            horArray=np.append(horArray,item)
                    vals,count=np.unique(horArray, return_counts=True)
                    vals=vals[count==1]
                    for valItem in vals:
                        horIndexCounter=0
                        for item in horRow:
#                             print(type(item))
                            if type(item)==np.ndarray:
                                if len(np.argwhere(item==valItem)) > 0:
#                                     print(horIndexCounter)
                                    gridList[y][horIndexCounter]=valItem    
#                                     print(item, "to set to",type(valItem))
                            horIndexCounter+=1
        
        
        
        
        
        
        
        
        vertArray=np.array([],dtype=int)
        for x in range(len(horRow)):
             if type(gridArray[y,x])==np.ndarray:
#                     print("np arrays only",gridArray[y,x])
                    vertRow=np.hsplit(gridArray,9)[x]
                    vertRow=vertRow.flatten()
#                     print("vertRow here", vertRow)
                    for item in vertRow:
#                         print(type(item))
                        if type(item)==np.ndarray:
                            vertArray=np.append(vertArray,item)
#                     print("This is the vertArray",vertArray)
                    vals,count=np.unique(vertArray, return_counts=True)
                    vals=vals[count==1]
                    for valItem in vals:
                        vertIndexCounter=0
                        for item in vertRow:
#                             print(type(item))
                            if type(item)==np.ndarray:
                                if len(np.argwhere(item==valItem)) > 0:
#                                     print(vertIndexCounter)
                                    gridList[vertIndexCounter][x]=valItem    
#                                     print(item, "to set to",type(valItem))
                            vertIndexCounter+=1

                            
                            
                            
                            
#                         break
#                     break

                    
#         break

#                 square=squares[squareDict[str(y)+str(x)]]
#                 allHor=np.setdiff1d(allArray, horRow)
#                 allHorVert=np.setdiff1d(allHor, vertRow)
#                 allHorVertSquare=np.setdiff1d(allHorVert, square)
#                 gridList[y][x]=allHorVertSquare
#     print("\n",gridList)
    
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


# In[5]:


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


# In[8]:


def runner2():
#     print("Starting data gathering")
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
        while gridArray.sum()!=405:
            lastSum=gridArray.sum()
#             print("current sum=",gridArray.sum())
            numberOfLoops+=1
            print("solver on loop",numberOfLoops,"of",key)
            gridArray, gridList=solver(gridArray, gridList)
            updatedSum=gridArray.sum()
            if updatedSum==405:
                succesfulCounter+=1
                print(key,"solved in",numberOfLoops,"loops!")
                break
            if updatedSum==lastSum:
                print("FUCK FUCK FUCK Failed after loop",numberOfLoops,", on",key,"Time to call in the extraSolver")
                while gridArray.sum()!=405:
                    lastSum=gridArray.sum()
        #             print("current sum=",gridArray.sum())
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
                        break
                break
            continue
            
    print("sudoku puzzle solver finished",succesfulCounter,"of 50 puzzles")


# In[9]:


import numpy as np
runner2()

