import json
import re

file_path = 'd:/Diplom1/static/js/translations.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const translations = (\{.*\});', content, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    
    new_keys = {
        "uz": {
            "nav_settings": "Sozlamalar",
            "nav_logout": "Chiqish",
            "login_title": "CattleActiv-ML",
            "login_desc": "Tizimga kirish uchun ma'lumotlarni kiriting",
            "login_user": "Login:",
            "login_pass": "Parol:",
            "login_btn": "Kirish",
            "settings_title": "Sozlamalar",
            "settings_pass_change": "Parolni O'zgartirish",
            "settings_old_pass": "Eski parol:",
            "settings_new_pass": "Yangi parol:",
            "settings_save": "Saqlash",
            "settings_lang": "Tilni Tanlash",
            "settings_back": "← Bosh sahifaga qaytish"
        },
        "ru": {
            "nav_settings": "Настройки",
            "nav_logout": "Выход",
            "login_title": "CattleActiv-ML",
            "login_desc": "Введите данные для входа",
            "login_user": "Логин:",
            "login_pass": "Пароль:",
            "login_btn": "Войти",
            "settings_title": "Настройки",
            "settings_pass_change": "Смена пароля",
            "settings_old_pass": "Старый пароль:",
            "settings_new_pass": "Новый пароль:",
            "settings_save": "Сохранить",
            "settings_lang": "Выбор языка",
            "settings_back": "← На главную"
        },
        "en": {
            "nav_settings": "Settings",
            "nav_logout": "Logout",
            "login_title": "CattleActiv-ML",
            "login_desc": "Enter your login details",
            "login_user": "Username:",
            "login_pass": "Password:",
            "login_btn": "Login",
            "settings_title": "Settings",
            "settings_pass_change": "Change Password",
            "settings_old_pass": "Old password:",
            "settings_new_pass": "New password:",
            "settings_save": "Save",
            "settings_lang": "Select Language",
            "settings_back": "← Back to Home"
        },
        "qq": {
            "nav_settings": "Sazlamalar",
            "nav_logout": "Shıǵıw",
            "login_title": "CattleActiv-ML",
            "login_desc": "Sistemaǵa kiriw ushın maǵlıwmatlardı kirgiziń",
            "login_user": "Login:",
            "login_pass": "Parol:",
            "login_btn": "Kiriw",
            "settings_title": "Sazlamalar",
            "settings_pass_change": "Paroldi Ózgertiw",
            "settings_old_pass": "Góne parol:",
            "settings_new_pass": "Taza parol:",
            "settings_save": "Saqlaw",
            "settings_lang": "Tildi Tańlaw",
            "settings_back": "← Bas betke qaytıw"
        }
    }

    for lang in data:
        if lang in new_keys:
            data[lang].update(new_keys[lang])
            
    new_content = 'const translations = ' + json.dumps(data, indent=4, ensure_ascii=False) + ';'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Translations updated successfully.")
