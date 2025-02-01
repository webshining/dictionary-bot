from aiogram.fsm.state import State, StatesGroup


class WordState(StatesGroup):
    add = State()
    dictionary_create = State()
