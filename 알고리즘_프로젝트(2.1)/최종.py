import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
                file.write(f"{movie.title},{','.join(movie.times)},{movie.theater},{movie.age_limit}\n")

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
    def __init__(self, booking_system, contact_list, movies_file, reservations_file):
        super().__init__()
        self.booking_system = booking_system
        self.contact_list = contact_list
        self.movies_file = movies_file
        self.reservations_file = reservations_file
        self.title("영화 예매 및 연락처 관리 시스템")

        self.admin_login_button = tk.Button(self, text="관리자 로그인", command=self.admin_login)
        self.admin_login_button.pack(pady=10)

        self.user_login_button = tk.Button(self, text="사용자 로그인", command=self.user_login_frame)
        self.user_login_button.pack(pady=10)

        self.user_register_button = tk.Button(self, text="회원가입", command=self.user_register_frame)
        self.user_register_button.pack(pady=10)

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

        self.contact_listbox = tk.Listbox(listbox_frame, width=60, height=10)
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
        phone_number = simpledialog.askstring("Input", "삭제할 전화번호:")
        if phone_number:
            delete_contact(self.contact_list, phone_number)
            self.refresh_listbox(self.contact_listbox)

    def on_search_contact(self):
        phone_number = simpledialog.askstring("Input", "검색할 전화번호:")
        if phone_number:
            search_contact(self.contact_list, phone_number, self.contact_listbox)

    def on_update_contact(self):
        phone_number = simpledialog.askstring("Input", "수정할 전화번호:")
        if phone_number:
            new_password = simpledialog.askstring("Input", "새로운 비밀번호:")
            if new_password:
                update_contact(self.contact_list, phone_number, new_password)
                self.refresh_listbox(self.contact_listbox)

    def refresh_listbox(self, listbox):
        listbox.delete(0, tk.END)
        for contact in self.contact_list:
            listbox.insert(tk.END, contact.print_info())

    def on_exit(self):
        save_contacts(self.contact_list, self.reservations_file)
        self.destroy()

    def on_home(self):
        self.refresh_listbox(self.contact_listbox)

    def load_contacts(self):
        load_contacts(self.contact_list, self.contact_listbox, self.reservations_file)

    def user_login_frame(self):
        self.clear_frame()
        ttk.Label(self, text="사용자 로그인").pack(pady=10)
        
        ttk.Label(self, text="전화번호를 입력하세요 (예: 010-1234-5678):").pack()
        self.user_phone_entry = ttk.Entry(self)
        self.user_phone_entry.pack(pady=5)
        
        ttk.Label(self, text="비밀번호를 입력하세요:").pack()
        self.user_password_entry = ttk.Entry(self, show="*")
        self.user_password_entry.pack(pady=5)
        
        login_button = ttk.Button(self, text="로그인", command=self.login_user)
        login_button.pack(pady=10)
        
        back_button = ttk.Button(self, text="뒤로", command=self.main_frame)
        back_button.pack(pady=5)

    def user_register_frame(self):
        self.clear_frame()
        ttk.Label(self, text="회원가입").pack(pady=10)
        
        ttk.Label(self, text="전화번호를 입력하세요 (예: 010-1234-5678):").pack()
        self.register_phone_entry = ttk.Entry(self)
        self.register_phone_entry.pack(pady=5)
        
        ttk.Label(self, text="비밀번호를 입력하세요:").pack()
        self.register_password_entry = ttk.Entry(self, show="*")
        self.register_password_entry.pack(pady=5)
        
        ttk.Label(self, text="비밀번호를 다시 입력하세요:").pack()
        self.register_confirm_password_entry = ttk.Entry(self, show="*")
        self.register_confirm_password_entry.pack(pady=5)
        
        register_button = ttk.Button(self, text="가입", command=self.register_user)
        register_button.pack(pady=10)
        
        back_button = ttk.Button(self, text="뒤로", command=self.main_frame)
        back_button.pack(pady=5)

    def register_user(self):
        phone_number = self.register_phone_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.register_confirm_password_entry.get()
        
        if not re.match(r"010-\d{4}-\d{4}$", phone_number):
            messagebox.showerror("오류", "전화번호 형식이 올바르지 않습니다. 다시 입력하세요.")
            return
        
        if password != confirm_password:
            messagebox.showerror("오류", "비밀번호가 일치하지 않습니다. 다시 입력하세요.")
            return
        
        for contact in self.contact_list:
            if contact.phone_number == phone_number:
                messagebox.showerror("오류", "이미 가입된 전화번호입니다.")
                return
        
        self.contact_list.append(Contact(phone_number, password))
        save_contacts(self.contact_list, self.reservations_file)
        messagebox.showinfo("가입 완료", "회원가입이 완료되었습니다.")
        self.main_frame()

    def login_user(self):
        phone_number = self.user_phone_entry.get()
        password = self.user_password_entry.get()
        
        for contact in self.contact_list:
            if contact.phone_number == phone_number and contact.password == password:
                self.user = contact
                self.user_reservation_system()
                return
        
        messagebox.showerror("오류", "전화번호 또는 비밀번호가 일치하지 않습니다.")

    def user_reservation_system(self):
        self.clear_frame()
        UserReservationSystem(self, self.movies_file, self.reservations_file, self.user)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def main_frame(self):
        self.clear_frame()
        self.admin_login_button.pack(pady=10)
        self.user_login_button.pack(pady=10)
        self.user_register_button.pack(pady=10)
        self.directory_label.pack(pady=10)

# UserReservationSystem 클래스: 사용자 영화 예매 시스템
class UserReservationSystem:
    def __init__(self, root, movies_file, reservations_file, user):
        self.root = root
        self.movies_file = movies_file
        self.reservations_file = reservations_file
        self.movies = []
        self.ticket_prices = {
            '성인': 18000,
            '청소년': 15000,
            '어린이': 9000
        }
        self.user = user
        self.load_movies()
        self.main_menu()
    
    def load_movies(self):
        if os.path.exists(self.movies_file):
            with open(self.movies_file, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 4:
                        title = data[0]
                        times = data[1].split(';')
                        theater = data[2]
                        age_limit = data[3]
                        self.movies.append(Movie(title, times, theater, age_limit))
                    else:
                        print(f"Invalid line format: {line.strip()}")

    def main_menu(self):
        self.root.clear_frame()
        ttk.Label(self.root, text=f"{self.user.phone_number}으로 로그인되었습니다.").pack(pady=10)
        
        reserve_button = ttk.Button(self.root, text="1. 영화 예매", command=self.make_reservation)
        reserve_button.pack(pady=10)
        
        view_button = ttk.Button(self.root, text="2. 예매 내역 조회", command=self.view_reservations)
        view_button.pack(pady=10)
        
        logout_button = ttk.Button(self.root, text="3. 로그아웃", command=self.root.main_frame)
        logout_button.pack(pady=10)

    def make_reservation(self):
        self.root.clear_frame()
        ttk.Label(self.root, text="영화를 선택하세요:").pack(pady=10)
        
        self.movie_listbox = tk.Listbox(self.root)
        for movie in self.movies:
            self.movie_listbox.insert(tk.END, f"{movie.title} (연령 제한: {movie.age_limit})")
        self.movie_listbox.pack(pady=10)
        
        select_button = ttk.Button(self.root, text="선택", command=self.select_movie)
        select_button.pack(pady=10)
    
    def select_movie(self):
        try:
            index = self.movie_listbox.curselection()[0]
            self.selected_movie = self.movies[index]
            self.select_age_groups()
        except IndexError:
            messagebox.showerror("오류", "영화를 선택하세요.")
    
    def select_age_groups(self):
        self.root.clear_frame()
        ttk.Label(self.root, text="연령대별 인원수를 선택하세요:").pack(pady=10)
        
        ttk.Label(self.root, text="성인 (19세 이상):").pack()
        self.adult_spinbox = ttk.Spinbox(self.root, from_=0, to=10)
        self.adult_spinbox.pack(pady=5)
        
        ttk.Label(self.root, text="청소년 (13-18세):").pack()
        self.teen_spinbox = ttk.Spinbox(self.root, from_=0, to=10)
        self.teen_spinbox.pack(pady=5)
        
        ttk.Label(self.root, text="어린이 (12세 이하):").pack()
        self.child_spinbox = ttk.Spinbox(self.root, from_=0, to=10)
        self.child_spinbox.pack(pady=5)
        
        next_button = ttk.Button(self.root, text="다음", command=self.check_age_groups)
        next_button.pack(pady=10)
    
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
            self.main_menu()
    
    def select_date(self):
        self.root.clear_frame()
        today = datetime.datetime.today()
        self.selected_date = today.strftime('%Y-%m-%d')
        ttk.Label(self.root, text=f"오늘 날짜로 예약됩니다: {self.selected_date}").pack(pady=10)
        
        next_button = ttk.Button(self.root, text="다음", command=self.select_time)
        next_button.pack(pady=10)
    
    def select_time(self):
        self.root.clear_frame()
        ttk.Label(self.root, text=f"{self.selected_movie.title}의 가능한 상영 시간:").pack(pady=10)
        
        self.time_listbox = tk.Listbox(self.root)
        for time in self.selected_movie.times:
            self.time_listbox.insert(tk.END, time)
        self.time_listbox.pack(pady=10)
        
        select_button = ttk.Button(self.root, text="선택", command=self.save_time)
        select_button.pack(pady=10)
    
    def save_time(self):
        try:
            index = self.time_listbox.curselection()[0]
            self.selected_time = self.selected_movie.times[index]
            self.select_seat()
        except IndexError:
            messagebox.showerror("오류", "상영 시간을 선택하세요.")
    
    def select_seat(self):
        self.root.clear_frame()
        ttk.Label(self.root, text=f"{self.selected_movie.title}의 {self.selected_time} 상영 시간의 가능한 좌석:").pack(pady=10)
        
        ttk.Label(self.root, text="스크린").pack(pady=5)

        self.seat_buttons = []
        self.selected_seats = []

        seat_frame = ttk.Frame(self.root)
        seat_frame.pack(pady=10)

        for i, seat in enumerate(self.selected_movie.seats[self.selected_time]):
            row = i // 6
            col = i % 6
            seat_button = ttk.Checkbutton(seat_frame, text=seat, command=lambda s=seat: self.toggle_seat(s))
            seat_button.grid(row=row, column=col, padx=5, pady=5)
            self.seat_buttons.append(seat_button)
        
        select_button = ttk.Button(self.root, text="선택 완료", command=self.save_seat)
        select_button.pack(pady=10)
    
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
                index = self.selected_movie.seats[self.selected_time].index(seat)
                self.selected_movie.seats[self.selected_time][index] = '■'
            self.confirm_reservation()
        else:
            messagebox.showerror("오류", "선택한 좌석 수가 인원 수와 맞지 않습니다.")
    
    def confirm_reservation(self):
        self.root.clear_frame()
        
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
        
        self.user.reservations.append(reservation_info)
        save_contacts(self.root.contact_list, self.reservations_file)
        
        age_groups_str = ", ".join([f"{k} {v}명" for k, v in self.age_groups.items() if v > 0])
        reservation_details = (
            f"영화: {self.selected_movie.title}\n"
            f"날짜: {self.selected_date}\n"
            f"시간: {self.selected_time}\n"
            f"좌석: {', '.join(self.selected_seats)}\n"
            f"연령대: {age_groups_str}\n"
            f"총액: {total_cost}원"
        )
        
        ttk.Label(self.root, text="예약 정보:").pack(pady=10)
        ttk.Label(self.root, text=reservation_details).pack(pady=10)
        
        pay_card_button = ttk.Button(self.root, text="결제 (카드)", command=lambda: self.complete_payment("카드"))
        pay_card_button.pack(pady=5)
        
        pay_cash_button = ttk.Button(self.root, text="결제 (현금)", command=lambda: self.complete_payment("현금"))
        pay_cash_button.pack(pady=5)
        
        cancel_button = ttk.Button(self.root, text="취소", command=self.cancel_reservation)
        cancel_button.pack(pady=10)
    
    def complete_payment(self, method):
        self.user.reservations[-1]["결제 방법"] = method
        save_contacts(self.root.contact_list, self.reservations_file)
        messagebox.showinfo("결제 완료", f"결제가 완료되었습니다! ({method})")
        self.main_menu()
    
    def cancel_reservation(self):
        self.user.reservations.pop()
        save_contacts(self.root.contact_list, self.reservations_file)
        messagebox.showinfo("예약 취소", "예약이 취소되었습니다.")
        self.main_menu()
    
    def view_reservations(self):
        self.root.clear_frame()
        if not self.user.reservations:
            ttk.Label(self.root, text="예매 내역이 없습니다.").pack(pady=10)
        else:
            for i, reservation in enumerate(self.user.reservations):
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
                ttk.Label(self.root, text=reservation_details).pack(pady=10)
        
        back_button = ttk.Button(self.root, text="뒤로", command=self.main_menu)
        back_button.pack(pady=10)

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
            contact.password = new_password
            messagebox.showinfo("Updated", f"[수정] 전화번호: {phone_number}, 새로운 비밀번호: {new_password}")
            return
    messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

def save_contacts(contact_list, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for contact in contact_list:
            reservations = str(contact.reservations)
            file.write(f"{contact.phone_number}|{contact.password}|{reservations}\n")

def load_contacts(contact_list, listbox, filename):
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
                        reservations = eval(parts[2])  # eval 사용 주의
                        contact_list.append(Contact(phone_number, password, reservations))
                contact_list.sort(key=lambda x: x.phone_number)
                listbox.delete(0, tk.END)
                for contact in contact_list:
                    listbox.insert(tk.END, contact.print_info())
            except Exception as e:
                messagebox.showerror("Error", f"연락처 파일을 읽는 도중 오류가 발생했습니다: {e}")
    else:
        messagebox.showerror("Error", "저장된 연락처 파일을 찾을 수 없습니다.")

# 프로그램 실행
file_path = r"C:\Users\LG\Desktop\movies.txt"
reservations_file = r"C:\Users\LG\Desktop\reservations.txt"
booking_system = BookingSystem(file_path)
contact_list = []
load_contacts(contact_list, tk.Listbox(), reservations_file)
app = Application(booking_system, contact_list, file_path, reservations_file)
app.mainloop()
