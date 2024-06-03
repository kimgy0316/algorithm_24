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

def set_contact(contact_list):
    name = simpledialog.askstring("Input", "Name:")
    phone_number = simpledialog.askstring("Input", "전화번호:")
    if name and phone_number:
        for contact in contact_list:
            if contact.phone_number == phone_number:
                messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                return None
        return Contact(name, phone_number)
    return None

def delete_contact(contact_list, name, phone_number):
    for i, contact in enumerate(contact_list):
        if contact.name == name and contact.phone_number == phone_number:
            del contact_list[i]
            messagebox.showinfo("Deleted", f"[삭제] 이름: {name}, 전화번호: {phone_number}")
            return
    messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {name}, 전화번호: {phone_number}")

def search_contact(contact_list, name, listbox):
    found_contacts = [contact for contact in contact_list if name in contact.name]
    listbox.delete(0, tk.END)
    for contact in found_contacts:
        listbox.insert(tk.END, contact.print_info())

def update_contact(contact_list, name):
    for contact in contact_list:
        if contact.name == name:
            new_phone_number = simpledialog.askstring("Input", "새로운 전화번호:")
            if new_phone_number:
                for c in contact_list:
                    if c.phone_number == new_phone_number:
                        messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                        return
                contact.phone_number = new_phone_number
                messagebox.showinfo("Updated", "Contact updated")
                return
    messagebox.showerror("Error", "가입되지 않은 사용자입니다.")

def save_contacts(contact_list, filename="contacts.json"):
    with open(filename, "w") as file:
        json_list = [{"name": contact.name, "phone_number": contact.phone_number} for contact in contact_list]
        json.dump(json_list, file)

def load_contacts(contact_list, listbox, filename="contacts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            json_list = json.load(file)
            contact_list.clear()  # 기존 연락처 리스트 초기화
            for contact in json_list:
                contact_list.append(Contact(contact["name"], contact["phone_number"]))
            contact_list.sort(key=lambda x: (x.name, x.phone_number))  # 이름을 가나다순으로 정렬 후, 동일한 이름의 경우 전화번호 오름차순으로 정렬
        refresh_listbox(contact_list, listbox)  # 리스트박스 업데이트
    else:
        messagebox.showerror("Error", "저장된 연락처 파일을 찾을 수 없습니다.")

def on_add_contact(contact_list, listbox):
    contact = set_contact(contact_list)
    if contact:
        contact_list.append(contact)
        refresh_listbox(contact_list, listbox)

def on_delete_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "삭제할 고객명:")
    if name:
        matching_contacts = [contact for contact in contact_list if name in contact.name]
        if matching_contacts:
            phone_numbers = "\n".join([contact.phone_number for contact in matching_contacts])
            selected_phone_number = simpledialog.askstring("Input", f"{name}의 전화번호를 선택하세요:\n{phone_numbers}")
            if selected_phone_number:
                delete_contact(contact_list, name, selected_phone_number)
                refresh_listbox(contact_list, listbox)
        else:
            messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {name}")

def on_search_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "검색할 고객명:")
    if name:
        search_contact(contact_list, name, listbox)

def on_update_contact(contact_list):
    name = simpledialog.askstring("Input", "수정할 고객명")
    if name:
        update_contact(contact_list, name)

def refresh_listbox(contact_list, listbox):
    listbox.delete(0, tk.END)
    for contact in contact_list:
        listbox.insert(tk.END, contact.print_info())

def on_exit(contact_list):
    save_contacts(contact_list)
    root.destroy()

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

    update_button = tk.Button(button_frame, text="수정", command=lambda: on_update_contact(contact_list))
    update_button.pack(fill=tk.X)

    exit_button = tk.Button(button_frame, text="종료", command=lambda: on_exit(contact_list))
    exit_button.pack(fill=tk.X)

    load_contacts(contact_list, listbox)

    root.mainloop()

if __name__ == "__main__":
    contact_list = []
    create_gui(contact_list)
