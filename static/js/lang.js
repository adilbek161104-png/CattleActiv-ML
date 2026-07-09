document.addEventListener('DOMContentLoaded', () => {
    const langSwitch = document.getElementById('langSwitch');
    
    // Check localStorage for saved language, default to 'uz'
    const currentLang = localStorage.getItem('appLang') || 'uz';
    
    if (langSwitch) {
        langSwitch.value = currentLang;
        langSwitch.addEventListener('change', (e) => {
            const selectedLang = e.target.value;
            setLanguage(selectedLang);
        });
    }

    setLanguage(currentLang);
});

function setLanguage(lang) {
    if (!translations[lang]) return;
    
    localStorage.setItem('appLang', lang);
    
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            // Check if element is an input placeholder or standard text element
            if (el.tagName === 'INPUT' && el.hasAttribute('placeholder')) {
                el.placeholder = translations[lang][key];
            } else {
                // If the element has inner icons, preserve them
                const icon = el.querySelector('i');
                if (icon) {
                    el.innerHTML = '';
                    el.appendChild(icon);
                    el.innerHTML += ' ' + translations[lang][key];
                } else {
                    el.textContent = translations[lang][key];
                }
            }
        }
    });
}
