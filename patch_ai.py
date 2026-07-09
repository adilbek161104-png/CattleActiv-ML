import os

file = r"d:\Diplom1\templates\ai_diagnosis.html"

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<h2 style="color: #8b5cf6; margin-bottom: 0.5rem;"><i class="fas fa-stethoscope"></i> <span data-i18n="nav_ai_diag">AI Kasallik Diagnostikasi</span></h2>',
    '<h2 style="color: var(--primary-color); margin-bottom: 0.5rem;"><i class="fas fa-stethoscope"></i> <span data-i18n="diag_header">AI Kasallik Diagnostikasi</span></h2>'
)

content = content.replace(
    '<p style="color: var(--text-muted); font-size: 1rem;">Molning tashqi kasallik belgilarini (masalan: og\'zidan ko\'pik, yara, oqsoqlash) yozing va AIdan maslahat oling.</p>',
    '<p style="color: var(--text-muted); font-size: 1rem;" data-i18n="diag_desc">Molning tashqi kasallik belgilarini (masalan: og\'zidan ko\'pik, yara, oqsoqlash) yozing va AIdan maslahat oling.</p>'
)

content = content.replace(
    '<input type="text" id="symptomInput" class="modern-select" style="flex: 1; border-radius: 8px; font-size: 1rem;" placeholder="Kasallik belgilarini yozing...">',
    '<input type="text" id="symptomInput" class="modern-select" style="flex: 1; border-radius: 8px; font-size: 1rem;" placeholder="Kasallik belgilarini yozing..." data-i18n="diag_placeholder">'
)

content = content.replace(
    '<button class="btn primary-btn chat-btn" onclick="askSymptomAi()" style="border-radius: 8px; background: #8b5cf6; padding: 0 1.5rem;"><i class="fas fa-paper-plane"></i> So\'rash</button>',
    '<button class="btn primary-btn chat-btn" onclick="askSymptomAi()" style="border-radius: 8px; background: var(--primary-color); padding: 0 1.5rem;"><i class="fas fa-paper-plane"></i> <span data-i18n="diag_ask">So\'rash</span></button>'
)

content = content.replace(
    '<div class="chat-msg ai-msg">Assalomu alaykum! Men AI Veterinarmon. Qoramoldagi kasallik belgilarini tasvirlab bering (masalan: "og\'zidan ko\'pik kelyapti va tuyog\'ida yara bor").</div>',
    '<div class="chat-msg ai-msg" data-i18n="diag_greet">Assalomu alaykum! Men AI Veterinarmon. Qoramoldagi kasallik belgilarini tasvirlab bering (masalan: "og\'zidan ko\'pik kelyapti va tuyog\'ida yara bor").</div>'
)

# Fix top border color
content = content.replace(
    '<div class="card iot-panel" style="border-top: 4px solid #8b5cf6;">',
    '<div class="card iot-panel" style="border-top: 4px solid var(--primary-color);">'
)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated ai_diagnosis.html")
