import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import re

# movie.dir을 설정합니다.
script_dir = os.path.dirname(os.path.abspath(__file__))
movie_dir = os.path.join(script_dir, "direc", "movies.txt")

# Contact 클래스: 연락처 정보를 저장
class Contact:
    def __init__(self, phone_number, password, reservations=None):
        self.phone_number = phone_number
        self.password = password
        self.reservations = reservations if reservations is not None else []

    def print_info(self):
        return f"전화번호: {self.phone_number}, 비밀번호: {self.password}\n"

# Movie 클래스: 영화 정보를 저장
class Movie:
    def __init__(self, title, times, theater, age_limit):
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
        return f"{self.title},{','.join(self.times)},{self.theater},{self.age_limit}"

# BookingSystem 클래스: 영화 예매 시스템의 핵심 로직
class BookingSystem:
    def __init__(self, file_path):
        self.movies = []
        self.file_path = file_path
        self.admin_password = "123"
        self.ticket_prices = {'성인': 10000, '청소년': 8000, '어린이': 5000}  # 가격 정보 추가
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

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.login_frame()

    def login_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.main_frame, text="영화 예매 시스템에 오신 것을 환영합니다").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.main_frame, text="관리자 로그인", command=self.admin_login).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="사용자 로그인", command=self.user_login_frame).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="회원가입", command=self.user_register_frame).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.directory_label = ttk.Label(self.main_frame, text=f"movies.txt 파일은 이 디렉토리에 있습니다: {self.booking_system.file_path}")
        self.directory_label.grid(row=4, column=0, columnspan=2, pady=10)

    def admin_login(self):
        password = simpledialog.askstring("비밀번호", "관리자 비밀번호를 입력하세요:", show='*')
        if password == self.booking_system.admin_password:
            self.admin_panel()
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다")

    def admin_panel(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Button(self.main_frame, text="영화 관리", command=self.manage_movies).grid(row=0, column=0, pady=10)
        ttk.Button(self.main_frame, text="연락처 관리", command=self.contact_management).grid(row=1, column=0, pady=10)
        ttk.Button(self.main_frame, text="로그아웃", command=self.login_frame).grid(row=2, column=0, pady=10)
    
    def manage_movies(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="등록된 영화 목록").grid(row=0, column=0)
        
        self.movies_listbox = tk.Listbox(self.main_frame, width=30, height=20)
        self.movies_listbox.grid(row=1, column=0)
        
        self.update_movie_list()
        
        ttk.Button(self.main_frame, text="영화 추가", command=self.add_movie).grid(row=2, column=0, pady=5)
        ttk.Button(self.main_frame, text="영화 조회", command=self.view_movies).grid(row=3, column=0, pady=5)
        ttk.Button(self.main_frame, text="뒤로", command=self.admin_panel).grid(row=4, column=0, pady=5)

    def update_movie_list(self):
        self.booking_system.sort_movies()
        self.movies_listbox.delete(0, tk.END)
        for movie in self.booking_system.movies:
            self.movies_listbox.insert(tk.END, movie.title)

    
        try:
            index = self.time_listbox.curselection()[0]
            self.selected_time = self.time_listbox.get(index).strip()
            print(f"Selected time: {self.selected_time}")  # 디버깅을 위해 추가
            print(f"Available times: {list(self.selected_movie.seats.keys())}")  # 디버깅을 위해 추가
            self.select_seat()
        except IndexError:
            messagebox.showerror("오류", "상영 시간을 선택하세요.")

    def add_movie(self):
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        new_theater = simpledialog.askstring("영화 추가", "새 영화 상
