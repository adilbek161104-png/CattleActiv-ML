import re
import codecs

with codecs.open('templates/ai_diagnosis.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the inline style of symptom-btn with class-based approach
style_pattern = r' style="text-align: left; background: var\(--card-bg\); border: 1px solid var\(--border-color\); padding: 10px 15px; border-radius: 8px; cursor: pointer; color: var\(--text-color\); font-size: 0\.95rem; transition: 0\.3s; box-shadow: 0 2px 4px rgba\(0,0,0,0\.05\);"'
content = re.sub(style_pattern, '', content)

css_addition = """
                    .symptom-btn {
                        text-align: left; 
                        background: rgba(0, 0, 0, 0.3) !important; 
                        border: 1px solid rgba(255, 255, 255, 0.15) !important; 
                        padding: 10px 15px; 
                        border-radius: 8px; 
                        cursor: pointer; 
                        color: #ffffff !important; 
                        font-size: 0.95rem; 
                        transition: all 0.3s ease; 
                        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1), 0 2px 6px rgba(0,0,0,0.2) !important;
                        backdrop-filter: blur(5px);
                    }
                    .symptom-btn:hover {
                        background: rgba(0, 0, 0, 0.5) !important;
                        color: white !important;
                        transform: translateY(-2px);
                        border-color: var(--primary-color) !important;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
                    }
"""

content = re.sub(r'\.symptom-btn:hover \{.*?\n\s*\}', css_addition.strip(), content, flags=re.DOTALL)

with codecs.open('templates/ai_diagnosis.html', 'w', encoding='utf-8') as f:
    f.write(content)
