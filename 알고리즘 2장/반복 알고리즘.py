def factorial(n):
    result = 1
    for k in range(n, 0, -1):
        result = result * k
    return result

n = int(input("팩토리얼 문제를 계산할 정수를 입력하시오 : "))
print(n, "의 팩토리얼은 ", factorial(n), "입니다.")