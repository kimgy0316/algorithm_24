def union_set(A, B):
    a = set(A)
    b = set(B)
    c = a.union(b)
    return list(c)

A = [1, 2, 3, 4, 5]
B = [4, 5, 6, 7, 8]

union = union_set(A, B)
print("합집합:", union)