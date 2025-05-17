from utils import *

def parameters_generator(N, R_r, K_c):
    # calculate parameter
    G = N -R_r +1
    alpha, beta = [], []
    # 计算alpha和beta
    for i in range(1,G+1):
        alpha_i = N-R_r+K_c+1-i
        beta_i = N+1-i
        alpha.append(alpha_i)
        beta.append(beta_i)

    # 计算L
    L = lcm_list(alpha)

    # 计算gamma，取整
    gamma = [L//alpha[0]]
    for i in range(1,G):
        gamma.append(L//(alpha[i-1]*alpha[i]))

    # 计算lambda，取整  
    lambda_i = [0]
    for i in range(G):
        lambda_i.append(L//alpha[i])

    # print("G:",G)
    # print("alpha:",alpha)
    # print("beta:",beta)
    # print("gamma:",gamma)
    # print("lambda_i:",lambda_i)
    # print("L:",L)

    return  G, alpha, beta, gamma, lambda_i, L


