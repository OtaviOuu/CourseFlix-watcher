import schedule
import time

from courseflix import CourseFlixManager
from telegrambot import TelegramBot


def job():
    bot = TelegramBot()
    manager = CourseFlixManager()

    new_courses = manager.get_new_courses()

    if new_courses:
        message = "🚀 Novos cursos foram encontrados! 🚀\n\n\n"
        for course in new_courses:
            message += f"📚 {course}\n\n"

        bot.send_notification(message)
    else:
        print("Nenhum curso novo encontrado.")


if __name__ == "__main__":

    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
