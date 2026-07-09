import re
import codecs

with codecs.open('static/js/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_keys = {
    'uz': {
        'diag_clear': 'Tozalash',
        'diag_thinking': 'O\'ylanmoqda...',
        'diag_error': 'Xatolik yuz berdi. Iltimos keyinroq qayta urinib ko\'ring.',
        'diag_select_default': 'Tayyor kasalliklar bo\'yicha ma\'lumot...',
        'diag_select_oqsil': '1. Oqsil (Yashur)',
        'diag_select_kuydirgi': '2. Kuydirgi (Sibir yarasi)',
        'diag_select_brutsellyoz': '3. Brutsellyoz',
        'diag_select_qoraopka': '4. Qorao\'pka (Pasterellyoz)',
        'diag_select_qutirish': '5. Qutirish (Beshenstvo)',
        'diag_select_mastit': '6. Mastit',
        'diag_select_ketoz': '7. Ketoz',
        'diag_select_timpaniya': '8. Timpaniya (Qorin dam bo\'lishi)',
        'diag_select_leykoz': '9. Leykoz',
        'diag_select_telyazioz': '10. Telyazioz (Ko\'z qurti)',
        'diag_sym_title': 'Kasallik belgilari bo\'yicha tezkor tanlov:',
        'diag_sym_1': '1. Kasallik belgilar: Isitma, og\'izdan so\'lak oqishi, til va lablarda pufakchalar paydo bo\'lishi.',
        'diag_sym_2': '2. Kasallik belgilar: Tana haroratining keskin ko\'tarilishi, tabiiy teshiklardan qora qon kelishi.',
        'diag_sym_3': '3. Kasallik belgilar: Ko\'pincha sezilarli belgisiz o\'tadi, asosan abort (bolatashlash) orqali bilinadi.',
        'diag_sym_4': '4. Kasallik belgilar: Yo\'tal, burundan yiringli suyuqlik kelishi, nafas qisishi.',
        'diag_sym_5': '5. Kasallik belgilar: Tajovuzkorlik yoki haddan tashqari qo\'rquv, yutish qobiliyatining yo\'qolishi, falajlik.',
        'diag_sym_6': '6. Kasallik belgilar: Yelinning shishishi, qizarishi, sutning tarkibi o\'zgarishi (qon yoki yiring aralashishi).',
        'diag_sym_7': '7. Kasallik belgilar: Ishtahaning yo\'qolishi, sut va siydikdan atseton hidi kelishi.',
        'diag_sym_8': '8. Kasallik belgilar: Qorinning chap tomoni shishishi, hayvonning bezovtalanishi, nafas olishning qiyinlashishi.',
        'diag_sym_9': '9. Kasallik belgilar: Tashqi bezlarning (limfa tugunlarining) shishishi, ko\'zlarning bo\'rtib chiqishi.',
        'diag_sym_10': '10. Kasallik belgilar: Ko\'zdan yosh oqishi, yorug\'likdan qo\'rqish, ko\'zning xiralashishi.'
    },
    'ru': {
        'diag_clear': 'Очистить',
        'diag_thinking': 'Думаю...',
        'diag_error': 'Произошла ошибка. Пожалуйста, попробуйте позже.',
        'diag_select_default': 'Информация по готовым заболеваниям...',
        'diag_select_oqsil': '1. Ящур',
        'diag_select_kuydirgi': '2. Сибирская язва',
        'diag_select_brutsellyoz': '3. Бруцеллез',
        'diag_select_qoraopka': '4. Пастереллез',
        'diag_select_qutirish': '5. Бешенство',
        'diag_select_mastit': '6. Мастит',
        'diag_select_ketoz': '7. Кетоз',
        'diag_select_timpaniya': '8. Тимпания',
        'diag_select_leykoz': '9. Лейкоз',
        'diag_select_telyazioz': '10. Телязиоз (Глазной червь)',
        'diag_sym_title': 'Быстрый выбор по симптомам:',
        'diag_sym_1': '1. Симптомы: Лихорадка, слюнотечение, появление пузырьков на языке и губах.',
        'diag_sym_2': '2. Симптомы: Резкое повышение температуры, выделение черной крови из естественных отверстий.',
        'diag_sym_3': '3. Симптомы: Часто протекает бессимптомно, в основном проявляется абортами.',
        'diag_sym_4': '4. Симптомы: Кашель, гнойные выделения из носа, одышка.',
        'diag_sym_5': '5. Симптомы: Агрессия или сильный страх, потеря способности глотать, паралич.',
        'diag_sym_6': '6. Симптомы: Отек и покраснение вымени, изменение состава молока (с кровью или гноем).',
        'diag_sym_7': '7. Симптомы: Потеря аппетита, запах ацетона от молока и мочи.',
        'diag_sym_8': '8. Симптомы: Вздутие левой стороны живота, беспокойство животного, затрудненное дыхание.',
        'diag_sym_9': '9. Симптомы: Увеличение внешних желез (лимфоузлов), выпучивание глаз.',
        'diag_sym_10': '10. Симптомы: Слезотечение, светобоязнь, помутнение глаз.'
    },
    'en': {
        'diag_clear': 'Clear',
        'diag_thinking': 'Thinking...',
        'diag_error': 'An error occurred. Please try again later.',
        'diag_select_default': 'Information on known diseases...',
        'diag_select_oqsil': '1. Foot-and-Mouth Disease (FMD)',
        'diag_select_kuydirgi': '2. Anthrax',
        'diag_select_brutsellyoz': '3. Brucellosis',
        'diag_select_qoraopka': '4. Pasteurellosis',
        'diag_select_qutirish': '5. Rabies',
        'diag_select_mastit': '6. Mastitis',
        'diag_select_ketoz': '7. Ketosis',
        'diag_select_timpaniya': '8. Tympany (Bloat)',
        'diag_select_leykoz': '9. Leukosis',
        'diag_select_telyazioz': '10. Thelaziasis (Eyeworm)',
        'diag_sym_title': 'Quick selection by symptoms:',
        'diag_sym_1': '1. Symptoms: Fever, drooling, appearance of blisters on the tongue and lips.',
        'diag_sym_2': '2. Symptoms: Sharp rise in temperature, black blood from natural openings.',
        'diag_sym_3': '3. Symptoms: Often asymptomatic, mainly manifested by abortions.',
        'diag_sym_4': '4. Symptoms: Cough, purulent nasal discharge, shortness of breath.',
        'diag_sym_5': '5. Symptoms: Aggression or extreme fear, loss of ability to swallow, paralysis.',
        'diag_sym_6': '6. Symptoms: Swelling and redness of the udder, changes in milk (blood or pus mixed).',
        'diag_sym_7': '7. Symptoms: Loss of appetite, smell of acetone from milk and urine.',
        'diag_sym_8': '8. Symptoms: Swelling on the left side of the abdomen, restlessness, difficulty breathing.',
        'diag_sym_9': '9. Symptoms: Swelling of external glands (lymph nodes), bulging eyes.',
        'diag_sym_10': '10. Symptoms: Tearing, photophobia, clouding of the eyes.'
    },
    'qq': {
        'diag_clear': 'Tazalaw',
        'diag_thinking': 'Oylanbaqta...',
        'diag_error': 'Qátelik júz berdi. Iltimas keyinrek qayta urınıp kóriń.',
        'diag_select_default': 'Tayyar kesellikler boyınsha maǵlıwmat...',
        'diag_select_oqsil': '1. Awzıl (Yashur)',
        'diag_select_kuydirgi': '2. Kúydirgi (Sibir yarası)',
        'diag_select_brutsellyoz': '3. Brucellyoz',
        'diag_select_qoraopka': '4. Qaraókpe (Pasterellyoz)',
        'diag_select_qutirish': '5. Qutırıw (Beshenstvo)',
        'diag_select_mastit': '6. Mastit',
        'diag_select_ketoz': '7. Ketoz',
        'diag_select_timpaniya': '8. Timpaniya (Qarın isip ketiwi)',
        'diag_select_leykoz': '9. Leykoz',
        'diag_select_telyazioz': '10. Telyazioz (Kóz qurtı)',
        'diag_sym_title': 'Kesellik belgileri boyınsha tez ańlaw:',
        'diag_sym_1': '1. Kesellik belgiler: Isitpa, awzınan silekey aǵıwı, til hám erinlerde kópirshikler payda bolıwı.',
        'diag_sym_2': '2. Kesellik belgiler: Dene temperaturasınıń keskin kóteriliwi, tábiyiy tesiklerinen qara qan keliwi.',
        'diag_sym_3': '3. Kesellik belgiler: Kóbinese sezilerli belgisiz ótedi, tiykarınan abort (balataslaw) arqalı bilinedi.',
        'diag_sym_4': '4. Kesellik belgiler: Jóteliw, murnınan irińli suyıqlıq keliwi, dem qısıwı.',
        'diag_sym_5': '5. Kesellik belgiler: Kúshli qorqıw yamasa agressiya, jutıw qábiliyetiniń joytılıwı, falajlıq.',
        'diag_sym_6': '6. Kesellik belgiler: Jeliniń isip ketiwi, qızarıwı, súttiń quramı ózgeriwi (qan yamasa iriń aralasıwı).',
        'diag_sym_7': '7. Kesellik belgiler: Tábeyiniń joytılıwı, sút hám siydekten aceton iyisi keliwi.',
        'diag_sym_8': '8. Kesellik belgiler: Qarınnıń shep tárepi isiwi, haywannıń biymázalanishi, dem alıwdıń qıyınlasıwı.',
        'diag_sym_9': '9. Kesellik belgiler: Sırtqı bezlerdiń (limfa túyinleriniń) isip ketiwi, kózlerdiń bórtip shıǵıwı.',
        'diag_sym_10': '10. Kesellik belgiler: Kózden jas aǵıwı, jaqtılıqtan qorqıw, kózdiń xiralasıwı.'
    }
}

for lang, keys in new_keys.items():
    # Construct replacement string
    insert_str = ""
    for k, v in keys.items():
        v = v.replace("'", "\\'")
        insert_str += f'        "{k}": "{v}",\n'
    
    # Find insertion point
    pattern = r'("' + lang + r'":\s*\{)(.*?)(cows_cow_num)'
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        # insert before cows_cow_num
        content = content.replace(match.group(0), match.group(1) + match.group(2) + insert_str + '        "cows_cow_num"')

with codecs.open('static/js/translations.js', 'w', encoding='utf-8') as f:
    f.write(content)
