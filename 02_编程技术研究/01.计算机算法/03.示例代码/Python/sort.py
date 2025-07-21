# -*- coding: utf-8 -*-
'''
    Created on 2009-10-28

    @author: lingjie
    @name  :   sorting_algorithm
'''

import random

def selection_sort(arr):
    n = len(arr)
    for i in range(n-1, 0, -1):
        max_idx = i
        for j in range(i):
            if arr[j] > arr[max_idx]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr

def counting_sort(arr):
    if not arr:
        return []
    minv, maxv = min(arr), max(arr)
    count = [0] * (maxv - minv + 1)
    for num in arr:
        count[num - minv] += 1
    sorted_arr = []
    for idx, cnt in enumerate(count):
        sorted_arr.extend([idx + minv] * cnt)
    return sorted_arr

def radix_sort(arr):
    if not arr:
        return []
    max_num = max(arr)
    exp = 1
    output = arr[:]
    while max_num // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in output:
            buckets[(num // exp) % 10].append(num)
        output = [num for bucket in buckets for num in bucket]
        exp *= 10
    return output

def bucket_sort(arr):
    if not arr:
        return []
    minv, maxv = min(arr), max(arr)
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]
    for num in arr:
        idx = int((num - minv) / (maxv - minv + 1) * bucket_count)
        buckets[idx].append(num)
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(insertion_sort(bucket))
    return sorted_arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

def sort_check(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def main():
    coll = [random.uniform(0, 1) for _ in range(99)]
    if sort_check(coll):
        print("yes")
    else:
        print("not")
    coll = bucket_sort(coll)
    print(coll)
    if sort_check(coll):
        print("yes")
    else:
        print("not")

if __name__ == "__main__":
    main()

# import cProfile; cProfile.run('main()')
