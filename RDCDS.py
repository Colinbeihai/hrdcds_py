import numpy as np
from utils import *
from parameters import parameters_generator
from display import visualize_matrix, analyze_repetitions

class RDCDS:
    def __init__(self, K_c, R_r, N):
        self.N = N
        self.R_r = R_r
        self.K_c = K_c

    def parameters_generator(self):
        self.G, self.alpha, self.beta, self.gamma, self.lambda_i, self.L = parameters_generator(self.N, self.R_r, self.K_c)

    def Generation_W_Z(self):
        W = [f"W_{{{k+1}}}" for k in range(self.L)]
        Z = []
        Z_list = [f"Z_{{{k+1}}}" for k in range((self.R_r-self.K_c)*self.lambda_i[-1])]
        start = 0
        for i in range(self.G):
            end = start + (self.R_r-self.K_c)*self.gamma[i]
            Z_slice = Z_list[start:end]
            Z.append(np.array(Z_slice).reshape(self.R_r-self.K_c, self.gamma[i]))
            start = end
        return W, Z

    def SCGen(self, W, Z):
        M = []
        W_next = None
        for i in range(self.G):
            if i == 0:
                # First matrix uses original W
                message_matrix = np.array(W).reshape(self.alpha[i], self.gamma[i])
                noise_matrix = Z[i]
                M.append(np.concatenate((message_matrix, noise_matrix), axis=0))
            else:
                # Subsequent matrices use rows from previous matrices
                rows_to_concat = []
                for j in range(i):
                    rows_to_concat.append(M[j][self.R_r-j+i-1,:])
                W_next = np.concatenate(rows_to_concat)
                message_matrix = np.array(W_next).reshape(self.alpha[i], self.gamma[i])
                noise_matrix = Z[i]
                zero = np.zeros((self.N-self.beta[i])*self.gamma[i], dtype=int)
                zero_matrix = np.array(zero).reshape(self.N-self.beta[i], self.gamma[i])
            
                # Build current matrix
                M.append(np.concatenate((message_matrix, noise_matrix, zero_matrix), axis=0))
        
        # Concatenate all matrices horizontally
        matrix = np.concatenate(M, axis=1)
        return matrix


if __name__=='__main__':
    # choose system parameters
    N, R_r, K_c = 9, 5, 2
    rdcds = RDCDS(K_c, R_r, N)
    rdcds.parameters_generator()
    print(np.array(rdcds.gamma)/rdcds.L)
    W, Z = rdcds.Generation_W_Z()
    matrix = rdcds.SCGen(W, Z)
    # print(matrix)

    # 台阶矩阵可视化
    # _, color_regions = analyze_repetitions(matrix, rdcds.gamma)    
    # visualize_matrix(matrix, color_regions)
