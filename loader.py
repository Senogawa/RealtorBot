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

def create_config_data_message() -> tuple:
    """
    Выгрузка данных из конфига и составление сообщения
    """

    cnf = ConfigParser()
    cnf.read("conf.ini")

    config_data = {
        "admins": cnf.get("TELEGRAM", "admins"),
        "smartagent":{
            "forms_quantity": cnf.get("SMARTAGENT", "forms_quantity"),
            "trials_finds_quantity": cnf.get("SMARTAGENT", "trials_finds_quantity"),
            "trials_finds_form_quantity": cnf.get("SMARTAGENT", "trials_finds_form_quantity")
        }
    }
    message_text = "<b>[Параметры администраторов]</b>\n"
    message_text += f"ID администраторов: {config_data.get('admins')}\n\n"
    message_text += "<b>[Параметры для обычных пользователей]</b>\n"
    message_text += f"Количество форм для поиска: {config_data.get('smartagent').get('forms_quantity')}\n\n"
    message_text += f"<b>[Параметры для тестовых пользователей]</b>\n"
    message_text += f"Количество пробных поисков: {config_data.get('smartagent').get('trials_finds_quantity')}\n"
    message_text += f"Количество пробных форм для поиска: {config_data.get('smartagent').get('trials_finds_form_quantity')}\n\n"
    message_text += "Выберите действие: "

    return (config_data, message_text)

def get_config_data():
    """
    Получение данных из конфигурационного файла
    """

    cnf = ConfigParser()
    cnf.read("conf.ini")

    config_data = {
        "admins": cnf.get("TELEGRAM", "admins"),
        "smartagent":{
            "forms_quantity": cnf.get("SMARTAGENT", "forms_quantity"),
            "trials_finds_quantity": cnf.get("SMARTAGENT", "trials_finds_quantity"),
            "trials_finds_form_quantity": cnf.get("SMARTAGENT", "trials_finds_form_quantity")
        }
    }
    return config_data

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


del bot_cnf
del db_cnf
del smart_agent_cnf
