
# 冒泡排序
def bubbleSort(coll):
    if(coll == []): return []
    endl = len(coll)
    for i in range(endl, 0, -1):
        for j in range(0, i - 1):
            if(coll[j] > coll[j + 1]):
                coll[j], coll[j + 1] = coll[j + 1], coll[j]

# 快速排序
def quickSort(coll):
    if(coll == []): return []
    return quickSort([x for x in coll[1:] if x < coll[0]]) + \
                        coll[0:1] + \
                        quickSort([x for x in coll[1:] if x >= coll[0]])

