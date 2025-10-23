# import random
# import datetime
# import json
# from pathlib import Path


# DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
# PHRASES_FILE = DATA_DIR / 'phrases.json'
# EMOJIS_FILE = DATA_DIR / 'emojis.json'


# # загрузка вариантов фраз и эмодзи
# with open(PHRASES_FILE, 'r', encoding='utf-8') as f:
#     PHRASES = json.load(f)


# with open(EMOJIS_FILE, 'r', encoding='utf-8') as f:
#     EMOJIS = json.load(f)


# async def generate_capital(tg_id: int) -> float:
#     # детерминированно-случайная генерация, чтобы при повторной генерации вне БД
#     # результат был похож, но мы всё равно сохраняем в БД
#     rnd = random.Random()
#     seed = (tg_id << 32) ^ int(datetime.datetime.utcnow().timestamp())
#     rnd.seed(seed)


#     # пример диапазона: 0 - 10_000_000
#     val = rnd.random() * 10_000_000
#     # округлим до центов
#     return round(val, 2)


# def pick_phrase_and_emoji(capital: float) -> (str, str):
#     # PHRASES — список объектов {"min":0, "max":100, "phrases": [...], "category": "poor"}
#     # EMOJIS — словарь {"poor": ["💀","🥀"], "rich": ["💎","🤑"]}


#     for item in PHRASES:
#         if capital >= item['min'] and capital <= item['max']:
#             phrase = random.choice(item['phrases'])
#             cat = item.get('category', 'neutral')
#             emoji = random.choice(EMOJIS.get(cat, ['💵']))
#             return phrase, emoji
#     # fallback
#     return 'Неизвестно', '💵'

import random
import datetime
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
PHRASES_FILE = DATA_DIR / 'phrases.json'
EMOJIS_FILE = DATA_DIR / 'emojis.json'

# Загрузка вариантов фраз и эмодзи
with open(PHRASES_FILE, 'r', encoding='utf-8') as f:
    PHRASES = json.load(f)

with open(EMOJIS_FILE, 'r', encoding='utf-8') as f:
    EMOJIS = json.load(f)

# Вероятностное распределение капитала
CAPITAL_DISTRIBUTION = [
    {"range": (0, 100), "weight": 0.35},          # беднота
    {"range": (100, 1000), "weight": 0.30},       # выживающие
    {"range": (1000, 10000), "weight": 0.20},     # средний класс
    {"range": (10000, 100000), "weight": 0.10},   # богатые
    {"range": (100000, 1000000), "weight": 0.04}, # элита
    {"range": (1000000, 10000000), "weight": 0.01} # миллиардеры
]

async def generate_capital(tg_id: int) -> float:
    """
    Генерация капитала с вероятностями и детерминированным seed
    для одного пользователя в течение одной сессии.
    """
    rnd = random.Random()
    seed = (tg_id << 32) ^ int(datetime.datetime.utcnow().timestamp())
    rnd.seed(seed)

    # Выбор диапазона по вероятности
    choice = rnd.choices(CAPITAL_DISTRIBUTION, weights=[r["weight"] for r in CAPITAL_DISTRIBUTION])[0]
    low, high = choice["range"]
    return round(rnd.uniform(low, high), 2)

def pick_phrase_and_emoji(capital: float) -> (str, str):
    """
    Выбирает подходящую фразу и эмодзи для капитала.
    PHRASES — список объектов {"min":0, "max":100, "phrases":[...], "category":"poor"}
    EMOJIS — словарь {"poor": ["💀","🥀"], "rich": ["💎","🤑"]}
    """
    for item in PHRASES:
        if item['min'] <= capital <= item['max']:
            phrase = random.choice(item['phrases'])
            cat = item.get('category', 'neutral')
            emoji = random.choice(EMOJIS.get(cat, ['💵']))
            return phrase, emoji
    # fallback
    return 'Неизвестно', '💵'
