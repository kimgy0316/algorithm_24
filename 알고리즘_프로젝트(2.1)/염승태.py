import datetime

class Movie:
    def __init__(self, title, times, age_limit):
        self.title = title
        self.times = times
        self.age_limit = age_limit
        self.seats = {time: [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
            'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'
        ] for time in times}

class ReservationSystem:
    def __init__(self):
        self.movies = [
            Movie("범죄도시 4", ["10:00", "10:30", "11:00", "11:20", "12:00", "13:00", "16:00", "19:00", "20:15"], 19),
            Movie("귀멸의 칼날", ["11:00", "14:00", "17:00", "20:00", "10:00", "13:00", "16:00", "19:07", "20:00"], 15),
            Movie("보라", ["12:00", "15:00", "18:00", "18:20", "20:00", "20:10", "21:00", "22:00", "22:40"], 12),
            Movie("영화 4", ["10:30", "13:30", "14:30", "15:30", "16:00", "16:40", "17:00", "19:00", "20:00"], 12),
            Movie("영화 5", ["11:30", "12:30", "13:30", "14:30", "15:00", "15:30", "16:00", "19:00", "20:05"], 12)
        ]
        self.ticket_prices = {
            '성인': 13000,
            '중고등학생': 10000,
            '유아': 6000
        }
        self.reservations = []

    def display_movies(self):
        print("예매 가능한 영화 목록:")
        for i, movie in enumerate(self.movies):
            print(f"{i+1}. {movie.title} (연령 제한: {movie.age_limit}세 이상)")

    def select_movie(self):
        self.display_movies()
        while True:
            try:
                choice = int(input("영화를 선택하세요 (번호 입력): ")) - 1
                if 0 <= choice < len(self.movies):
                    return self.movies[choice]
                else:
                    print("잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def select_date(self):
        today = datetime.datetime.today()
        print(f"오늘 날짜로 예약됩니다: {today.strftime('%Y-%m-%d')}")
        return today

    def select_time(self, movie):
        print(f"{movie.title}의 가능한 상영 시간:")
        for i, time in enumerate(movie.times):
            print(f"{i+1}. {time}")
        while True:
            try:
                choice = int(input("상영 시간을 선택하세요 (번호 입력): ")) - 1
                if 0 <= choice < len(movie.times):
                    return movie.times[choice]
                else:
                    print("잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def select_seat(self, movie, time, num_people):
        print(f"{movie.title}의 {time} 상영 시간의 가능한 좌석:")
        print(movie.seats[time])
        seats = []
        for _ in range(num_people):
            while True:
                seat = input("좌석을 선택하세요: ")
                if seat in movie.seats[time]:
                    index = movie.seats[time].index(seat)
                    movie.seats[time][index] = '■'
                    seats.append(seat)
                    break
                else:
                    print("해당 좌석은 선택할 수 없습니다. 다시 선택하세요.")
        return seats

    def select_age_group(self, age):
        while True:
            print("연령대를 선택하세요:")
            print("1. 성인 (13000원)")
            print("2. 중고등학생 (10000원)")
            print("3. 유아 (6000원)")
            try:
                choice = int(input("번호를 선택하세요: "))
                if choice == 1 and age >= 19:
                    return '성인'
                elif choice == 2 and 13 <= age < 19:
                    return '중고등학생'
                elif choice == 3 and age < 13:
                    return '유아'
                else:
                    print("선택한 연령대가 나이와 맞지 않습니다. 다시 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def select_num_people(self):
        print("인원을 선택하세요 (1~5명):")
        while True:
            try:
                num_people = int(input())
                if 1 <= num_people <= 5:
                    return num_people
                else:
                    print("잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def check_age_restriction(self, movie, num_people):
        print(f"{movie.title}의 연령 제한은 {movie.age_limit}세 이상입니다.")
        ages = []
        for i in range(num_people):
            while True:
                try:
                    age = int(input(f"인원 {i+1}의 나이를 입력하세요: "))
                    if age >= movie.age_limit:
                        ages.append(age)
                        break
                    else:
                        print(f"해당 영화는 {movie.age_limit}세 이상만 관람할 수 있습니다. 나이가 적합하지 않습니다.")
                        return False
                except ValueError:
                    print("숫자를 입력하세요.")
        return ages

    def make_reservation(self):
        movie = self.select_movie()
        if movie:
            num_people = self.select_num_people()
            ages = self.check_age_restriction(movie, num_people)
            if ages:
                date = self.select_date()
                time = self.select_time(movie)
                seats = self.select_seat(movie, time, num_people)

                total_cost = 0
                age_groups = []
                for i, age in enumerate(ages):
                    print(f"인원 {i+1}의 연령대를 선택하세요:")
                    age_group = self.select_age_group(age)
                    total_cost += self.ticket_prices[age_group]
                    age_groups.append(age_group)

                reservation_info = {
                    "영화": movie.title,
                    "날짜": date.date(),
                    "시간": time,
                    "좌석": seats,
                    "연령대": age_groups,
                    "총액": total_cost
                }
                self.reservations.append(reservation_info)

                print(f"\n예약 정보:\n영화: {movie.title}\n날짜: {date.date()}\n시간: {time}\n좌석: {', '.join(seats)}\n연령대: {', '.join(age_groups)}\n총액: {total_cost}원")

                confirm = input("결제하시겠습니까? (yes/no): ")
                if confirm.lower() == "yes":
                    print("결제가 완료되었습니다!")
                else:
                    print("예약이 취소되었습니다.")
                    self.reservations.pop()
                print()
            else:
                print("예약이 취소되었습니다.\n")

    def view_reservations(self):
        print("\n예매 내역 조회:")
        if not self.reservations:
            print("예매 내역이 없습니다.")
        else:
            for i, reservation in enumerate(self.reservations):
                print(f"{i+1}. 영화: {reservation['영화']}, 날짜: {reservation['날짜']}, 시간: {reservation['시간']}, 좌석: {', '.join(reservation['좌석'])}, 연령대: {', '.join(reservation['연령대'])}, 총액: {reservation['총액']}원")
        print()

    def run(self):
        while True:
            print("영화 예매 시스템에 오신 것을 환영합니다")
            print("1. 영화 예매")
            print("2. 예매 내역 조회")
            print("3. 종료")
            try:
                choice = int(input("번호를 선택하세요: "))
                if choice == 1:
                    self.make_reservation()
                elif choice == 2:
                    self.view_reservations()
                elif choice == 3:
                    print("프로그램을 종료합니다.")
                    self.view_reservations()
                    break
                else:
                    print("잘못된 선택입니다. 다시 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

if __name__ == "__main__":
    system = ReservationSystem()

    system.run()
