import numpy as np
import sys

def matrix_chain_order(p):
    n = len(p) - 1  
    m = np.zeros((n + 1, n + 1), dtype=int)  
    s = np.zeros((n + 1, n + 1), dtype=int)  

    
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1  
            m[i][j] = sys.maxsize  

            
            for k in range(i, j):
                
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q  
                    s[i][j] = k  
    return m, s

def print_optimal_parenthesization(s, i, j):
    if i == j:
        return f"A{i}"  
    else:
        
        left_part = print_optimal_parenthesization(s, i, s[i][j])
        right_part = print_optimal_parenthesization(s, s[i][j] + 1, j)
        return f"({left_part}{right_part})"


p = [100,10,100,1,1000,100]


m, s = matrix_chain_order(p)


print("p = [100,10,100,1,1000,100]")

print("\nコスト行列 m:")

print(m[1:, 1:])

print("\n分割点行列 s:")

print(s[1:, 1:])

total_multiplications = m[1][len(p) - 1]
print(f"\n総乗算回数: {total_multiplications}")

optimal_parenthesization = print_optimal_parenthesization(s, 1, len(p) - 1)
print(f"最適な結合: {optimal_parenthesization}")

