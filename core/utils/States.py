from aiogram.fsm.state import StatesGroup, State

class Stateses(StatesGroup):
    INPUT_HREF = State()
    INPUT_TEXT = State()
    NONE = State
