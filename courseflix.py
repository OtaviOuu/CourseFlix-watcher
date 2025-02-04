import requests
from parsel.selector import Selector
import json


class CourseFlixManager:
    def __init__(self):
        self.base_url = "https://courseflix.net/"

    def _load_stored_courses(self) -> list:
        try:
            with open("courses.json", "r") as file:
                return json.load(file)["courses"]
        except FileNotFoundError:
            with open("courses.json", "w") as file:
                json.dump({"courses": []}, file)
                return []

    def _get_selector(self, html_text) -> Selector:
        return Selector(html_text)

    def _save_new_courses(self, new_courses: list[str]) -> None:
        try:
            with open("courses.json", "r+") as file:
                past_courses = json.load(file)
                past_courses["courses"].extend(new_courses)
                file.seek(0)
                file.write(json.dumps(past_courses))
                file.truncate()
        except FileNotFoundError:
            pass

    def get_new_courses(self) -> list:
        response = requests.get(url=f"{self.base_url}/course?page=1")
        html = self._get_selector(response.text)

        title_selector = "a[href^='https://courseflix.net/course/'] span.truncate::text"
        courses_links = html.css(title_selector).getall()

        stored_courses = self._load_stored_courses()
        new_courses = [
            course for course in courses_links if course not in stored_courses
        ]
        if new_courses:
            self._save_new_courses(new_courses)
            return new_courses
        return []
