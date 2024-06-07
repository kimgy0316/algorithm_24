import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Contact 클래스: 연락처 정보를 저장
class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def print_info(self):
        return f"이름: {self.name}  전화번호: {self.phone_number}\n"

# Movie 클래스: 영화 정보를 저장
class Movie:
    def __init__(self, title, times, theater, age_limit):
        self.title = title
        self.times = times
        self.theater = theater
        self.age_limit = age_limit

    def to_string(self):
        return f"{self.title},{','.join(self.times)},{self.theater},{self.age_limit}"

# BookingSystem 클래스: 영화 예매 시스템의 핵심 로직
class BookingSystem:
    def __init__(self, file_path):
        self.movies = []
        self.file_path = file_path
        self.admin_password = "admin123"
        self.load_movies()
        self.sort_movies()

    def load_movies(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(',')
                    title = parts[0]
                    times = parts[1].split(',')
                    theater = parts[2]
                    age_limit = parts[3]
                    self.movies.append(Movie(title, times, theater, age_limit))

    def save_movies(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for movie in self.movies:
                file.write(f"{movie.to_string()}\n")

    def sort_movies(self):
        self.movies.sort(key=lambda movie: movie.title)

    def display_movies(self):
        movies_list = ""
        for idx, movie in enumerate(self.movies):
            movies_list += f"{idx + 1}. {movie.title} ({movie.age_limit})\n"
        return movies_list

    def binary_search_movie_by_name(self, name):
        left, right = 0, len(self.movies) - 1
        found_movies = []

        while left <= right:
            mid = (left + right) // 2
            if name.lower() in self.movies[mid].title.lower():
                found_movies.append(self.movies[mid])
                l, r = mid - 1, mid + 1
                while l >= left and name.lower() in self.movies[l].title.lower():
                    found_movies.append(self.movies[l])
                    l -= 1
                while r <= right and name.lower() in self.movies[r].title.lower():
                    found_movies.append(self.movies[r])
                    r += 1
                break
            elif name.lower() < self.movies[mid].title.lower():
                right = mid - 1
            else:
                left = mid + 1

        return found_movies

    def edit_movie(self, idx, new_title, new_times, new_theater, new_age_limit):
        if 0 <= idx < len(self.movies):
            self.movies[idx].title = new_title
            self.movies[idx].times = new_times
            self.movies[idx].theater = new_theater
            self.movies[idx].age_limit = new_age_limit
            self.sort_movies()
            self.save_movies()
            return True
        return False

    def delete_movie(self, idx):
        if 0 <= idx < len(self.movies):
            del self.movies[idx]
            self.save_movies()
            return True
        return False

# Application 클래스: Tkinter를 사용한 애플리케이션의 GUI
class Application(tk.Tk):
    def __init__(self, booking_system, contact_list):
        super().__init__()
        self.booking_system = booking_system
        self.contact_list = contact_list
        self.title("영화 예매 및 연락처 관리 시스템")

        self.admin_login_button = tk.Button(self, text="관리자 로그인", command=self.admin_login)
        self.admin_login_button.pack(pady=10)

        self.directory_label = tk.Label(self, text=f"movies.txt 파일은 이 디렉토리에 있습니다: {self.booking_system.file_path}")
        self.directory_label.pack(pady=10)

    def admin_login(self):
        password = simpledialog.askstring("비밀번호", "관리자 비밀번호를 입력하세요:", show='*')
        if password == self.booking_system.admin_password:
            self.admin_panel()
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다")

    def admin_panel(self):
        admin_window = tk.Toplevel(self)
        admin_window.title("관리자 패널")

        movie_list_frame = tk.Frame(admin_window)
        movie_list_frame.pack(side="left", padx=10, pady=10)

        movies_label = tk.Label(movie_list_frame, text="등록된 영화 목록")
        movies_label.pack()

        self.movies_listbox = tk.Listbox(movie_list_frame, width=30, height=20)
        self.movies_listbox.pack()

        self.update_movie_list()

        button_frame = tk.Frame(admin_window)
        button_frame.pack(side="right", padx=10, pady=10)

        add_button = tk.Button(button_frame, text="영화 추가", command=self.add_movie)
        add_button.pack(pady=5)

        view_button = tk.Button(button_frame, text="영화 조회", command=self.view_movies)
        view_button.pack(pady=5)

        contact_management_button = tk.Button(button_frame, text="연락처 관리", command=self.contact_management)
        contact_management_button.pack(pady=5)

    def update_movie_list(self):
        self.booking_system.sort_movies()
        self.movies_listbox.delete(0, tk.END)
        for movie in self.booking_system.movies:
            self.movies_listbox.insert(tk.END, movie.title)

    def add_movie(self):
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        new_theater = simpledialog.askstring("영화 추가", "새 영화 상영관을 입력하세요:")
        new_age_limit = simpledialog.askstring("영화 추가", "새 영화 연령 제한을 입력하세요:")
        self.booking_system.movies.append(Movie(new_title, new_times, new_theater, new_age_limit))
        self.booking_system.sort_movies()
        self.booking_system.save_movies()
        self.update_movie_list()
        messagebox.showinfo("성공", "영화가 성공적으로 추가되었습니다")

    def view_movies(self):
        search_window = tk.Toplevel(self)
        search_window.title("영화 조회")

        search_label = tk.Label(search_window, text="영화 제목을 입력하세요:")
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)

        search_button = tk.Button(search_window, text="검색", command=lambda: self.search_movies(search_entry.get(), search_window))
        search_button.pack(pady=5)

    def search_movies(self, name, search_window):
        found_movies = self.booking_system.binary_search_movie_by_name(name)
        if found_movies:
            movies_list = "\n".join([f"{idx + 1}. {movie.title} ({movie.age_limit})" for idx, movie in enumerate(found_movies)])
            movies_label = tk.Label(search_window, text=movies_list)
            movies_label.pack(pady=10)

            select_button = tk.Button(search_window, text="영화 선택", command=lambda: self.select_movie(found_movies, search_window))
            select_button.pack(pady=5)
        else:
            messagebox.showinfo("검색 결과", "일치하는 영화가 없습니다.")

    def select_movie(self, movies, search_window):
        movie_index = simpledialog.askinteger("영화 선택", "선택할 영화 번호를 입력하세요:") - 1
        if 0 <= movie_index < len(movies):
            movie = movies[movie_index]
            search_window.destroy()
            self.show_movie_details(movie)
        else:
            messagebox.showerror("오류", "유효하지 않은 영화 번호입니다")

    def show_movie_details(self, movie):
        details_window = tk.Toplevel(self)
        details_window.title("영화 정보")

        title_label = tk.Label(details_window, text=f"제목: {movie.title}")
        title_label.pack(pady=5)

        times_label = tk.Label(details_window, text=f"상영 시간: {', '.join(movie.times)}")
        times_label.pack(pady=5)

        theater_label = tk.Label(details_window, text=f"상영관: {movie.theater}")
        theater_label.pack(pady=5)

        age_limit_label = tk.Label(details_window, text=f"연령 제한: {movie.age_limit}")
        age_limit_label.pack(pady=5)

        edit_button = tk.Button(details_window, text="영화 수정", command=lambda: self.edit_movie_details(movie, details_window))
        edit_button.pack(pady=5)

        delete_button = tk.Button(details_window, text="영화 삭제", command=lambda: self.delete_movie_details(movie, details_window))
        delete_button.pack(pady=5)

    def edit_movie_details(self, movie, details_window):
        new_title = simpledialog.askstring("영화 수정", "새 영화 제목을 입력하세요:", initialvalue=movie.title)
        new_times = simpledialog.askstring("영화 수정", "새 영화 시간을 입력하세요 (쉼표로 구분):", initialvalue=','.join(movie.times)).split(',')
        new_theater = simpledialog.askstring("영화 수정", "새 상영관을 입력하세요:", initialvalue=movie.theater)
        new_age_limit = simpledialog.askstring("영화 수정", "새 연령 제한을 입력하세요:", initialvalue=movie.age_limit)
        if new_title is not None and new_times is not None and new_theater is not None and new_age_limit is not None:
            if self.booking_system.edit_movie(self.booking_system.movies.index(movie), new_title, new_times, new_theater, new_age_limit):
                self.update_movie_list()
                messagebox.showinfo("성공", "영화가 성공적으로 수정되었습니다")
                details_window.destroy()
            else:
                messagebox.showerror("오류", "영화 수정에 실패했습니다")
        else:
            messagebox.showerror("오류", "수정 정보를 모두 입력하세요")

    def delete_movie_details(self, movie, details_window):
        confirm = messagebox.askyesno("확인", f"정말로 '{movie.title}' 영화를 삭제하시겠습니까?")
        if confirm:
            if self.booking_system.delete_movie(self.booking_system.movies.index(movie)):
                self.update_movie_list()
                messagebox.showinfo("성공", "영화가 성공적으로 삭제되었습니다")
                details_window.destroy()
            else:
                messagebox.showerror("오류", "영화 삭제에 실패했습니다")

    def contact_management(self):
        contact_window = tk.Toplevel(self)
        contact_window.title("연락처 관리")

        listbox_frame = tk.Frame(contact_window)
        listbox_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.contact_listbox = tk.Listbox(listbox_frame, width=40, height=10)
        self.contact_listbox.pack(side=tk.LEFT, padx=(0, 10))

        button_frame = tk.Frame(contact_window)
        button_frame.pack(side=tk.RIGHT)

        search_button = tk.Button(button_frame, text="검색", command=lambda: self.on_search_contact())
        search_button.pack(fill=tk.X)

        add_button = tk.Button(button_frame, text="추가", command=lambda: self.on_add_contact())
        add_button.pack(fill=tk.X)

        delete_button = tk.Button(button_frame, text="삭제", command=lambda: self.on_delete_contact())
        delete_button.pack(fill=tk.X)

        update_button = tk.Button(button_frame, text="수정", command=lambda: self.on_update_contact())
        update_button.pack(fill=tk.X)

        home_button = tk.Button(button_frame, text="홈", command=lambda: self.on_home())
        home_button.pack(fill=tk.X)

        exit_button = tk.Button(button_frame, text="종료", command=lambda: self.on_exit())
        exit_button.pack(fill=tk.X)

        self.load_contacts()

    def on_add_contact(self):
        contact = set_contact(self.contact_list)
        if contact:
            self.contact_list.append(contact)
            self.refresh_listbox(self.contact_listbox)

    def on_delete_contact(self):
        name = simpledialog.askstring("Input", "삭제할 고객명:")
        if name:
            matching_contacts = [contact for contact in self.contact_list if contact.name == name]
            if matching_contacts:
                phone_number = simpledialog.askstring("Input", "삭제할 전화번호:")
                if phone_number:
                    delete_contact(self.contact_list, name, phone_number)
                    self.refresh_listbox(self.contact_listbox)
            else:
                messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

    def on_search_contact(self):
        name = simpledialog.askstring("Input", "검색할 고객명:")
        if name:
            search_contact(self.contact_list, name, self.contact_listbox)

    def on_update_contact(self):
        name = simpledialog.askstring("Input", "수정할 고객명:")
        if name:
            matching_contacts = [contact for contact in self.contact_list if contact.name == name]
            if matching_contacts:
                phone_number = simpledialog.askstring("Input", "현재 전화번호:")
                new_phone_number = simpledialog.askstring("Input", "새로운 전화번호:")
                if phone_number and new_phone_number:
                    update_contact(self.contact_list, name, phone_number, new_phone_number)
                    self.refresh_listbox(self.contact_listbox)
            else:
                messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

    def refresh_listbox(self, listbox):
        listbox.delete(0, tk.END)
        for contact in self.contact_list:
            listbox.insert(tk.END, contact.print_info())

    def on_exit(self):
        save_contacts(self.contact_list)
        self.destroy()

    def on_home(self):
        self.refresh_listbox(self.contact_listbox)

    def load_contacts(self):
        load_contacts(self.contact_list, self.contact_listbox)

# 연락처 관리 함수들
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
    found_contacts = sorted([contact for contact in contact_list if name in contact.name], key=lambda x: (x.name, x.phone_number))
    listbox.delete(0, tk.END)
    for contact in found_contacts:
        listbox.insert(tk.END, contact.print_info())

def update_contact(contact_list, name, phone_number, new_phone_number):
    for contact in contact_list:
        if contact.name == name and contact.phone_number == phone_number:
            contact.phone_number = new_phone_number
            messagebox.showinfo("Updated", f"[수정] 이름: {name}, 새로운 전화번호: {new_phone_number}")
            return
    messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

def save_contacts(contact_list, filename=r"C:\Users\LG\Desktop\phone_number.txt"):
    with open(filename, "w") as file:
        for contact in contact_list:
            file.write(f"{contact.name},{contact.phone_number}\n")

def load_contacts(contact_list, listbox, filename=r"C:\Users\LG\Desktop\phone_number.txt"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                lines = file.readlines()
                contact_list.clear()
                for line in lines:
                    name, phone_number = line.strip().split(',')
                    contact_list.append(Contact(name, phone_number))
                contact_list.sort(key=lambda x: (x.name, x.phone_number))
                listbox.delete(0, tk.END)
                for contact in contact_list:
                    listbox.insert(tk.END, contact.print_info())
            except Exception as e:
                messagebox.showerror("Error", f"연락처 파일을 읽는 도중 오류가 발생했습니다: {e}")
    else:
        messagebox.showerror("Error", "저장된 연락처 파일을 찾을 수 없습니다.")

# 프로그램 실행
file_path = r"C:\Users\LG\Desktop\movies.txt"
booking_system = BookingSystem(file_path)
contact_list = []
app = Application(booking_system, contact_list)
app.mainloop()
