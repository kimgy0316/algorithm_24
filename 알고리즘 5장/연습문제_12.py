def median_of_three(A, left, right):
    mid = (left + right) // 2
    if A[left] > A[mid]:
        A[left], A[mid] = A[mid], A[left]
    if A[left] > A[right]:
        A[left], A[right] = A[right], A[left]
    if A[mid] > A[right]:
        A[mid], A[right] = A[right], A[mid]
    return mid

def partition(A, left, right):
    mid = median_of_three(A, left, right)
    A[left], A[mid] = A[mid], A[left]
    pivot = A[left]
    low = left + 1
    high = right

    while low <= high:
        while low <= right and A[low] <= pivot:
            low += 1
        while high >= left and A[high] > pivot:
            high -= 1
        if low < high:
            A[low], A[high] = A[high], A[low]

    A[left], A[high] = A[high], A[left]
    return high

def quicksort(A, left, right):
    if left < right:
        pivot_index = partition(A, left, right)
        quicksort(A, left, pivot_index - 1)
        quicksort(A, pivot_index + 1, right)

A = [3, 2, 1, 5, 4, 6, 9, 8, 7]
quicksort(A, 0, len(A) - 1)
print(A)
