import re
import codecs

with codecs.open('static/js/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

emojis = {
    '1': '🌡️',
    '2': '🩸',
    '3': '📉',
    '4': '🫁',
    '5': '🧠',
    '6': '🥛',
    '7': '🤢',
    '8': '🎈',
    '9': '👁️',
    '10': '💧'
}

for i in range(1, 11):
    emoji = emojis[str(i)]
    # Replace diag_select_
    content = re.sub(rf'("diag_select_[a-z]+": ")({i}\. )', rf'\1{emoji} \2', content)
    # Replace diag_sym_
    content = re.sub(rf'("diag_sym_{i}": ")({i}\. )', rf'\1{emoji} \2', content)

with codecs.open('static/js/translations.js', 'w', encoding='utf-8') as f:
    f.write(content)
