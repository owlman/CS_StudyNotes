#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    NumPy数组操作示例
    
    Updated on 2025-11-26
'''

import numpy as np

def demonstrate_basic_arrays():
    """演示基本数组操作"""
    print("=== NumPy基本数组操作 ===\n")
    
    # 基于列表对象生成一维数组
    list_obj = [1, 2, 3, 4, 5, 6]
    arr_1d = np.array(list_obj)
    print("一维数组:")
    print(f"数组数据: {arr_1d}")
    print(f"数组元素类型: {arr_1d.dtype}")
    print(f"数组维度: {arr_1d.ndim}")
    print(f"数组形状: {arr_1d.shape}")
    print(f"数组大小: {arr_1d.size}\n")

    # 基于列表对象生成二维数组
    list_obj_2d = [[1, 2], [3, 4], [5, 6]]
    arr_2d = np.array(list_obj_2d)
    print("二维数组:")
    print(f"数组数据:\n{arr_2d}") 
    print(f"数组维度: {arr_2d.ndim}") 
    print(f"数组形状: {arr_2d.shape}")  # shape是一个元组
    print(f"数组大小: {arr_2d.size}\n")

def demonstrate_special_arrays():
    """演示特殊数组创建"""
    print("=== 特殊数组创建 ===\n")
    
    # zeros数组
    zeros_1d = np.zeros(6)
    print("长度为6，元素都是0的一维数组:")
    print(zeros_1d)
    
    zeros_2d = np.zeros((2, 3)) 
    print("\n2x3，元素都是0的二维数组:")
    print(zeros_2d)
    
    # ones数组
    ones_2d = np.ones((2, 3))
    print("\n2x3，元素都是1的二维数组:")
    print(ones_2d)
    
    # empty数组
    empty_2d = np.empty((3, 3))
    print("\n3x3，元素未经初始化的二维数组:")
    print(empty_2d)
    
    # full数组
    full_2d = np.full((2, 3), 7)
    print("\n2x3，元素都是7的二维数组:")
    print(full_2d)
    
    # eye数组（单位矩阵）
    eye_3 = np.eye(3)
    print("\n3x3单位矩阵:")
    print(eye_3)
    
    # arange数组
    arange_arr = np.arange(0, 10, 2)
    print("\n0到9，步长为2的数组:")
    print(arange_arr)
    
    # linspace数组
    linspace_arr = np.linspace(0, 10, 5)
    print("\n0到10之间5个等间距的数组:")
    print(linspace_arr)

def demonstrate_array_operations():
    """演示数组操作"""
    print("\n=== 数组操作 ===\n")
    
    # 创建示例数组
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([[7, 8, 9], [10, 11, 12]])
    
    print("数组A:")
    print(a)
    print("\n数组B:")
    print(b)
    
    # 数组加法
    print("\n数组加法 (A + B):")
    print(a + b)
    
    # 数组乘法（元素级）
    print("\n元素级乘法 (A * B):")
    print(a * b)
    
    # 矩阵乘法
    print("\n矩阵乘法 (A @ B.T):")
    print(a @ b.T)
    
    # 数组统计
    print(f"\n数组A的和: {a.sum()}")
    print(f"数组A的平均值: {a.mean()}")
    print(f"数组A的最大值: {a.max()}")
    print(f"数组A的最小值: {a.min()}")
    print(f"数组A的标准差: {a.std()}")
    
    # 数组索引和切片
    print(f"\n数组A的第0行: {a[0]}")
    print(f"数组A的第1列: {a[:, 1]}")
    print(f"数组A的[0,1]位置元素: {a[0, 1]}")

def demonstrate_array_manipulation():
    """演示数组变形和操作"""
    print("\n=== 数组变形和操作 ===\n")
    
    # 创建一维数组
    arr = np.arange(12)
    print(f"原始一维数组: {arr}")
    
    # reshape变形
    arr_reshaped = arr.reshape(3, 4)
    print(f"\n变形为3x4数组:\n{arr_reshaped}")
    
    # transpose转置
    arr_transposed = arr_reshaped.T
    print(f"\n转置后的数组:\n{arr_transposed}")
    
    # flatten展平
    arr_flattened = arr_reshaped.flatten()
    print(f"\n展平后的数组: {arr_flattened}")
    
    # concatenate连接
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[5, 6], [7, 8]])
    arr_concat = np.concatenate((arr1, arr2), axis=0)
    print(f"\n垂直连接数组:\n{arr_concat}")
    
    arr_concat_h = np.concatenate((arr1, arr2), axis=1)
    print(f"\n水平连接数组:\n{arr_concat_h}")
    
    # split分割
    arr_split = np.split(arr_concat, 2, axis=0)
    print(f"\n分割后的数组: {[sub_arr.tolist() for sub_arr in arr_split]}")

def demonstrate_data_types():
    """演示数据类型"""
    print("\n=== 数据类型 ===\n")
    
    # 不同数据类型的数组
    int_arr = np.array([1, 2, 3], dtype=np.int32)
    float_arr = np.array([1.1, 2.2, 3.3], dtype=np.float64)
    bool_arr = np.array([True, False, True], dtype=np.bool_)
    string_arr = np.array(['hello', 'world'], dtype=np.str_)
    
    print(f"整数数组: {int_arr}, 类型: {int_arr.dtype}")
    print(f"浮点数组: {float_arr}, 类型: {float_arr.dtype}")
    print(f"布尔数组: {bool_arr}, 类型: {bool_arr.dtype}")
    print(f"字符串数组: {string_arr}, 类型: {string_arr.dtype}")
    
    # 类型转换
    converted_arr = int_arr.astype(np.float64)
    print(f"\n类型转换后: {converted_arr}, 新类型: {converted_arr.dtype}")

def demonstrate_boolean_indexing():
    """演示布尔索引"""
    print("\n=== 布尔索引 ===\n")
    
    # 创建示例数组
    arr = np.array([[1, 5, 3], [8, 2, 7], [4, 6, 9]])
    print("原始数组:")
    print(arr)
    
    # 布尔条件
    mask = arr > 5
    print(f"\n大于5的布尔掩码:\n{mask}")
    
    # 使用布尔索引
    filtered_arr = arr[arr > 5]
    print(f"\n大于5的元素: {filtered_arr}")
    
    # 多条件
    multi_mask = (arr > 3) & (arr < 8)
    multi_filtered = arr[multi_mask]
    print(f"\n大于3且小于8的元素: {multi_filtered}")

def main():
    """主函数"""
    try:
        demonstrate_basic_arrays()
        demonstrate_special_arrays()
        demonstrate_array_operations()
        demonstrate_array_manipulation()
        demonstrate_data_types()
        demonstrate_boolean_indexing()
        
        print("\n=== NumPy版本信息 ===")
        print(f"NumPy版本: {np.__version__}")
        
    except ImportError:
        print("请先安装NumPy: pip install numpy")
    except Exception as e:
        print(f"执行过程中出现错误: {e}")

if __name__ == "__main__":
    main()
 
