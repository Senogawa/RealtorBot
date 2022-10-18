from aiogram.dispatcher.filters.state import StatesGroup, State

class BotStates(StatesGroup):
    form_type_state = State()
    multi_form_type_state = State()
    accept_form_type_state = State()
    sell_of_rent_state = State()
    price_from_state = State()
    price_to_state = State()
    street_or_station_input_state = State()
    street_of_station = State()
    street_or_station_choice_state = State()
    confirmation_state = State()