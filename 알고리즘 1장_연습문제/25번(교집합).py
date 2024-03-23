def intersection_set(A, B):
    a = set(A)
    b = set(B)
    c = a.intersection(b)
    return list(c)

A = [1, 2, 3, 4, 5]
B = [4, 5, 6, 7, 8]

intersection = intersection_set(A, B)
print("교집합:", intersection)