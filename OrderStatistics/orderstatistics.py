# -*- coding: utf-8 -*-
#Order statistics
#1. (Naive algorithm)Sort and then return the order statistics.

#2. Randomized divide and conquer algorithm
import random

def partitionRandimize(array, start, end):
    r = random.randint(start, end)
    array[r], array[start] = array[start], array[r]
    pivot = array[start]
    l = start
    for i in range(start+1, end+1):
        if array[i] <= pivot:
            l = l + 1
            array[i], array[l] = array[l], array[i]
    array[start], array[l] = array[l], array[start]
    return l

def RandomSelect(array, p, q, i):
    #ith smallest in array[p:q]
    if p == q:
        return array[p]
    r = partitionRandimize(array, p, q)
    k = r-p+1 #k = rank(array[r]) in array[p:q]
    if i == k:
        return array[r]
    elif i < k:
        return RandomSelect(array, p, r-1, i)
    else:
        return RandomSelect(array, r+1, q, i-k)

#3. Worst-case linear time order statistics [Blum, Floyd, Pratt, Rivest, Tarjan]
#Idea: genertate good pivot recursively
import math

def partition(array, start, end):

    pivot = array[start]
    l = start
    for i in range(start+1, end+1):
        if array[i] <= pivot:
            l = l + 1
            array[i], array[l] = array[l], array[i]
    array[start], array[l] = array[l], array[start]

    return l

def median(array, p, q):
    for i in range(p+1, q+1):
        temp = array[i]
        if array[i] < array[i-1]:
            j = i - 1
            while j >= p and temp <= array[j]:
                array[j+1] = array[j]
                j -= 1
            array[j+1] =temp

    return array[math.floor((p+q)/2)]

def findIndex(array, p, q, key):
    for i in range(p, q+1):
        if array[i] == key:
            return i
    return 0

def Select(array, p, q, i):

    if p == q:
        return array[p]
    n = q-p+1

    #1. Divide the n elements into math.floor(n/5) groups of 5 elements each
    #   Find  the median of each group
    groups = math.ceil(n/5)
    groupmedians = [0] * groups
    for j in range(0, groups-1):
        groupmedians[j] = median(array, p+5*j, p+5*j+4)
    groupmedians[groups-1] = median(array, p+5*(groups-1), q)
    #2. Recursively select the median x of the math.floor(n/5) group medians
    if groups == 1:
        pivot = groupmedians[0]
    else:
        pivot = Select(groupmedians, 0, groups-1, math.floor(groups/2))
    #3. Partition with x as pivot. Let k = rank(x)
    temp = findIndex(array, p, q, pivot)
    array[temp], array[p] = array[p], array[temp]
    r = partition(array, p, q)
    k = r-p+1 #k = rank(array[r]) in array[p:q]
    #4.
    if i == k:
        return array[r]
    elif i < k:
        return Select(array, p, r-1, i)
    else:
        return Select(array, r+1, q, i-k)

array = random.sample(range(1,100000),10000)
i=6
test = sorted(array)[i-1]
randomselect = RandomSelect(array, 0, len(array) - 1, i)
select = Select(array, 0, len(array) - 1, i)
print('Real:', test)
print('RandomSelect:', randomselect)
print('Select:', select)
