from aiogram import types
from loader import card_states

class Boards:
    form_type_board = types.ReplyKeyboardMarkup(resize_keyboard = True)
    __form_buttons_main_layer = list(card_states.keys())
    __form_buttons_main_layer.remove("Аренда")
    __form_buttons_main_layer.remove("Продажа")
    __form_buttons_first_layer = list(card_states.get("Квартира")[1].keys())
    __form_buttons_second_layer = list(card_states.get("Коммерческая недвижимость")[1].keys())
    
    form_type_board.add("Выбрать все объявления")
    form_type_board.add(*__form_buttons_main_layer)
    form_type_board.add("Закончить с выбором параметров")

    form_type_flat = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Выбрать все")
    form_type_flat.add(*__form_buttons_first_layer)
    form_type_flat.add("Назад")
    form_type_flat.add("Закончить с выбором параметров")

    form_type_commercian = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Выбрать все")
    form_type_commercian.add(*__form_buttons_second_layer)
    form_type_commercian.add("Назад")
    form_type_commercian.add("Закончить с выбором параметров")

    accept_form_data_board = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Все верно")
    accept_form_data_board.add("Заполнить заново")

    sell_or_rent_board = types.ReplyKeyboardMarkup(resize_keyboard = True).add(*["Аренда", "Продажа"])
    sell_or_rent_board.add("Назад")

    price_from_to_board = types.ReplyKeyboardMarkup(resize_keyboard = True)
    price_from_to_board.add("Не указывать ценовой диапазон")
    price_from_to_board.add("Назад")

    streets_or_station_input_board = types.ReplyKeyboardMarkup(resize_keyboard = True)
    streets_or_station_input_board.add("Не выбирать улицу")
    streets_or_station_input_board.add("Назад")

    confirmation_board = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Начать поиск")
    confirmation_board.add("Назад")
    confirmation_board.add("Указать параметры с самого начала")

    back_button_board = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Назад")

    all_form_answers = [*__form_buttons_first_layer, *__form_buttons_main_layer, *__form_buttons_second_layer, "Выбрать все объявления", "Выбрать все", "Назад"]
if __name__ == "__main__":
    p = Boards()