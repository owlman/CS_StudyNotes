'''
    Created on 2013-10-28
    
    @author: lingjie
    @name:   searching_algorithm
'''
import sys
import cProfile
import collections
from sort import *

_=float('inf')

def BinarySearch(coll, target):
    low = 0
    high = len(coll) - 1
    
    while low <= high:
        mid = (low + high) // 2
        midVal = coll[mid]
        
        if midVal < target:
            low = mid + 1
        elif midVal > target:
            high = mid - 1
        else:
            return mid

    return -1

def dijkstra(graph, n):
    dist    = [0] * n
    prev    = [0] * n
    flag    = [False] * n
    flag[0] = True

    k = 0
    for i in range(n):
        dist[i] = graph[k][i]

    for j in range(n-1):
        min_i = _
        for i in range(n):
            if(dist[i] < min_i and not flag[i]):
				min_i = dist[i]
				k = i

        if(k == 0):
			return

        flag[k] = True
        for i in range(n):
            if(dist[i] > dist[k]+graph[k][i]):
				dist[i] = dist[k]+graph[k][i]
				prev[i] = k

    return dist, prev

def prim(graph, n):
    dist    = [0] * n
    prev    = [0] * n
    flag    = [False] * n
    flag[0] = True

    k = 0
    for i in range(n):
        dist[i] = graph[k][i]
    
    for j in range(n-1):
        min_i = _
        for i in range(n):
            if(min_i > dist[i] and not flag[i]):
                min_i = dist[i]
                k = i

        if(k == 0):
            return

        flag[k]=True
        for i in range(n):
            if(dist[i] > graph[k][i] and not flag[i]):
                dist[i] = graph[k][i]
                prev[i] = k

    return dist, prev
    
def recDFS(G, s, S=None): 
    if S is None: S = set()         # Initialize the history
    S.add(s)                        # We've visited s
    for u in G[s]:                  # Explore neighbors
        if u in S: continue         # Already visited: Skip
        recDFS(G, u, S)             # New: Explore recursively 

def iterDFS(G, s): 
    S, Q = set(), []                # Visited-set and queue
    Q.append(s)                     # We plan on visiting s
    while Q:                        # Planned nodes left?
        u = Q.pop()                 # Get one 
        if u in S: continue         # Already visited? Skip it
        S.add(u)                    # We've visited it now
        Q.extend(G[u])              # Schedule all neighbors
        yield u                     # Report u as visited 


def maxPermutatian(coll):
    size = len(coll)
    rem = set(range(size))
    count = [0] * size
    count = collections.Counter(coll)
    
    quit = [i for i in rem if count[i] == 0]
    while quit:
        i = quit.pop()
        rem.remove(i)
        j = coll[i]
        count[j] -= 1
        if count[j] == 0:
            quit.append(j)

    return rem

def testMaxPermutatian():
    M = [2, 2, 0, 5, 3, 5, 7, 4]
    print maxPermutatian(M)

def testSearch():
    coll = sort.quickSort([5, 4, 6, 7, 2, 8, 9, 0])
    
    if(BinarySearch(coll, 5) == -1):
        print "No"
    else:
        print "Yes"

def testGraphSearch():
    n = 6
    graph = [
              [0,6,3,_,_,_],
              [6,0,2,5,_,_],
              [3,2,0,3,4,_],
              [_,5,3,0,2,3],
              [_,_,4,2,0,5],
              [_,_,_,3,5,0],
            ]
    
    #dis,pre=dijkstra(graph,n)
    dis,pre=prim(graph,n)
    

    print(dis)
    print(pre)

def testDFS():
    graph = [1,2,4,8,9,0,5]
    node  = 9
    #ret = list(iterDFS(graph,node))
    #print(ret)
    

if(__name__ == "__main__"):
    testDFS()
#    testSearch()
#    testMaxPermutatian()
    cProfile.run("testDFS")
