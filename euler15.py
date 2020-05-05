#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:06:05 2020

@author: aaronSmith
"""

#grid size +1, the values are representative of the intersecting grid corners
gridOutlineSize=21

#creates and prints an array of filled in with all 1's
a = [[1 for y in range(gridOutlineSize)] for x in range(gridOutlineSize)]

#prints the new array with 1's
print("\nOriginal Array: The grid is",len(a[0]),"x",len(a))
for line in a:
    print(line)




"""loops through the grid starting at the 2nd row, it replaces the 1's with 
the sum of all the x(column values) that are directly above and to the left 
in the row above, values show how many possible paths there are to that 
corner"""

def pathCounter(a):
    for i in range(1,len(a)): 
        x=0
        for j in a:
            a[i][x]=sum(a[i-1][0:x+1])
            x+=1 
    return a[-1][-1]
    

#runs code and adds timing
from timeit import default_timer
#records start time
start = default_timer() 

#runs the pathCounter and returns the final answer   
pathCounter(a)

#records end time
end = default_timer()

#adds whitespace
print("\nUpdated Array")
#prints updated array
for line in a:
    print(line)
    
print("\n\nThe final number of paths to get to the lower right corner is",
      a[-1][-1],", and it ran in",end-start,"seconds")