import os
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re

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

class ReservationSystem:
    def __init__(self, root, movies_file='movies.txt', reservations_file='reservations.txt'):
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
        self.login_frame()
    
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
    
    def save_movies(self):
        with open(self.movies_file, "w", encoding="utf-8") as file:
            for movie in self.movies:
                times = ';'.join(movie.times)
                file.write(f"{movie.title},{times},{movie.theater},{movie.age_limit}\n")
    
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
        
        self.reservations[phone_number] = {"password": password, "reservations": []}
        self.save_reservations()
        messagebox.showinfo("가입 완료", "회원가입이 완료되었습니다.")
        self.login_frame()
    
    def login(self):
        phone_number = self.phone_entry.get()
        password = self.password_entry.get()
        if re.match(r"010-\d{4}-\d{4}$", phone_number):
            if phone_number in self.reservations:  # 회원 목록에 있는 번호인지 확인
                if self.reservations[phone_number]["password"] == password:
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
                index = self.selected_movie.seats[self.selected_time].index(seat)
                self.selected_movie.seats[self.selected_time][index] = '■'
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
    root = tk.Tk()
    root.title("영화 예매 시스템")
    movies_file = r"C:\Users\LG\Desktop\movies.txt"
    reservations_file = r"C:\Users\LG\Desktop\reservations.txt"
    system = ReservationSystem(root, movies_file, reservations_file)
    root.mainloop()
