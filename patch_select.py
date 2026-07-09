import os, glob, re
for f in glob.glob('d:/Diplom1/templates/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = r'<select id="langSwitch" class="modern-select"[^>]+>'
    replacement = r'<select id="langSwitch" class="modern-select">'
    new_content = re.sub(pattern, replacement, content)
    if content != new_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Patched {f}')
