import re

file_path = 'd:/Diplom1/templates/cows.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    (r'<h2>Qoramollar Profil Bazasi <span class="live-indicator">', r'<h2><span data-i18n="cows_title">Qoramollar Profil Bazasi</span> <span class="live-indicator">'),
    (r'<p class="subtitle">Barcha ro\'yxatdan o\'tgan qoramollarning umumiy holati \(Jiltirbas hududi\)</p>', r'<p class="subtitle" data-i18n="cows_subtitle">Barcha ro\'yxatdan o\'tgan qoramollarning umumiy holati (Jiltirbas hududi)</p>'),
    (r'<h2 style="margin-bottom: 1.5rem; color: var\(--primary-color\);"><i class="fas fa-edit"></i> Qoramolni Tahrirlash</h2>', r'<h2 style="margin-bottom: 1.5rem; color: var(--primary-color);"><i class="fas fa-edit"></i> <span data-i18n="cows_edit_title">Qoramolni Tahrirlash</span></h2>'),
    (r'<label>Zoti:</label>', r'<label data-i18n="cows_breed">Zoti:</label>'),
    (r'<label>Yoshi:</label>', r'<label data-i18n="cows_age">Yoshi:</label>'),
    (r'<label>Vazni \(kg\):</label>', r'<label data-i18n="cows_weight">Vazni (kg):</label>'),
    (r'<label>Sog\'in \(litr\):</label>', r'<label data-i18n="cows_milk">Sog\'in (litr):</label>'),
    (r'<label>Yangi Rasm \(ixtiyoriy\):</label>', r'<label data-i18n="cows_new_img">Yangi Rasm (ixtiyoriy):</label>'),
    (r'>Bekor qilish</button>', r' data-i18n="cows_cancel">Bekor qilish</button>'),
    (r'<button type="submit" class="btn primary-btn">Saqlash</button>', r'<button type="submit" class="btn primary-btn" data-i18n="cows_save">Saqlash</button>')
]

for old, new in replacements:
    html = re.sub(old, new, html)

# Inject `t` function
js_helper = """
        const t = (key) => {
            const lang = localStorage.getItem('appLang') || 'uz';
            return window.translations && window.translations[lang] && window.translations[lang][key] ? window.translations[lang][key] : key;
        };
"""
html = html.replace("function renderCowsDatabase(cowProfiles, liveData) {", js_helper + "\n        function renderCowsDatabase(cowProfiles, liveData) {")

# Update renderCowsDatabase
html = re.sub(
    r'<div style="grid-column: 1/-1; text-align: center; padding: 2rem;">Hali qoramollar kiritilmagan.</div>',
    r'<div style="grid-column: 1/-1; text-align: center; padding: 2rem;">${t("cows_empty")}</div>',
    html
)

# Replace static tags inside JS string
html = html.replace('<span>Zoti:</span>', '<span>${t("cows_breed")}</span>')
html = html.replace('<span>Yoshi:</span>', '<span>${t("cows_age")}</span>')
html = html.replace('<span>Vazni:</span>', '<span>${t("cows_weight")}</span>')
html = html.replace("<span>Sog'in (kunlik):</span>", '<span>${t("cows_milk")}</span>')
html = html.replace("yosh</strong>", '${t("cows_age_yrs")}</strong>')
html = html.replace("Profil</h3>", '${t("cows_profile")}</h3>')
html = html.replace('Ma\\\'lumot yo\\\'q', '${t("cows_status_no_data")}')
html = html.replace('Sog\\\'lom', '${t("cows_status_healthy")}')
html = html.replace('<span>Harorat:</span>', '<span>${t("cows_temp")}</span>')
html = html.replace('<span>Chaynash:</span>', '<span>${t("cows_rum")}</span>')
html = html.replace('daqiqa', '${t("cows_mins")}')

# Update DOM properties in openViewModal
html = html.replace("document.getElementById('view_cow_temp').innerText = \"Ma'lumot yo'q\";", "document.getElementById('view_cow_temp').innerText = t('cows_status_no_data');")
html = html.replace("document.getElementById('view_cow_rum').innerText = \"Ma'lumot yo'q\";", "document.getElementById('view_cow_rum').innerText = t('cows_status_no_data');")

# Also call setLanguage inside renderCowsDatabase to translate dynamic data-i18n elements if there were any, 
# but here we used `t` directly so no need.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("cows.html updated.")
