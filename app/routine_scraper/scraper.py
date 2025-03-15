from dataclasses import dataclass, field
from routine import Routine
import re
import ijson
from bs4 import BeautifulSoup


@dataclass
class Route:
    pre_workout: str = field(init=False)
    main_workout: str = field(init=False)
    post_workout: str = field(init=False)
    capacity: int = field(init=False)
    style: str = field(init=False)


class Scraper:
    def __init__(self, json_file):
        self.messages = set()
        self.looked = 0
        self.json_file = json_file
        self.target_hashtags = {"#level1", "#level2", "#level3"}
        self.styles = {"#комплекс", '#брасс', '#кроль', '#спина'}
        self.pre_workout_text = "Разминка"
        self.main_workout_text = "Основное"
        self.post_workout_text = "Закупка"
        self.capacity_text = "Объем"

    def scrape_messages(self):
        with open(self.json_file, 'r', encoding='utf-8') as f:
            for message in ijson.items(f, "messages.item"):
                self.looked += 1
                if "text_entities" in message:
                    for entity in message["text_entities"]:
                        if isinstance(entity, dict):
                            if entity.get("type") == "hashtag" and entity.get("text") in self.target_hashtags:
                                self.messages.add(message.get("id"))

    def get_route(self, message_id):
        route = Route()
        with open(self.json_file, 'r', encoding='utf-8') as f:
            for message in ijson.items(f, "message.item"):
                if message.get("id") == message_id:
                    entities = message["text_entities"]
                    for i, entity in enumerate(entities):
                        # Prework
                        if isinstance(entity, dict) and self.pre_workout_text in entity.get("text"):
                            if i + 1 < len(entities):
                                route.pre_workout = entity[i+1]
                        # Main
                        if isinstance(entity, dict) and self.main_workout_text in entity.get("text"):
                            if i + 1 < len(entities):
                                route.main_workout = entity[i+1]
                        # Post
                        if isinstance(entity, dict) and self.post_workout_text in entity.get("text"):
                            if i + 1 < len(entities):
                                route.post_workout = entity[i+1]
                        # Capacity
                        if isinstance(entity, dict) and self.capacity_text in entity.get("text"):
                            route.capacity = self.get_capacity_from_text(entity.get("text"))
                        # Style
                        if isinstance(entity, dict) and entity.get("type") == "hashtag":
                            if entity.get("text") in self.styles:
                                route.style = entity.get("text")
        return route

    def get_capacity_from_text(self, text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group(0))

class HtmlScraper:
    def __init__(self, html_file):
        self.messages = set()
        self.looked = 0
        self.file = html_file
        self.target_hashtags = {"#level1", "#level2", "#level3"}
        self.styles = {"#комплекс", '#брасс', '#кроль', '#спина'}
        self.pre_workout_text = "Разминка"
        self.main_workout_text = "Основное"
        self.post_workout_text = "Закупка"
        self.capacity_text = "Объем"

    def scrap_file(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        all_text_elements = soup.find_all("div", class_="text")
        routine_texts = set()
        for element in all_text_elements:
            links = element.find_all("a")
            if self.target_hashtags.intersection([link.get_text() for link in links]):
                routine_texts.add(element.decode_contents().replace("<br/>", "\n"))
        routines = set()
        workout_map = {
            self.pre_workout_text: "pre_workout",
            self.main_workout_text: "workout",
            self.post_workout_text: "post_workout"
        }
        level_map = {level: num+1 for num, level in enumerate(self.target_hashtags)}
        for text in routine_texts:
            routine = Routine()
            strong_separated = [t.strip().replace(":", "") for t in text.replace("</strong>", "<strong>").split("<strong>")]
            for i, text_element in enumerate(strong_separated):
                if text_element in workout_map:
                    setattr(routine, workout_map[text_element],
                            strong_separated[i+1] if i + 1 < len(strong_separated) else None)
                if self.capacity_text in text_element:
                    routine.capacity = text_element.split()[-1]
            routines.add(routine)
        return routines


if __name__ == "__main__":
    sc = HtmlScraper('messages.html')
    x = sc.scrap_file()
    for i in x:
        print(i)
    print(len(x))
