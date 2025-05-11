# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 23:24:55 2025

@author: liitl
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image

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
    fig.set_size_inches(ncols * 0.5, nrows * 0.5)  # 控制整体图像大小
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_aspect('equal')  # 保持单元格为正方形

    # 绘制边框
    for i in range(nrows):
        for j in range(ncols):
            rect = patches.Rectangle((j, nrows-1-i), 1, 1,
                                     fill=False, edgecolor='black', linewidth=0.8)
            ax.add_patch(rect)

    # 涂色
    for color, region in color_regions:
        for (i, j) in region:
            rect = patches.Rectangle((j, nrows-1-i), 1, 1,
                                     facecolor=color, edgecolor='black', linewidth=0.8)
            ax.add_patch(rect)

    # 添加 LaTeX 文本
    for i in range(nrows):
        for j in range(ncols):
            ax.text(j + 0.95, nrows-1-i + 0.05,
                    r'${%s}$' % matrix[i][j],
                    ha='right', va='bottom', fontsize=12)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('image.png')
    plt.show()

if __name__=='__main__':
    L,K_c,R_r,N = 72, 4, 5, 6

    # 构造示例向量并重塑为 6×12 矩阵
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
    matrix = np.concatenate((matrix, matrix2), axis=1)

    # 定义涂色区域：黄色标记第1行第1、2格，红色标记第6行第12格
    color_regions = [
        ("yellow", [(5, 0), (5, 1),(5, 2), (5, 3),(5, 4), (5, 5)]),
        ("yellow",    [(0, 6),(0, 7), (2, 6),(2, 7), (1, 6),(1, 7)])
    ]

    visualize_matrix(matrix, color_regions)

