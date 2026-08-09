# Test bot for Sobirys — console simulator
# Run: python test_bot.py
# No Telegram token needed

import json
import time

with open("workouts/programs.json", "r", encoding="utf-8") as f:
    PROGRAMS = json.load(f)

QUESTIONS = [
    ("goal", "Какая у тебя цель? Можно выбрать несколько, через запятую:", {
        "1": ("lose", "🎯 Похудение"),
        "2": ("mass", "💪 Масса"),
        "3": ("strength", "🏋️ Сила"),
        "4": ("endurance", "🏃 Выносливость"),
        "5": ("health", "❤️ Здоровье"),
    }),
    ("location", "Где будешь тренироваться? Можно несколько:", {
        "1": ("home", "🏠 Дома"),
        "2": ("gym", "🏢 В зале"),
        "3": ("street", "🌳 На улице"),
        "4": ("mixed", "🔄 Смешанно"),
    }),
    ("equipment", "Какое оборудование есть? Можно несколько:", {
        "1": ("none", "🙅 Ничего"),
        "2": ("dumbbells", "🏋️‍♂️ Гантели"),
        "3": ("bands", "🎗️ Резинки"),
        "4": ("barbell", "🏋️ Штанга"),
        "5": ("full", "🏭 Полный зал"),
    }),
    ("experience", "Какой у тебя опыт?", {
        "1": ("beginner", "🐣 Новичок"),
        "2": ("intermediate", "🦊 Средний"),
        "3": ("advanced", "🦁 Продвинутый"),
    }),
    ("frequency", "Сколько раз в неделю?", {
        "1": ("2", "2️⃣ Два раза"),
        "2": ("3", "3️⃣ Три раза"),
        "3": ("4", "4️⃣ Четыре раза"),
        "4": ("5", "5️⃣+ Пять и более"),
    }),
    ("duration", "Сколько времени на тренировку?", {
        "1": ("15", "⏱️ 15 мин"),
        "2": ("30", "⏱️ 30 мин"),
        "3": ("45", "⏱️ 45 мин"),
        "4": ("60", "⏱️ 60 мин"),
    }),
    ("limitations", "Есть ли ограничения? (0 — нет, или несколько через запятую)", {
        "0": ("none", "🟢 Нет"),
        "1": ("back", "🦴 Спина"),
        "2": ("knees", "🦵 Колени"),
        "3": ("shoulders", "💪 Плечи"),
        "4": ("other", "⚠️ Другое"),
    }),
    ("tariff", "Выбирай тариф:", {
        "1": ("free", "🆓 Free (0 ₽)"),
        "2": ("lite", "💎 Lite (99 ₽)"),
        "3": ("pro", "🔥 Pro (249 ₽)"),
        "4": ("elite", "👑 Elite (499 ₽)"),
    }),
]

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
        for g in goals:
            if g in prog.get("goal", []): score += 3; break
        for loc in locations:
            if loc in prog.get("location", []): score += 2; break
        for eq in equipment:
            if eq in prog.get("equipment", []): score += 2; break
        if experience == prog.get("level"): score += 1
        if freq == prog.get("frequency"): score += 1
        if dur >= prog.get("duration", 30) - 10 and dur <= prog.get("duration", 30) + 15: score += 1
        has_lim = any(l != "none" for l in limitations)
        if has_lim:
            if prog.get("level") == "beginner" and prog.get("duration", 30) <= 30:
                score += 1
            if pid in ["tabata", "express15"]:
                score += 1
        scores[pid] = score
    return max(scores, key=scores.get)

def run_quiz():
    answers = {}
    print("=" * 50)
    print("🤖 АНКЕТА СОБЕРИСЬ")
    print("=" * 50)
    for key, question, options in QUESTIONS:
        print()
        print(question)
        for num, (val, label) in options.items():
            print("  " + num + ". " + label)
        while True:
            choice = input("Выбирай (можно несколько через запятую): ").strip()
            nums = [c.strip() for c in choice.split(",")]
            vals = []
            ok = True
            for n in nums:
                if n in options:
                    vals.append(options[n][0])
                else:
                    ok = False
                    break
            if ok and vals:
                answers[key] = vals if len(vals) > 1 else vals[0]
                break
            print("Неправильный ввод. Попробуй снова.")
    return answers

def show_plan(answers):
    program_id = match_program(answers)
    program = PROGRAMS[program_id]
    print()
    print("=" * 50)
    print("🎉 ТВОЙ ПЛАН ГОТОВ!")
    print("=" * 50)
    print("💪 Программа: " + program["name"])
    print("🎯 Цель: " + ", ".join(answers["goal"] if isinstance(answers["goal"], list) else [answers["goal"]]))
    print("📍 Где: " + ", ".join(answers["location"] if isinstance(answers["location"], list) else [answers["location"]]))
    print("🏋️ Оборудование: " + ", ".join(answers["equipment"] if isinstance(answers["equipment"], list) else [answers["equipment"]]))
    print("🎓 Опыт: " + answers["experience"])
    print("📅 Частота: " + answers["frequency"] + " раза в неделю")
    print("⏱️ Время: " + answers["duration"] + " минут")
    print("💎 Тариф: " + answers["tariff"])
    print()
    print(program["description"])
    return program_id

def run_workout(program_id):
    program = PROGRAMS[program_id]
    day = program["days"][0]
    exercises = day["exercises"]
    print()
    print("=" * 50)
    print("💪 ТРЕНИРОВКА: " + day["name"])
    print("=" * 50)
    for i, ex in enumerate(exercises):
        print()
        print("--- Упражнение " + str(i+1) + "/" + str(len(exercises)) + " ---")
        print("💪 " + ex["name"])
        print("📖 " + ex["description"])
        print("🔁 Подходы: " + str(ex["sets"]) + " x " + str(ex["reps"]))
        print("⏱️ Отдых: " + str(ex["rest"]) + " секунд")
        input("[Нажми ENTER когда сделал...]")
        if ex["rest"] > 0 and i < len(exercises) - 1:
            print("⏱️ Отдых " + str(ex["rest"]) + " секунд...")
            time.sleep(min(ex["rest"], 3))
            print("🔥 Время! Следующее упражнение.")
    print()
    print("=" * 50)
    print("🎉 ТРЕНИРОВКА ЗАВЕРШЕНА!")
    print("✅ Сделано: " + str(len(exercises)) + " упражнений")
    print("💪 Молодец! Отдыхай.")
    print("=" * 50)

def main():
    print("👋 Добро пожаловать в тестовый бот Соберись!")
    print("Эта версия работает в консоли без Telegram.")
    while True:
        print()
        print("--- ГЛАВНОЕ МЕНЮ ---")
        print("1. 📝 Пройти анкету и начать тренировку")
        print("2. 🚪 Выйти")
        choice = input("Выбирай: ").strip()
        if choice == "1":
            answers = run_quiz()
            program_id = show_plan(answers)
            print()
            print("1. 🚀 Начать тренировку")
            print("2. 🔙 Назад в меню")
            c2 = input("Выбирай: ").strip()
            if c2 == "1":
                run_workout(program_id)
        elif choice == "2":
            print("👋 Пока!")
            break
        else:
            print("Неправильный ввод.")

if __name__ == "__main__":
    main()
