import os
import glob
import re

template_dir = 'd:/Diplom1/templates'
files = glob.glob(os.path.join(template_dir, '*.html'))

nav_links_to_add = '''
            <a href="/settings"><i class="fas fa-cog"></i> <span data-i18n="nav_settings">Sozlamalar</span></a>
            <a href="/logout" style="background: #ef4444;"><i class="fas fa-sign-out-alt"></i> <span data-i18n="nav_logout">Chiqish</span></a>
'''

lang_selector = '''
            <select id="langSwitch" class="modern-select" style="margin-top:15px; width:100%;">
                <option value="uz">O'zbek</option>
                <option value="ru">Русский</option>
                <option value="en">English</option>
                <option value="qq">Qaraqalpaq</option>
            </select>
'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all existing Sozlamalar and Chiqish
    content = re.sub(r'<a href="/settings".*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a href="/logout".*?</a>', '', content, flags=re.DOTALL)
    
    # 2. Remove language selector from navbar
    content = re.sub(r'<select id="langSwitch".*?</select>', '', content, flags=re.DOTALL)

    # 3. Add them back ONLY to the navbar if it exists
    if '<div class="nav-links">' in content:
        # insert before the closing div of nav-links
        # Since the closing div might be anywhere, let's find the end of nav-links
        # A simpler way: we know <a href="/about">...</a> is the last link usually.
        content = re.sub(r'(<a href="/about".*?</a>)', r'\1' + nav_links_to_add, content, count=1, flags=re.DOTALL)

    # 4. If this is settings.html, inject the language selector
    if 'settings.html' in file:
        if '<select id="langSwitch"' not in content:
            content = content.replace('</form>', '</form>' + lang_selector)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {file}")
