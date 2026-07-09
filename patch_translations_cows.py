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
            'cows_title': 'Qoramollar Profil Bazasi',
            'cows_subtitle': "Barcha ro'yxatdan o'tgan qoramollarning umumiy holati",
            'cows_loading': "Ma'lumotlar yuklanmoqda...",
            'cows_empty': 'Hali qoramollar kiritilmagan.',
            'cows_profile': 'Profil',
            'cows_breed': 'Zoti:',
            'cows_age': 'Yoshi:',
            'cows_age_yrs': 'yosh',
            'cows_weight': 'Vazni:',
            'cows_milk': "Sog'in (kunlik):",
            'cows_status_no_data': "Ma'lumot yo'q",
            'cows_status_healthy': "Sog'lom",
            'cows_temp': 'Harorat:',
            'cows_rum': 'Chaynash:',
            'cows_mins': 'daqiqa',
            'cows_edit_title': 'Qoramolni Tahrirlash',
            'cows_new_img': 'Yangi Rasm (ixtiyoriy):',
            'cows_cancel': 'Bekor qilish',
            'cows_save': 'Saqlash'
        },
        'ru': {
            'cows_title': 'База профилей коров',
            'cows_subtitle': 'Общее состояние всех зарегистрированных коров',
            'cows_loading': 'Загрузка данных...',
            'cows_empty': 'Коровы еще не добавлены.',
            'cows_profile': 'Профиль',
            'cows_breed': 'Порода:',
            'cows_age': 'Возраст:',
            'cows_age_yrs': 'лет',
            'cows_weight': 'Вес:',
            'cows_milk': 'Удой (дневной):',
            'cows_status_no_data': 'Нет данных',
            'cows_status_healthy': 'Здорова',
            'cows_temp': 'Температура:',
            'cows_rum': 'Жвачка:',
            'cows_mins': 'минут',
            'cows_edit_title': 'Редактировать корову',
            'cows_new_img': 'Новое фото (необязательно):',
            'cows_cancel': 'Отмена',
            'cows_save': 'Сохранить'
        },
        'en': {
            'cows_title': 'Cows Profile Database',
            'cows_subtitle': 'Overall status of all registered cows',
            'cows_loading': 'Loading data...',
            'cows_empty': 'No cows added yet.',
            'cows_profile': 'Profile',
            'cows_breed': 'Breed:',
            'cows_age': 'Age:',
            'cows_age_yrs': 'yrs',
            'cows_weight': 'Weight:',
            'cows_milk': 'Milk (daily):',
            'cows_status_no_data': 'No data',
            'cows_status_healthy': 'Healthy',
            'cows_temp': 'Temperature:',
            'cows_rum': 'Rumination:',
            'cows_mins': 'mins',
            'cows_edit_title': 'Edit Cow',
            'cows_new_img': 'New Image (optional):',
            'cows_cancel': 'Cancel',
            'cows_save': 'Save'
        },
        'qq': {
            'cows_title': 'Qaramallar Profil Bazası',
            'cows_subtitle': 'Barlıq dizimnen ótken qaramallardıń ulıwma jaǵdayı',
            'cows_loading': 'Maǵlıwmatlar júklenbekte...',
            'cows_empty': 'Ele qaramallar kirgizilmegen.',
            'cows_profile': 'Profili',
            'cows_breed': 'Túri:',
            'cows_age': 'Jası:',
            'cows_age_yrs': 'jas',
            'cows_weight': 'Salmaǵı:',
            'cows_milk': 'Sawın (kúnlik):',
            'cows_status_no_data': 'Maǵlıwmat joq',
            'cows_status_healthy': 'Salamat',
            'cows_temp': 'Temperaturası:',
            'cows_rum': 'Gúyiw:',
            'cows_mins': 'minut',
            'cows_edit_title': 'Qaramaldı Ońlaw',
            'cows_new_img': 'Taza Súwret (qálegen):',
            'cows_cancel': 'Biykarlaw',
            'cows_save': 'Saqlaw'
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
