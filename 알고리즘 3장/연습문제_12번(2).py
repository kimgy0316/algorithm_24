def closest_pair(p):
    n = len(p)
    p.sort()

    min_dist = float("inf")
    for i in range(n - 1):
        dist = abs(p[i] - p[i + 1])
        if dist < min_dist:
            min_dist = dist
    return min_dist

