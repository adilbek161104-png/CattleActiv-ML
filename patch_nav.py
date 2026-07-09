import os
import glob

template_dir = 'd:/Diplom1/templates'
files = glob.glob(os.path.join(template_dir, '*.html'))

nav_add = '''
            <a href="/settings"><i class="fas fa-cog"></i> <span data-i18n="nav_settings">Sozlamalar</span></a>
            <a href="/logout" style="background: #ef4444;"><i class="fas fa-sign-out-alt"></i> <span data-i18n="nav_logout">Chiqish</span></a>
'''

for file in files:
    if 'login.html' in file or 'settings.html' in file: continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<a href="/logout"' not in content:
        content = content.replace('</select>', '</select>' + nav_add)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {file}")
