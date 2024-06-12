import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import re

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
        self.times = [time.strip() for time_slot in times for time in time_slot.split(';') if time.strip()]
        self.theater = theater
        self.age_limit = age_limit
        self.seats = {time: [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
            'E1', 'E2', 'E3', 'E4', 'E5', 'E6',
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6'
        ] for time in self.times}

    def to_string(self):
        return f"{self.title},{';'.join(self.times)},{self.theater},{self.age_limit}"

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
        # 삽입 정렬 알고리즘으로 영화 목록 정렬
        for i in range(1, len(self.movies)):
            key_movie = self.movies[i]
            j = i - 1
            while j >= 0 and key_movie.title < self.movies[j].title:
                self.movies[j + 1] = self.movies[j]
                j -= 1
            self.movies[j + 1] = key_movie

    def display_movies(self):
        movies_list = ""
        for idx, movie in enumerate(self.movies):
            movies_list += f"{idx + 1}. {movie.title} ({movie.age_limit})\n"
        return movies_list

    def linear_search_movie_by_name(self, name):
        # 선형 검색 알고리즘을 사용하여 영화 제목으로 영화 검색
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

    def confirm_time_selection(self):
        if not self.time_listbox.curselection():
            return
        try:
            index = self.time_listbox.curselection()[0]
            self.selected_time = self.time_listbox.get(index).strip()
            self.select_seat()
        except IndexError:
            messagebox.showerror("오류", "상영 시간을 선택하세요.")

    def add_movie(self):
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        new_theater = simpledialog.askstring("영화 추가", "새 영화 상영관을 입력하세요:")
        new_age_limit = simpledialog.askstring("영화 추가", "새 영화 연령 제한을 입력하세요:")
        new_movie = Movie(new_title, new_times, new_theater, new_age_limit)
        self.booking_system.movies.append(new_movie)
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
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        listbox_frame = ttk.Frame(self.main_frame)
        listbox_frame.grid(row=0, column=0, padx=10, pady=10)

        self.contact_listbox = tk.Listbox(listbox_frame, width=60, height=10)  # 넓이를 더 넓게 설정
        self.contact_listbox.grid(row=0, column=0, padx=(0, 10))

        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(button_frame, text="검색", command=self.on_search_contact).grid(row=0, column=0, pady=5)
        ttk.Button(button_frame, text="추가", command=self.on_add_contact).grid(row=1, column=0, pady=5)
        ttk.Button(button_frame, text="삭제", command=self.on_delete_contact).grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="수정", command=self.on_update_contact).grid(row=3, column=0, pady=5)
        ttk.Button(button_frame, text="뒤로", command=self.admin_panel).grid(row=5, column=0, pady=5)

        self.load_contacts()

    def on_add_contact(self):
        contact = self.set_contact()
        if contact:
            self.contact_list.append(contact)
            self.refresh_listbox(self.contact_listbox)

    def on_delete_contact(self):
        phone_number = simpledialog.askstring("Input", "삭제할 전화번호:")
        if phone_number:
            self.delete_contact(phone_number)
            self.refresh_listbox(self.contact_listbox)

    def on_search_contact(self):
        phone_number = simpledialog.askstring("Input", "검색할 전화번호:")
        if phone_number:
            self.search_contact(phone_number)

    def on_update_contact(self):
        phone_number = simpledialog.askstring("Input", "수정할 전화번호:")
        if phone_number:
            new_password = simpledialog.askstring("Input", "새로운 비밀번호:")
            if new_password:
                self.update_contact(phone_number, new_password)
                self.refresh_listbox(self.contact_listbox)

    def refresh_listbox(self, listbox):
        listbox.delete(0, tk.END)
        for contact in self.contact_list:
            listbox.insert(tk.END, contact.print_info())

    def on_home(self):
        self.refresh_listbox(self.contact_listbox)

    def load_contacts(self):
        self.load_contacts_from_file()
        self.refresh_listbox(self.contact_listbox)

    def user_login_frame(self):# 사용자 로그인창
        for widget in self.main_frame.winfo_children():# 기존 위젯 제거
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=0, column=0, sticky='e')
        self.phone_entry = ttk.Entry(self.main_frame)
        self.phone_entry.grid(row=0, column=1)
        
        ttk.Label(self.main_frame, text="비밀번호를 입력하세요:").grid(row=1, column=0, sticky='e')
        self.password_entry = ttk.Entry(self.main_frame, show="*") # 비밀번호는 * 표시 
        self.password_entry.grid(row=1, column=1)
        
        ttk.Button(self.main_frame, text="로그인", command=self.user_login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="뒤로", command=self.login_frame).grid(row=3, column=0, columnspan=2, pady=10)

    def user_register_frame(self): # 사용자 회원가입
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=0, column=0, sticky='e')
        self.register_phone_entry = ttk.Entry(self.main_frame)
        self.register_phone_entry.grid(row=0, column=1)
        
        ttk.Label(self.main_frame, text="비밀번호를 입력하세요:").grid(row=1, column=0, sticky='e')
        self.register_password_entry = ttk.Entry(self.main_frame, show="*") # 비밀번호는 * 표시 
        self.register_password_entry.grid(row=1, column=1)
        
        ttk.Label(self.main_frame, text="비밀번호를 다시 입력하세요:").grid(row=2, column=0, sticky='e')
        self.register_confirm_password_entry = ttk.Entry(self.main_frame, show="*")
        self.register_confirm_password_entry.grid(row=2, column=1) # register 넘어가서 비밀번호 검사함
        
        ttk.Button(self.main_frame, text="가입", command=self.user_register).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="뒤로", command=self.login_frame).grid(row=4, column=0, columnspan=2, pady=10)

    def user_register(self):
        phone_number = self.register_phone_entry.get() # 입력한 핸드폰 번호
        password = self.register_password_entry.get() # 입력한 비밀번호 
        confirm_password = self.register_confirm_password_entry.get()
        
        if not re.match(r"010-\d{4}-\d{4}$", phone_number):
            messagebox.showerror("오류", "전화번호 형식이 올바르지 않습니다. 다시 입력하세요.")
            return
        
        if password != confirm_password:
            messagebox.showerror("오류", "비밀번호가 일치하지 않습니다. 다시 입력하세요.")
            return
        
        if phone_number in [contact.phone_number for contact in self.contact_list]: #contact에 있는 번호 검사
            messagebox.showerror("오류", "이미 가입된 전화번호입니다.")
            return
        
        new_contact = Contact(phone_number, password)
        self.contact_list.append(new_contact)
        self.save_contacts_to_file() # 영화 예약 정보 저장파일
        messagebox.showinfo("가입 완료", "회원가입이 완료되었습니다.")
        self.login_frame()

    def user_login(self):
        phone_number = self.phone_entry.get()
        password = self.password_entry.get()
        
        for contact in self.contact_list: 
            if contact.phone_number == phone_number and contact.password == password: # 전화번호와 비밀번호가 일치하면 로그인
                self.current_user = contact
                self.user_main_menu()
                return
        messagebox.showerror("오류", "전화번호 또는 비밀번호가 올바르지 않습니다.")
        
    def user_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text=f"{self.current_user.phone_number}으로 로그인되었습니다.").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.main_frame, text="영화 예매", command=self.make_reservation).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="예매 내역 조회", command=self.view_reservations).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="로그아웃", command=self.login_frame).grid(row=3, column=0, columnspan=2, pady=10)

    def make_reservation(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="영화를 선택하세요:").grid(row=0, column=0, columnspan=2, pady=10)
        
        self.movie_listbox = tk.Listbox(self.main_frame)
        for movie in self.booking_system.movies:
            self.movie_listbox.insert(tk.END, f"{movie.title} (연령 제한: {movie.age_limit})")
        self.movie_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.main_frame, text="선택", command=self.select_movie_for_reservation).grid(row=2, column=0, columnspan=2, pady=10)
        
    def select_movie_for_reservation(self):
        try:
            index = self.movie_listbox.curselection()[0]
            self.selected_movie = self.booking_system.movies[index]
            self.select_age_groups()
        except IndexError:
            messagebox.showerror("오류", "영화를 선택하세요.")
    
    def select_age_groups(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
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
        
        ttk.Button(self.main_frame, text="다음", command=self.check_age_groups).grid(row=4, column=0, columnspan=2, pady=10)

    def check_age_groups(self):
        adults = int(self.adult_spinbox.get())
        teens = int(self.teen_spinbox.get())
        children = int(self.child_spinbox.get())
        
        if self.selected_movie.age_limit == "ALL" or self.selected_movie.age_limit == "Unknown Age":
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
            self.user_main_menu()

    def select_date(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        today = datetime.datetime.today()
        self.selected_date = today.strftime('%Y-%m-%d')
        ttk.Label(self.main_frame, text=f"오늘 날짜로 예약됩니다: {self.selected_date}").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.main_frame, text="다음", command=self.select_time).grid(row=1, column=0, columnspan=2, pady=10)
    
    def select_time(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.main_frame, text=f"{self.selected_movie.title}의 가능한 상영 시간:").grid(row=0, column=0, columnspan=2, pady=10)

        self.time_listbox = tk.Listbox(self.main_frame) # 상영시간 저장됨 
        self.available_times = self.selected_movie.times
        for time in self.available_times:
            self.time_listbox.insert(tk.END, time)
        self.time_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="확인", command=self.confirm_time_selection).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="뒤로", command=self.select_age_groups).grid(row=3, column=0, columnspan=2, pady=10)

        if not self.time_listbox.curselection():
                return
        try:
            index = self.time_listbox.curselection()[0]
            self.selected_time = self.time_listbox.get(index).strip()
            self.select_seat()
        except IndexError:
            messagebox.showerror("오류", "상영 시간을 선택하세요.")
     
    def select_seat(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.main_frame, text=f"{self.selected_movie.title}의 {self.selected_time} 상영 시간의 가능한 좌석:").grid(row=0, column=0, columnspan=6, pady=10)
        ttk.Label(self.main_frame, text="스크린").grid(row=1, column=0, columnspan=6, pady=5)

        self.seat_buttons = []
        self.selected_seats = []
        try:
            selected_time_key = self.selected_time
            for i, seat in enumerate(self.selected_movie.seats[selected_time_key]):
                row = i // 6
                col = i % 6
                seat_button = ttk.Checkbutton(self.main_frame, text=seat, command=lambda s=seat: self.toggle_seat(s))
                seat_button.grid(row=row+2, column=col, padx=5, pady=5)
                self.seat_buttons.append(seat_button)
        except KeyError as e:
            print(e)

        self.selected_seats = []
        ttk.Button(self.main_frame, text="선택 완료", command=self.save_seat).grid(row=8, column=0, columnspan=6, pady=10)
        ttk.Button(self.main_frame, text="뒤로", command=self.select_time).grid(row=9, column=0, columnspan=6, pady=10)

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
            selected_time_key = None
            for time_key in self.selected_movie.seats.keys():
                if self.selected_time in time_key.split(';'):
                    selected_time_key = time_key
                    break

            if selected_time_key is None:
                messagebox.showerror("오류", "선택된 시간에 대한 좌석 정보를 찾을 수 없습니다.")
                return

            for seat in self.selected_seats:
                index = self.selected_movie.seats[selected_time_key].index(seat)
                self.selected_movie.seats[selected_time_key][index] = '■'
            self.confirm_reservation()
        else:
            messagebox.showerror("오류", "선택한 좌석 수가 인원 수와 맞지 않습니다.")

    
    def confirm_reservation(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        total_cost = (
            self.age_groups['성인'] * self.booking_system.ticket_prices['성인'] +
            self.age_groups['청소년'] * self.booking_system.ticket_prices['청소년'] +
            self.age_groups['어린이'] * self.booking_system.ticket_prices['어린이']
        )

        reservation_info = {
            "영화": self.selected_movie.title,
            "날짜": self.selected_date,
            "시간": self.selected_time,
            "좌석": self.selected_seats,
            "연령대": self.age_groups,
            "총액": total_cost
        }

        self.current_user.reservations.append(reservation_info)
        self.save_contacts_to_file()

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

        ttk.Button(self.main_frame, text="결제 (카드)", command=lambda: self.complete_payment("카드")).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="결제 (현금)", command=lambda: self.complete_payment("현금")).grid(row=2, column=1, pady=10)
        ttk.Button(self.main_frame, text="취소", command=self.cancel_reservation).grid(row=3, column=0, columnspan=2, pady=10)
    
    def complete_payment(self, method):
        self.current_user.reservations[-1]["결제 방법"] = method
        self.save_contacts_to_file()
        messagebox.showinfo("결제 완료", f"결제가 완료되었습니다! ({method})")
        self.user_main_menu()
    
    def cancel_reservation(self):
        self.current_user.reservations.pop()
        self.save_contacts_to_file()
        messagebox.showinfo("예약 취소", "예약이 취소되었습니다.")
        self.user_main_menu()
    
    def view_reservations(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
    
        if not self.current_user.reservations:
            ttk.Label(self.main_frame, text="예매 내역이 없습니다.").grid(row=0, column=0, pady=10)
        else:
            self.current_user.reservations = self.selection_sort(self.current_user.reservations, key='영화')
            for i, reservation in enumerate(self.current_user.reservations):
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
    
        ttk.Button(self.main_frame, text="뒤로", command=self.user_main_menu).grid(row=i+1, column=0, pady=10)

    def quicksort(self, reservations):
        if len(reservations) <= 1:
            return reservations
        else:
            pivot = reservations[len(reservations) // 2]
            less = [x for x in reservations if x["날짜"] < pivot["날짜"]]
            equal = [x for x in reservations if x["날짜"] == pivot["날짜"]]
            greater = [x for x in reservations if x["날짜"] > pivot["날짜"]]
            return self.quicksort(less) + equal + self.quicksort(greater)

    def view_reservations(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        reservations = self.current_user.reservations
        reservations = self.quicksort(reservations)

        if not reservations:
            ttk.Label(self.main_frame, text="예매 내역이 없습니다.").grid(row=0, column=0, pady=10)
        else:
            for i, reservation in enumerate(reservations):
                reservation_details = (
                    f"{i+1}. 영화: {reservation['영화']}\n"
                    f"날짜: {reservation['날짜']}\n"
                    f"시간: {reservation['시간']}\n"
                    f"좌석: {', '.join(reservation['좌석'])}\n"
                    f"결제 방법: {reservation['결제 방법']}"
                )
                ttk.Label(self.main_frame, text=reservation_details).grid(row=i, column=0, pady=10)

        ttk.Button(self.main_frame, text="뒤로", command=self.user_main_menu).grid(row=len(reservations) + 1, column=0, pady=10)


    # 연락처 관리 함수들
    def set_contact(self): # 전화번호, 비밀번호 저장(추가)
        phone_number = simpledialog.askstring("Input", "전화번호:")
        password = simpledialog.askstring("Input", "비밀번호:")
        if phone_number and password: #
            for contact in self.contact_list:
                if contact.phone_number == phone_number: # 기존 전화번호와 new전화번호 비교
                    messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                    return None
            return Contact(phone_number, password)
        return None

    def delete_contact(self, phone_number):# 관리자(사용자의 전화번호 삭제)
        for i, contact in enumerate(self.contact_list):
            if contact.phone_number == phone_number:
                del self.contact_list[i]
                messagebox.showinfo("Deleted", f"[삭제] 전화번호: {phone_number}")
                return
        messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {phone_number}")

    def search_contact(self, phone_number): #관리자(사용자의 전화번호 검색)
        found_contacts = sorted([contact for contact in self.contact_list if phone_number in contact.phone_number], key=lambda x: x.phone_number)
        self.contact_listbox.delete(0, tk.END)
        for contact in found_contacts:
            self.contact_listbox.insert(tk.END, contact.print_info())

    def update_contact(self, phone_number, new_password): # 관리자(사용자의 전화번호, 비밀번호 수정)
        for contact in self.contact_list:
            if contact.phone_number == phone_number:
                contact.password = new_password
                messagebox.showinfo("Updated", f"[수정] 전화번호: {phone_number}, 새로운 비밀번호: {new_password}")
                return
        messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

    def save_contacts_to_file(self, filename=r"C:\Users\LG\Desktop\reservations.txt"):# 회원 정보를 파일에 저장
        with open(filename, "w", encoding="utf-8") as file:
            for contact in self.contact_list:
                reservations = repr(contact.reservations)
                file.write(f"{contact.phone_number}|{contact.password}|{reservations}\n")

    def load_contacts_from_file(self, filename=r"C:\Users\LG\Desktop\reservations.txt"):# 파일에서 저장된 회원 정보 불러오기 
        if os.path.exists(filename): # 파일이 존재하는지 확인
            with open(filename, "r", encoding="utf-8") as file: #존재하면 파일을 열어서 정보를 불러옴
                lines = file.readlines()
                self.contact_list.clear() #회원정보 변환후 contact_list에 추가
                for line in lines:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        phone_number = parts[0]
                        password = parts[1]
                        reservations = eval(parts[2])
                        self.contact_list.append(Contact(phone_number, password, reservations)) 
                        # contact_list를 전화번호 순으로 정렬
                self.contact_list.sort(key=lambda x: x.phone_number)
        else:
            messagebox.showerror("Error", "저장된 연락처 파일을 찾을 수 없습니다.")

# 프로그램 실행
file_path = r"C:\Users\LG\Desktop\movies.txt"
contact_list = []
booking_system = BookingSystem(file_path)
app = Application(booking_system, contact_list)
app.mainloop()
