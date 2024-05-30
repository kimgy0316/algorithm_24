# 아이디
# 비밀번호
# 영화 정보 추가
# 영화 정보 조회
#
class Node:
    def __init__(self, data=None):
        self.data = data
        self.link = None

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def get_entry(self, pos):
        p = self.head
        for _ in range(pos):
            if p is None:
                return None
            p = p.link
        return p

    def size(self):
        count = 0
        p = self.head
        while p is not None:
            count += 1
            p = p.link
        return count

    def replace(self, pos, element):
        node = self.get_entry(pos)
        if node is not None:
            node.data = element

    def insert_next(self, prev, node):
        if node is not None:
            node.link = prev.link
            prev.link = node

    def insert(self, pos, element):
        new_node = Node(element)
        if pos == 0:
            new_node.link = self.head
            self.head = new_node
        else:
            prev = self.get_entry(pos - 1)
            if prev is not None:
                self.insert_next(prev, new_node)
            else:
                del new_node

    def remove_next(self, before):
        removed = before.link
        if removed is not None:
            before.link = removed.link
        return removed

    def delete(self, pos):
        if pos == 0 and not self.is_empty():
            removed = self.head
            self.head = self.head.link
            del removed
        else:
            prev = self.get_entry(pos - 1)
            if prev is not None:
                removed = self.remove_next(prev)
                if removed is not None:
                    del removed

    def clear(self):
        while not self.is_empty():
            self.delete(0)

    def display(self):
        i = 0
        p = self.head
        while p is not None:
            print(f"{i:3d}: {p.data}")
            p = p.link
            i += 1

    def display_1(self):
        p = self.head
        while p is not None:
            print(p.data, end='')
            p = p.link

    def find_str(self, search_str):
        i = 0
        p = self.head
        while p is not None:
            if search_str in p.data:
                print(f"{i:3d}: {p.data}")
            p = p.link
            i += 1

    def find_and_change(self, search_str, replace_str):
        p = self.head
        while p is not None:
            if search_str in p.data:
                p.data = p.data.replace(search_str, replace_str)
            p = p.link

def main():
    linked_list = LinkedList()
    flag = False

    while True:
        command = input("[메뉴선택] i-입력, d-삭제, r-변경, p-출력, I-파일읽기, s-저장, q-종료, f-검색, c-바꾸기 ⇒ ").strip()

        if command == 'i':
            pos = int(input(" 입력행 번호 : "))
            content = input(" 입력행 내용 : ")
            linked_list.insert(pos, content)
            flag = True
        elif command == 'd':
            pos = int(input(" 삭제행 번호 : "))
            linked_list.delete(pos)
            flag = True
        elif command == 'r':
            pos = int(input(" 변경행 번호: "))
            content = input(" 변경행 내용: ")
            linked_list.replace(pos, content)
            flag = True
        elif command == 'I':
            try:
                with open("Test.txt", "r") as fp:
                    for line in fp:
                        linked_list.insert(linked_list.size(), line)
            except FileNotFoundError:
                print("파일을 찾을 수 없습니다.")
        elif command == 's':
            with open("Test.txt", "w") as fp:
                p = linked_list.head
                while p is not None:
                    fp.write(p.data)
                    p = p.link
        elif command == 'p':
            linked_list.display()
        elif command == 'f':
            search_str = input(" 검색 문자열 입력: ")
            linked_list.find_str(search_str)
        elif command == 'c':
            search_str = input(" 검색 문자열 입력: ")
            replace_str = input(" 바꿀 문자열 입력: ")
            linked_list.find_and_change(search_str, replace_str)
            flag = True
        elif command == 'q':
            if flag:
                save = input("수정된 내용이 있습니다. 파일에 저장하시겠습니까?(y/n) ").strip().lower()
                if save == 'y':
                    with open("Test.txt", "w") as fp:
                        p = linked_list.head
                        while p is not None:
                            fp.write(p.data)
                            p = p.link
            break
        else:
            print("올바르지 않은 명령입니다.")

if __name__ == "__main__":
    main()
