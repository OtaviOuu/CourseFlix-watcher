import requests
from parsel.selector import Selector


class CourseFlixManager:
    def __init__(self):
        self.base_url = "https://courseflix.net/"

    def _load_stored_courses(self) -> list:
        with open("courses.txt", "r") as file:
            return [line.rstrip() for line in file]

    def _get_selector(self, html_text) -> Selector:
        return Selector(html_text)

    def _write_courses(self, courses: list):
        with open("courses.txt", "a") as file:
            for course in courses:
                file.write(course + "\n")

    def _write_to_counter(self, new_courses_quantity: int):
        with open("new.txt", "r") as file:
            new_courses_stack = int(file.read().strip())
        with open("new.txt", "w") as file:
            file.write(str(new_courses_stack + new_courses_quantity))

    def get_new_courses(self) -> list:
        response = requests.get(url=f"{self.base_url}/course?page=1")
        html = self._get_selector(response.text)
        courses_links = html.css(
            "a[href^='https://courseflix.net/course/'] span.truncate::text"
        ).getall()

        stored_courses = self._load_stored_courses()
        new_courses = [
            course for course in courses_links if course not in stored_courses
        ]
        if new_courses:
            self._write_courses(new_courses)
            self._write_to_counter(len(new_courses))
            return new_courses
        return []
