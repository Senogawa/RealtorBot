from configparser import ConfigParser


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
        },
        "subscriptions_prices":{
            "1-month":int(cnf.get("SUBSCRIPTIONS", "1_month")) / 100,
            "2-month":int(cnf.get("SUBSCRIPTIONS", "2_month")) / 100,
            "3-month":int(cnf.get("SUBSCRIPTIONS", "3_month")) / 100
        }
    }
    message_text = "<b>[Параметры администраторов]</b>\n"
    message_text += f"ID администраторов: {config_data.get('admins')}\n\n"
    message_text += "<b>[Параметры для обычных пользователей]</b>\n"
    message_text += f"Количество форм для поиска: {config_data.get('smartagent').get('forms_quantity')}\n\n"
    message_text += f"<b>[Параметры для тестовых пользователей]</b>\n"
    message_text += f"Количество пробных поисков: {config_data.get('smartagent').get('trials_finds_quantity')}\n"
    message_text += f"Количество пробных форм для поиска: {config_data.get('smartagent').get('trials_finds_form_quantity')}\n"
    message_text += f"Стоимость подписок:\n        1 - месяц: {config_data.get('subscriptions_prices').get('1-month')}₽\n        2 - месяц: {config_data.get('subscriptions_prices').get('2-month')}₽\n        3 - месяц: {config_data.get('subscriptions_prices').get('3-month')}₽\n\n"
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
        "root": cnf.get("TELEGRAM", "root"),
        "smartagent":{
            "forms_quantity": cnf.get("SMARTAGENT", "forms_quantity"),
            "trials_finds_quantity": cnf.get("SMARTAGENT", "trials_finds_quantity"),
            "trials_finds_form_quantity": cnf.get("SMARTAGENT", "trials_finds_form_quantity")
        }
    }
    return config_data

def set_config_parameter(section: str, parameter: str, value: str, add_admin: bool = False):
    """
    Изменение параметров в конфигурационном файле
    """

    config = ConfigParser()
    config.read("conf.ini")
    if section == "TELEGRAM" and parameter == "admins" and add_admin:
        admins = config.get(section, parameter)
        if len(admins) == 0:
            admins += f"{value}"
        else:
            admins += f", {value}"

        config.set(section, parameter, admins)
        with open("conf.ini", "w") as f:
            config.write(f)
        return

    elif section == "TELEGRAM" and parameter == "admins" and not add_admin:
        value = value.split(",")
        value = ", ".join(value)
        config.set(section, parameter, value)
        with open("conf.ini", "w") as f:
            config.write(f)
        return

    config.set(section, parameter, value)
    with open("conf.ini", "w") as f:
        config.write(f)

    

if __name__ == "__main__":
    print(get_config_data())