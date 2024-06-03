import tkinter as tk  # tkinter 모듈을 가져옵니다 (GUI 라이브러리)
from tkinter import simpledialog, messagebox  # tkinter의 서브 모듈을 가져옵니다 (입력 대화상자 및 메시지 박스)
import json  # JSON 형식으로 데이터를 처리하기 위한 모듈을 가져옵니다
import os  # 운영 체제와 상호작용하기 위한 모듈을 가져옵니다

class Movie:  # 클래스 정의 시작
    def __init__(self, title, times, theater):  # 생성자 메서드 정의
        self.title = title  # 영화 제목을 인스턴스 변수로 설정
        self.times = times  # 상영 시간을 인스턴스 변수로 설정
        self.theater = theater  # 상영관을 인스턴스 변수로 설정

    def to_dict(self):  # 객체를 딕셔너리로 변환하는 메서드 정의
        return {"title": self.title, "times": self.times, "theater": self.theater}  # 영화 정보를 딕셔너리로 반환

class BookingSystem:  # 예약 시스템 클래스 정의
    def __init__(self, file_path):  # 생성자 메서드 정의
        self.movies = []  # 영화 목록 초기화
        self.seats = {}  # 좌석 정보 초기화
        self.file_path = file_path  # 파일 경로 설정
        self.admin_password = "admin123"  # 관리자 비밀번호 설정
        self.load_movies()  # 영화 정보 불러오기

    def load_movies(self):  # 영화 정보를 파일에서 불러오는 메서드 정의
        if os.path.exists(self.file_path):  # 파일 경로가 존재하는지 확인
            with open(self.file_path, "r") as file:  # 파일 열기
                movies_data = json.load(file)  # JSON 파일을 딕셔너리로 로드
                for movie_data in movies_data:  # 각 영화 데이터에 대해 반복
                    movie = Movie(movie_data["title"], movie_data["times"], movie_data["theater"])  # Movie 객체 생성
                    self.movies.append(movie)  # 영화 목록에 추가
                    for time in movie.times:  # 각 상영 시간에 대해 반복
                        self.seats[time] = ['O'] * 10  # 해당 시간의 좌석 정보 초기화
        else:  # 파일이 존재하지 않는 경우
            # 기본 영화 정보 생성
            self.movies = [
                Movie("보라빛", ["10:00", "13:00", "16:00"], "관1"),
                Movie("보라색", ["11:00", "14:00", "17:00"], "관2"),
                Movie("보리보리", ["12:00", "15:00", "18:00"], "관3")
            ]
            for movie in self.movies:  # 각 영화에 대해 반복
                for time in movie.times:  # 각 상영 시간에 대해 반복
                    self.seats[time] = ['O'] * 10  # 해당 시간의 좌석 정보 초기화
            self.save_movies()  # 영화 정보 저장

    def save_movies(self):  # 영화 정보를 파일에 저장하는 메서드 정의
        movies_data = [movie.to_dict() for movie in self.movies]  # 각 영화를 딕셔너리로 변환하여 리스트에 저장
        with open(self.file_path, "w") as file:  # 파일 열기
            json.dump(movies_data, file)  # 영화 정보를 JSON 형식으로 파일에 저장

    def display_movies(self):  # 영화 목록을 출력하는 메서드 정의
        movies_list = ""  # 영화 목록 문자열 초기화
        for idx, movie in enumerate(self.movies):  # 각 영화에 대해 반복
            # 영화 정보를 문자열에 추가
            movies_list += f"{idx + 1}. {movie.title} - 상영 시간: {', '.join(movie.times)}, 상영관: {movie.theater}\n"
        return movies_list  # 영화 목록 문자열 반환

    def search_movie_by_name(self, name):  # 영화 제목으로 영화를 검색하는 메서드 정의
        found_movies = []  # 검색된 영화를 저장할 리스트 초기화
        for movie in self.movies:  # 각 영화에 대해 반복
            words = name.lower().split()  # 검색어를 소문자로 변환하고 단어로 분할하여 리스트로 만듦
            movie_title_lower = movie.title.lower()  # 영화 제목을 소문자로 변환
            if all(word in movie_title_lower for word in words):  # 검색어가 영화 제목에 모두 포함되는지 확인
                found_movies.append(movie)  # 검색된 영화 목록
                found_movies.append(movie)  # 검색된 영화 목록에 추가
        return found_movies  # 검색된 영화 목록 반환

    def edit_movie(self, movie, new_title, new_times):  # 영화 정보를 수정하는 메서드 정의
        movie.title = new_title  # 영화 제목 수정
        movie.times = new_times  # 영화 상영 시간 수정
        self.save_movies()  # 영화 정보 저장

    def delete_movie(self, movie):  # 영화를 삭제하는 메서드 정의
        self.movies.remove(movie)  # 영화 목록에서 영화 삭제
        self.save_movies()  # 영화 정보 저장

class Application(tk.Tk):  # 애플리케이션 클래스 정의
    def __init__(self, booking_system):  # 생성자 메서드 정의
        super().__init__()  # 부모 클래스의 생성자 호출
        self.booking_system = booking_system  # 예약 시스템 객체 설정
        self.title("영화 예매 시스템")  # 창 제목 설정

        # 관리자 로그인 버튼 생성 및 배치
        self.admin_login_button = tk.Button(self, text="관리자 로그인", command=self.admin_login)
        self.admin_login_button.pack(pady=10)

        # 영화 목록 보기 버튼 생성 및 배치
        self.movie_list_button = tk.Button(self, text="영화 목록 보기", command=self.view_movies)
        self.movie_list_button.pack(pady=10)

        # 파일 경로 표시 레이블 생성 및 배치
        self.directory_label = tk.Label(self, text=f"movies.json 파일은 이 디렉토리에 생성됩니다: {self.booking_system.file_path}")
        self.directory_label.pack(pady=10)

    def admin_login(self):  # 관리자 로그인 메서드 정의
        password = simpledialog.askstring("비밀번호", "관리자 비밀번호를 입력하세요:", show='*')  # 비밀번호 입력 다이얼로그 표시
        if password == self.booking_system.admin_password:  # 입력된 비밀번호가 관리자 비밀번호와 일치하는지 확인
            self.admin_panel()  # 관리자 패널 메서드 호출
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다")  # 오류 메시지 표시

    def admin_panel(self):  # 관리자 패널 메서드 정의
        admin_window = tk.Toplevel(self)  # 새로운 윈도우 생성
        admin_window.title("관리자 패널")  # 윈도우 제목 설정

        # 영화 추가 버튼 생성 및 배치
        add_button = tk.Button(admin_window, text="영화 추가", command=self.add_movie)
        add_button.pack(pady=10)

        # 영화 조회 버튼 생성 및 배치
        view_button = tk.Button(admin_window, text="영화 조회", command=self.view_movies)
        view_button.pack(pady=10)

    def add_movie(self):  # 영화 추가 메서드 정의
        # 사용자로부터 새 영화 제목을 입력받음
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        # 사용자로부터 새 영화 시간을 입력받고 쉼표로 구분하여 리스트로 변환
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        # 새 영화 정보를 예약 시스템에 추가
        self.booking_system.movies.append(Movie(new_title, new_times))
        # 변경된 영화 정보를 파일에 저장
        self.booking_system.save_movies()
        # 성공 메시지 표시
        messagebox.showinfo("성공", "영화가 성공적으로 추가되었습니다")

    def view_movies(self):  # 영화 목록 보기 메서드 정의
        search_window = tk.Toplevel(self)  # 새로운 검색 윈도우 생성
        search_window.title("영화 검색")  # 검색 윈도우 제목 설정

        search_label = tk.Label(search_window, text="영화를 검색하세요:")  # 검색 레이블 생성
        search_label.pack(pady=10)  # 레이블 배치

        search_entry = tk.Entry(search_window)  # 검색 엔트리 생성
        search_entry.pack(pady=5)  # 엔트리 배치

        # 검색 버튼 생성 및 검색 엔트리의 내용을 인자로 하는 콜백 함수로 설정
        search_button = tk.Button(search_window, text="검색", command=lambda: self.search_and_display_movies(search_window, search_entry.get()))
        search_button.pack(pady=5)  # 버튼 배치

    def search_and_display_movies(self, view_window, name):  # 영화 검색 및 표시 메서드 정의
        found_movies = self.booking_system.search_movie_by_name(name)  # 입력된 이름으로 영화 검색
        if found_movies:  # 검색 결과가 있는 경우
            for idx, movie in enumerate(found_movies):  # 검색된 영화 목록을 반복하며
                movie_frame = tk.Frame(view_window)  # 새로운 프레임 생성
                movie_frame.pack(pady=5)  # 프레임 배치

                movie_label = tk.Label(movie_frame, text=f"{idx + 1}. {movie.title}")  # 영화 제목을 표시하는 레이블 생성
                movie_label.pack(side=tk.LEFT)  # 레이블 배치

                # 수정 버튼 생성 및 영화 객체와 콜백 함수 연결하여 배치
                edit_button = tk.Button(movie_frame, text="수정", command=lambda m=movie: self.edit_movie(m, view_window))
                edit_button.pack(side=tk.LEFT, padx=5)

                # 삭제 버튼 생성 및 영화 객체와 콜백 함수 연결하여 배치
                delete_button = tk.Button(movie_frame, text="삭제", command=lambda m=movie: self.delete_movie(m, view_window))
                delete_button.pack(side=tk.LEFT, padx=5)
        else:  # 검색 결과가 없는 경우
            messagebox.showinfo("검색 결과", "일치하는 영화가 없습니다.")  # 정보 메시지 표시

    def search_and_select_movie(self, search_window, name):  # 영화 검색 및 선택 메서드 정의
        found_movies = self.booking_system.search_movie_by_name(name)  # 입력된 이름으로 영화 검색
        if found_movies:  # 검색 결과가 있는 경우
            movie_index = simpledialog.askinteger("영화 선택", "선택할 영화 번호를 입력하세요:") - 1  # 사용자에게 영화 선택을 요청
            if 0 <= movie_index < len(found_movies):  # 올바른 인덱스인 경우
                self.manage_movie(found_movies[movie_index], search_window)  # 선택된 영화를 관리하는 메서드 호출
            else:  # 올바르지 않은 인덱스인 경우
                messagebox.showerror("오류", "유효하지 않은 영화 번호입니다")  # 오류 메시지 표시
        else:  # 검색 결과가 없는 경우
            messagebox.showerror("오류", "일치하는 영화가 없습니다.")  # 오류 메시지 표시

    def manage_movie(self, movie, view_window):  # 영화 관리 메서드 정의
        manage_window = tk.Toplevel(view_window)  # 새로운 관리 윈도우 생성
        manage_window.title("영화 관리")  # 윈도우 제목 설정

        # 영화 수정 버튼 생성 및 배치
        edit_button = tk.Button(manage_window, text="영화 수정", command=lambda: self.edit_movie(movie, manage_window))
        edit_button.pack(pady=10)

        # 영화 삭제 버튼 생성 및 배치
        delete_button = tk.Button(manage_window, text="영화 삭제", command=lambda: self.delete_movie(movie, manage_window))
        delete_button.pack(pady=10)

    def edit_movie(self, movie, manage_window):  # 영화 수정 메서드 정의
        # 새 영화 제목을 입력 받음
        new_title = simpledialog.askstring("영화 수정", "새 영화 제목을 입력하세요:")
        # 새 영화 시간을 입력 받고 쉼표로 구분하여 리스트로 변환
        new_times = simpledialog.askstring("영화 수정", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        # 예약 시스템에 영화 수정 요청
        self.booking_system.edit_movie(movie, new_title, new_times)
        # 성공 메시지 표시
        messagebox.showinfo("성공", "영화가 성공적으로 수정되었습니다")
        # 관리 윈도우 닫기
        manage_window.destroy()

    def delete_movie(self, movie, manage_window):  # 영화 삭제 메서드 정의
        self.booking_system.delete_movie(movie)  # 예약 시스템에서 영화 삭제
        messagebox.showinfo("성공", "영화가 성공적으로 삭제되었습니다")  # 성공 메시지 표시
        manage_window.destroy()  # 관리 윈도우 닫기

# 파일 경로를 바탕화면에 맞게 수정
file_path = "C:\Users\LG\Desktop\moveis"
# BookingSystem 클래스의 인스턴스 생성 및 파일 경로 전달
booking_system = BookingSystem(file_path)
# 애플리케이션 클래스의 인스턴스 생성 및 예약 시스템 객체 전달
app = Application(booking_system)
# 애플리케이션 실행
app.mainloop()