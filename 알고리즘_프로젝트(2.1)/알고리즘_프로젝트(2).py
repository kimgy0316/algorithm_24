import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# 영화 정보를 저장하는 Movie 클래스
class Movie:
    def __init__(self, title, times, theater):
        self.title = title
        self.times = times
        self.theater = theater

    def to_dict(self):
        return {"title": self.title, "times": self.times, "theater": self.theater}

# 영화 예매 시스템을 관리하는 BookingSystem 클래스
class BookingSystem:
    def __init__(self, file_path):
        self.movies = []
        self.seats = {}
        self.file_path = file_path
        self.admin_password = "admin123"
        self.load_movies()

    # 파일이 존재하면 파일에서 영화를 불러오는 메서드
    def load_movies(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                movies_data = json.load(file)
                for movie_data in movies_data:
                    movie = Movie(movie_data["title"], movie_data["times"], movie_data["theater"])
                    self.movies.append(movie)
                    for time in movie.times:
                        self.seats[time] = ['O'] * 10
        else:
            # 파일이 존재하지 않으면 기본 영화를 초기화
            self.movies = [
                Movie("보라빛", ["10:00", "13:00", "16:00"], "관1"),
                Movie("보라색", ["11:00", "14:00", "17:00"], "관2"),
                Movie("보리보리", ["12:00", "15:00", "18:00"], "관3")
                ]
            for movie in self.movies:
                for time in movie.times:
                    self.seats[time] = ['O'] * 10
            self.save_movies()

    # 영화를 파일에 저장하는 메서드
    def save_movies(self):
        movies_data = [movie.to_dict() for movie in self.movies]
        with open(self.file_path, "w") as file:
            json.dump(movies_data, file)

    # 모든 영화를 문자열로 반환하는 메서드
    def display_movies(self):
        movies_list = ""
        for idx, movie in enumerate(self.movies):
            movies_list += f"{idx + 1}. {movie.title} - 상영 시간: {', '.join(movie.times)}, 상영관: {movie.theater}\n"
        return movies_list

    # 영화 제목으로 영화를 검색하는 메서드
    def search_movie_by_name(self, name):
        found_movies = []
        for movie in self.movies:
            words = name.lower().split()  # 검색어를 단어로 분할하여 리스트로 만듦
            movie_title_lower = movie.title.lower()
            if all(word in movie_title_lower for word in words):
                found_movies.append(movie)
        return found_movies

    # 영화를 수정하는 메서드
    def edit_movie(self, movie, new_title, new_times):
        movie.title = new_title
        movie.times = new_times
        self.save_movies()

    # 영화를 삭제하는 메서드
    def delete_movie(self, movie):
        self.movies.remove(movie)
        self.save_movies()

# 애플리케이션 클래스
class Application(tk.Tk):
    def __init__(self, booking_system):
        super().__init__()
        self.booking_system = booking_system
        self.title("영화 예매 시스템")

        # 관리자 로그인 버튼
        self.admin_login_button = tk.Button(self, text="관리자 로그인", command=self.admin_login)
        self.admin_login_button.pack(pady=10)

        # 영화 목록 보기 버튼
        self.movie_list_button = tk.Button(self, text="영화 목록 보기", command=self.view_movies)
        self.movie_list_button.pack(pady=10)

        # 파일 경로 레이블
        self.directory_label = tk.Label(self, text=f"movies.json 파일은 이 디렉토리에 생성됩니다: {self.booking_system.file_path}")
        self.directory_label.pack(pady=10)

    # 관리자 로그인 메서드
    def admin_login(self):
        password = simpledialog.askstring("비밀번호", "관리자 비밀번호를 입력하세요:", show='*')
        if password == self.booking_system.admin_password:
            self.admin_panel()
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다")

    # 관리자 패널을 여는 메서드
    def admin_panel(self):
        admin_window = tk.Toplevel(self)
        admin_window.title("관리자 패널")

        # 영화 추가 버튼
        add_button = tk.Button(admin_window, text="영화 추가", command=self.add_movie)
        add_button.pack(pady=10)

        # 영화 조회 버튼
        view_button = tk.Button(admin_window, text="영화 조회", command=self.view_movies)
        view_button.pack(pady=10)

    # 영화 추가 메서드
    def add_movie(self):
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        self.booking_system.movies.append(Movie(new_title, new_times))
        self.booking_system.save_movies()
        messagebox.showinfo("성공", "영화가 성공적으로 추가되었습니다")

    # 영화 목록 보기 메서드
    def view_movies(self):
        search_window = tk.Toplevel(self)
        search_window.title("영화 검색")

        search_label = tk.Label(search_window, text="영화를 검색하세요:")
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)

        search_button = tk.Button(search_window, text="검색", command=lambda: self.search_and_display_movies(search_window, search_entry.get()))
        search_button.pack(pady=5)

    # 영화 검색 및 결과 표시 메서드
    def search_and_display_movies(self, view_window, name):
        found_movies = self.booking_system.search_movie_by_name(name)
        if found_movies:
            for idx, movie in enumerate(found_movies):
                movie_frame = tk.Frame(view_window)
                movie_frame.pack(pady=5)

                movie_label = tk.Label(movie_frame, text=f"{idx + 1}. {movie.title}")
                movie_label.pack(side=tk.LEFT)

                edit_button = tk.Button(movie_frame, text="수정", command=lambda m=movie: self.edit_movie(m, view_window))
                edit_button.pack(side=tk.LEFT, padx=5)

                delete_button = tk.Button(movie_frame, text="삭제", command=lambda m=movie: self.delete_movie(m, view_window))
                delete_button.pack(side=tk.LEFT, padx=5)
        else:
            messagebox.showinfo("검색 결과", "일치하는 영화가 없습니다.")

    # 검색된 영화 선택 메서드
    def search_and_select_movie(self, search_window, name):
        found_movies = self.booking_system.search_movie_by_name(name)
        if found_movies:
            movie_index = simpledialog.askinteger("영화 선택", "선택할 영화 번호를 입력하세요:") - 1
            if 0 <= movie_index < len(found_movies):
                self.manage_movie(found_movies[movie_index], search_window)
            else:
                messagebox.showerror("오류", "유효하지 않은 영화 번호입니다")
        else:
            messagebox.showerror("오류", "일치하는 영화가 없습니다.")

   # 선택된 영화 관리 메서드
def manage_movie(self, movie, view_window):
    manage_window = tk.Toplevel(view_window)  # 새로운 창 열기
    manage_window.title("영화 관리")  # 창 제목 설정

    # 영화 수정 버튼
    edit_button = tk.Button(manage_window, text="영화 수정", command=lambda: self.edit_movie(movie, manage_window))
    edit_button.pack(pady=10)

    # 영화 삭제 버튼
    delete_button = tk.Button(manage_window, text="영화 삭제", command=lambda: self.delete_movie(movie, manage_window))
    delete_button.pack(pady=10)

# 영화 수정 메서드
def edit_movie(self, movie, manage_window):
    new_title = simpledialog.askstring("영화 수정", "새 영화 제목을 입력하세요:")  # 새 영화 제목 입력 창
    new_times = simpledialog.askstring("영화 수정", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')  # 새 영화 시간 입력 창
    self.booking_system.edit_movie(movie, new_title, new_times)  # 영화 정보 수정
    messagebox.showinfo("성공", "영화가 성공적으로 수정되었습니다")  # 영화 수정 성공 메시지
    manage_window.destroy()  # 창 닫기

# 영화 삭제 메서드
def delete_movie(self, movie, manage_window):
    self.booking_system.delete_movie(movie)  # 영화 정보 삭제
    messagebox.showinfo("성공", "영화가 성공적으로 삭제되었습니다")  # 영화 삭제 성공 메시지
    manage_window.destroy()  # 창 닫기

# 애플리케이션 실행
file_path = "C:/Users/LG/Desktop/movies.json"  # 파일 경로 설정
booking_system = BookingSystem(file_path)  # BookingSystem 인스턴스 생성
app = Application(booking_system)  # Application 인스턴스 생성
app.mainloop()  # 애플리케이션 메인 루프 실행
