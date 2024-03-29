import requests
from fake_useragent import UserAgent
from loader import smartagent_meta
from loader import card_states
import json
import os
import time
from config_module import get_config_data
import asyncio
import aiohttp
from database_methods import run_command
import copy

class SmartAgentClient:
    phpsessionid = ""
    def __init__(self):
        """
        Инициализация первичной сессии
        """

        headers = {
            "user-agent":UserAgent().random
        }
        data = {
            "login":smartagent_meta.user,
            "password":smartagent_meta.password,
            "compid":"",
            "fingerprint":"264f832b6e6025c20a49616ad4f51712",
            "timezone":"Europe/Moscow"
        }
        self.session = requests.Session()
        res = self.session.post("https://smartagent.ru/auth/ajax", headers = headers, data = data)
        res = res.json()
        if not res["success"]:
            raise AttributeError("Ошибка инициализации клиента, неверный логин или пароль")

        self.session.cookies.set("pushdealer_token", "8pxry1kgfy")
        self.session.cookies.set("pushdealer_permission", "denied")
        self.headers = {
            "user-agent":UserAgent().random,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            #"Content-Type": "multipart/form-data; boundary=---------------------------793856791064077589889787832688",
            #"Content-Length": "183",
            "Origin": "https://smartagent.ru",
            "Cookie": f"pushdealer_token=8pxry1kgfy; pushdealer_permission=denied; PHPSESSID={self.session.cookies['PHPSESSID']}",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cache-Control": "max-age=0",
            "Host": "smartagent.ru",
            "TE": "trailers"
            }

        self.data = {
            "source[current]":"all",
            "source[all][type_status]":"1",
            "source[all][state_status]":"1",
            "source[all][direct][0]":"1",
            "section":"4",
            "price[type]":"all",
            "price[from]":"",
            "price[to]":"",
            "stage":"all",
            "mode":"list",
            "status":"active",
            "page":"1",
            "force":"1",
            "region":"1",
            "quantity":"15"
            }
        print("Клиент инициализирован")
        

    async def get_streets_and_stations_dict(self, street: str) -> dict:
        """
        Получение списка улиц и станций метро и их id значений
        """

        data = {
            "query": street,
            "region_id": "1",
            "is_search": "1"
        }

        streets_and_stations_dict = {
            "streets":{},
            "stations":{}
        }
        while True:
            try:
                res  = self.session.post("https://smartagent.ru/searcher/index/search2?fingerprint=264f832b6e6025c20a49616ad4f51712", headers = self.headers, data = data)
                await asyncio.sleep(0)
                break
            except requests.exceptions.ConnectionError:
                continue
        streets_and_stations = res.json()
        
        for street in streets_and_stations["payload"]["streets"]:
            streets_and_stations_dict["streets"][street["label"]] = street["id"]
        
        for stations in streets_and_stations["payload"]["stations"]:
            streets_and_stations_dict["stations"][stations["label"]] = stations["id"]

        return streets_and_stations_dict


    async def get_all_cards(self, sell_or_rent: bool, test_user: bool = False, price_from: str = "", price_to: str = "", streets_or_stations:tuple = "", user_id:int = 0, rooms: list = [], message = None) -> list:
        """
        Получение списка любой недвижимости\n
        streets_or_stations=('Москва г, Кандинского ул', get_streets_and_stations_dict(street: str))
        """

        async def get_phone(id: str) -> tuple:
            """
            Получение номера телефона
            """
            #return (None, None)
            number = self.session.post(
                    url = "https://smartagent.ru/public-object/open-phone?fingerprint=264f832b6e6025c20a49616ad4f51712",
                    headers = self.headers,
                    data = {
                        "id":f"{id}",
                        "property":"1"
                    }
                )
            await asyncio.sleep(0)
            number = number.json()
            #print(number)
            if not number.get("success"):
                return (None, None)

            number_tuple = (number["payload"].get("name"), number["payload"].get("phone"))
            if dict is type(number_tuple[1]):
                return ("Ссылка на объект", number_tuple[1].get("url"))
            return number_tuple

        # print(get_phone("57351350"))
        # os._exit(0)

        data = copy.deepcopy(self.data)

        if sell_or_rent: #TODO maybe problems
            data["section"] = card_states["Продажа"]

        if streets_or_stations != "" and streets_or_stations[0] in streets_or_stations[1]["streets"].keys():
            data["streets[0]"] = streets_or_stations[1]["streets"][streets_or_stations[0]]

        if streets_or_stations != "" and streets_or_stations[0] in streets_or_stations[1]["stations"].keys():
            data["stations[0]"] = streets_or_stations[1]["stations"][streets_or_stations[0]]

        if len(rooms) != 0:
            for id, room in enumerate(rooms):
                data[f"rooms[{id}]"] = room 
        config_data = get_config_data()
        if test_user:
            test_user_info = await run_command(f"SELECT * FROM test_users WHERE test_member_id='{message.from_id}'")
            test_user_info = test_user_info[0]
            data["quantity"] = test_user_info['trials_finds_form_quantity']

        else:
            data["quantity"] = config_data.get("smartagent").get("forms_quantity")

        data["price[from]"] = price_from
        data["price[to]"] = price_to
        #print(self.data)
        req = self.session.post("https://smartagent.ru/search2/search?fingerprint=264f832b6e6025c20a49616ad4f51712", headers = self.headers, data = data)
        cards_dict = req.json()
        #print(cards_dict)
        if cards_dict["payload"]["total"] == 0:
            print(cards_dict)
            return None

        all_cards = list() #Список со всеми объявлениями
        card_dict = dict() #Содержимое all_cards
        
        for card in cards_dict["payload"]["rows"]:
            
            i = 0
            images = []
            card_dict = {}
            if "Земля" not in card.get("caption"):
                card_dict["name"] = f"{card.get('caption')}, {card.get('total_area')}м², {card.get('floor')}/{card.get('floors')} эт." #TODO продолжить наполнение, затем конкретный поиск
                card_dict["living_area"] = card.get("living_area")
                card_dict["kitchen_area"] = card.get("kitchen_area")
            else:
                card_dict["name"] = f"{card.get('caption')}, {card.get('land_area')} сот."
            card_dict["price"] = card["price"].get("RUB")
            if "Земля" not in card.get("caption") and "Доля" not in card.get("caption") and "Комната" not in card.get("caption"):
                print(card_dict["name"])
                if sell_or_rent:
                    card_dict["area_price"] = card["price"]["area"].get("RUB")
            card_dict["id"] = str(card.get("id"))
            card_dict["metro"] = {
                "name":card.get("metro_station"),
                "lenght":card.get("metro_distance")
            }
            card_dict["date"] = card["date"].get("date")
            card_dict["address_area"] = card.get("address_area")
            card_dict["address_quick"] = card.get("address_quick")
            card_dict["description"] = card.get("description") if  'Объект имеет статус "Эксклюзивный источник"' not in card.get("description") else "Информация недоступна" #TODO убрать комментарий
            card_dict["phone"] = await get_phone(card_dict.get("id"))
            try: #Проверка на доступность фото
                if card["images"][0].get("blured"):
                    print("!")
                    await asyncio.sleep(0.1)
                    images.append("No_photo.jpg")
                    card_dict["images"] = images
                    all_cards.append(card_dict)
                    continue

            except IndexError:
                images.append("No_photo.jpg")
                card_dict["images"] = images
                all_cards.append(card_dict)
                continue

            for image in card.get("images"):
                while True:
                    try:
                        async with aiohttp.request("GET", image.get("img"), headers = {"user-agent":UserAgent().random}) as response:
                        #req = requests.get(image.get("img"), headers = {"user-agent":UserAgent().random}) #TODO maybe problems here from async
                            req_status = response.status
                            req_content = await response.read()
                        await asyncio.sleep(0)
                    except requests.exceptions.ConnectionError:
                        req_status = 503
                        break

                    #print(image.get("img"))

                    if req_status == 200:
                        break

                    elif req_status == 503:
                        break
                    elif req_status == 404:
                        break
                    elif req_status == 403:
                        break

                    await asyncio.sleep(0.1) #asyncio
                if req_status == 503 or req_status == 404 or req_status == 403:
                    images.append("No_photo.jpg")
                    continue
                image_name = f"{card_dict.get('id')}_{user_id}_{i}.jpg"
                with open(f"./parsingModule/images/{card_dict.get('id')}_{user_id}_{i}.jpg", "wb") as f:
                    f.write(req_content)

                i += 1
                images.append(image_name)

            card_dict["images"] = images
            all_cards.append(card_dict)
            
            
        return all_cards


                
    def delete_all_photo(self, images: list):
        """
        Удаление всех использованных фото
        """

        for image in images:
            if image == "No_photo.jpg" or image == "Нет возможности получить фото":
                continue

            os.remove(f"./parsingModule/images/{image}")

    def test_requests(self, id):
        #cook = requests.cookies.create_cookie("nbtmp", "=MjNzkwMTc0ODA1N")
        cook1 = requests.cookies.create_cookie("nbtmpp", "dJyWyI3OTAxNzQ4MDU2MyIsIjc5MDE3NDgwNTYzNyIsIjc3OTAxNzQ4MDU2M")
        #self.session.cookies.set_cookie(cook)
        self.session.cookies.set_cookie(cook1)
        print(self.session.cookies)
        number = self.session.post(
        url = "https://smartagent.ru/public-object/open-phone?fingerprint=264f832b6e6025c20a49616ad4f51712",
        headers = self.headers,
        data = {
            "id":f"{id}",
            "property":"4"
            }
        )
        print(number)
        number = number.json()
        print(number)

if __name__ == "__main__":
    s = SmartAgentClient()
    # st = s.get_streets_and_stations_dict("Кантемировская")
    # # print(st)
    # k = s.get_all_cards(True, streets_or_stations=('Кантемировская', st))
    # # print(k)
    # # #rooms = ["23", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35"]
    # # for im in k:
    # #     s.delete_all_photo(im["images"])
    s.test_requests(57849828)
    