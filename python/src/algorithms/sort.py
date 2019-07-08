# -*- coding: utf-8 -*-
'''
    Created on 2009-10-28

    @author: lingjie
    @name  :   sorting_algorithm
'''

import sys
import random
import cProfile

def gnomesort(seq): 
    i = 0
    while i < len(seq):    
        if i == 0 or seq[i-1] <= seq[i]:
            i += 1
        else:
            seq[i], seq[i-1] = seq[i-1], seq[i]
            i -= 1 

def selectionSort(coll):
    if(coll == []): return []
    for i in range(len(coll)-1,0,-1):
        max_j = i
        for j in range(i):
            if coll[j] > coll[max_j]: max_j = j
        coll[i], coll[max_j] = coll[max_j], coll[i]

    return coll

def selectionSort_recursive(coll, i):
    if(i == 0): return []
    max_j = i

    for j in range(i):
        if coll[j] > coll[max_j]: max_j = j
    coll[i], coll[max_j] = coll[max_j], coll[i]
    selectionSort_recursive(coll, i-1)

    return coll

def countingSort(coll):
    if(coll == []): return []
    endl = len(coll)
    minv = min(coll)
    maxv = max(coll)
    temp = [0 for i in range(maxv - minv + 1)]

    for i in range(endl):
        temp[coll[i] - minv] += 1
    index = 0
    for i in range(minv, maxv + 1):
        for j in range(temp[i - minv]):
            coll[index] = i
            index += 1
    return coll

def radixSort(coll, length):
    if(coll == []): return []
    
    for d in xrange(length):
        LSD = [[] for _ in xrange(10)]
        for n in coll:
            LSD[n / (10 ** d) % 10].append(n)
        coll = [tmp_a for tmp_b in LSD for tmp_a in tmp_b]
    
    return coll

def bucketSort(coll):
    if(coll == []): return []
    
    length = len(coll)
    buckets = [[] for _ in xrange(length)] 
    for tmp_a in coll:
        buckets[int(length * tmp_a)].append(tmp_a)
    tmp_coll = []
    for tmp_b in buckets:
        tmp_coll.extend(insertSort(tmp_b))

    return tmp_coll


def insertSort(coll):
    if(coll == []): return []
    for i in range(1,len(coll)):
        j = i
        while j > 0 and coll[j-1] > coll[j]:
             coll[j-1], coll[j] = coll[j], coll[j-1]  
             j -= 1
              
    return coll 


def insertSort_recursive(coll,i):
    if(i == 0): return []
    insertSort_recursive(coll,i-1)                        
    j = i                                           
    while j > 0 and coll[j-1] > coll[j]:         
        coll[j-1], coll[j] = coll[j],coll[j-1]   
        j -= 1
     
    return coll                                      

def shellSort(coll):
    if(coll == []): return []
    size = len(coll)
    step = size / 2
    while(step >= 1):
        for i in range(step, size):
            tmp = coll[i]
            ins = i
            while(ins >= step and tmp < coll[ins - step]):
                coll[ins] = coll[ins - step]
                ins -= step
            coll[ins] = tmp
        step = step / 2
    
    return coll

def bubbleSort(coll):
    if(coll == []): return []
    endl = len(coll)
    for i in range(endl, 0, -1):
        for j in range(0, i - 1):
            if(coll[j] > coll[j + 1]):
                coll[j], coll[j + 1] = coll[j + 1], coll[j]

def quickSort(coll):
    if(coll == []): return []
    return quickSort([x for x in coll[1:] if x < coll[0]]) + \
                         coll[0:1] + \
                         quickSort([x for x in coll[1:] if x >= coll[0]])

def merge(coll, start, mid, endl):
    if(coll == []): return []
    temp = set()
    index1, endl1 = start, mid
    index2, endl2 = mid + 1 , endl
    while(index1 < endl1 and index2 < endl2):
        if(coll[index1] < coll[index2]):
            temp.add(coll[index1])
            index1 += 1
        else:
            temp.add(coll[index2])
            index2 += 1
    for data in coll[index1:endl1]:
        temp.add(data)
    for data in coll[index2:endl2]:
        temp.add(data)
    return temp

def mergeSort(coll, start, endl):
    if(coll == []): return []
    mid = 0
    if(start < endl):
        mid = (start + endl) / 2
        mergeSort(coll, start, mid)
        mergeSort(coll, mid + 1, endl)
        coll = merge(coll, start, mid, endl)
    return coll

def heap_adjust(data, s, m):
    if 2 * s > m:
        return
    temp = s - 1
    if data[2 * s - 1] > data[temp]:
        temp = 2 * s - 1
    if 2 * s <= m - 1 and data[2 * s] > data[temp]:
        temp = 2 * s
    if temp <> s - 1:
        data[s - 1], data[temp] = data[temp], data[s - 1]
        heap_adjust(data, temp + 1, m)

def heapSort(coll):
    if(coll == []): return []
    m = len(coll) / 2
    for i in range(m, 0, -1):
        heap_adjust(coll, i, len(coll))
    coll[0], coll[-1] = coll[-1], coll[0]
    for n in range(len(coll) - 1, 1, -1):
        heap_adjust(coll, 1, n)
        coll[0], coll[n - 1] = coll[n - 1], coll[0]
    return coll

def sortCheck(seq):
    n = len(seq)
    for i in range(n-1):
        if seq[i] > seq[i+1]:
            return False

    return True


def main():
    coll = [random.uniform(0, 1) for _ in xrange(99)]
    size = len(coll)
    if sortCheck(coll):
    	print "yes"
    else:
        print "not"
    coll = bucketSort(coll)
    print(coll)
    if sortCheck(coll):
        print "yes"
    else:
        print "not"

if(__name__ == "__main__"):
    main()
#cProfile.run('main()')
