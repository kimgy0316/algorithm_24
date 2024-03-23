def is_proper_subset(A, B):

    A = set(A)
    B = set(B)
    
    if A.issubset(B) and A != B:
        return True
    else:
        return False

A = [1, 2, 3]
B = [1, 2, 3, 4, 5]

result = is_proper_subset(A, B)
if result:
    print("A는 B의 진부분집합입니다.")
else:
    print("A는 B의 진부분집합이 아닙니다.")