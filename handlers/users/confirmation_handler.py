from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.all_boards import Boards
from states.state import BotStates
from loader import card_states
from SmartAgentObject import agent
import asyncio


async def confirmation_options_and_start_parsing(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        form_data = await state.get_data()
        try:
            form_data.pop("street_or_station")
        except KeyError:
            pass

        try:
            form_data.pop("streets_and_stations_dict")
        except KeyError:
            pass
        
        await state.set_data(form_data)

        await message.answer("Введите улицу или метро для поиска", reply_markup = Boards.streets_or_station_input_board)
        await BotStates.street_or_station_input_state.set()
        return

    elif message.text == "Указать параметры с самого начала":
        await state.set_data({
            "form_type":list(),
            "form_type_names":list()

        })
        #res = await state.get_data()
        #print(res)
        await message.answer("Выберите тип объявления", reply_markup = Boards.form_type_board)
        await BotStates.form_type_state.set()
        return

    elif message.text == "Начать поиск": #Отправка объявлений в бота
        await message.answer("Начинается сбор данных")
        form_data = await state.get_data()

        form_type = form_data["form_type"]
        price_from = form_data["price_from"]
        price_to = form_data["price_to"]
        sell_or_rent = form_data["sell_or_rent"]
        streets_and_stations_dict = form_data.get("streets_and_stations_dict")
        print(streets_and_stations_dict)
        street_or_station = form_data.get("street_or_station")
        streets_and_stations_data = (street_or_station[0], streets_and_stations_dict) if streets_and_stations_dict else ""

        searched_data = agent.get_all_cards(sell_or_rent, price_from, price_to, streets_or_stations = (street_or_station[0], streets_and_stations_dict), user_id = message.from_id, rooms = form_type) if streets_and_stations_data != "" else agent.get_all_cards(sell_or_rent, price_from, price_to, user_id = message.from_id, rooms = form_type)
        if searched_data == None:
            await message.answer("По данным параметрам ничего не найдено")
            return
        #print(searched_data)

        for form in searched_data:
            #print(form["address_quick"])
            message_about_form = f"Название: {form['name']}\n\n"
            message_about_form += f"Жилая площадь: {form.get('living_area', 'Информация отсутствует')}\n\n"
            message_about_form += f"Площадь кухни: {form.get('kitchen_area', 'Информация отсутствует')}\n\n"
            message_about_form += f"Цена: {form.get('price')} | {form.get('area_price')}\n\n" if sell_or_rent and "Земля" not in form.get("name") and "Доля" not in form.get("name") and "Комната" not in form.get("name") else f"Цена: {form.get('price')}\n\n"
            message_about_form += f"Адресс: {form.get('address_area')} | {form.get('address_quick')}\n\n" if form["address_quick"] != "" else f"Адресс: {form.get('address_area')}\n\n" if form.get('address_area') != None else ""
            message_about_form += f"Описание: {form.get('description')}\n\n"
            message_about_form += f"Метро: {form.get('metro').get('name')} {form.get('metro').get('lenght')}\n\n" if form.get("metro").get("name") != "" else ""
            message_about_form += f"Дата размещения: {form.get('date')}\n\n"
            #message_about_form += f"Номер телефона: {form.get('phone')[0]} {form.get('phone')[1]}\n" if form.get("phone")[1] != None else "Номер телефона: Данные не доступны"
            message_about_form += f"Номер телефона: {form.get('phone')[1]}\n" if form.get("phone")[1] != None else "Номер телефона: Данные не доступны"
            media = types.MediaGroup()
            for image in form["images"]:
                if form["images"].index(image) == 10:
                    break
                media.attach_photo(types.InputFile(f"./parsingModule/images/{image}"))

            await message.answer(message_about_form, parse_mode = "HTML") #TODO обход защиты от флуда
            await message.answer_media_group(media)
            agent.delete_all_photo(form["images"])
            await asyncio.sleep(3)
            #TODO стейт для отключения возможности контактирования с ботом
            #TODO переход в начальное меню

        return

    await message.answer("Пожалуйста воспользуйтесь клавиатурой")
    return
    



def register_all_confirmation_handlers(dp: Dispatcher):
    dp.register_message_handler(confirmation_options_and_start_parsing, state = BotStates.confirmation_state)