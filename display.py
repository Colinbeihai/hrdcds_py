# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 23:24:55 2025

@author: liitl
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*tRNS: invalid with alpha channel")

colors = ["yellow", "cyan", "green", "red", "purple", "orange"]  # 预定义颜色列表

def analyze_repetitions(matrix, gamma):
    """   
    返回:
    {
        "M1_repeats": {
            "elements": [元素1, 元素2,...],  
            "positions": [(行,列),...] 
        },
    }
    """
    # 1. 分割矩阵并记录偏移
    submatrices = []
    col_offsets = [0]
    for cols in gamma:
        submatrices.append(matrix[:, col_offsets[-1]:col_offsets[-1]+cols])
        col_offsets.append(col_offsets[-1] + cols)
    
    # 2. 重复元素分析
    repetitions = {}
    
    for i in range(1, len(submatrices)):
        current_key = f"M{i}_repeats"
        repetitions[current_key] = {"elements": set(), "positions": []}
        
        # 获取当前矩阵的非零元素及位置
        non_zero_i = np.where(submatrices[i] != '0')
        elements_i = set(submatrices[i][non_zero_i].flatten())
        
        for j in range(i):
            # 获取前面矩阵的非零元素
            non_zero_j = np.where(submatrices[j] != '0')
            elements_j = set(submatrices[j][non_zero_j].flatten())
            
            # 找出非零重复元素
            common_elements = elements_i & elements_j
            
            for elem in common_elements:
                repetitions[current_key]["elements"].add(elem)
                
                # 记录当前矩阵中的位置
                rows, cols = np.where(submatrices[i] == elem)
                for r, c in zip(rows, cols):
                    global_col = col_offsets[i] + c
                    repetitions[current_key]["positions"].append((int(r), int(global_col)))
                
                # 记录来源矩阵中的位置
                prev_rows, prev_cols = np.where(submatrices[j] == elem)
                for r, c in zip(prev_rows, prev_cols):
                    global_col = col_offsets[j] + c
                    repetitions[current_key]["positions"].append((int(r), int(global_col)))
        
        # 最终清理可能存在的空记录
        if not repetitions[current_key]["elements"]:
            del repetitions[current_key]

        # 打印结果
        # for key, data in repetitions.items():
        #     print(f"\n{key}:")
        #     print(f"重复元素: {sorted(data['elements'])}")
        #     print("位置坐标:")
        #     for pos in sorted(data["positions"]):
        #         print(f"  {pos}")

        color_regions = []
        for i, (key, data) in enumerate(repetitions.items()):
            if i >= len(colors):  # 如果重复模式多于颜色数量，循环使用颜色
                color = colors[i % len(colors)]
            else:
                color = colors[i]
            color_regions.append((color, data["positions"]))
    
    return repetitions, color_regions


def visualize_matrix(matrix, color_regions):
    """
    矩阵可视化函数，适配小单元格
    :param matrix: 2D list 或 NumPy 数组，元素为字符串
    :param color_regions: list of tuples (color, region)
    """
    plt.rcParams["text.usetex"] = True
    nrows, ncols = len(matrix), len(matrix[0])
    
    # 适配紧凑矩阵：小画布、正方形单元格
    fig, ax = plt.subplots()
    fig.set_size_inches(ncols * 0.5, nrows * 0.5)
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_aspect('equal')

    # 预计算所有单元格位置
    positions = [(j, nrows-1-i) for i in range(nrows) for j in range(ncols)]
    
    # 批量绘制边框
    rects = [patches.Rectangle((j, y), 1, 1, fill=False, 
                              edgecolor='black', linewidth=0.8) 
             for (j, y) in positions]
    for rect in rects:
        ax.add_patch(rect)

    # 使用字典加速颜色区域查找
    color_map = {}
    for color, region in color_regions:
        for (i, j) in region:
            color_map[(i, j)] = color

    # 批量绘制颜色区域
    colored_rects = []
    for (j, y) in positions:
        i = nrows-1 - int(y)
        if (i, j) in color_map:
            rect = patches.Rectangle((j, y), 1, 1,
                                   facecolor=color_map[(i, j)],
                                   edgecolor='black', linewidth=0.8)
            colored_rects.append(rect)
    for rect in colored_rects:
        ax.add_patch(rect)

    # 批量添加文本
    texts = []
    for i in range(nrows):
        for j in range(ncols):
            texts.append(ax.text(j + 0.95, nrows-1-i + 0.05,
                              r'${%s}$' % matrix[i][j],
                              ha='right', va='bottom', fontsize=12))

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('image.png')
    plt.show()

if __name__=='__main__':
    # example
    L,K_c,R_r,N = 12, 2, 4, 6

    # 构造示例向量并重塑
    W = [f"W_{{{k+1}}}" for k in range(12)]
    message_matrix = np.array(W).reshape(4, 3)
    Z = [f"Z_{{{k+1}}}" for k in range(6)]
    noise_matrix = np.array(Z).reshape(2, 3)
    matrix = np.concatenate((message_matrix, noise_matrix), axis=0)

    W = matrix[4,:]
    message_matrix = np.array(W).reshape(3, 1)
    Z = [f"Z_{{{k+1}}}" for k in range(6,8)]
    noise_matrix = np.array(Z).reshape(2, 1)
    zero = np.zeros(1, dtype=int)
    zero_matrix = np.array(zero).reshape(1,1)
    matrix2 = np.concatenate((message_matrix, noise_matrix, zero_matrix), axis=0)

    W = np.concatenate((matrix[5,:],matrix2[4]))
    message_matrix = np.array(W).reshape(2, 2)
    Z = [f"Z_{{{k+1}}}" for k in range(8,12)]
    noise_matrix = np.array(Z).reshape(2, 2)
    zero = np.zeros(4, dtype=int)
    zero_matrix = np.array(zero).reshape(2, 2)
    matrix3 = np.concatenate((message_matrix, noise_matrix, zero_matrix), axis=0)

    matrix = np.concatenate((matrix, matrix2, matrix3), axis=1)

    # 定义涂色区域：黄色标记
    color_regions = [
        ("yellow", [(4, 0), (4, 1),(4, 2), (0, 3),(1, 3), (2, 3)]),
        ("cyan",   [(5, 0),(5, 1), (5, 2),(4, 3), (0, 4),(0, 5), (1, 4),(1, 5)])
    ]

    visualize_matrix(matrix, color_regions)

