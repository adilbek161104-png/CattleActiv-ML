# -*- coding: utf-8 -*-
import codecs
import re

with codecs.open('ai_translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

updates = {
    'oqsil': "['isitma', \"so'lak\", 'pufakcha', 'yara', 'tuyoq', 'shuyel', 'oqsil', 'yashur', \"cho'loqlik\", 'kopik', \"ko'pik\", 'isitpa', 'silekey', 'kópirshik', 'tuyaq', 'aqsaw', 'лихорадка', 'слюнотечение', 'пузырьки', 'ящур', 'хромота', 'fever', 'drooling', 'blister', 'fmd', 'lameness']",
    'kuydirgi': "['harorat', \"ko'taril\", 'qora qon', 'burun', \"og'iz\", 'orqa chiqaruv', 'kuydirgi', 'sibir yarasi', 'teshik', 'kóteriliw', 'qara qan', 'mırın', 'awız', 'kúydirgi', 'sibir yarası', 'температура', 'черная кровь', 'нос', 'рот', 'сибирская язва', 'temperature', 'black blood', 'nose', 'mouth', 'anthrax']",
    'brutsellyoz': "['abort', 'bola tashlash', 'bolatashlash', 'bepusht', \"yo'ldosh\", 'brutsellyoz', 'belgisiz', 'balataslaw', 'tuwmas', 'brucellyoz', 'аборт', 'выкидыш', 'бесплодие', 'бруцеллез', 'abortion', 'miscarriage', 'infertility', 'brucellosis']",
    'qoraopka': "['yo\\'tal', 'yiringli', 'suyuqlik', 'nafas qisishi', 'pasterellyoz', 'qorao\\'pka', 'qoraopka', 'plevropnevmoniya', 'ozib', 'jóteliw', 'irińli', 'suyıqlıq', 'dem qısıw', 'qaraókpe', 'кашель', 'гной', 'одышка', 'пастереллез', 'пневмония', 'cough', 'pus', 'shortness of breath', 'pasteurellosis', 'pneumonia']",
    'qutirish': "['tajovuzkor', \"qo'rquv\", 'yutish', 'falaj', 'qutirish', 'beshenstvo', 'asab', 'qorqıw', 'agressiya', 'jutıw', 'falajlıq', 'qutırıw', 'агрессия', 'страх', 'глотать', 'паралич', 'бешенство', 'aggression', 'fear', 'swallow', 'paralysis', 'rabies']",
    'mastit': "['yelin', 'shish', 'qizarish', 'sut', 'qon', 'yiring', 'mastit', 'atrofiya', 'jelin', 'isiw', 'qızarıw', 'sút', 'qan', 'iriń', 'вымя', 'отек', 'покраснение', 'молоко', 'кровь', 'гной', 'мастит', 'udder', 'swelling', 'redness', 'milk', 'blood', 'mastitis']",
    'ketoz': "['ishtaha', 'atseton', 'hidi', 'ketoz', 'jigar', 'semirish', 'modda almashinuvi', 'siydik', 'tábeyin', 'aceton', 'iyis', 'bawır', 'semiriw', 'siydek', 'аппетит', 'ацетон', 'запах', 'кетоз', 'печень', 'моча', 'appetite', 'acetone', 'smell', 'ketosis', 'liver', 'urine']",
    'timpaniya': "['qorin', 'chap', 'shish', 'bezovta', 'gaz', \"bo'g'ilib\", 'timpaniya', \"dam bo'lishi\", 'qarın', 'shep', 'isiw', 'biymázalanish', 'dem qısıw', 'вздутие', 'живот', 'левый', 'беспокойство', 'газ', 'тимпания', 'bloat', 'abdomen', 'left', 'restless', 'gas', 'tympany']",
    'leykoz': "['tashqi bez', 'limfa', 'tugun', \"bo'rtib\", 'leykoz', \"o'sma\", 'sırtqı bez', 'túyin', 'bórtip', 'железа', 'лимфа', 'узел', 'лейкоз', 'опухоль', 'gland', 'lymph', 'node', 'bulging', 'leukosis', 'tumor']",
    'telyazioz': "[\"ko'z\", 'yosh oqishi', \"yorug'lik\", \"qo'rqish\", 'xiralash', \"ko'r\", 'chuvalchang', 'telyazioz', 'qurt', 'kóz', 'jas aǵıw', 'jaqtılıq', 'xiralasıw', 'soqır', 'глаз', 'слеза', 'свет', 'мутнеть', 'червь', 'телязиоз', 'eye', 'tear', 'light', 'clouding', 'blind', 'worm', 'thelaziasis']"
}

for k, v in updates.items():
    pattern = r"'" + k + r"':\s*\{\s*'keywords':\s*\[.*?\]"
    replacement = f"'{k}': {{\n        'keywords': {v}"
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with codecs.open('ai_translations.py', 'w', encoding='utf-8') as f:
    f.write(content)
