def partition(A, left, right):
    pivot_index = median_of_three(A, left, right)
    A[left], A[pivot_index] = A[pivot_index], A[left]
    
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

def median_of_three(a, l, r): 
    m = (l + r) // 2
    if ((a[l] < a[m] and a[m] < a[r]) or (a[r] < a[m] and a[m] < a[l])): 
        return m 
    if ((a[m] < a[l] and a[l] < a[r]) or (a[r] < a[l] and a[l] < a[m])): 
        return l 
    else: 
        return r

def quick_sort(A, left, right):
    if left < right:
        pivot_index = partition(A, left, right)
        quick_sort(A, left, pivot_index - 1)
        quick_sort(A, pivot_index + 1, right)

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
quick_sort(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
