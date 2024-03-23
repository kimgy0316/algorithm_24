def reverse(string):
    stack = list(string)
    reversed = ""
    while stack:
        reversed += stack.pop()
    return reversed

if __name__ == "__main__":
    string = input("문자열을 입력하세요: ")
    reversed = reverse(string)
    print("역순으로 출력된 문자열:", reversed)