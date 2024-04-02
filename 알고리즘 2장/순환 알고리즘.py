def hanoi_tower(n, fr, tmp, to):
    if (n==1):
        print("원판 1: %s --> %s" % (fr, to))
    else : 
        hanoi_tower(n-1, fr, to, tmp)
        print("원판 %s: %s --> %s" % (n, fr, to))
        hanoi_tower(n-1, tmp, fr, to)

n = int(input("원판의 갯수(타워는 3개) >>> "))
hanoi_tower(n, 'A', 'B', 'C')