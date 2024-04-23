def partition(A, left, right):
    pivot = A[right] 
    i = left - 1
    for j in range(left, right):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i] 
    A[i + 1], A[right] = A[right], A[i + 1]  
    return i + 1 
def quick_select(A, left, right, k):
    if left == right:
        return A[left]
    pos = partition(A, left, right)
    if pos - left == k - 1:
        return A[pos]
    elif pos - left > k - 1:
        return quick_select(A, left, pos - 1, k)
    else:
        return quick_select(A, pos + 1, right, k - pos + left - 1)
array = [12, 5, 7, 9, 18, 3, 8]
print("입력 리스트 =", array)
n = len(array)
print("중간값: ", quick_select(array, 0, n - 1, 3))