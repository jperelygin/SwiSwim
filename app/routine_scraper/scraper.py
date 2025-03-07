from dataclasses import dataclass, field
import re
import ijson


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
        self.json_file = html_file
        self.target_hashtags = {"#level1", "#level2", "#level3"}
        self.styles = {"#комплекс", '#брасс', '#кроль', '#спина'}
        self.pre_workout_text = "Разминка"
        self.main_workout_text = "Основное"
        self.post_workout_text = "Закупка"
        self.capacity_text = "Объем"

    def 


if __name__ == "__main__":
    sc = Scraper('result.json')
    sc.scrape_messages()
    print(sc.messages)
    print(sc.looked)
    print(sc.get_route(message_id=19))
