from dataclasses import dataclass
from configparser import ConfigParser


@dataclass
class Bot:
    token:str
    admins:str

@dataclass
class Database:
    user:str
    password:str
    host:str
    port:int
    db:str

@dataclass
class SmartAgent:
    user:str
    password:str


cnf = ConfigParser()
cnf.read("conf.ini")

bot_cnf = cnf["TELEGRAM"]
db_cnf = cnf["DATABASE"]
smart_agent_cnf = cnf["SMARTAGENT"]
bot_meta = Bot(bot_cnf["token"], bot_cnf["admins"].split(","))
db_meta = Database(db_cnf["user"], db_cnf["password"], db_cnf["host"], int(db_cnf["port"]), db_cnf["db"])
smartagent_meta = SmartAgent(smart_agent_cnf["user"], smart_agent_cnf["password"])

card_states = {
    "Аренда":"4", # section
    "Продажа":"3", #section
    
    "Квартира":(("24", "36", "1", "2", "3", "4", "5", "6", "7", "8"),
        {
        "Студия":"24", #rooms[0]
        "СвобПлан":"36",
        "1-комн":"1",
        "2-комн":"2",
        "3-комн":"3",
        "4-комн":"4",
        "5-комн":"5",
        "6+комн":"6"
        }),
    
    "Комната":"21", #rooms[0]
    "Койко-место":"20",
    "Дом":"10",
    "Доля":"22",
    "Таунхаус":"9",
    "Участок":"11",
    "Коммерческая недвижимость":(("23", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35"),{
        "Офис":"23",
        "Склад":"26",
        "ОбщПит":"28",
        "Здание":"30",
        "Автосервис":"32",
        "БытУслуги":"34",
        "ТоргПомещение":"25",
        "СвобНазначения":"27",
        "Гараж/Паркинг":"29",
        "Производство":"31",
        "ГотовыйБизнес":"33",
        "КоммЗемля":"35"
    }) #premise 2

}

payments_or_test_trial_message = "Oops!\nПохоже у Вас нет подписки на использование данного бота\nЖелаете приобрести подписку или попробовать тестовый период?"

del bot_cnf
del db_cnf
del smart_agent_cnf
