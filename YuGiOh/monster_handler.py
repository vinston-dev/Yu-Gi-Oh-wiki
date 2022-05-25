from unicodedata import name
import requests
import json
from typing import Any, List, TypeVar, Callable, Type, cast

class ApiDataManager:
    name: str
    type: str
    desc: str
    atk: int
    defense: int
    level: int
    race: str
    attribute: str

    def __init__(self, name: str, type: str, desc: str, atk: int, defense: int, level: int, race: str, attribute: str) -> None:
        self.name = name
        self.type = type
        self.desc = desc
        self.atk = atk
        self.defense = defense
        self.level = level
        self.race = race
        self.attribute = attribute
    # Gets the json data from keys to return it into ApiDataManager
    @staticmethod
    def get_api_data(obj: Any) -> 'ApiDataManager':
        name = obj.get("name")
        type = obj.get("type")
        desc = obj.get("desc")
        atk = obj.get("atk")
        defense = obj.get("def")
        level = obj.get("level")
        race = obj.get("race")
        attribute = obj.get("attribute")

        return ApiDataManager(name, type, desc, atk, defense, level, race, attribute)


class Card():
    name: str
    desc: str
    type: str
    url: str

    def __init__(self, name: str, desc: str, type: str) -> None:
        self.name = name
        self.desc = desc
        self.type = type


class Monster(Card):
    atk: int
    defense: int
    level: int
    race: str
    attribute: str
    def __init__(self, card: ApiDataManager) -> None:
        super().__init__(card.name, card.desc, card.type)
        self.atk = card.atk
        self.defense = card.defense
        self.level = card.level
        self.race = card.race
        self.attribute = card.attribute


class Trap(Card):
    def __init__(self, card: ApiDataManager) -> None:
        super().__init__(card.name, card.desc, card.type)


class Spell(Card):
    def __init__(self, card: ApiDataManager) -> None:
        super().__init__(card.name, card.desc, card.type)


T = TypeVar("T")
# we can take in any function that takes in argument of type ApiDataManager and returns None
def get_card_data(card_name: str, card_type: Callable[[ApiDataManager], None]) -> T:
    # calls api to get data about inputed card name
    response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?name='+ card_name)
    data = response.json()
    if "error" in data:       
        return None
    # puts api card data into ApiDataManager instance
    result = ApiDataManager.get_api_data(data.get("data")[0])
    # returns data into either Monster, Trap or Spell class
    result_monster = card_type(result) 
    result_monster.url = data["data"][0]["card_images"][0]["image_url"]
    return result_monster

def print_card_data(monster: T):
    attrs = vars(monster)
    # %s gets swapped out for the attributes name and value
    for item in attrs.items():
        if item[1] != None and item[0] != "url":
            print(f"{item[0]}: {item[1]}\n")
