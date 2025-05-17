from main import SCGen
import math
from fractions import Fraction
from RDCDS import RDCDS
import numpy as np

def IndepenceSet(K_c, R_r):
    K_c=sorted(K_c,reverse=True)
    M=0
    K_sum=0
    for i in range(len(K_c)):
        K_sum += 1/K_c[i]
        if K_sum > 1 - 1e-6:
            M=i+1
            break
    if M == 0:
        raise ValueError("K_c values cannot compose a system")
    elif M > R_r:
        raise ValueError("K_c values cannot satisfy the independence set condition")
    return M

def cut_side(gamma, size, I):
    sum_gamma = 0
    result = []

    for i in range(len(gamma)):
        if sum_gamma + gamma[i] < size:
            result.append(gamma[i])
            sum_gamma += gamma[i]
        else:
            result.append(size - sum_gamma)
            sum_gamma += size - sum_gamma
            I=size
            break
    if sum(gamma) < size + 1e-6:
        result = gamma.copy()
        I=0
    return result, I

def Generation(K_c, R_r, N):
    I=0
    M=IndepenceSet(K_c, R_r)
    gamma_sum = []
    I=1
    for i in range(len(K_c)):
        print("I: ",I)
        if I==0:
            break
        else:
            rdcds = RDCDS(K_c=M, R_r=R_r, N=N)
            rdcds.parameters_generator()
            gamma=I*np.array(rdcds.gamma)/rdcds.L
            if i==0:
                size = 1/K_c[i]
            else:
                size = 1/K_c[i] - 1/K_c[i-1]
            gamma, I = cut_side(gamma, size, I)
            M=M-1
            R_r=R_r-1
            N=N-1
            gamma_sum.append(gamma)
            # print("gamma_sum: ",list(gamma_sum))
    return gamma_sum




if __name__ == "__main__":
    N=7
    R_r=5
    K_c=[4,3,1,1,1,1,1]
    if len(K_c) != N:
        raise ValueError("K_c must be of length N")
    gamma_sum = Generation(K_c, R_r, N)
    print("gamma_sum: ", gamma_sum)
    # Flatten gamma_sum and convert to fractions
    flattened = []
    for sublist in gamma_sum:
        flattened.extend(sublist)
    
    # Convert to fractions to find common denominator
    fractions_list = [Fraction(str(x)).limit_denominator() for x in flattened]
    
    # Find LCM of all denominators
    denominators = [f.denominator for f in fractions_list]
    L = 1
    for d in denominators:
        L = L * d // math.gcd(L, d)
    
    # Multiply each element by L
    scaled = [[x*L for x in sublist] for sublist in gamma_sum]
    
    print("Minimal integer L:", L)
    print("L * gamma_sum:", scaled)


