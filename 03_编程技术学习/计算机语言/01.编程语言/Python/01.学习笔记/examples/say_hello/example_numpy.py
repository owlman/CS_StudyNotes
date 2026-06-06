import numpy as np;

# 基于列表对象生成一维数组
listObj = [1,2,3,4,5,6]
arr = np.array(listObj)
print("数组中的数据：\n", arr)
print("数组元素的类型：\n",arr.dtype)

# 基于列表对象生成二维数组
listObj = [[1,2],[3,4],[5,6]]
arr = np.array(listObj)
print("数组中的数据：\n", arr) 
print("数组的维度：\n", arr.ndim) 
print("数组中各维度的长度：\n", arr.shape)  # shape是一个元组

arr = np.zeros(6)
print("创建长度为 6，元素都是 0 的一维数组：\n", arr) 
arr = np.zeros((2,3)) 
print("创建 2x3，元素都是 0 的二维数组：\n", arr) 
arr = np.ones((2,3))
print("创建 2x3，元素都是 1 的二维数组：\n", arr) 
arr = np.empty((3,3))
print("创建 2x3，元素未经初始化的二维数组：\n", arr) 
