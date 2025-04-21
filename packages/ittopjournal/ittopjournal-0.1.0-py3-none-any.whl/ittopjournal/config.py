
###  ДАННЫЕ ДЛЯ ПАРСИНГА ЗАГОЛОВКОВ  ###
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36"
ORIGIN="https://journal.top-academy.ru"
REFERER="https://journal.top-academy.ru/"


###  URL API ОФИЦИАЛЬНОГО СЕРВЕРА JOURNAL  ###

# URL основа
BASE_API_URL = "https://msapi.top-academy.ru/api/v2"
# URL для авторизации пользователей, чтобы получать актуальные токены
AUTH_URL = f"{BASE_API_URL}/auth/login"
# URL для отправки пар которые были оценены
EVALUATION_LESSONS = f"{BASE_API_URL}/feedback/students/evaluate-lesson"
# URL для получения списка пар которые нужно оценить
EVALUATION_LESSONS_LIST = f"{BASE_API_URL}/feedback/students/evaluate-lesson-list"
# URL для получения feedback info (Отзывы о студенте)
FEEDBACK_INFO = f"{BASE_API_URL}/reviews/index/list"
# URL для получения информации о среднем балле студента
METRIC_GRADE = f"{BASE_API_URL}/dashboard/chart/average-progress"
# URL для получения информации о посещениях студента
METRIC_ATTENDANCE = f"{BASE_API_URL}/dashboard/chart/attendance"
# URL для получения рейтинга группы студентов
RATING_GROUP = f"{BASE_API_URL}/dashboard/progress/leader-group"
# URL для получения рейтинга потока для студентов
RATING_STREAM = f"{BASE_API_URL}/dashboard/progress/leader-stream"
# URL для получения массива с расписанием пар с сервера сайта по дате
SCHEDULE_URL = f"{BASE_API_URL}/schedule/operations/get-by-date?date_filter={{date}}"
# URL для получения информации о посещениях занятий и оценки
STUDENT_VISITS = f"{BASE_API_URL}/progress/operations/student-visits"
# URL для получения user info (По типу группы и т.д)
USER_INFO = f"{BASE_API_URL}/settings/user-info"