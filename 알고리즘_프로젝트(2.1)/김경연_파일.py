import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def print_info(self):
        return f"이름: {self.name}  전화번호: {self.phone_number}\n"

def binary_search(contact_list, target, key=lambda x: x.name):
    """
    이진 탐색을 사용하여 연락처 리스트에서 타겟 이름 또는 전화번호의 위치를 찾는다.
    해당 요소가 존재하지 않으면 삽입 위치를 반환한다.
    """
    low, high = 0, len(contact_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if key(contact_list[mid]) < target:
            low = mid + 1
        elif key(contact_list[mid]) > target:
            high = mid - 1
        else:
            return mid
    return low  # 위치를 반환하여 삽입/검색 등에 사용

def set_contact(contact_list):
    name = simpledialog.askstring("Input", "Name:")
    phone_number = simpledialog.askstring("Input", "전화번호:")
    if name and phone_number:
        # 이미 존재하는 전화번호인지 확인
        for contact in contact_list:
            if contact.phone_number == phone_number:
                messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                return None
        return Contact(name, phone_number)
    return None

def delete_contact(contact_list, name, phone_number):
    # 이름을 기준으로 이진 탐색을 사용하여 삭제할 연락처 찾기
    index = binary_search(contact_list, name)
    while index < len(contact_list) and contact_list[index].name == name:
        if contact_list[index].phone_number == phone_number:
            del contact_list[index]
            messagebox.showinfo("Deleted", f"[삭제] 이름: {name}, 전화번호: {phone_number}")
            return
        index += 1
    messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {name}, 전화번호: {phone_number}")

def search_contact(contact_list, name, listbox):
    # 이름을 기준으로 이진 탐색을 사용하여 검색된 연락처 표시
    index = binary_search(contact_list, name)
    listbox.delete(0, tk.END)
    while index < len(contact_list) and contact_list[index].name == name:
        listbox.insert(tk.END, contact_list[index].print_info())
        index += 1

def update_contact(contact_list, name, listbox):
    listbox.delete(0, tk.END)
    # 이름을 기준으로 이진 탐색을 사용하여 수정할 연락처 찾기
    index = binary_search(contact_list, name)
    if index < len(contact_list) and contact_list[index].name == name:
        while index < len(contact_list) and contact_list[index].name == name:
            listbox.insert(tk.END, contact_list[index].print_info())
            index += 1
        selected_phone_number = simpledialog.askstring("Input", "수정할 전화번호를 입력하세요:")
        if selected_phone_number:
            index = binary_search(contact_list, name)
            while index < len(contact_list) and contact_list[index].name == name:
                if contact_list[index].phone_number == selected_phone_number:
                    new_phone_number = simpledialog.askstring("Input", "새로운 전화번호:")
                    if new_phone_number:
                        # 새 전화번호가 이미 존재하는지 확인
                        for c in contact_list:
                            if c.phone_number == new_phone_number:
                                messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                                return
                        contact_list[index].phone_number = new_phone_number
                        contact_list.sort(key=lambda x: (x.name, x.phone_number))
                        refresh_listbox(contact_list, listbox)
                        messagebox.showinfo("Updated", "수정이 완료되었습니다.")
                        return
                index += 1
            messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")
    else:
        messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

def save_contacts(contact_list, filename="contacts.json"):
    with open(filename, "w") as file:
        json_list = [{"name": contact.name, "phone_number": contact.phone_number} for contact in contact_list]
        json.dump(json_list, file)

def load_contacts(contact_list, listbox, filename="contacts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                json_list = json.load(file)
                contact_list.clear()
                for contact in json_list:
                    name = contact.get("name", "")
                    phone_number = contact.get("phone_number", "")
                    if name and phone_number:
                        contact_list.append(Contact(name, phone_number))
                    else:
                        messagebox.showerror("Error", "연락처 파일에 필수 정보가 누락되었습니다.")
                contact_list.sort(key=lambda x: (x.name, x.phone_number))
                refresh_listbox(contact_list, listbox)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "저장된 연락처 파일을 읽을 수 없습니다.")
    else:
        messagebox.showwarning("Warning", "저장된 연락처 파일을 찾을 수 없습니다. 새로운 연락처를 추가해주세요.")

def on_add_contact(contact_list, listbox):
    contact = set_contact(contact_list)
    if contact:
        # 이진 탐색을 사용하여 올바른 위치에 연락처 삽입
        index = binary_search(contact_list, contact.name)
        contact_list.insert(index, contact)
        refresh_listbox(contact_list, listbox)

def on_delete_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "삭제할 고객명:")
    if name:
        listbox.delete(0, tk.END)
        # 이름을 기준으로 이진 탐색을 사용하여 삭제할 연락처 표시
        index = binary_search(contact_list, name)
        while index < len(contact_list) and contact_list[index].name == name:
            listbox.insert(tk.END, contact_list[index].print_info())
            index += 1
        selected_phone_number = simpledialog.askstring("Input", "삭제할 전화번호를 입력하세요:")
        if selected_phone_number:
            delete_contact(contact_list, name, selected_phone_number)
            refresh_listbox(contact_list, listbox)

def on_search_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "검색할 고객명:")
    if name:
        search_contact(contact_list, name, listbox)

def on_update_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "수정할 고객명:")
    if name:
        update_contact(contact_list, name, listbox)

def refresh_listbox(contact_list, listbox):
    listbox.delete(0, tk.END)
    # 연락처를 이름순으로 정렬한 후, 전화번호가 숫자로 인식되어 오름차순으로 정렬됩니다.
    sorted_contacts = sorted(contact_list, key=lambda x: (x.name, int(x.phone_number)))
    for contact in sorted_contacts:
        listbox.insert(tk.END, contact.print_info())

def on_exit(contact_list):
    save_contacts(contact_list)
    root.destroy()

def on_home(contact_list, listbox):
    refresh_listbox(contact_list, listbox)

def create_gui(contact_list):
    global root
    root = tk.Tk()
    root.title("Contact Manager")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    listbox = tk.Listbox(frame, width=40, height=10)
    listbox.pack(side=tk.LEFT, padx=(0, 10))

    refresh_listbox(contact_list, listbox)

    button_frame = tk.Frame(frame)
    button_frame.pack(side=tk.RIGHT)

    search_button = tk.Button(button_frame, text="검색", command=lambda: on_search_contact(contact_list, listbox))
    search_button.pack(fill=tk.X)

    add_button = tk.Button(button_frame, text="추가", command=lambda: on_add_contact(contact_list, listbox))
    add_button.pack(fill=tk.X)

    delete_button = tk.Button(button_frame, text="삭제", command=lambda: on_delete_contact(contact_list, listbox))
    delete_button.pack(fill=tk.X)

    update_button = tk.Button(button_frame, text="수정", command=lambda: on_update_contact(contact_list, listbox))
    update_button.pack(fill=tk.X)

    home_button = tk.Button(button_frame, text="홈", command=lambda: on_home(contact_list, listbox))
    home_button.pack(fill=tk.X)

    exit_button = tk.Button(button_frame, text="종료", command=lambda: on_exit(contact_list))
    exit_button.pack(fill=tk.X)

    load_contacts(contact_list, listbox)

    root.mainloop()

if __name__ == "__main__":
    contact_list = []
    create_gui(contact_list)
