import tkinter as tk
from tkinter import messagebox
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
        ] for time in times}

class ReservationSystem:
    def __init__(self):
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

    def merge(self, A, left, mid, right):
        temp = [0] * len(A)
        k = left
        i = left
        j = mid + 1
        while i <= mid and j <= right:
            if A[i].title <= A[j].title:
                temp[k] = A[i]
                i, k = i + 1, k + 1
            else:
                temp[k] = A[j]
                j, k = j + 1, k + 1

        if i > mid:
            temp[k:k + right - j + 1] = A[j:right + 1]
        else:
            temp[k:k + mid - i + 1] = A[i:mid + 1]

        A[left:right + 1] = temp[left:right + 1]

    def merge_sort(self, A, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(A, left, mid)
            self.merge_sort(A, mid + 1, right)
            self.merge(A, left, mid, right)

    def display_movies(self):
        self.merge_sort(self.movies, 0, len(self.movies) - 1)
        movie_list = []
        for i, movie in enumerate(self.movies):
            movie_list.append(f"{i+1}. {movie.title} (연령 제한: {movie.age_limit}세 이상)")
        return "\n".join(movie_list)

    def select_movie(self, choice):
        if 0 <= choice < len(self.movies):
            return self.movies[choice]
        else:
            return None

    def select_date(self):
        today = datetime.datetime.today()
        return today

    def select_time(self, movie, choice):
        if 0 <= choice < len(movie.times):
            return movie.times[choice]
        else:
            return None

    def select_seat(self, movie, time, seats):
        if all(seat in movie.seats[time] for seat in seats):
            for seat in seats:
                index = movie.seats[time].index(seat)
                movie.seats[time][index] = '■'
            return True
        else:
            return False

    def select_num_people(self, num_people):
        if 1 <= num_people <= 5:
            return num_people
        else:
            return None

    def check_age_restriction(self, movie, age_groups):
        adults, teens, children = age_groups
        total_people = adults + teens + children
        if (movie.age_limit == 19 and (teens > 0 or children > 0)) or (movie.age_limit == 15 and children > 0):
            return None
        else:
            return {'성인': adults, '청소년': teens, '어린이': children}

    def make_reservation(self, phone_number, movie_choice, num_people, age_groups, time_choice, seat_selection):
        movie = self.select_movie(movie_choice)
        if movie:
            num_people = self.select_num_people(num_people)
            age_groups = self.check_age_restriction(movie, age_groups)
            if age_groups:
                date = self.select_date()
                time = self.select_time(movie, time_choice)
                if time and self.select_seat(movie, time, seat_selection):
                    total_cost = (
                        age_groups['성인'] * self.ticket_prices['성인'] +
                        age_groups['청소년'] * self.ticket_prices['청소년'] +
                        age_groups['어린이'] * self.ticket_prices['어린이']
                    )

                    reservation_info = {
                        "영화": movie.title,
                        "날짜": date.date(),
                        "시간": time,
                        "좌석": seat_selection,
                        "연령대": age_groups,
                        "총액": total_cost
                    }

                    if phone_number not in self.reservations:
                        self.reservations[phone_number] = []

                    self.reservations[phone_number].append(reservation_info)
                    return reservation_info
        return None

    def view_reservations(self, phone_number):
        if phone_number not in self.reservations or not self.reservations[phone_number]:
            return "예매 내역이 없습니다."
        else:
            reservation_list = []
            for i, reservation in enumerate(self.reservations[phone_number]):
                age_groups_str = ", ".join([f"{k} {v}명" for k, v in reservation['연령대'].items() if v > 0])
                reservation_list.append(f"{i+1}. 영화: {reservation['영화']}, 날짜: {reservation['날짜']}, 시간: {reservation['시간']}, 좌석: {', '.join(reservation['좌석'])}, 연령대: {age_groups_str}, 총액: {reservation['총액']}원")
            return "\n".join(reservation_list)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("영화 예매 시스템")
        self.geometry("400x300")
        self.reservation_system = ReservationSystem()
        self.users = {}
        self.current_user = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self, text="전화번호").pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        tk.Label(self, text="비밀번호").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="로그인", command=self.login).pack()
        tk.Button(self, text="회원가입", command=self.register).pack()

    def register(self):
        def submit_registration():
            phone = phone_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if password != confirm_password:
                messagebox.showerror("오류", "비밀번호를 다시 입력해 주세요.")
                return
            
            if phone in self.users:
                messagebox.showerror("오류", "이 전화번호는 이미 가입되어 있습니다.")
            else:
                self.users[phone] = password
                messagebox.showinfo("Success", "회원가입이 완료되었습니다!")
                register_window.destroy()

        register_window = tk.Toplevel(self)
        register_window.title("회원가입")

        tk.Label(register_window, text="전화번호").pack()
        phone_entry = tk.Entry(register_window)
        phone_entry.pack()

        tk.Label(register_window, text="비밀번호").pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()
        
        tk.Label(register_window, text="비밀번호 재입력").pack()
        confirm_password_entry = tk.Entry(register_window, show="*")
        confirm_password_entry.pack()

        tk.Button(register_window, text="가입", command=submit_registration).pack()

    def login(self):
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        
        if phone in self.users and self.users[phone] == password:
            self.current_user = phone
            messagebox.showinfo("성공", "로그인이 완료되었습니다!")
            self.create_reservation_screen()
        else:
            messagebox.showerror("오류", "전화번호와 비밀번호가 맞지 않습니다.")

    def create_reservation_screen(self):
        self.clear_screen()
        tk.Label(self, text="영화 목록").pack()

        movie_list = self.reservation_system.display_movies()
        tk.Label(self, text=movie_list).pack()

        tk.Label(self, text="영화를 선택하세요 (번호)").pack()
        self.movie_choice_entry = tk.Entry(self)
        self.movie_choice_entry.pack()

        tk.Label(self, text="상영 시간을 선택하세요 (번호)").pack()
        self.time_choice_entry = tk.Entry(self)
        self.time_choice_entry.pack()

        tk.Label(self, text="좌석을 선택하세요 (쉼표로 구분)").pack()
        self.seat_choice_entry = tk.Entry(self)
        self.seat_choice_entry.pack()

        tk.Label(self, text="성인 수").pack()
        self.adult_entry = tk.Entry(self)
        self.adult_entry.pack()

        tk.Label(self, text="청소년 수").pack()
        self.teen_entry = tk.Entry(self)
        self.teen_entry.pack()

        tk.Label(self, text="어린이 수").pack()
        self.child_entry = tk.Entry(self)
        self.child_entry.pack()

        tk.Button(self, text="예매하기", command=self.make_reservation).pack()
        tk.Button(self, text="예매 내역 보기", command=self.view_reservations).pack()

    def make_reservation(self):
        movie_choice = int(self.movie_choice_entry.get()) - 1
        time_choice = int(self.time_choice_entry.get()) - 1
        seats = self.seat_choice_entry.get().split(',')
        adults = int(self.adult_entry.get())
        teens = int(self.teen_entry.get())
        children = int(self.child_entry.get())
        age_groups = (adults, teens, children)

        reservation_info = self.reservation_system.make_reservation(
            self.current_user, movie_choice, adults + teens + children, age_groups, time_choice, seats
        )

        if reservation_info:
            messagebox.showinfo("성공", "예매가 완료되었습니다!")
        else:
            messagebox.showerror("오류", "예매에 실패했습니다. 입력 정보를 확인해 주세요.")

    def view_reservations(self):
        reservations = self.reservation_system.view_reservations(self.current_user)
        messagebox.showinfo("예매 내역", reservations)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()