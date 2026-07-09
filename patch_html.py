import os
import glob
import re

template_dir = r"d:\Diplom1\templates"
files = glob.glob(os.path.join(template_dir, "*.html"))

nav_regex = re.compile(
    r'(<div class="nav-links">.*?)(<a href="/about".*?Sayt Haqida</span></a>)(.*?)(<select id="langSwitch".*?</select>)(.*?</div>)', 
    re.DOTALL
)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Reorder navbar
    if '<select id="langSwitch"' in content and '<a href="/about"' in content:
        # Move 'about' tag to be after 'select' tag
        new_content = nav_regex.sub(r'\1\3\4\n            \2\5', content)
        if new_content != content:
            content = new_content
            
    # 2. Add missing data-i18n tags for dashboard.html
    if 'dashboard.html' in file:
        content = content.replace('<h2>Farm Monitoring Platform', '<h2><span data-i18n="dash_title">Farm Monitoring Platform</span>')
        content = content.replace('LIVE</span>', '<span data-i18n="dash_live">LIVE</span></span>')
        content = content.replace('<i class="fas fa-brain" style="color: var(--primary-color);"></i> AI Diagnosis', '<i class="fas fa-brain" style="color: var(--primary-color);"></i> <span data-i18n="dash_ai_diag">AI Diagnosis</span>')
        content = content.replace('<i class="fas fa-map-marker-alt" style="color: var(--accent-color);"></i> GPS Tracking', '<i class="fas fa-map-marker-alt" style="color: var(--accent-color);"></i> <span data-i18n="dash_gps">GPS Tracking</span>')
        content = content.replace('<i class="fas fa-user-md" style="color: #8b5cf6;"></i> AI Vet Assistant', '<i class="fas fa-user-md" style="color: #8b5cf6;"></i> <span data-i18n="dash_ai_vet">AI Vet Assistant</span>')
        content = content.replace('<i class="fas fa-play"></i> Simulyatsiya', '<i class="fas fa-play"></i> <span data-i18n="dash_sim">Simulyatsiya</span>')
        content = content.replace('<i class="fas fa-plus"></i> Yangi Tekshiruv', '<i class="fas fa-plus"></i> <span data-i18n="dash_new_test">Yangi Tekshiruv</span>')
        content = content.replace('<i class="fas fa-layer-group"></i> Barcha qoramollar holatini ko\'rish (10 ta)', '<i class="fas fa-layer-group"></i> <span data-i18n="dash_view_all">Barcha qoramollar holatini ko\'rish</span>')
        content = content.replace('<i class="fas fa-chevron-up"></i> Yopish va Yuqoriga', '<i class="fas fa-chevron-up"></i> <span data-i18n="dash_close_up">Yopish va Yuqoriga</span>')
        content = content.replace('<h3><i class="fas fa-map-marker-alt"></i> Live GPS Tracking</h3>', '<h3><i class="fas fa-map-marker-alt"></i> <span data-i18n="dash_live_gps">Live GPS Tracking</span></h3>')
        content = content.replace('<i class="fas fa-expand"></i> Kattalashtirish', '<i class="fas fa-expand"></i> <span data-i18n="dash_expand">Kattalashtirish</span>')
        content = content.replace('<h3><i class="fas fa-robot"></i> AI Veterinariya Assistenti</h3>', '<h3><i class="fas fa-robot"></i> <span data-i18n="dash_ai_assistant">AI Veterinariya Assistenti</span></h3>')
        content = content.replace('<i class="fas fa-comment-medical"></i> Assistentni Ochish', '<i class="fas fa-comment-medical"></i> <span data-i18n="dash_open_ai">Assistentni Ochish</span>')
        content = content.replace('<div class="chat-msg ai-msg">Assalomu alaykum! Men AI Veterinarmon. Qaysi qoramol haqida so\'ramoqchisiz?</div>', '<div class="chat-msg ai-msg" data-i18n="dash_ai_greet">Assalomu alaykum! Men AI Veterinarmon. Qaysi qoramol haqida so\'ramoqchisiz?</div>')
        content = content.replace('<i class="fas fa-paper-plane"></i> So\'rash', '<i class="fas fa-paper-plane"></i> <span data-i18n="dash_ask">So\'rash</span>')
        content = content.replace('<h3><i class="fas fa-history"></i> Barcha Ma\'lumotlar Tarixi</h3>', '<h3><i class="fas fa-history"></i> <span data-i18n="dash_history">Barcha Ma\'lumotlar Tarixi</span></h3>')
        content = content.replace('<i class="fas fa-eye"></i> Tarixni Ko\'rsatish', '<i class="fas fa-eye"></i> <span data-i18n="dash_show_hist">Tarixni Ko\'rsatish</span>')
        
    # 3. Add missing data-i18n tags for sensor_input.html
    if 'sensor_input.html' in file:
        content = content.replace('<h2>Live Sensor Data Input</h2>', '<h2><span data-i18n="sensor_title">Live Sensor Data Input</span></h2>')
        content = content.replace('<span class="dot pulse"></span> System Online', '<span class="dot pulse"></span> <span data-i18n="sensor_online">System Online</span>')
        content = content.replace('<label><i class="fas fa-tag"></i> Cow ID:</label>', '<label><i class="fas fa-tag"></i> <span data-i18n="sensor_cow_id">Cow ID:</span></label>')
        content = content.replace('<label><i class="fas fa-shoe-prints"></i> Qadamlar (kunlik):</label>', '<label><i class="fas fa-shoe-prints"></i> <span data-i18n="sensor_steps">Qadamlar (kunlik):</span></label>')
        content = content.replace('<label><i class="fas fa-running"></i> Yurish vaqti (soat):</label>', '<label><i class="fas fa-running"></i> <span data-i18n="sensor_movement">Yurish vaqti (soat):</span></label>')
        content = content.replace('<label><i class="fas fa-tooth"></i> Chaynash (Rumination) daqiqa:</label>', '<label><i class="fas fa-tooth"></i> <span data-i18n="sensor_rumination">Chaynash (Rumination) daqiqa:</span></label>')
        content = content.replace('<label><i class="fas fa-thermometer-half"></i> Tana harorati (°C):</label>', '<label><i class="fas fa-thermometer-half"></i> <span data-i18n="sensor_temp">Tana harorati (°C):</span></label>')
        content = content.replace('<i class="fas fa-microchip"></i> Start AI Diagnosis', '<i class="fas fa-microchip"></i> <span data-i18n="sensor_start_ai">Start AI Diagnosis</span>')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated HTML files.")
