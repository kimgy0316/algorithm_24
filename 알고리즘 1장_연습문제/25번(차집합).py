def difference_set(A, B):

    a = set(A)
    b = set(B)
    c = a.difference(b)
    return list(c)

A = [1, 2, 3, 4, 5]
B = [4, 5, 6, 7, 8]

difference = difference_set(A, B)
print("차집합:", difference)