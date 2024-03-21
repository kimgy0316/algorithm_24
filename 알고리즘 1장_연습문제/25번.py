A = [1, 2, 3, 4]
B = [3, 4, 5, 6]

def union(A, B):
    return set(A) | set(B)

print("A와 B의 교집합:", union(A, B))