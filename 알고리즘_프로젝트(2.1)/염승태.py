import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re

class Movie:
    def __init__(self, title, times, age_limit):
        self.title = title
        self.times = times
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
    def __init__(self, root):
        self.root = root
        self.movies = [
            Movie("범죄도시 4", ["10:00", "11:00", "11:20", "16:00", "19:00", "20:15"], 19),
            Movie("귀멸의 칼날", ["11:00", "14:00", "17:00", "19:07", "20:00"], 15),
            Movie("보라", ["12:00", "15:00", "16:00", "18:20", "20:00", "21:00", "22:00"], 12),
            Movie("영화 4", ["13:30", "14:30", "15:30", "16:00", "17:00", "19:00", "20:30"], 12),
            Movie("영화 5", ["12:00", "13:30", "14:20", "16:00", "19:00", "20:05"], 12)
        ]
        self.ticket_prices = {
            '성인': 18000,
            '청소년': 15000,
            '어린이': 9000
        }
        self.reservations = {}
        self.current_phone_number = ""
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.login_frame()
    
    def login_frame(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="영화 예매 시스템에 오신 것을 환영합니다").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=1, column=0, sticky='e')
        self.phone_entry = ttk.Entry(self.main_frame)
        self.phone_entry.grid(row=1, column=1)
        
        login_button = ttk.Button(self.main_frame, text="로그인", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def login(self):
        phone_number = self.phone_entry.get()
        if re.match(r"010-\d{4}-\d{4}$", phone_number):
            self.current_phone_number = phone_number
            if phone_number not in self.reservations:
                self.reservations[phone_number] = []
            self.main_menu()
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
            self.movie_listbox.insert(tk.END, f"{movie.title} (연령 제한: {movie.age_limit}세 이상)")
        self.movie_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        
        select_button = ttk.Button(self.main_frame, text="선택", command=self.select_movie)
        select_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def select_movie(self):
        try:
            index = self.movie_listbox.curselection()[0]
            self.selected_movie = self.movies[index]
            self.select_num_people()
        except IndexError:
            messagebox.showerror("오류", "영화를 선택하세요.")
    
    def select_num_people(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="인원을 선택하세요 (1~5명):").grid(row=0, column=0, pady=10)
        
        self.num_people_spinbox = ttk.Spinbox(self.main_frame, from_=1, to=5)
        self.num_people_spinbox.grid(row=0, column=1)
        
        next_button = ttk.Button(self.main_frame, text="다음", command=self.enter_ages)
        next_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    def enter_ages(self):
        self.num_people = int(self.num_people_spinbox.get())
        self.clear_frame()
        self.age_entries = []
        
        for i in range(self.num_people):
            ttk.Label(self.main_frame, text=f"인원 {i+1}의 나이:").grid(row=i, column=0, pady=5)
            age_entry = ttk.Entry(self.main_frame)
            age_entry.grid(row=i, column=1, pady=5)
            self.age_entries.append(age_entry)
        
        next_button = ttk.Button(self.main_frame, text="다음", command=self.check_ages)
        next_button.grid(row=self.num_people, column=0, columnspan=2, pady=10)
    
    def check_ages(self):
        try:
            self.ages = [int(entry.get()) for entry in self.age_entries]
            if all(age >= self.selected_movie.age_limit for age in self.ages):
                self.select_date()
            else:
                messagebox.showerror("오류", f"해당 영화는 {self.selected_movie.age_limit}세 이상만 관람할 수 있습니다.")
        except ValueError:
            messagebox.showerror("오류", "모든 나이를 올바르게 입력하세요.")
    
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
            if len(self.selected_seats) < self.num_people:
                self.selected_seats.append(seat)
            else:
                messagebox.showerror("오류", "선택한 좌석 수가 인원 수를 초과했습니다.")
    
    def save_seat(self):
        if len(self.selected_seats) == self.num_people:
            for seat in self.selected_seats:
                index = self.selected_movie.seats[self.selected_time].index(seat)
                self.selected_movie.seats[self.selected_time][index] = '■'
            self.confirm_reservation()
        else:
            messagebox.showerror("오류", "선택한 좌석 수가 인원 수와 맞지 않습니다.")
    
    def confirm_reservation(self):
        self.clear_frame()
        age_groups = {'성인': 0, '청소년': 0, '어린이': 0}
        for age in self.ages:
            if age >= 19:
                age_groups['성인'] += 1
            elif age >= 13:
                age_groups['청소년'] += 1
            else:
                age_groups['어린이'] += 1
        
        total_cost = (
            age_groups['성인'] * self.ticket_prices['성인'] +
            age_groups['청소년'] * self.ticket_prices['청소년'] +
            age_groups['어린이'] * self.ticket_prices['어린이']
        )
        
        reservation_info = {
            "영화": self.selected_movie.title,
            "날짜": self.selected_date,
            "시간": self.selected_time,
            "좌석": self.selected_seats,
            "연령대": age_groups,
            "총액": total_cost
        }
        
        if self.current_phone_number not in self.reservations:
            self.reservations[self.current_phone_number] = []
        
        self.reservations[self.current_phone_number].append(reservation_info)
        
        age_groups_str = ", ".join([f"{k} {v}명" for k, v in age_groups.items() if v > 0])
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
        self.reservations[self.current_phone_number][-1]["결제 방법"] = method
        messagebox.showinfo("결제 완료", f"결제가 완료되었습니다! ({method})")
        self.main_menu()
    
    def cancel_reservation(self):
        self.reservations[self.current_phone_number].pop()
        messagebox.showinfo("예약 취소", "예약이 취소되었습니다.")
        self.main_menu()
    
    def view_reservations(self):
        self.clear_frame()
        if self.current_phone_number not in self.reservations or not self.reservations[self.current_phone_number]:
            ttk.Label(self.main_frame, text="예매 내역이 없습니다.").grid(row=0, column=0, pady=10)
        else:
            for i, reservation in enumerate(self.reservations[self.current_phone_number]):
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
        back_button.grid(row=len(self.reservations[self.current_phone_number]), column=0, columnspan=2, pady=10)
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("영화 예매 시스템")
    system = ReservationSystem(root)
    root.mainloop()
