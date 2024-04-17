def is_safe(g, v, pos, path): 
    if g[path[pos-1]][v] == 0: 
        return False
    for vertex in path: 
        if vertex == v: 
            return False
    return True

def hamiltonian_recur(g, path, pos): 
    n = len(g)
    if pos == n:
        if g[path[pos-1]][path[0]] == 1: 
            return True
        else: 
            return False
    for v in range(1, n): 
        if is_safe(g, v, pos, path) == True: 
            path[pos] = v 
            if hamiltonian_recur(g, path, pos+1) == True: 
                return True
            path[pos] = -1
    return False

def hamiltonian_cycle(g): 
    n = len(g)
    path = [-1] * (n+1) 
    path[0] = path[n] = 0 # 0번부터 출발하자.
 
    if hamiltonian_recur(g, path, 1) == False: 
        print("해밀토니언 사이클 없음") 
        return False
    else:
        print("해밀토니안 사이클:", path) 
        return True

# 간단한 그래프 테스트
g_simple = [[0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0]]

print("간단한 그래프 테스트:")
hamiltonian_cycle(g_simple)