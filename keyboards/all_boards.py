from aiogram import types
from loader import card_states

class Boards:
    form_type_board = types.ReplyKeyboardMarkup(resize_keyboard = True)
    __form_buttons_main_layer = list(card_states.keys())
    __form_buttons_first_layer = list(card_states.get("Квартира")[1].keys())
    __form_buttons_second_layer = list(card_states.get("Коммерческая недвижимость")[1].keys())
    
    form_type_board.add("Выбрать все объявления")
    form_type_board.add(*__form_buttons_main_layer)

    form_type_flat = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Выбрать все")
    form_type_flat.add(*__form_buttons_first_layer)

    form_type_commercian = types.ReplyKeyboardMarkup(resize_keyboard = True).add("Выбрать все")
    form_type_commercian.add(*__form_buttons_second_layer)

    all_form_answers = [__form_buttons_first_layer, __form_buttons_main_layer, __form_buttons_second_layer, "Выбрать все объявления", "Выбрать все"]
if __name__ == "__main__":
    p = Boards()