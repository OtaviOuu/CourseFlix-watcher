import schedule
import time

from courseflix import CourseFlixManager


def job():
    manager = CourseFlixManager()
    new_courses = manager.get_new_courses()
    print(new_courses)


if __name__ == "__main__":
    schedule.every(2).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
