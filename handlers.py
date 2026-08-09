import asyncio
import json
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
import keyboards as kb
from config import TARIFFS

router = Router()

with open("workouts/programs.json", "r", encoding="utf-8") as f:
    PROGRAMS = json.load(f)

class Quiz(StatesGroup):
    goal = State()
    location = State()
    equipment = State()
    experience = State()
    frequency = State()
    duration = State()
    limitations = State()
    tariff = State()

def match_program(answers):
    goals = answers.get("goal", [])
    if isinstance(goals, str):
        goals = [goals]
    locations = answers.get("location", [])
    if isinstance(locations, str):
        locations = [locations]
    equipment = answers.get("equipment", [])
    if isinstance(equipment, str):
        equipment = [equipment]
    experience = answers.get("experience")
    freq = int(answers.get("frequency", "3"))
    dur = int(answers.get("duration", "30"))
    limitations = answers.get("limitations", [])
    if isinstance(limitations, str):
        limitations = [limitations]
    scores = {}
    for pid, prog in PROGRAMS.items():
        score = 0
        prog_goals = prog.get("goal", [])
        for g in goals:
            if g in prog_goals: score += 3; break
        for loc in locations:
            if loc in prog.get("location", []): score += 2; break
        for eq in equipment:
            if eq in prog.get("equipment", []): score += 2; break
        if experience == prog.get("level"): score += 1
        if freq == prog.get("frequency"): score += 1
        if dur >= prog.get("duration", 30) - 10 and dur <= prog.get("duration", 30) + 15: score += 1
        has_limitations = any(l != "none" for l in limitations)
        if has_limitations:
            if prog.get("level") == "beginner" and prog.get("duration", 30) <= 30:
                score += 1
            if pid in ["tabata", "express15"]:
                score += 1
        scores[pid] = score
    return max(scores, key=scores.get)

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.username)
    nl = chr(10)
    text = "👋 Привет, " + str(message.from_user.first_name) + "!" + nl + nl
    text += "Я бот Соберись — построю тренировку именно под тебя 💪" + nl + nl
    text += "Ответь на 8 простых вопросов, и я подберу идеальную программу." + nl
    text += "Готов начать? 🚀"
    await message.answer(text, reply_markup=kb.main_menu())

@router.callback_query(F.data == "main_menu")
async def main_menu_cb(callback: CallbackQuery):
    nl = chr(10)
    text = "🏠 Главное меню" + nl + nl
    text += "📝 Начать анкету — подобрать программу" + nl
    text += "💪 Моя тренировка — начать занятие" + nl
    text += "📊 Статистика — твой прогресс" + nl
    text += "💎 Тарифы — возможности"
    await callback.message.edit_text(text, reply_markup=kb.main_menu())
    await callback.answer()

@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Quiz.goal)
    await state.update_data(goal=[])
    nl = chr(10)
    text = "🎯 Вопрос 1 из 8" + nl + nl
    text += "Какая у тебя цель? Можно выбрать несколько!" + nl
    text += "Нажимай на варианты, а потом жми Готово ✅"
    await callback.message.edit_text(text, reply_markup=kb.quiz_goal([]))
    await callback.answer()

@router.callback_query(Quiz.goal, F.data.startswith("q_goal:"))
async def quiz_goal_cb(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split(":")[1]
    current = await state.get_data()
    selected = current.get("goal", [])
    if data == "done":
        if not selected:
            await callback.answer("Выбери хотя бы одну цель!", show_alert=True)
            return
        await state.set_state(Quiz.location)
        await state.update_data(location=[])
        nl = chr(10)
        text = "🏠 Вопрос 2 из 8" + nl + nl
        text += "Где планируешь тренироваться? Можно выбрать несколько!"
        await callback.message.edit_text(text, reply_markup=kb.quiz_location([]))
        await callback.answer()
        return
    if data in selected:
        selected.remove(data)
    else:
        selected.append(data)
    await state.update_data(goal=selected)
    await callback.message.edit_reply_markup(reply_markup=kb.quiz_goal(selected))
    await callback.answer()

@router.callback_query(Quiz.location, F.data.startswith("q_loc:"))
async def quiz_loc_cb(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split(":")[1]
    current = await state.get_data()
    selected = current.get("location", [])
    if data == "done":
        if not selected:
            await callback.answer("Выбери хотя бы один вариант!", show_alert=True)
            return
        await state.set_state(Quiz.equipment)
        await state.update_data(equipment=[])
        nl = chr(10)
        text = "🏋️ Вопрос 3 из 8" + nl + nl
        text += "Какое оборудование есть? Можно выбрать несколько!"
        await callback.message.edit_text(text, reply_markup=kb.quiz_equipment([]))
        await callback.answer()
        return
    if data in selected:
        selected.remove(data)
    else:
        selected.append(data)
    await state.update_data(location=selected)
    await callback.message.edit_reply_markup(reply_markup=kb.quiz_location(selected))
    await callback.answer()

@router.callback_query(Quiz.equipment, F.data.startswith("q_eq:"))
async def quiz_eq_cb(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split(":")[1]
    current = await state.get_data()
    selected = current.get("equipment", [])
    if data == "done":
        if not selected:
            await callback.answer("Выбери хотя бы одно!", show_alert=True)
            return
        await state.set_state(Quiz.experience)
        nl = chr(10)
        text = "🎓 Вопрос 4 из 8" + nl + nl
        text += "Какой у тебя опыт в тренировках?"
        await callback.message.edit_text(text, reply_markup=kb.quiz_experience())
        await callback.answer()
        return
    if data in selected:
        selected.remove(data)
    else:
        selected.append(data)
    await state.update_data(equipment=selected)
    await callback.message.edit_reply_markup(reply_markup=kb.quiz_equipment(selected))
    await callback.answer()

@router.callback_query(Quiz.experience, F.data.startswith("q_exp:"))
async def quiz_exp_cb(callback: CallbackQuery, state: FSMContext):
    exp = callback.data.split(":")[1]
    await state.update_data(experience=exp)
    await state.set_state(Quiz.frequency)
    nl = chr(10)
    text = "📅 Вопрос 5 из 8" + nl + nl
    text += "Сколько раз в неделю планируешь тренироваться?"
    await callback.message.edit_text(text, reply_markup=kb.quiz_frequency())
    await callback.answer()

@router.callback_query(Quiz.frequency, F.data.startswith("q_freq:"))
async def quiz_freq_cb(callback: CallbackQuery, state: FSMContext):
    freq = callback.data.split(":")[1]
    await state.update_data(frequency=freq)
    await state.set_state(Quiz.duration)
    nl = chr(10)
    text = "⏱️ Вопрос 6 из 8" + nl + nl
    text += "Сколько времени готов уделять тренировке?"
    await callback.message.edit_text(text, reply_markup=kb.quiz_duration())
    await callback.answer()

@router.callback_query(Quiz.duration, F.data.startswith("q_dur:"))
async def quiz_dur_cb(callback: CallbackQuery, state: FSMContext):
    dur = callback.data.split(":")[1]
    await state.update_data(duration=dur)
    await state.set_state(Quiz.limitations)
    await state.update_data(limitations=[])
    nl = chr(10)
    text = "🩹 Вопрос 7 из 8" + nl + nl
    text += "Есть ли ограничения по здоровью? Можно выбрать несколько." + nl
    text += "Если всё ок — просто жми Готово ✅"
    await callback.message.edit_text(text, reply_markup=kb.quiz_limitations([]))
    await callback.answer()

@router.callback_query(Quiz.limitations, F.data.startswith("q_lim:"))
async def quiz_lim_cb(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split(":")[1]
    current = await state.get_data()
    selected = current.get("limitations", [])
    if data == "done":
        if not selected:
            await state.update_data(limitations=["none"])
        await state.set_state(Quiz.tariff)
        nl = chr(10)
        text = "💎 Вопрос 8 из 8" + nl + nl
        text += "Выбирай тариф:"
        await callback.message.edit_text(text, reply_markup=kb.quiz_tariff())
        await callback.answer()
        return
    if data == "none":
        selected = ["none"]
    else:
        if "none" in selected:
            selected.remove("none")
        if data in selected:
            selected.remove(data)
        else:
            selected.append(data)
    await state.update_data(limitations=selected)
    await callback.message.edit_reply_markup(reply_markup=kb.quiz_limitations(selected))
    await callback.answer()

@router.callback_query(Quiz.tariff, F.data.startswith("q_tar:"))
async def quiz_tar_cb(callback: CallbackQuery, state: FSMContext):
    tariff = callback.data.split(":")[1]
    data = await state.get_data()
    data["tariff"] = tariff
    user_id = callback.from_user.id
    db.save_questionnaire(user_id, data)
    program_id = match_program(data)
    program = PROGRAMS[program_id]
    db.set_program(user_id, program_id)
    await state.clear()
    nl = chr(10)
    text = "🎉 Отлично! Твой план готов!" + nl + nl
    text += "💪 Программа: " + program["name"] + nl
    text += "📍 Где: " + ", ".join(data.get("location", [])) + nl
    text += "🏋️ Оборудование: " + ", ".join(data.get("equipment", [])) + nl
    text += "📅 Частота: " + data["frequency"] + " раза в неделю" + nl
    text += "⏱️ Время: " + data["duration"] + " минут" + nl
    text += "💎 Тариф: " + TARIFFS[tariff]["name"] + nl + nl
    text += program["description"] + nl + nl
    text += "Готов к первой тренировке? 🔥"
    await callback.message.edit_text(text, reply_markup=kb.workout_start_or_change())
    await callback.answer()

ACTIVE_WORKOUTS = {}

@router.callback_query(F.data == "my_workout")
async def my_workout(callback: CallbackQuery):
    user_id = callback.from_user.id
    program_id = db.get_program(user_id)
    if not program_id or program_id not in PROGRAMS:
        await callback.message.edit_text("У тебя пока нет программы. Пройди анкету! 📝", reply_markup=kb.back_to_menu())
        await callback.answer()
        return
    program = PROGRAMS[program_id]
    day = program["days"][0]
    ACTIVE_WORKOUTS[user_id] = {
        "program_id": program_id,
        "day_idx": 0,
        "ex_idx": 0,
        "start_time": asyncio.get_event_loop().time(),
        "exercises_done": 0
    }
    await show_exercise(callback.message, user_id)
    await callback.answer()

async def show_exercise(message, user_id):
    data = ACTIVE_WORKOUTS.get(user_id)
    if not data:
        return
    program = PROGRAMS[data["program_id"]]
    day = program["days"][data["day_idx"]]
    ex = day["exercises"][data["ex_idx"]]
    total = len(day["exercises"])
    nl = chr(10)
    text = "💪 Упражнение " + str(data["ex_idx"] + 1) + "/" + str(total) + nl
    text += ex["name"] + nl + nl
    text += "📖 Описание: " + ex["description"] + nl + nl
    text += "🔁 Подходы: " + str(ex["sets"]) + " x " + str(ex["reps"]) + nl
    text += "⏱️ Отдых: " + str(ex["rest"]) + " секунд"
    has_timer = ex["rest"] > 0
    await message.edit_text(text, reply_markup=kb.workout_controls(data["ex_idx"], total, has_timer, ex["rest"]))

@router.callback_query(F.data.startswith("timer:"))
async def start_timer(callback: CallbackQuery, bot: Bot):
    seconds = int(callback.data.split(":")[1])
    msg = await callback.message.answer("⏱️ Таймер запущен: " + str(seconds) + " секунд...")
    await asyncio.sleep(seconds)
    await bot.send_message(callback.from_user.id, "🔥 Время! Следующий подход или упражнение.")
    await callback.answer()

@router.callback_query(F.data.startswith("next_ex:"))
async def next_exercise(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = ACTIVE_WORKOUTS.get(user_id)
    if not data:
        await callback.answer("Ошибка. Начни заново.")
        return
    program = PROGRAMS[data["program_id"]]
    day = program["days"][data["day_idx"]]
    data["ex_idx"] += 1
    data["exercises_done"] += 1
    if data["ex_idx"] >= len(day["exercises"]):
        duration = int((asyncio.get_event_loop().time() - data["start_time"]) / 60)
        exercises_done = data["exercises_done"]
        db.log_workout(user_id, data["program_id"], day["name"], duration, exercises_done)
        del ACTIVE_WORKOUTS[user_id]
        stats = db.get_stats(user_id)
        nl = chr(10)
        text = "🎉 Тренировка завершена!" + nl + nl
        text += "✅ Сделано: " + str(exercises_done) + " упражнений" + nl
        text += "⏱️ Время: " + str(duration) + " минут" + nl
        text += "🔥 Серия: " + str(stats["streak"]) + " тренировок подряд" + nl + nl
        text += "Молодец! Отдыхай и восстанавливайся 💪"
        await callback.message.edit_text(text, reply_markup=kb.after_workout())
    else:
        await show_exercise(callback.message, user_id)
    await callback.answer()

@router.callback_query(F.data.startswith("prev_ex:"))
async def prev_exercise(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = ACTIVE_WORKOUTS.get(user_id)
    if data and data["ex_idx"] > 0:
        data["ex_idx"] -= 1
        await show_exercise(callback.message, user_id)
    await callback.answer()

@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery):
    user_id = callback.from_user.id
    stats = db.get_stats(user_id)
    nl = chr(10)
    text = "📊 Твоя статистика:" + nl + nl
    text += "🏋️ Всего тренировок: " + str(stats["workouts_done"]) + nl
    text += "🔥 Серия подряд: " + str(stats["streak"]) + nl + nl
    text += "Продолжай в том же духе! Ты крут 💪"
    await callback.message.edit_text(text, reply_markup=kb.back_to_menu())
    await callback.answer()

@router.callback_query(F.data == "tariffs")
async def show_tariffs(callback: CallbackQuery):
    nl = chr(10)
    text = "💎 Доступные тарифы:" + nl + nl
    for key, t in TARIFFS.items():
        text += t["name"] + " — " + str(t["price"]) + " ₽/мес" + nl
        text += "  🏋️ Тренировок: " + str(t["workouts_per_month"]) + " в месяц" + nl + nl
    text += "💳 Оплатить можно позже (в разработке)."
    await callback.message.edit_text(text, reply_markup=kb.back_to_menu())
    await callback.answer()
