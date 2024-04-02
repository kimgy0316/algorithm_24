def compute_square_B(n) :
    sum = 0
    for i in range(n):
        sum = sum + n;
    return sum

n = int(input("제곱하고 싶은 수를 입력하시오 : "))

print(n, "의 제곱은 ", compute_square_B(n), "입니다.")