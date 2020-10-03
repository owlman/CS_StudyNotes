/*
 * tools.c
 *
 *  Created on: 2014-11-6
 *      Author: lingjie
 */
#include "algorithm.h"

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

int _max(int *array, const int size)
{
    int i = 0;
    int _max = array[i];
    while (i < size)
    {
        if (_max < array[i])
        {
            _max = array[i];
        }
        ++i;
    }
    return _max;
}

int _min(int *array, const int size)
{
    int i = 0;
    int _min = array[i];
    while (i < size)
    {
        if (_min > array[i])
        {
            _min = array[i];
        }
        ++i;
    }
    return _min;
}




