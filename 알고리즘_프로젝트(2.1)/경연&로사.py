import tkinter as tk  # Tkinter 라이브러리 임포트
from tkinter import simpledialog, messagebox  # Tkinter의 서브 모듈 임포트
import os  # 운영 체제 관련 기능을 사용하기 위해 os 모듈 임포트

# Movie 클래스: 각 영화의 정보를 저장
class Movie:
    def __init__(self, title, times, theater, age_limit):
        self.title = title  # 영화 제목
        self.times = times  # 영화 상영 시간 목록
        self.theater = theater  # 영화 상영관
        self.age_limit = age_limit  # 영화 연령 제한

    # 영화 정보를 문자열로 변환하여 반환
    def to_string(self):
        return f"{self.title},{','.join(self.times)},{self.theater},{self.age_limit}"

# BookingSystem 클래스: 영화 예매 시스템의 핵심 로직
class BookingSystem:
    def __init__(self, file_path):
        self.movies = []  # 영화 목록
        self.file_path = file_path  # 영화 정보를 저장할 파일 경로
        self.admin_password = "admin123"  # 관리자 비밀번호
        self.load_movies()  # 파일에서 영화 정보를 로드
        self.sort_movies()  # 영화 목록을 정렬

    # 영화 정보를 파일에서 읽어오는 메서드
    def load_movies(self):
        if os.path.exists(self.file_path):  # 파일이 존재하는지 확인
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(',')
                    title = parts[0]
                    times = parts[1].split(',')
                    theater = parts[2]
                    age_limit = parts[3]  # 연령 제한 추가
                    self.movies.append(Movie(title, times, theater, age_limit))

    # 영화 정보를 파일에 저장하는 메서드
    def save_movies(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for movie in self.movies:
                file.write(f"{movie.to_string()}\n")

    # 영화 목록을 제목 기준으로 정렬하는 메서드
    def sort_movies(self):
        self.movies.sort(key=lambda movie: movie.title)

    # 영화 목록을 문자열 형태로 반환하는 메서드
    def display_movies(self):
        movies_list = ""
        for idx, movie in enumerate(self.movies):
            movies_list += f"{idx + 1}. {movie.title} ({movie.age_limit})\n"  # 연령 제한 추가
        return movies_list

    # 이진 검색을 사용하여 영화 제목으로 영화를 찾는 메서드
    def binary_search_movie_by_name(self, name):
        left, right = 0, len(self.movies) - 1
        found_movies = []

        while left <= right:
            mid = (left + right) // 2
            if name.lower() in self.movies[mid].title.lower():
                found_movies.append(self.movies[mid])
                # 인접한 요소에서 일치하는 다른 영화들도 검색
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

    # 영화 정보를 수정하는 메서드
    def edit_movie(self, idx, new_title, new_times, new_theater, new_age_limit):
        if 0 <= idx < len(self.movies):
            self.movies[idx].title = new_title
            self.movies[idx].times = new_times
            self.movies[idx].theater = new_theater
            self.movies[idx].age_limit = new_age_limit
            self.sort_movies()  # 수정 후 목록 정렬
            self.save_movies()
            return True
        return False

    # 영화 정보를 삭제하는 메서드
    def delete_movie(self, idx):
        if 0 <= idx < len(self.movies):
            del self.movies[idx]
            self.save_movies()
            return True
        return False

# Application 클래스: Tkinter를
class Application(tk.Tk):
    def __init__(self, booking_system):
        super().__init__()
        self.booking_system = booking_system
        self.title("영화 예매 시스템")

        self.admin_login_button = tk.Button(self, text="관리자 로그인", command=self.admin_login)
        self.admin_login_button.pack(pady=10)

        self.directory_label = tk.Label(self, text=f"movies.txt 파일은 이 디렉토리에 있습니다: {self.booking_system.file_path}")
        self.directory_label.pack(pady=10)

    # 관리자 로그인 메서드
    def admin_login(self):
        password = simpledialog.askstring("비밀번호", "관리자 비밀번호를 입력하세요:", show='*')
        if password == self.booking_system.admin_password:
            self.admin_panel()
        else:
            messagebox.showerror("오류", "비밀번호가 틀렸습니다")

    # 관리자 패널을 표시하는 메서드
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

    # 영화 목록을 업데이트하는 메서드
    def update_movie_list(self):
        self.booking_system.sort_movies()  # 목록을 업데이트하기 전에 정렬
        self.movies_listbox.delete(0, tk.END)
        for movie in self.booking_system.movies:
            self.movies_listbox.insert(tk.END, movie.title)

    # 영화를 추가하는 메서드
    def add_movie(self):
        new_title = simpledialog.askstring("영화 추가", "새 영화 제목을 입력하세요:")
        new_times = simpledialog.askstring("영화 추가", "새 영화 시간을 입력하세요 (쉼표로 구분):").split(',')
        new_theater = simpledialog.askstring("영화 추가", "새 영화 상영관을 입력하세요:")
        new_age_limit = simpledialog.askstring("영화 추가", "새 영화 연령 제한을 입력하세요:")  # 연령 제한 추가
        self.booking_system.movies.append(Movie(new_title, new_times, new_theater, new_age_limit))
        self.booking_system.sort_movies()  # 추가 후 목록 정렬
        self.booking_system.save_movies()
        self.update_movie_list()
        messagebox.showinfo("성공", "영화가 성공적으로 추가되었습니다")

    # 영화를 조회하는 메서드
    def view_movies(self):
        search_window = tk.Toplevel(self)
        search_window.title("영화 조회")

        search_label = tk.Label(search_window, text="영화 제목을 입력하세요:")
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)

        search_button = tk.Button(search_window, text="검색", command=lambda: self.search_movies(search_entry.get(), search_window))
        search_button.pack(pady=5)

    # 영화를 검색하는 메서드
    def search_movies(self, name, search_window):
        found_movies = self.booking_system.binary_search_movie_by_name(name)
        if found_movies:
            movies_list = "\n".join([f"{idx + 1}. {movie.title} ({movie.age_limit})" for idx, movie in enumerate(found_movies)])  # 연령 제한 추가
            movies_label = tk.Label(search_window, text=movies_list)
            movies_label.pack(pady=10)

            select_button = tk.Button(search_window, text="영화 선택", command=lambda: self.select_movie(found_movies, search_window))
            select_button.pack(pady=5)
        else:
            messagebox.showinfo("검색 결과", "일치하는 영화가 없습니다.")

    # 선택한 영화를 상세히 보는 메서드
    def select_movie(self, movies, search_window):
        movie_index = simpledialog.askinteger("영화 선택", "선택할 영화 번호를 입력하세요:") - 1
        if 0 <= movie_index < len(movies):
            movie = movies[movie_index]
            search_window.destroy()  # 검색 창 닫기
            self.show_movie_details(movie)
        else:
            messagebox.showerror("오류", "유효하지 않은 영화 번호입니다")

    # 영화 상세 정보를 표시하는 메서드
    def show_movie_details(self, movie):
        details_window = tk.Toplevel(self)
        details_window.title("영화 정보")

        title_label = tk.Label(details_window, text=f"제목: {movie.title}")
        title_label.pack(pady=5)

        times_label = tk.Label(details_window, text=f"상영 시간: {', '.join(movie.times)}")
        times_label.pack(pady=5)

        theater_label = tk.Label(details_window, text=f"상영관: {movie.theater}")
        theater_label.pack(pady=5)

        age_limit_label = tk.Label(details_window, text=f"연령 제한: {movie.age_limit}")  # 연령 제한 추가
        age_limit_label.pack(pady=5)

        edit_button = tk.Button(details_window, text="영화 수정", command=lambda: self.edit_movie_details(movie, details_window))
        edit_button.pack(pady=5)

        delete_button = tk.Button(details_window, text="영화 삭제", command=lambda: self.delete_movie_details(movie, details_window))
        delete_button.pack(pady=5)

    # 영화 정보를 수정하는 메서드
    def edit_movie_details(self, movie, details_window):
        new_title = simpledialog.askstring("영화 수정", "새 영화 제목을 입력하세요:", initialvalue=movie.title)
        new_times = simpledialog.askstring("영화 수정", "새 영화 시간을 입력하세요 (쉼표로 구분):", initialvalue=','.join(movie.times)).split(',')
        new_theater = simpledialog.askstring("영화 수정", "새 상영관을 입력하세요:", initialvalue=movie.theater)
        new_age_limit = simpledialog.askstring("영화 수정", "새 연령 제한을 입력하세요:", initialvalue=movie.age_limit)  # 연령 제한 수정
        if new_title is not None and new_times is not None and new_theater is not None and new_age_limit is not None:
            if self.booking_system.edit_movie(self.booking_system.movies.index(movie), new_title, new_times, new_theater, new_age_limit):
                self.update_movie_list()  # 수정 후 목록 업데이트
                messagebox.showinfo("성공", "영화가 성공적으로 수정되었습니다")
                details_window.destroy()
            else:
                messagebox.showerror("오류", "영화 수정에 실패했습니다")
        else:
            messagebox.showerror("오류", "수정 정보를 모두 입력하세요")

    # 영화를 삭제하는 메서드
    def delete_movie_details(self, movie, details_window):
        confirm = messagebox.askyesno("확인", f"정말로 '{movie.title}' 영화를 삭제하시겠습니까?")
        if confirm:
            if self.booking_system.delete_movie(self.booking_system.movies.index(movie)):
                self.update_movie_list()  # 삭제 후 목록 업데이트
                messagebox.showinfo("성공", "영화가 성공적으로 삭제되었습니다")
                details_window.destroy()
            else:
                messagebox.showerror("오류", "영화 삭제에 실패했습니다")

# 프로그램 실행
file_path = r"C:\Users\LG\Desktop\movies.txt"  # 영화 정보를 저장할 파일 경로
booking_system = BookingSystem(file_path)  # BookingSystem 인스턴스 생성
app = Application(booking_system)  # Application 인스턴스 생성
app.mainloop()  # Tkinter 메인 루프 실행

#//////////////////////////////////////////////////////////////////////////////


class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def print_info(self):
        return f"이름: {self.name}  전화번호: {self.phone_number}\n"

def binary_search(contact_list, target, key=lambda x: x.name):
    """
    이진 탐색을 사용하여 연락처 리스트에서 타겟 이름 또는 전화번호의 위치를 찾는다.
    해당 요소가 존재하지 않으면 삽입 위치를 반환한다.
    """
    low, high = 0, len(contact_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if key(contact_list[mid]) < target:
            low = mid + 1
        elif key(contact_list[mid]) > target:
            high = mid - 1
        else:
            return mid
    return low  # 위치를 반환하여 삽입/검색 등에 사용

def set_contact(contact_list):
    name = simpledialog.askstring("Input", "Name:")
    phone_number = simpledialog.askstring("Input", "전화번호:")
    if name and phone_number:
        # 이미 존재하는 전화번호인지 확인
        for contact in contact_list:
            if contact.phone_number == phone_number:
                messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                return None
        return Contact(name, phone_number)
    return None

def delete_contact(contact_list, name, phone_number):
    # 이름을 기준으로 이진 탐색을 사용하여 삭제할 연락처 찾기
    index = binary_search(contact_list, name)
    while index < len(contact_list) and contact_list[index].name == name:
        if contact_list[index].phone_number == phone_number:
            del contact_list[index]
            messagebox.showinfo("Deleted", f"[삭제] 이름: {name}, 전화번호: {phone_number}")
            return
        index += 1
    messagebox.showerror("Error", f"일치하는 연락처를 찾을 수 없습니다: {name}, 전화번호: {phone_number}")

def search_contact(contact_list, name, listbox):
    # 이름을 기준으로 이진 탐색을 사용하여 검색된 연락처 표시
    index = binary_search(contact_list, name)
    listbox.delete(0, tk.END)
    while index < len(contact_list) and contact_list[index].name == name:
        listbox.insert(tk.END, contact_list[index].print_info())
        index += 1

def update_contact(contact_list, name, listbox):
    listbox.delete(0, tk.END)
    # 이름을 기준으로 이진 탐색을 사용하여 수정할 연락처 찾기
    index = binary_search(contact_list, name)
    if index < len(contact_list) and contact_list[index].name == name:
        while index < len(contact_list) and contact_list[index].name == name:
            listbox.insert(tk.END, contact_list[index].print_info())
            index += 1
        selected_phone_number = simpledialog.askstring("Input", "수정할 전화번호를 입력하세요:")
        if selected_phone_number:
            index = binary_search(contact_list, name)
            while index < len(contact_list) and contact_list[index].name == name:
                if contact_list[index].phone_number == selected_phone_number:
                    new_phone_number = simpledialog.askstring("Input", "새로운 전화번호:")
                    if new_phone_number:
                        # 새 전화번호가 이미 존재하는지 확인
                        for c in contact_list:
                            if c.phone_number == new_phone_number:
                                messagebox.showerror("Error", "이미 가입된 사용자입니다.")
                                return
                        contact_list[index].phone_number = new_phone_number
                        contact_list.sort(key=lambda x: (x.name, x.phone_number))
                        refresh_listbox(contact_list, listbox)
                        messagebox.showinfo("Updated", "수정이 완료되었습니다.")
                        return
                index += 1
            messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")
    else:
        messagebox.showerror("Error", "일치하는 연락처를 찾을 수 없습니다.")

def save_contacts(contact_list, filename="contacts.json"):
    with open(filename, "w") as file:
        json_list = [{"name": contact.name, "phone_number": contact.phone_number} for contact in contact_list]
        json.dump(json_list, file)

def load_contacts(contact_list, listbox, filename="contacts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                json_list = json.load(file)
                contact_list.clear()
                for contact in json_list:
                    name = contact.get("name", "")
                    phone_number = contact.get("phone_number", "")
                    if name and phone_number:
                        contact_list.append(Contact(name, phone_number))
                    else:
                        messagebox.showerror("Error", "연락처 파일에 필수 정보가 누락되었습니다.")
                contact_list.sort(key=lambda x: (x.name, x.phone_number))
                refresh_listbox(contact_list, listbox)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "저장된 연락처 파일을 읽을 수 없습니다.")
    else:
        messagebox.showwarning("Warning", "저장된 연락처 파일을 찾을 수 없습니다. 새로운 연락처를 추가해주세요.")

def on_add_contact(contact_list, listbox):
    contact = set_contact(contact_list)
    if contact:
        # 이진 탐색을 사용하여 올바른 위치에 연락처 삽입
        index = binary_search(contact_list, contact.name)
        contact_list.insert(index, contact)
        refresh_listbox(contact_list, listbox)

def on_delete_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "삭제할 고객명:")
    if name:
        listbox.delete(0, tk.END)
        # 이름을 기준으로 이진 탐색을 사용하여 삭제할 연락처 표시
        index = binary_search(contact_list, name)
        while index < len(contact_list) and contact_list[index].name == name:
            listbox.insert(tk.END, contact_list[index].print_info())
            index += 1
        selected_phone_number = simpledialog.askstring("Input", "삭제할 전화번호를 입력하세요:")
        if selected_phone_number:
            delete_contact(contact_list, name, selected_phone_number)
            refresh_listbox(contact_list, listbox)

def on_search_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "검색할 고객명:")
    if name:
        search_contact(contact_list, name, listbox)

def on_update_contact(contact_list, listbox):
    name = simpledialog.askstring("Input", "수정할 고객명:")
    if name:
        update_contact(contact_list, name, listbox)

def refresh_listbox(contact_list, listbox):
    listbox.delete(0, tk.END)
    # 연락처를 이름순으로 정렬한 후, 전화번호가 숫자로 인식되어 오름차순으로 정렬됩니다.
    sorted_contacts = sorted(contact_list, key=lambda x: (x.name, int(x.phone_number)))
    for contact in sorted_contacts:
        listbox.insert(tk.END, contact.print_info())

def on_exit(contact_list):
    save_contacts(contact_list)
    root.destroy()

def on_home(contact_list, listbox):
    refresh_listbox(contact_list, listbox)

def login():
    global root, contact_list
    login_window = tk.Tk()
    login_window.title("Login")
    
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin":
            login_window.destroy()
            create_gui(contact_list)
        else:
            messagebox.showerror("Error", "올바르지 않은 사용자 이름 또는 비밀번호입니다.")
    
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    
    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    
    login_button = tk.Button(login_window, text="Login", command=authenticate)
    login_button.pack()

    login_window.mainloop()

def create_gui(contact_list):
    global root
    root = tk.Tk()
    root.title("Contact Manager")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    listbox = tk.Listbox(frame, width=40, height=10)
    listbox.pack(side=tk.LEFT, padx=(0, 10))

    refresh_listbox(contact_list, listbox)

    button_frame = tk.Frame(frame)
    button_frame.pack(side=tk.RIGHT)

    search_button = tk.Button(button_frame, text="검색", command=lambda: on_search_contact(contact_list, listbox))
    search_button.pack(fill=tk.X)

    add_button = tk.Button(button_frame, text="추가", command=lambda: on_add_contact(contact_list, listbox))
    add_button.pack(fill=tk.X)

    delete_button = tk.Button(button_frame, text="삭제", command=lambda: on_delete_contact(contact_list, listbox))
    delete_button.pack(fill=tk.X)

    update_button = tk.Button(button_frame, text="수정", command=lambda: on_update_contact(contact_list, listbox))
    update_button.pack(fill=tk.X)

    home_button = tk.Button(button_frame, text="홈", command=lambda: on_home(contact_list, listbox))
    home_button.pack(fill=tk.X)

    exit_button = tk.Button(button_frame, text="종료", command=lambda: on_exit(contact_list))
    exit_button.pack(fill=tk.X)

    load_contacts(contact_list, listbox)

    root.mainloop()

if __name__ == "__main__":
    contact_list = []
    create_gui(contact_list)

