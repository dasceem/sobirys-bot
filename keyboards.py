from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать анкету", callback_data="start_quiz")],
        [InlineKeyboardButton(text="Моя тренировка", callback_data="my_workout")],
        [InlineKeyboardButton(text="Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="Тарифы", callback_data="tariffs")],
    ])

def quiz_goal():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Похудение", callback_data="q_goal:lose")],
        [InlineKeyboardButton(text="Масса", callback_data="q_goal:mass")],
        [InlineKeyboardButton(text="Сила", callback_data="q_goal:strength")],
        [InlineKeyboardButton(text="Выносливость", callback_data="q_goal:endurance")],
        [InlineKeyboardButton(text="Здоровье", callback_data="q_goal:health")],
    ])

def quiz_location():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дома", callback_data="q_loc:home")],
        [InlineKeyboardButton(text="В зале", callback_data="q_loc:gym")],
        [InlineKeyboardButton(text="На улице", callback_data="q_loc:street")],
        [InlineKeyboardButton(text="Смешанно", callback_data="q_loc:mixed")],
    ])

def quiz_equipment():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ничего", callback_data="q_eq:none")],
        [InlineKeyboardButton(text="Гантели", callback_data="q_eq:dumbbells")],
        [InlineKeyboardButton(text="Резинки", callback_data="q_eq:bands")],
        [InlineKeyboardButton(text="Штанга", callback_data="q_eq:barbell")],
        [InlineKeyboardButton(text="Полный зал", callback_data="q_eq:full")],
    ])

def quiz_experience():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новичок", callback_data="q_exp:beginner")],
        [InlineKeyboardButton(text="Средний", callback_data="q_exp:intermediate")],
        [InlineKeyboardButton(text="Продвинутый", callback_data="q_exp:advanced")],
    ])

def quiz_frequency():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="2 раза", callback_data="q_freq:2")],
        [InlineKeyboardButton(text="3 раза", callback_data="q_freq:3")],
        [InlineKeyboardButton(text="4 раза", callback_data="q_freq:4")],
        [InlineKeyboardButton(text="5+", callback_data="q_freq:5")],
    ])

def quiz_duration():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="15 мин", callback_data="q_dur:15")],
        [InlineKeyboardButton(text="30 мин", callback_data="q_dur:30")],
        [InlineKeyboardButton(text="45 мин", callback_data="q_dur:45")],
        [InlineKeyboardButton(text="60 мин", callback_data="q_dur:60")],
    ])

def quiz_limitations():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Нет ограничений", callback_data="q_lim:none")],
        [InlineKeyboardButton(text="Спина", callback_data="q_lim:back")],
        [InlineKeyboardButton(text="Колени", callback_data="q_lim:knees")],
        [InlineKeyboardButton(text="Плечи", callback_data="q_lim:shoulders")],
        [InlineKeyboardButton(text="Другое", callback_data="q_lim:other")],
    ])

def quiz_tariff():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Free (0 ₽)", callback_data="q_tar:free")],
        [InlineKeyboardButton(text="Lite (99 ₽/мес)", callback_data="q_tar:lite")],
        [InlineKeyboardButton(text="Pro (249 ₽/мес)", callback_data="q_tar:pro")],
        [InlineKeyboardButton(text="Elite (499 ₽/мес)", callback_data="q_tar:elite")],
    ])

def workout_controls(exercise_idx, total, has_timer=False, timer_sec=0):
    buttons = []
    if has_timer and timer_sec > 0:
        buttons.append([InlineKeyboardButton(text="Таймер " + str(timer_sec) + " сек", callback_data="timer:" + str(timer_sec))])
    buttons.append([InlineKeyboardButton(text="Готово, дальше", callback_data="next_ex:" + str(exercise_idx))])
    if exercise_idx > 0:
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="prev_ex:" + str(exercise_idx))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def finish_workout():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Завершить тренировку", callback_data="finish_workout")],
    ])

def after_workout():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="Следующая тренировка", callback_data="my_workout")],
        [InlineKeyboardButton(text="В меню", callback_data="main_menu")],
    ])

def back_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В меню", callback_data="main_menu")],
    ])

def workout_start_or_change():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать тренировку", callback_data="my_workout")],
        [InlineKeyboardButton(text="Изменить план", callback_data="start_quiz")],
        [InlineKeyboardButton(text="В меню", callback_data="main_menu")],
    ])
