def median_of_three(a, l, r):
    m = (l + r) // 2
    if (a[l] < a[m] and a[m] < a[r]) or (a[r] < a[m] and a[m] < a[l]):
        return m
    if (a[m] < a[l] and a[l] < a[r]) or (a[r] < a[l] and a[l] < a[m]):
        return l
    else:
        return r