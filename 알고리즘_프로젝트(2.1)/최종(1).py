import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
from hashlib import sha256

# Contact 클래스: 연락처 정보를 저장
class Contact:
    def __init__(self, phone_number, password, reservations=None):
        self.phone_number = phone_number
        self.password_plain = password
        self.password = self.hash_password(password)
        self.reservations = reservations if reservations is not None else []

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def print_info(self):
        return f"전화번호: {self.phone_number}, 비밀번호: {self.password_plain}\n"

# Movie 클래스: 영화 정보를 저장
class Movie:
    def __init__(self, title, times, theater, age_limit, seats=None):
        self.title = title
        self.times = times
        self.theater = theater
        self.age_limit = age_limit
        self.seats = {time: [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 
            'E1', 'E2', 'E3', 'E4', 'E5', 'E6',
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6'
        ] for time in times}

    def to_string(self):
        times_str = ';'.join(self.times)
        seats_str = ';'.join([f"{time}:{','.join(self.seats[time])}" for time in self.times])
        return f"{self.title},{times_str},{self.theater},{self.age_limit},{seats_str}"

    @staticmethod
    def from_string(movie_str):
        parts = movie_str.strip().split(',')
        title = parts[0]
        times = parts[1].split(';')
        theater = parts[2]
        age_limit = parts[3]
        if len(parts) > 4:
            seats = {time: seats.split(',') for time, seats in (item.split(':') for item in parts[4].split(';'))}
        else:
            seats = {time: ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6"] for time in times}
        return Movie(title, times, theater, age_limit, seats)

# BookingSystem 클래스: 영화 예매 시스템의 핵심 로직
class BookingSystem:
    def __init__(self, file_path):
        self.movies = []
        self.file_path = file_path
        self.admin_password = self.hash_password("admin123")
        self.load_movies()

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def load_movies(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    self.movies.append(Movie.from_string(line.strip()))

    def save_movies(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for movie in self.movies:
                file.write(f"{movie.to_string()}\n")

    def insert_sorted_movie(self, new_movie):
        self.movies.append(new_movie)
        i = len(self.movies) - 2
        while i >= 0 and self.movies[i].title > new_movie.title:
            self.movies[i + 1] = self.movies[i]
            i -= 1
        self.movies[i + 1] = new_movie

    def display_movies(self):
        movies_list = ""
        for idx, movie in enumerate(self.movies):
            movies_list += f"{idx + 1}. {movie.title} ({movie.age_limit})\n"
        return movies_list

    def linear_search_movie_by_name(self, name):
        found_movies = []
        for movie in self.movies:
            if name.lower() in movie.title.lower():
                found_movies.append(movie)
        return found_movies

    def edit_movie(self, idx, new_title, new_times, new_theater, new_age_limit):
        if 0 <= idx < len(self.movies):
            self.movies[idx].title = new_title
            self.movies[idx].times = new_times
            self.movies[idx].theater = new_theater
            self.movies[idx].age_limit = new_age_limit
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
    def __init__(self, booking_system, contact_list, movies_file, reservations_file):
        super().__init__()
        self.booking_system = booking_system
        self.contact_list = contact_list
        self.movies_file = movies_file
        self.reservations_file = reservations_file
        self.title("영화 예매 및 연락처 관리 시스템")

        self.admin_login_button = tk.Button(self, text="관리자 로그인", command=self.admin_login)
        self.admin_login_button.pack(pady=10)

        self.user_login_button = tk.Button(self, text="사용자 로그인", command=self.login_user)
        self.user_login_button.pack(pady=10)

        self.user_register_button = tk.Button(self, text="회원가입", command=self.register_user)
        self.user_register_button.pack(pady=10)

    def admin_login(self):
        password = simpledialog.askstring("비밀번호", "관리자 비밀번호를 입력하세요:", show='*')
        if self.booking_system.hash_password(password) == self.booking_system.admin_password:
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
        self.movies_listbox.delete(0, tk.END)
        for movie in self.booking_system.movies:
            self.movies_listbox.insert(tk.END, movie.title)

    def add_movie(self):
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        new_theater = simpledialog.askstring("영화 추가", "새 영화 상영관을 입력하세요:")
        new_age_limit = simpledialog.askstring("영화 추가", "새 영화 연령 제한을 입력하세요:")
        new_movie = Movie(new_title, new_times, new_theater, new_age_limit)
        self.booking_system.insert_sorted_movie(new_movie)
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
        found_movies = self.booking_system.linear_search_movie_by_name(name)
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

        self.contact_listbox = tk.Listbox(listbox_frame, width=60, height=10)  # 넓이를 더 넓게 설정
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
        contact = self.set_contact(self.contact_list)
        if contact:
            self.contact_list.append(contact)
            self.refresh_listbox(self.contact_list, self.contact_listbox)

    def on_delete_contact(self):
        phone_number = simpledialog.askstring("Input", "삭제할 전화번호:")
        if phone_number:
            self.delete_contact(self.contact_list, phone_number)
            self.refresh_listbox(self.contact_list, self.contact_listbox)

    def on_search_contact(self):
        phone_number = simpledialog.askstring("Input", "검색할 전화번호:")
        if phone_number:
            self.search_contact(self.contact_list, phone_number, self.contact_listbox)

    def on_update_contact(self):
        phone_number = simpledialog.askstring("Input", "수정할 전화번호:")
        if phone_number:
            new_password = simpledialog.askstring("Input", "새로운 비밀번호:")
            if new_password:
                self.update_contact(self.contact_list, phone_number, new_password)
                self.refresh_listbox(self.contact_list, self.contact_listbox)

    def refresh_listbox(self, contact_list, listbox):
        listbox.delete(0, tk.END)
        for contact in contact_list:
            listbox.insert(tk.END, contact.print_info())

    def on_exit(self):
        self.save_contacts(self.contact_list)
        self.destroy()

    def on_home(self):
        self.refresh_listbox(self.contact_list, self.contact_listbox)

    def load_contacts(self):
        self.load_contacts_from_file(self.contact_list, self.contact_listbox)
    def login_user(self):
        self.destroy()
        root = tk.Tk()
        root.title("영화 예매 시스템")
        UserReservationSystem(root, self.movies_file, self.reservations_file)

    def register_user(self):
        self.destroy()
        root = tk.Tk()
        root.title("회원가입")
        UserReservationSystem(root, self.movies_file, self.reservations_file, register=True)

    def set_contact(self, contact_list):
        phone_number = simpledialog.askstring("Input", "전화번호:")
        password = simpledialog.askstring("Input", "비밀번호:")
        if phone_number and password:
            for contact in contact_list:
                if contact.phone_number == phone_number:
                    messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                    return None
            return Contact(phone_number, password)
        return None

    def delete_contact(self, contact_list, phone_number):
        for i, contact in enumerate(contact_list):
            if contact.phone_number == phone_number:
                del contact_list[i]
                messagebox.showinfo("Deleted", f"[삭제] 전화번호: {phone_number}")
                return
        messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {phone_number}")

    def search_contact(self, contact_list, phone_number, listbox):
        found_contacts = sorted([contact for contact in contact_list if phone_number in contact.phone_number], key=lambda x: x.phone_number)
        listbox.delete(0, tk.END)
        for contact in found_contacts:
            listbox.insert(tk.END, contact.print_info())

    def update_contact(self, contact_list, phone_number, new_password):
        for contact in contact_list:
            if contact.phone_number == phone_number:
                contact.password_plain = new_password
                contact.password = contact.hash_password(new_password)
                messagebox.showinfo("Updated", f"[수정] 전화번호: {phone_number}, 새로운 비밀번호: {new_password}")
                return
        messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

    def save_contacts(self, contact_list, filename="contacts.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            for contact in contact_list:
                reservations = str(contact.reservations)
                file.write(f"{contact.phone_number}|{contact.password_plain}|{contact.password}|{reservations}\n")

    def load_contacts_from_file(self, contact_list, listbox, filename="contacts.txt"):
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    lines = file.readlines()
                    contact_list.clear()
                    for line in lines:
                        parts = line.strip().split('|')
                        if len(parts) == 4:
                            phone_number = parts[0]
                            password_plain = parts[1]
                            password = parts[2]
                            reservations = eval(parts[3])
                            contact_list.append(Contact(phone_number, password_plain, reservations))
                    contact_list.sort(key=lambda x: x.phone_number)
                    listbox.delete(0, tk.END)
                    for contact in contact_list:
                        listbox.insert(tk.END, contact.print_info())
                except Exception as e:
                    messagebox.showerror("Error", f"연락처 파일을 읽는 도중 오류가 발생했습니다: {e}")
        else:
            messagebox.showerror("Error", "저장된 연락처 파일을 찾을 수 없습니다.")

# 연락처 관리 함수들
def set_contact(contact_list):
    phone_number = simpledialog.askstring("Input", "전화번호:")
    password = simpledialog.askstring("Input", "비밀번호:")
    if phone_number and password:
        for contact in contact_list:
            if contact.phone_number == phone_number:
                messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                return None
        return Contact(phone_number, password)
    return None

def delete_contact(contact_list, phone_number):
    for i, contact in enumerate(contact_list):
        if contact.phone_number == phone_number:
            del contact_list[i]
            messagebox.showinfo("Deleted", f"[삭제] 전화번호: {phone_number}")
            return
    messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {phone_number}")

def search_contact(contact_list, phone_number, listbox):
    found_contacts = sorted([contact for contact in contact_list if phone_number in contact.phone_number], key=lambda x: x.phone_number)
    listbox.delete(0, tk.END)
    for contact in found_contacts:
        listbox.insert(tk.END, contact.print_info())

def update_contact(contact_list, phone_number, new_password):
    for contact in contact_list:
        if contact.phone_number == phone_number:
            contact.password = sha256(new_password.encode()).hexdigest()
            messagebox.showinfo("Updated", f"[수정] 전화번호: {phone_number}, 새로운 비밀번호: {new_password}")
            return
    messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

def save_contacts(contact_list, filename=r"C:\Users\LG\Desktop\reservations.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for contact in contact_list:
            reservations = str(contact.reservations)
            file.write(f"{contact.phone_number}|{contact.password_plain}|{contact.password_hashed}|{reservations}\n")

def load_contacts(contact_list, listbox, filename=r"C:\Users\LG\Desktop\reservations.txt"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                lines = file.readlines()
                contact_list.clear()
                for line in lines:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        phone_number = parts[0]
                        password = parts[1]
                        reservations = eval(parts[2])
                        contact_list.append(Contact(phone_number, password, reservations))
                contact_list.sort(key=lambda x: x.phone_number)
                listbox.delete(0, tk.END)
                for contact in contact_list:
                    listbox.insert(tk.END, contact.print_info())
            except Exception as e:
                messagebox.showerror("Error", f"연락처 파일을 읽는 도중 오류가 발생했습니다: {e}")
    else:
        messagebox.showerror("Error", "저장된 연락처 파일을 찾을 수 없습니다.")

# 두 번째 코드
import datetime

class UserReservationSystem:
    def __init__(self, root, movies_file='movies.txt', reservations_file='reservations.txt', register=False):
        self.root = root
        self.movies_file = movies_file
        self.reservations_file = reservations_file
        self.movies = []
        self.ticket_prices = {
            '성인': 18000,
            '청소년': 15000,
            '어린이': 9000
        }
        self.reservations = {}
        self.current_phone_number = ""
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        self.load_movies()
        self.load_reservations()
        if register:
            self.register_frame()
        else:
            self.login_frame()
    
    def load_movies(self):
        if os.path.exists(self.movies_file):
            with open(self.movies_file, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 4 or len(data) == 5:  # 변경된 부분
                        title = data[0]
                        times = data[1].split(';')
                        theater = data[2]
                        age_limit = data[3]
                        seats = {time: ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6"] for time in times}  # 기본 좌석 목록
                        if len(data) == 5:  # 좌석 정보가 있는 경우
                            seat_data = data[4].split(';')
                            for seat_info in seat_data:
                                time, seats_str = seat_info.split(':')
                                seats[time] = seats_str.split(',')
                        self.movies.append(Movie(title, times, theater, age_limit, seats))
                    else:
                        print(f"Invalid line format: {line.strip()}")

    def save_movies(self):
        with open(self.movies_file, "w", encoding="utf-8") as file:
            for movie in self.movies:
                file.write(f"{movie.to_string()}\n")

    def load_reservations(self):
        if os.path.exists(self.reservations_file):
            with open(self.reservations_file, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split('|')
                    if len(data) == 3:
                        phone_number = data[0]
                        password = data[1]
                        reservations_str = data[2]
                        reservations_list = eval(reservations_str)
                        self.reservations[phone_number] = {"password": password, "reservations": reservations_list}

    def save_reservations(self):
        with open(self.reservations_file, "w", encoding="utf-8") as file:
            for phone_number, info in self.reservations.items():
                password = info["password"]
                reservations_str = repr(info["reservations"])
                file.write(f"{phone_number}|{password}|{reservations_str}\n")

    def login_frame(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="영화 예매 시스템에 오신 것을 환영합니다").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=1, column=0, sticky='e')
        self.phone_entry = ttk.Entry(self.main_frame)
        self.phone_entry.grid(row=1, column=1)

        ttk.Label(self.main_frame, text="비밀번호를 입력하세요:").grid(row=2, column=0, sticky='e')
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        login_button = ttk.Button(self.main_frame, text="로그인", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

        register_button = ttk.Button(self.main_frame, text="회원가입", command=self.register_frame)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)

    def register_frame(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="회원가입").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=1, column=0, sticky='e')
        self.register_phone_entry = ttk.Entry(self.main_frame)
        self.register_phone_entry.grid(row=1, column=1)

        ttk.Label(self.main_frame, text="비밀번호를 입력하세요:").grid(row=2, column=0, sticky='e')
        self.register_password_entry = ttk.Entry(self.main_frame, show="*")
        self.register_password_entry.grid(row=2, column=1)

        ttk.Label(self.main_frame, text="비밀번호를 다시 입력하세요:").grid(row=3, column=0, sticky='e')
        self.register_confirm_password_entry = ttk.Entry(self.main_frame, show="*")
        self.register_confirm_password_entry.grid(row=3, column=1)

        register_button = ttk.Button(self.main_frame, text="가입", command=self.register)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)

    def register(self):
        phone_number = self.register_phone_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.register_confirm_password_entry.get()

        if not re.match(r"010-\d{4}-\d{4}$", phone_number):
            messagebox.showerror("오류", "전화번호 형식이 올바르지 않습니다. 다시 입력하세요.")
            return

        if password != confirm_password:
            messagebox.showerror("오류", "비밀번호가 일치하지 않습니다. 다시 입력하세요.")
            return

        if phone_number in self.reservations:
            messagebox.showerror("오류", "이미 가입된 전화번호입니다.")
            return

        self.reservations[phone_number] = {"password": sha256(password.encode()).hexdigest(), "reservations": []}
        self.save_reservations()
        messagebox.showinfo("가입 완료", "회원가입이 완료되었습니다.")
        self.login_frame()

    def login(self):
        phone_number = self.phone_entry.get()
        password = self.password_entry.get()
        hashed_password = sha256(password.encode()).hexdigest()
        if re.match(r"010-\d{4}-\d{4}$", phone_number):
            if phone_number in self.reservations:  # 회원 목록에 있는 번호인지 확인
                if self.reservations[phone_number]["password"] == hashed_password:
                    self.current_phone_number = phone_number
                    self.main_menu()
                else:
                    messagebox.showerror("오류", "비밀번호가 일치하지 않습니다.")
            else:
                messagebox.showerror("오류", "가입되지 않은 전화번호입니다.")
        else:
            messagebox.showerror("오류", "전화번호 형식이 올바르지 않습니다. 다시 입력하세요.")

    def main_menu(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"{self.current_phone_number}으로 로그인되었습니다.").grid(row=0, column=0, columnspan=2, pady=10)

        reserve_button = ttk.Button(self.main_frame, text="1. 영화 예매", command=self.make_reservation)
        reserve_button.grid(row=1, column=0, columnspan=2, pady=10)

        view_button = ttk.Button(self.main_frame, text="2. 예매 내역 조회", command=self.view_reservations)
        view_button.grid(row=2, column=0, columnspan=2, pady=10)

        logout_button = ttk.Button(self.main_frame, text="3. 로그아웃", command=self.login_frame)
        logout_button.grid(row=3, column=0, columnspan=2, pady=10)

    def make_reservation(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="영화를 선택하세요:").grid(row=0, column=0, columnspan=2, pady=10)

        self.movie_listbox = tk.Listbox(self.main_frame)
        for movie in self.movies:
            self.movie_listbox.insert(tk.END, f"{movie.title} (연령 제한: {movie.age_limit})")
        self.movie_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        select_button = ttk.Button(self.main_frame, text="선택", command=self.select_movie)
        select_button.grid(row=2, column=0, columnspan=2, pady=10)

    def select_movie(self):
        try:
            index = self.movie_listbox.curselection()[0]
            self.selected_movie = self.movies[index]
            self.select_age_groups()
        except IndexError:
            messagebox.showerror("오류", "영화를 선택하세요.")

    def select_age_groups(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="연령대별 인원수를 선택하세요:").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="성인 (19세 이상):").grid(row=1, column=0, pady=5)
        self.adult_spinbox = ttk.Spinbox(self.main_frame, from_=0, to=10)
        self.adult_spinbox.grid(row=1, column=1, pady=5)

        ttk.Label(self.main_frame, text="청소년 (13-18세):").grid(row=2, column=0, pady=5)
        self.teen_spinbox = ttk.Spinbox(self.main_frame, from_=0, to=10)
        self.teen_spinbox.grid(row=2, column=1, pady=5)

        ttk.Label(self.main_frame, text="어린이 (12세 이하):").grid(row=3, column=0, pady=5)
        self.child_spinbox = ttk.Spinbox(self.main_frame, from_=0, to=10)
        self.child_spinbox.grid(row=3, column=1, pady=5)

        next_button = ttk.Button(self.main_frame, text="다음", command=self.check_age_groups)
        next_button.grid(row=4, column=0, columnspan=2, pady=10)

    def check_age_groups(self):
        adults = int(self.adult_spinbox.get())
        teens = int(self.teen_spinbox.get())
        children = int(self.child_spinbox.get())

        if self.selected_movie.age_limit == "ALL":
            self.age_groups = {'성인': adults, '청소년': teens, '어린이': children}
            self.select_date()
        elif self.selected_movie.age_limit == "19세" and teens == 0 and children == 0 and adults > 0:
            self.age_groups = {'성인': adults, '청소년': teens, '어린이': children}
            self.select_date()
        elif self.selected_movie.age_limit == "15세" and children == 0 and (adults > 0 or teens > 0):
            self.age_groups = {'성인': adults, '청소년': teens, '어린이': children}
            self.select_date()
        else:
            messagebox.showerror("오류", f"해당 영화는 {self.selected_movie.age_limit} 관람가입니다. 연령대가 맞지 않습니다.")
            self.main_menu()

    def select_date(self):
        self.clear_frame()
        today = datetime.datetime.today()
        self.selected_date = today.strftime('%Y-%m-%d')
        ttk.Label(self.main_frame, text=f"오늘 날짜로 예약됩니다: {self.selected_date}").grid(row=0, column=0, columnspan=2, pady=10)

        next_button = ttk.Button(self.main_frame, text="다음", command=self.select_time)
        next_button.grid(row=1, column=0, columnspan=2, pady=10)

    def select_time(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"{self.selected_movie.title}의 가능한 상영 시간:").grid(row=0, column=0, columnspan=2, pady=10)

        self.time_listbox = tk.Listbox(self.main_frame)
        for time in self.selected_movie.times:
            self.time_listbox.insert(tk.END, time)
        self.time_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        select_button = ttk.Button(self.main_frame, text="선택", command=self.save_time)
        select_button.grid(row=2, column=0, columnspan=2, pady=10)

    def save_time(self):
        try:
            index = self.time_listbox.curselection()[0]
            self.selected_time = self.selected_movie.times[index]
            self.select_seat()
        except IndexError:
            messagebox.showerror("오류", "상영 시간을 선택하세요.")

    def select_seat(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"{self.selected_movie.title}의 {self.selected_time} 상영 시간의 가능한 좌석:").grid(row=0, column=0, columnspan=6, pady=10)

        ttk.Label(self.main_frame, text="스크린").grid(row=1, column=0, columnspan=6, pady=5)

        self.seat_buttons = []
        for i, seat in enumerate(self.selected_movie.seats[self.selected_time]):
            row = i // 6
            col = i % 6
            seat_button = ttk.Checkbutton(self.main_frame, text=seat, command=lambda s=seat: self.toggle_seat(s))
            seat_button.grid(row=row+2, column=col, padx=5, pady=5)
            self.seat_buttons.append(seat_button)

        self.selected_seats = []
        select_button = ttk.Button(self.main_frame, text="선택 완료", command=self.save_seat)
        select_button.grid(row=8, column=0, columnspan=6, pady=10)

    def toggle_seat(self, seat):
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
        else:
            if len(self.selected_seats) < sum(self.age_groups.values()):
                self.selected_seats.append(seat)
            else:
                messagebox.showerror("오류", "선택한 좌석 수가 인원 수를 초과했습니다.")

    def save_seat(self):
        if len(self.selected_seats) == sum(self.age_groups.values()):
            for seat in self.selected_seats:
                # 좌석 상태를 '■'로 변경
                for time in self.selected_movie.times:
                    if time == self.selected_time:
                        self.selected_movie.seats[time] = [
                            '■' if s == seat else s for s in self.selected_movie.seats[time]
                        ]
            self.confirm_reservation()
        else:
            messagebox.showerror("오류", "선택한 좌석 수가 인원 수와 맞지 않습니다.")

    def confirm_reservation(self):
        self.clear_frame()

        total_cost = (
            self.age_groups['성인'] * self.ticket_prices['성인'] +
            self.age_groups['청소년'] * self.ticket_prices['청소년'] +
            self.age_groups['어린이'] * self.ticket_prices['어린이']
        )

        reservation_info = {
            "영화": self.selected_movie.title,
            "날짜": self.selected_date,
            "시간": self.selected_time,
            "좌석": self.selected_seats,
            "연령대": self.age_groups,
            "총액": total_cost
        }

        self.reservations[self.current_phone_number]["reservations"].append(reservation_info)
        self.save_reservations()

        age_groups_str = ", ".join([f"{k} {v}명" for k, v in self.age_groups.items() if v > 0])
        reservation_details = (
            f"영화: {self.selected_movie.title}\n"
            f"날짜: {self.selected_date}\n"
            f"시간: {self.selected_time}\n"
            f"좌석: {', '.join(self.selected_seats)}\n"
            f"연령대: {age_groups_str}\n"
            f"총액: {total_cost}원"
        )

        ttk.Label(self.main_frame, text="예약 정보:").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.main_frame, text=reservation_details).grid(row=1, column=0, columnspan=2, pady=10)

        pay_card_button = ttk.Button(self.main_frame, text="결제 (카드)", command=lambda: self.complete_payment("카드"))
        pay_card_button.grid(row=2, column=0, pady=10)

        pay_cash_button = ttk.Button(self.main_frame, text="결제 (현금)", command=lambda: self.complete_payment("현금"))
        pay_cash_button.grid(row=2, column=1, pady=10)

        cancel_button = ttk.Button(self.main_frame, text="취소", command=self.cancel_reservation)
        cancel_button.grid(row=3, column=0, columnspan=2, pady=10)

    def complete_payment(self, method):
        self.reservations[self.current_phone_number]["reservations"][-1]["결제 방법"] = method
        self.save_reservations()
        messagebox.showinfo("결제 완료", f"결제가 완료되었습니다! ({method})")
        self.main_menu()

    def cancel_reservation(self):
        self.reservations[self.current_phone_number]["reservations"].pop()
        self.save_reservations()
        messagebox.showinfo("예약 취소", "예약이 취소되었습니다.")
        self.main_menu()

    def view_reservations(self):
        self.clear_frame()
        if not self.reservations[self.current_phone_number]["reservations"]:
            ttk.Label(self.main_frame, text="예매 내역이 없습니다.").grid(row=0, column=0, pady=10)
        else:
            for i, reservation in enumerate(self.reservations[self.current_phone_number]["reservations"]):
                age_groups_str = ", ".join([f"{k} {v}명" for k, v in reservation['연령대'].items() if v > 0])
                reservation_details = (
                    f"{i+1}. 영화: {reservation['영화']}\n"
                    f"날짜: {reservation['날짜']}\n"
                    f"시간: {reservation['시간']}\n"
                    f"좌석: {', '.join(reservation['좌석'])}\n"
                    f"연령대: {age_groups_str}\n"
                    f"총액: {reservation['총액']}원\n"
                    f"결제 방법: {reservation.get('결제 방법', 'N/A')}\n"
                )
                ttk.Label(self.main_frame, text=reservation_details).grid(row=i, column=0, pady=10)

        back_button = ttk.Button(self.main_frame, text="뒤로", command=self.main_menu)
        back_button.grid(row=1, column=0, pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    movies_file = r"C:\Users\LG\Desktop\movies.txt"
    reservations_file = r"C:\Users\LG\Desktop\reservations.txt"
    booking_system = BookingSystem(movies_file)
    contact_list = []
    app = Application(booking_system, contact_list, movies_file, reservations_file)
    app.mainloop()