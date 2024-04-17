import queue

def sentinel_search(A, key):
    n = len(A)
    A.append(key)
    i=0
    while A[i] != key :
        i += 1
    if i == n : return-1
    return 1