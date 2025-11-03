/*
 * sort.c
 *
 *  Created on: 2014-11-6
 *      Author: lingjie
 */
#include "algorithm.h"

int selectionSort(int *array, const int size)
{
    int i,j;
    if (array==NULL || size<=0)
    {
        return 1;
    }
    for (i = 0; i < size; ++i)
    {
        int minindex = i;
        for (j = i+1; j < size; ++j)
        {
            if (array[j] < array[minindex])
            {
                minindex = j;
            }
        }
        swap(&array[i], &array[minindex]);
    }
    return 0;
}

int countingSort(int *array, const int size)
{
    int i,j, max, min, index;
    if (array==NULL || size<=0)
        return 1;
    
	max = _max(array,size);
    min = _min(array,size);
    int *temp = (int *)calloc(max-min+1,
                              sizeof(int));
	if(temp == NULL)
		return 1;

    for (i = 0; i < size; ++i)
        temp[array[i] - min] += 1;
    
	index = 0;
    for (i = min; i < max+1; ++i)
        for (j = 0; j < temp[i-min]; ++j)
        {
            array[index] = i;
            index++;
        }

	free(temp);
    return 0;
}

int bubbleSort(int *array, const int size)
{
    int i,j;
    if (array==NULL || size<=0)
    {
        return 1;
    }
    for (i = size-1; i > 0; --i)
    {
        for (j = 0; j < i; ++j)
        {
            if (array[j] > array[j+1])
            {
                swap(&array[j], &array[j+1]);
            }
        }
    }
    return 0;
}

int shellSort(int *array, const int size)
{
    //...4
    return 0;
}

int quickSort(int *array, const int size)
{
    //...5
    return 0;
}

int mergeSort(int *array, const int size)
{
    //...6
    return 0;
}

int heapSort(int *array, const int size)
{
    //...7
    return 0;
}

int insertSort(int *array, const int size)
{
    int i;
    if (array==NULL || size<0)
    {
        return 1;
    }
    for(i = 0; i < size; ++i)
    {
        int temp = array[i];
        int j = i;
        while (j>0 && temp<array[j-1])
        {
            array[j] = array[j-1];
            --j;
        }
        array[j] = temp;
    }
    return 0;
}
