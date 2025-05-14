import numpy as np
from utils import *
from parameters import parameters_generator
from display import visualize_matrix, analyze_repetitions

def SCGen(W, Z):
    """
    SCGen(W, Z)，生成台阶矩阵
    W: 消息
    Z: 噪声
    """
    M = []
    W_next = None
    for i in range(G):
        if i == 0:
            # First matrix uses original W
            message_matrix = np.array(W).reshape(alpha[i], gamma[i])
            noise_matrix = Z[i]
            M.append(np.concatenate((message_matrix, noise_matrix), axis=0))
        else:
            # Subsequent matrices use rows from previous matrices
            rows_to_concat = []
            for j in range(i):
                rows_to_concat.append(M[j][R_r-j+i-1,:])
            W_next = np.concatenate(rows_to_concat)
            message_matrix = np.array(W_next).reshape(alpha[i], gamma[i])
            noise_matrix = Z[i]
            zero = np.zeros((N-beta[i])*gamma[i], dtype=int)
            zero_matrix = np.array(zero).reshape(N-beta[i], gamma[i])
        
            # Build current matrix
            M.append(np.concatenate((message_matrix, noise_matrix, zero_matrix), axis=0))
    
    # Concatenate all matrices horizontally
    matrix = np.concatenate(M, axis=1)
    return matrix


if __name__=='__main__':
    # choose system parameters
    N, R_r, K_c = 9, 5, 2

    G, alpha, beta, gamma, lambda_i, L = parameters_generator(N, R_r, K_c)
    # 生成W，Z
    W = [f"W_{{{k+1}}}" for k in range(L)]
    Z = []
    Z_list = [f"Z_{{{k+1}}}" for k in range((R_r-K_c)*lambda_i[-1])]
    start = 0
    for i in range(G):
        end = start + (R_r-K_c)*gamma[i]
        Z_slice = Z_list[start:end]
        Z.append(np.array(Z_slice).reshape(R_r-K_c, gamma[i]))
        start = end

    matrix = SCGen(W, Z)
    print(matrix)

    # 台阶矩阵可视化
    _, color_regions = analyze_repetitions(matrix, gamma)    
    visualize_matrix(matrix, color_regions)
