#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:52:33 2020

@author: aaronSmith
"""


from pprint import pprint
import copy

def fileReader():
    tempList=[]   
    with open(r"/Users/aaronSmith/Documents/p067_triangle.txt","r") as f:
        lines = list(map(lambda l: l.strip(), f.readlines()))
        for i in range(len(lines)):
            for j in lines[i].split(","):

                tempList.append(j.split(" "))
                
    triangleList=[]
    for l in tempList:
        l=list(map(int,l))
        triangleList.append(l)
    
    return triangleList

def plinko(choices):
    try:
        listOfLists=[]
        while True:
            tempList=[]
            shrinkingChoices=copy.deepcopy(choices)

            if len(choices[3])>=len(choices[4]):
                tempList.append(shrinkingChoices[4].pop())
                tempList.append(choices[3].pop())
                shrinkingChoices=copy.deepcopy(choices)
                for i in range(2,-1,-1):
                    tempList.append(shrinkingChoices[i].pop())
                listOfLists.append(tempList)
                tempList=[]
                continue

            if len(choices[2])>=len(choices[3]):
                tempList.append(shrinkingChoices[4].pop())
                tempList.append(shrinkingChoices[3].pop())
                tempList.append(choices[2].pop())
                shrinkingChoices=copy.deepcopy(choices)
                for i in range(1,-1,-1):
                    tempList.append(shrinkingChoices[i].pop(-1))
                listOfLists.append(tempList)
                tempList=[]
                continue

            if len(choices[1])>=len(choices[2]):
                tempList.append(shrinkingChoices[4].pop())
                tempList.append(shrinkingChoices[3].pop())
                tempList.append(shrinkingChoices[2].pop())
                tempList.append(choices[1].pop())
                shrinkingChoices=copy.deepcopy(choices)
                tempList.append(shrinkingChoices[0].pop())
                listOfLists.append(tempList)
                tempList=[]
                continue

            if len(choices[0])>=len(choices[1]):
                tempList.append(shrinkingChoices[4].pop())
                tempList.append(shrinkingChoices[3].pop())
                tempList.append(shrinkingChoices[2].pop())
                tempList.append(shrinkingChoices[1].pop())
                tempList.append(choices[0].pop())
                shrinkingChoices=copy.deepcopy(choices)
                listOfLists.append(tempList)
                tempList=[]
                continue
                
            else:
                i=4
                tempList.append(choices[i].pop())
                shrinkingChoices=copy.deepcopy(choices)
                for i in range(3,-1,-1):
                    tempList.append(shrinkingChoices[i].pop())
                listOfLists.append(tempList)
                tempList=[]
 
    except IndexError:
#         listOfLists.pop()
        return listOfLists
    
triangleList=fileReader()
iY=0
finalPathSum=triangleList[0][0]
print("Current Path Sum=",finalPathSum,"after row",iY,"\n\n\n")


for i in range(len(triangleList)-5):
    testList=copy.deepcopy(triangleList[iY+1:iY+6])
    choices=copy.deepcopy(testList)

    allLists=[]
    listOfLists=plinko(choices)
    allLists.extend(listOfLists)

    reverseChoices=copy.deepcopy(testList)
    for i in range(len(reverseChoices)):
        reverseChoices[i].reverse()

    listOfLists=plinko(reverseChoices)
    allLists.extend(listOfLists)

    sumList=[]
    for l in allLists:
        sumList.append(sum(l)) 
    pickedNumber=allLists[sumList.index(max(sumList))][-1]
    finalPathSum+=pickedNumber
    print("\nOriginal Cone of choices")
    pprint(testList)
    print("\nThe best backwards path is", allLists[sumList.index(max(sumList))], "with a sum of", max(sumList),
          "\n",pickedNumber,"is the picked number in the next row\n")
    iY+=1
    if testList[0].index(pickedNumber)==0:
        for l in range(iY,len(triangleList)):
            triangleList[l].pop()
    else:
        for l in range(iY,len(triangleList)):
            triangleList[l].pop(0)
    print("Current Path Sum=",finalPathSum,"after row",iY,"\n\n\n")
finalPathSum+=max(sumList)
print("\nAdding in", max(sumList), "for the final 5 rows, and the grand total of", finalPathSum)

# finalAnswer supposed to be 7273
    
