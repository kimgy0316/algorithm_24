class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def print_info(self):
        print("Name: " + self.name)
        print("Phone Number: " + self.phone_number)

def set_contact(contact_list):
    name = input("Name: ")
    phone_number = input("Phone Number: ")
    for contact in contact_list:
        if contact.phone_number == phone_number:
            print("Error: 이미 가입된 사용자입니다.")
            return None
    contact = Contact(name, phone_number)
    return contact

def print_menu():
    print("1. 연락처 입력")
    print("2. 연락처 출력")
    print("3. 연락처 삭제")
    print("4. 연락처 조회")
    print("5. 연락처 수정")
    print("0. 종료")
    menu = input("메뉴선택: ")
    return int(menu)

def print_contact(contact_list):
    for contact in contact_list:
        contact.print_info()

def delete_contact(contact_list, name):
    for i, contact in enumerate(contact_list):
        if contact.name == name:
            del contact_list[i]
            print(f"Deleted contact: {name}")
            return
    print(f"Contact {name} not found")

def search_contact(contact_list, name):
    found = False
    for contact in contact_list:
        if contact.name == name:
            contact.print_info()
            found = True
    if not found:
        print("Contact not found")

def update_contact(contact_list, name):
    for contact in contact_list:
        if contact.name == name:
            new_phone_number = input("New Phone Number: ")
            for c in contact_list:
                if c.phone_number == new_phone_number:
                    print("Error: Contact with this phone number already exists.")
                    return
            contact.phone_number = new_phone_number
            print("Contact updated")
            return
    print("Contact not found")

def run():
    # 주소록 리스트
    contact_list = []

    while True:
        menu = print_menu()
        if menu == 1:
            contact = set_contact(contact_list)
            if contact is not None:
                contact_list.append(contact)
        elif menu == 2:
            print_contact(contact_list)
        elif menu == 3:
            name = input("Delete Name: ")
            delete_contact(contact_list, name)
        elif menu == 4:
            name = input("Search Name: ")
            search_contact(contact_list, name)
        elif menu == 5:
            name = input("Update Name: ")
            update_contact(contact_list, name)
        elif menu == 0:
            break

if __name__ == "__main__":
    run()
