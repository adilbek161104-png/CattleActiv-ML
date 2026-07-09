import json
import re

file_path = 'd:/Diplom1/static/js/translations.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const translations = (\{.*\});', content, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    
    new_keys = {
        'uz': {
            "Golshteyn": "Golshteyn",
            "Angus": "Angus",
            "Simmental": "Simmental",
            "Qizil cho'l": "Qizil cho'l",
            "Aralash": "Aralash",
            "Normal": "Sog'lom",
            "Mastit / Infeksiya": "Mastit / Infeksiya",
            "Ketoz / Acidosis": "Ketoz / Acidosis",
            "Lameness (Oyoq og'rig'i)": "Lameness (Oyoq og'rig'i)",
            "Estrus (Qizish)": "Estrus (Qizish)",
            "Hypocalcemia (Sut isitmasi)": "Hypocalcemia (Sut isitmasi)",
            "Heat Stress (Issiqlik stresi)": "Heat Stress (Issiqlik stresi)",
            "BRD (Pnevmoniya)": "BRD (Pnevmoniya)",
            "cows_live_sensor": "Live Sensor Data",
            "cows_cow_num": "Cow"
        },
        'ru': {
            "Golshteyn": "Голштинская",
            "Angus": "Ангус",
            "Simmental": "Симментальская",
            "Qizil cho'l": "Красная степная",
            "Aralash": "Смешанная",
            "Normal": "Здорова",
            "Mastit / Infeksiya": "Мастит / Инфекция",
            "Ketoz / Acidosis": "Кетоз / Ацидоз",
            "Lameness (Oyoq og'rig'i)": "Хромота",
            "Estrus (Qizish)": "Эструс (Охота)",
            "Hypocalcemia (Sut isitmasi)": "Гипокальциемия (Молочная лихорадка)",
            "Heat Stress (Issiqlik stresi)": "Тепловой стресс",
            "BRD (Pnevmoniya)": "BRD (Пневмония)",
            "cows_live_sensor": "Данные сенсора (Live)",
            "cows_cow_num": "Корова"
        },
        'en': {
            "Golshteyn": "Holstein",
            "Angus": "Angus",
            "Simmental": "Simmental",
            "Qizil cho'l": "Red Steppe",
            "Aralash": "Mixed",
            "Normal": "Healthy",
            "Mastit / Infeksiya": "Mastitis / Infection",
            "Ketoz / Acidosis": "Ketosis / Acidosis",
            "Lameness (Oyoq og'rig'i)": "Lameness",
            "Estrus (Qizish)": "Estrus (Heat)",
            "Hypocalcemia (Sut isitmasi)": "Hypocalcemia (Milk Fever)",
            "Heat Stress (Issiqlik stresi)": "Heat Stress",
            "BRD (Pnevmoniya)": "BRD (Pneumonia)",
            "cows_live_sensor": "Live Sensor Data",
            "cows_cow_num": "Cow"
        },
        'qq': {
            "Golshteyn": "Golshteyn",
            "Angus": "Angus",
            "Simmental": "Simmental",
            "Qizil cho'l": "Qızıl shól",
            "Aralash": "Aralas",
            "Normal": "Salamat",
            "Mastit / Infeksiya": "Mastit / Infekciya",
            "Ketoz / Acidosis": "Ketoz / Acidoz",
            "Lameness (Oyoq og'rig'i)": "Aqsaw (Ayaq awrıwı)",
            "Estrus (Qizish)": "Kúyiw (Estrus)",
            "Hypocalcemia (Sut isitmasi)": "Gipokalcemiya (Sút isitpesi)",
            "Heat Stress (Issiqlik stresi)": "Issı stres (Heat Stress)",
            "BRD (Pnevmoniya)": "BRD (Pnevmoniya)",
            "cows_live_sensor": "Janlı Sensor Maǵlıwmatları",
            "cows_cow_num": "Qaramal"
        }
    }
    
    for lang, keys in new_keys.items():
        if lang in data:
            data[lang].update(keys)
            
    new_content = 'const translations = ' + json.dumps(data, indent=4, ensure_ascii=False) + ';\n'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Translations updated successfully.')
else:
    print('Failed to parse translations object.')
