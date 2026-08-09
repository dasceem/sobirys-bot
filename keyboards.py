from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Начать анкету", callback_data="start_quiz")],
        [InlineKeyboardButton(text="💪 Моя тренировка", callback_data="my_workout")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="💎 Тарифы", callback_data="tariffs")],
    ])

def quiz_goal(selected=None):
    if selected is None:
        selected = []
    def btn(text, data):
        mark = "✅ " if data in selected else "⬜ "
        return InlineKeyboardButton(text=mark + text, callback_data="q_goal:" + data)
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🎯 Похудение", "lose"), btn("💪 Масса", "mass")],
        [btn("🏋️ Сила", "strength"), btn("🏃 Выносливость", "endurance")],
        [btn("❤️ Здоровье", "health")],
        [InlineKeyboardButton(text="Готово ✅", callback_data="q_goal:done")],
    ])

def quiz_location(selected=None):
    if selected is None:
        selected = []
    def btn(text, data):
        mark = "✅ " if data in selected else "⬜ "
        return InlineKeyboardButton(text=mark + text, callback_data="q_loc:" + data)
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🏠 Дома", "home"), btn("🏢 В зале", "gym")],
        [btn("🌳 На улице", "street"), btn("🔄 Смешанно", "mixed")],
        [InlineKeyboardButton(text="Готово ✅", callback_data="q_loc:done")],
    ])

def quiz_equipment(selected=None):
    if selected is None:
        selected = []
    def btn(text, data):
        mark = "✅ " if data in selected else "⬜ "
        return InlineKeyboardButton(text=mark + text, callback_data="q_eq:" + data)
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🙅 Ничего", "none")],
        [btn("🏋️‍♂️ Гантели", "dumbbells"), btn("🎗️ Резинки", "bands")],
        [btn("🏋️ Штанга", "barbell"), btn("🏭 Полный зал", "full")],
        [InlineKeyboardButton(text="Готово ✅", callback_data="q_eq:done")],
    ])

def quiz_experience():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐣 Новичок", callback_data="q_exp:beginner")],
        [InlineKeyboardButton(text="🦊 Средний", callback_data="q_exp:intermediate")],
        [InlineKeyboardButton(text="🦁 Продвинутый", callback_data="q_exp:advanced")],
    ])

def quiz_frequency():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="2️⃣ Два раза", callback_data="q_freq:2")],
        [InlineKeyboardButton(text="3️⃣ Три раза", callback_data="q_freq:3")],
        [InlineKeyboardButton(text="4️⃣ Четыре раза", callback_data="q_freq:4")],
        [InlineKeyboardButton(text="5️⃣+ Пять и более", callback_data="q_freq:5")],
    ])

def quiz_duration():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏱️ 15 мин — экспресс", callback_data="q_dur:15")],
        [InlineKeyboardButton(text="⏱️ 30 мин — стандарт", callback_data="q_dur:30")],
        [InlineKeyboardButton(text="⏱️ 45 мин — полноценно", callback_data="q_dur:45")],
        [InlineKeyboardButton(text="⏱️ 60 мин — максимум", callback_data="q_dur:60")],
    ])

def quiz_limitations(selected=None):
    if selected is None:
        selected = []
    def btn(text, data):
        mark = "✅ " if data in selected else "⬜ "
        return InlineKeyboardButton(text=mark + text, callback_data="q_lim:" + data)
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🟢 Нет ограничений", "none")],
        [btn("🦴 Спина", "back"), btn("🦵 Колени", "knees")],
        [btn("💪 Плечи", "shoulders"), btn("⚠️ Другое", "other")],
        [InlineKeyboardButton(text="Готово ✅", callback_data="q_lim:done")],
    ])

def quiz_tariff():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆓 Free — 0 ₽", callback_data="q_tar:free")],
        [InlineKeyboardButton(text="💎 Lite — 99 ₽/мес", callback_data="q_tar:lite")],
        [InlineKeyboardButton(text="🔥 Pro — 249 ₽/мес", callback_data="q_tar:pro")],
        [InlineKeyboardButton(text="👑 Elite — 499 ₽/мес", callback_data="q_tar:elite")],
    ])

def workout_controls(exercise_idx, total, has_timer=False, timer_sec=0):
    buttons = []
    if has_timer and timer_sec > 0:
        buttons.append([InlineKeyboardButton(text="⏱️ Таймер " + str(timer_sec) + " сек", callback_data="timer:" + str(timer_sec))])
    buttons.append([InlineKeyboardButton(text="✅ Готово, дальше", callback_data="next_ex:" + str(exercise_idx))])
    if exercise_idx > 0:
        buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="prev_ex:" + str(exercise_idx))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def finish_workout():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏁 Завершить тренировку", callback_data="finish_workout")],
    ])

def after_workout():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="💪 Следующая тренировка", callback_data="my_workout")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")],
    ])

def back_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")],
    ])

def workout_start_or_change():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать тренировку", callback_data="my_workout")],
        [InlineKeyboardButton(text="🔄 Изменить план", callback_data="start_quiz")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")],
    ])
