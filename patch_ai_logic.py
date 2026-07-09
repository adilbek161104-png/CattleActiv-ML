import re

file_path = 'd:/Diplom1/templates/ai_diagnosis.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add Clear button next to the input
old_input_area = re.search(r'<div class="chat-input-area"[^>]*>.*?</div>\s*</div>', html, re.DOTALL)
if old_input_area:
    new_input_area = """<div class="chat-input-area" style="margin-top: 1rem; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                    <select id="diseaseSelect" class="modern-select" style="border-radius: 8px; font-size: 1rem; flex: 0 0 auto;">
                        <option value="">Tayyor kasalliklar bo'yicha ma'lumot...</option>
                        <option value="oqsil">1. Oqsil (Yashur)</option>
                        <option value="kuydirgi">2. Kuydirgi (Sibir yarasi)</option>
                        <option value="brutsellyoz">3. Brutsellyoz</option>
                        <option value="qoraopka">4. Qorao'pka (Pasterellyoz)</option>
                        <option value="qutirish">5. Qutirish (Beshenstvo)</option>
                        <option value="mastit">6. Mastit</option>
                        <option value="ketoz">7. Ketoz</option>
                        <option value="timpaniya">8. Timpaniya (Qorin dam bo'lishi)</option>
                        <option value="leykoz">9. Leykoz</option>
                        <option value="telyazioz">10. Telyazioz (Ko'z qurti)</option>
                    </select>
                    <input type="text" id="symptomInput" class="modern-select" style="flex: 1; border-radius: 8px; font-size: 1rem;" placeholder="Kasallik belgilarini yozing..." data-i18n="diag_placeholder">
                    <button class="btn primary-btn chat-btn" onclick="askSymptomAi()" style="border-radius: 8px; background: var(--primary-color); padding: 0 1.5rem;"><i class="fas fa-paper-plane"></i> <span data-i18n="diag_ask">So'rash</span></button>
                    <button class="btn" onclick="document.getElementById('symptomChatBox').innerHTML = '';" style="border-radius: 8px; background: var(--danger-color); color: white; padding: 0 1.5rem;"><i class="fas fa-trash"></i> Tozalash</button>
                </div>
            </div>"""
    html = html.replace(old_input_area.group(0), new_input_area)

# Construct the large i18n object
script_insertion = """
        const diseaseDB = {
            'oqsil': {
                uz: {
                    name: "Oqsil (Yashur)",
                    symptoms: "🦠 <b>Turi:</b> Virusli va juda yuqumli kasallik.<br>🩺 <b>Belgilari:</b> Isitma, og'izdan so'lak oqishi, til va lablarda pufakchalar.",
                    details: "⚠️ <b>Asorati:</b> Yurak mushaklari shikastlanishi, sut kamayishi, buzovlar o'limi, cho'loqlik.<br>💊 <b>Davosi:</b> Maxsus davosi yo'q. Og'iz 2% borat kislotasi bilan yuviladi. Tuyoqlarga qatron surtiladi.<br>🛡️ <b>Profilaktika:</b> Faqat emlash orqali."
                },
                qq: {
                    name: "Oqsil (Yashur)",
                    symptoms: "🦠 <b>Túri:</b> Viruslı hám júdá juqpalı kesellik.<br>🩺 <b>Belgileri:</b> Isıtpa, awızdan silekey aǵıwı, til hám erinlerde kópirshikler.",
                    details: "⚠️ <b>Asıreti:</b> Júrek múskilleriniń zaqımlanıwı, sút azayıwı, buzawlardıń qırılıwı, sholaqlanıw.<br>💊 <b>Emlew:</b> Maxsus emi joq. Awız 2% borat kislotası menen juwıladı.<br>🛡️ <b>Aldın alıw:</b> Tek vakcinaciya arqalı."
                },
                ru: {
                    name: "Ящур",
                    symptoms: "🦠 <b>Тип:</b> Вирусное и высококонтагиозное заболевание.<br>🩺 <b>Симптомы:</b> Лихорадка, обильное слюноотделение, пузырьки на языке и губах.",
                    details: "⚠️ <b>Осложнения:</b> Поражение сердца, снижение надоев, хромота.<br>💊 <b>Лечение:</b> Специфического лечения нет. Промывание рта 2% борной кислотой.<br>🛡️ <b>Профилактика:</b> Вакцинация."
                },
                en: {
                    name: "Foot-and-Mouth Disease (FMD)",
                    symptoms: "🦠 <b>Type:</b> Highly contagious viral disease.<br>🩺 <b>Symptoms:</b> Fever, profuse salivation, blisters on tongue and lips.",
                    details: "⚠️ <b>Complications:</b> Heart damage, decreased milk yield, lameness.<br>💊 <b>Treatment:</b> No specific cure. Mouth washed with 2% boric acid.<br>🛡️ <b>Prevention:</b> Vaccination."
                }
            },
            'kuydirgi': {
                uz: {
                    name: "Kuydirgi (Sibir yarasi)",
                    symptoms: "🦠 <b>Turi:</b> Odamlar uchun ham o'ta xavfli yuqumli kasallik.<br>🩺 <b>Belgilari:</b> Tana haroratining keskin ko'tarilishi, burun va og'izdan qora qon kelishi.",
                    details: "⚠️ <b>Asorati:</b> O'lim bilan tugaydi. Sporalar tuproqda o'nlab yillar saqlanadi.<br>💊 <b>Davosi:</b> Ilk bosqichda maxsus zardob va katta dozada antibiotiklar (penitsillin).<br>❗ <b>Eslatma:</b> Hayvon o'lsa, yormasdan kuydirib ko'mish shart."
                },
                qq: {
                    name: "Kúydirgi (Sibir yarası)",
                    symptoms: "🦠 <b>Túri:</b> Adamlar ushın da júdá qáwipli juqpalı kesellik.<br>🩺 <b>Belgileri:</b> Dene temperaturasınıń keskin kóteriliwi, murın hám awızdan qara qan keliwi.",
                    details: "⚠️ <b>Asıreti:</b> Ólim menen tawsıladı. Sporalar topıraqta onlap jıllar saqlanadı.<br>💊 <b>Emlew:</b> Dáslepki basqıshta arnawlı zardob hám antibiotikler.<br>❗ <b>Esletpe:</b> Haywan ólse, soyıwǵa bolmaydı, jaǵıp kómiledi."
                },
                ru: {
                    name: "Сибирская язва",
                    symptoms: "🦠 <b>Тип:</b> Смертельно опасное инфекционное заболевание (в т.ч. для людей).<br>🩺 <b>Симптомы:</b> Резкое повышение температуры, выделение черной крови из носа и рта.",
                    details: "⚠️ <b>Осложнения:</b> Летальный исход. Споры сохраняются в почве десятилетиями.<br>💊 <b>Лечение:</b> На ранних стадиях сыворотка и антибиотики (пенициллин).<br>❗ <b>Важно:</b> Труп животного сжигают, вскрытие запрещено."
                },
                en: {
                    name: "Anthrax",
                    symptoms: "🦠 <b>Type:</b> Extremely dangerous infectious disease (zoonotic).<br>🩺 <b>Symptoms:</b> Sudden high fever, dark blood oozing from natural orifices.",
                    details: "⚠️ <b>Complications:</b> Usually fatal. Spores survive in soil for decades.<br>💊 <b>Treatment:</b> Early stage: specific antiserum and high-dose antibiotics.<br>❗ <b>Warning:</b> Carcass must be burned without necropsy."
                }
            },
            'brutsellyoz': {
                uz: {
                    name: "Brutsellyoz",
                    symptoms: "🦠 <b>Turi:</b> Surunkali kasallik (ko'payish organlariga ta'sir qiladi).<br>🩺 <b>Belgilari:</b> Sezilarli belgisiz o'tadi, asosan abort (bolatashlash) orqali bilinadi.",
                    details: "⚠️ <b>Asorati:</b> Bepushtlik, sutning yaroqsizligi. Odamga oson yuqadi.<br>💊 <b>Davosi:</b> Qoramollarni davolash samarasiz va xavfli.<br>❗ <b>Chora:</b> Kasal hayvonlar ajratilib so'yiladi. Qon tahlili o'tkaziladi."
                },
                qq: {
                    name: "Brukelloz",
                    symptoms: "🦠 <b>Túri:</b> Sozılmalı kesellik (kóbeyiw organlarına tásir etedi).<br>🩺 <b>Belgileri:</b> Jasırın ótedi, tiykarınan bala taslaw arqalı bilinedi.",
                    details: "⚠️ <b>Asıreti:</b> Tuwıw qábiletiniń joytılıwı, sút jaramsız bolıwı. Adamǵa da juǵadı.<br>💊 <b>Emlew:</b> Qaramallardı emlew qáwipli hám paydasız.<br>❗ <b>Shara:</b> Kesel haywanlar soyıwǵa jiberiledi. Qan analizi alınadı."
                },
                ru: {
                    name: "Бруцеллез",
                    symptoms: "🦠 <b>Тип:</b> Хроническое инфекционное заболевание репродуктивной системы.<br>🩺 <b>Симптомы:</b> Протекает бессимптомно, часто проявляется абортами.",
                    details: "⚠️ <b>Осложнения:</b> Бесплодие, негодность молока. Легко передается людям.<br>💊 <b>Лечение:</b> Лечение КРС неэффективно и опасно.<br>❗ <b>Меры:</b> Больных животных отправляют на убой."
                },
                en: {
                    name: "Brucellosis",
                    symptoms: "🦠 <b>Type:</b> Chronic infection affecting reproductive organs.<br>🩺 <b>Symptoms:</b> Often asymptomatic, mainly identified by abortions.",
                    details: "⚠️ <b>Complications:</b> Infertility, unusable milk. Zoonotic (spreads to humans).<br>💊 <b>Treatment:</b> Treating cattle is economically unviable and risky.<br>❗ <b>Action:</b> Infected animals must be culled."
                }
            },
            'qoraopka': {
                uz: {
                    name: "Qorao'pka (Pasterellyoz)",
                    symptoms: "🦠 <b>Turi:</b> Nafas yo'llari va o'pkaning yallig'lanishi.<br>🩺 <b>Belgilari:</b> Yo'tal, burundan yiringli suyuqlik kelishi, nafas qisishi.",
                    details: "⚠️ <b>Asorati:</b> O'pkaning yiringli yallig'lanishi, o'lim ko'rsatkichi yuqori.<br>💊 <b>Davosi:</b> Maxsus zardob va antibiotiklar (Terramitsin, Enrofloksatsin).<br>🛡️ <b>Qo'shimcha:</b> Vitaminlar va nafas olishni osonlashtiruvchi dorilar."
                },
                qq: {
                    name: "Qaraókpe (Pasterellyoz)",
                    symptoms: "🦠 <b>Túri:</b> Dem alıw jolları hám ókpeniń qabınıwı.<br>🩺 <b>Belgileri:</b> Jóteliw, murınnan irińli suwıqlıq aǵıwı, dem qısıwı.",
                    details: "⚠️ <b>Asıreti:</b> Ókpeniń irińli qabınıwı, ólim kórsetkishiniń joqarılıǵı.<br>💊 <b>Emlew:</b> Maxsus zardob hám antibiotikler (Terramicin, Enrofloksacin).<br>🛡️ <b>Qosımsha:</b> Vitaminler beriledi."
                },
                ru: {
                    name: "Пастереллез",
                    symptoms: "🦠 <b>Тип:</b> Воспаление дыхательных путей и легких.<br>🩺 <b>Симптомы:</b> Кашель, гнойные выделения из носа, одышка.",
                    details: "⚠️ <b>Осложнения:</b> Гнойное воспаление легких, высокая смертность.<br>💊 <b>Лечение:</b> Гипериммунная сыворотка и антибиотики (Террамицин).<br>🛡️ <b>Дополнительно:</b> Витамины и препараты для облегчения дыхания."
                },
                en: {
                    name: "Pasteurellosis (Bovine Respiratory Disease)",
                    symptoms: "🦠 <b>Type:</b> Respiratory tract and lung infection.<br>🩺 <b>Symptoms:</b> Coughing, purulent nasal discharge, shortness of breath.",
                    details: "⚠️ <b>Complications:</b> Purulent pneumonia, high mortality rate.<br>💊 <b>Treatment:</b> Hyperimmune serum and broad-spectrum antibiotics.<br>🛡️ <b>Extra:</b> Vitamins and respiratory relief meds."
                }
            },
            'qutirish': {
                uz: {
                    name: "Qutirish (Beshenstvo)",
                    symptoms: "🦠 <b>Turi:</b> Markaziy asab tizimiga ta'sir qiluvchi virusli kasallik.<br>🩺 <b>Belgilari:</b> Tajovuzkorlik, qo'rquv, yutish qobiliyatining yo'qolishi, falajlik.",
                    details: "⚠️ <b>Asorati:</b> Odamlar uchun hayotiy xavf. Hayvon doim o'ladi.<br>💊 <b>Davosi:</b> Davosi yo'q.<br>❗ <b>Chora:</b> Kasal hayvon darhol yo'q qilinadi. Har yili profilaktik emlash shart."
                },
                qq: {
                    name: "Qutırıw (Qudırıw)",
                    symptoms: "🦠 <b>Túri:</b> Oraylıq nerv sistemasına tásir etiwshi viruslı kesellik.<br>🩺 <b>Belgileri:</b> Basqalarǵa taslanıw, qorqıw, jutınıw qábiletin joytıw, sal bolıw.",
                    details: "⚠️ <b>Asıreti:</b> Adamlar ushın qáwipli. Haywan hár qashan óledi.<br>💊 <b>Emlew:</b> Emi joq.<br>❗ <b>Shara:</b> Kesel haywan joq etiledi. Hár jılı emlew kerek."
                },
                ru: {
                    name: "Бешенство",
                    symptoms: "🦠 <b>Тип:</b> Вирусное заболевание центральной нервной системы.<br>🩺 <b>Симптомы:</b> Агрессия или страх, невозможность глотать, паралич.",
                    details: "⚠️ <b>Осложнения:</b> Летальный исход. Смертельно опасно для людей.<br>💊 <b>Лечение:</b> Не излечимо.<br>❗ <b>Меры:</b> Животное подлежит уничтожению. Обязательна ежегодная вакцинация."
                },
                en: {
                    name: "Rabies",
                    symptoms: "🦠 <b>Type:</b> Viral disease affecting the central nervous system.<br>🩺 <b>Symptoms:</b> Aggressiveness or fear, inability to swallow, paralysis.",
                    details: "⚠️ <b>Complications:</b> Always fatal. Extremely dangerous to humans.<br>💊 <b>Treatment:</b> No cure.<br>❗ <b>Action:</b> Animal must be euthanized. Annual vaccination is required."
                }
            },
            'mastit': {
                uz: {
                    name: "Mastit",
                    symptoms: "🦠 <b>Turi:</b> Sut bezlarining yallig'lanishi.<br>🩺 <b>Belgilari:</b> Yelinning shishishi, qizarishi, sutda qon yoki yiring aralashishi.",
                    details: "⚠️ <b>Asorati:</b> Yelinning ishdan chiqishi (atrofiya), sutning butunlay yo'qolishi.<br>💊 <b>Davosi:</b> Yelin ichiga maxsus antibiotikli shprits-tubalar (Mastisan) yuboriladi.<br>🛡️ <b>Qo'shimcha:</b> Yelinni massaj qilish va quruq joyda saqlash."
                },
                qq: {
                    name: "Mastit",
                    symptoms: "🦠 <b>Túri:</b> Sút bezleriniń qabınıwı.<br>🩺 <b>Belgileri:</b> Jelini isedi, qızaradı, sútte qan yamasa iriń boladı.",
                    details: "⚠️ <b>Asıreti:</b> Jeliniń islemey qalıwı, súttiń tolıq joytılıwı.<br>💊 <b>Emlew:</b> Jelin ishi ushın arnawlı antibiotik shpricler (Mastisan) qollanıladı.<br>🛡️ <b>Qosımsha:</b> Jelin uqalanadı, qaramal qurǵaq jerde baǵıladı."
                },
                ru: {
                    name: "Мастит",
                    symptoms: "🦠 <b>Тип:</b> Воспаление молочных желез.<br>🩺 <b>Симптомы:</b> Отек вымени, покраснение, кровь или гной в молоке.",
                    details: "⚠️ <b>Осложнения:</b> Атрофия вымени, полная потеря молока.<br>💊 <b>Лечение:</b> Внутривыменные антибиотики в шприцах-тубах (Мастисан).<br>🛡️ <b>Дополнительно:</b> Массаж вымени, содержание в сухом месте."
                },
                en: {
                    name: "Mastitis",
                    symptoms: "🦠 <b>Type:</b> Inflammation of the mammary glands.<br>🩺 <b>Symptoms:</b> Udder swelling, redness, blood or pus in the milk.",
                    details: "⚠️ <b>Complications:</b> Atrophy of the udder, complete loss of milk production.<br>💊 <b>Treatment:</b> Intramammary antibiotic infusions (e.g., Mastisan).<br>🛡️ <b>Extra:</b> Udder massage and keeping the environment dry."
                }
            },
            'ketoz': {
                uz: {
                    name: "Ketoz",
                    symptoms: "🦠 <b>Turi:</b> Modda almashinuvi buzilishi.<br>🩺 <b>Belgilari:</b> Ishtahaning yo'qolishi, sut va siydikdan atseton hidi kelishi.",
                    details: "⚠️ <b>Asorati:</b> Jigar semirishi, bepushtlik va immunitet tushishi.<br>💊 <b>Davosi:</b> Vena ichiga 40% li glyukoza eritmasi yuboriladi.<br>🍲 <b>Parhez:</b> Kunjara kamaytirilib, sabzi va qand lavlagi ko'paytiriladi."
                },
                qq: {
                    name: "Ketoz",
                    symptoms: "🦠 <b>Túri:</b> Zatlar almasıwı buzılıwı.<br>🩺 <b>Belgileri:</b> Ishtaha joytıladı, sút hám siysekten aseton iysi keledi.",
                    details: "⚠️ <b>Asıreti:</b> Bawır semiriwi, tuwmastıq hám immunitet túsip ketiwi.<br>💊 <b>Emlew:</b> Vena ishine 40% glyukoza jiberiledi.<br>🍲 <b>Peyhiz:</b> Kunjaralar azaytılıp, palız eginleri kóbeytiledi."
                },
                ru: {
                    name: "Кетоз",
                    symptoms: "🦠 <b>Тип:</b> Нарушение обмена веществ.<br>🩺 <b>Симптомы:</b> Потеря аппетита, запах ацетона от молока и мочи.",
                    details: "⚠️ <b>Осложнения:</b> Ожирение печени, бесплодие, снижение иммунитета.<br>💊 <b>Лечение:</b> Внутривенно вводится 40% раствор глюкозы.<br>🍲 <b>Диета:</b> Уменьшение концентратов, добавление свеклы и моркови."
                },
                en: {
                    name: "Ketosis",
                    symptoms: "🦠 <b>Type:</b> Metabolic disorder.<br>🩺 <b>Symptoms:</b> Loss of appetite, breath/milk/urine smells like acetone.",
                    details: "⚠️ <b>Complications:</b> Fatty liver, infertility, immunosuppression.<br>💊 <b>Treatment:</b> Intravenous 40% glucose solution.<br>🍲 <b>Diet:</b> Reduce concentrates, increase high-quality forage and sweet roots."
                }
            },
            'timpaniya': {
                uz: {
                    name: "Timpaniya (Qorin dam bo'lishi)",
                    symptoms: "🦠 <b>Turi:</b> Katta qorinning gazlar bilan to'lib ketishi.<br>🩺 <b>Belgilari:</b> Qorinning chap tomoni shishishi, nafas olishning qiyinlashishi.",
                    details: "⚠️ <b>Asorati:</b> Tez yordam ko'rsatilmasa, hayvon bo'g'ilib o'ladi.<br>💊 <b>Davosi:</b> Og'iz orqali Timpanol yoki o'simlik yog'i ichiriladi.<br>❗ <b>Favqulodda chora:</b> Veterinar troakar bilan chap yonboshdan teshadi."
                },
                qq: {
                    name: "Timpaniya (Qarın isip ketiwi)",
                    symptoms: "🦠 <b>Túri:</b> Úlken qarınnıń gazler menen tolıwı.<br>🩺 <b>Belgileri:</b> Qarınnıń shep tárepi isedi, dem alıw qıyınlasadı.",
                    details: "⚠️ <b>Asıreti:</b> Tiyisli járdem kórsetilmese, dem qısıwınan óledi.<br>💊 <b>Emlew:</b> Awızdan Timpanol yamasa ósimlik mayı ishirtiledi.<br>❗ <b>Shara:</b> Veterinar qarınnıń shep tárepin tesip gazdi shıǵaradı."
                },
                ru: {
                    name: "Тимпания рубца",
                    symptoms: "🦠 <b>Тип:</b> Острое вздутие рубца (желудка) газами.<br>🩺 <b>Симптомы:</b> Вздутие левой стороны живота, затрудненное дыхание.",
                    details: "⚠️ <b>Осложнения:</b> Смерть от удушья (сдавливание легких и сердца).<br>💊 <b>Лечение:</b> Внутрь заливают Тимпанол или растительное масло.<br>❗ <b>Экстренно:</b> Прокол рубца троакаром (ветеринаром)."
                },
                en: {
                    name: "Bloat (Tympany)",
                    symptoms: "🦠 <b>Type:</b> Excessive accumulation of gas in the rumen.<br>🩺 <b>Symptoms:</b> Swelling on the left side of the abdomen, difficulty breathing.",
                    details: "⚠️ <b>Complications:</b> Death by asphyxiation due to lung/heart compression.<br>💊 <b>Treatment:</b> Oral administration of anti-bloat meds or vegetable oil.<br>❗ <b>Emergency:</b> Trocar insertion to release gas by a vet."
                }
            },
            'leykoz': {
                uz: {
                    name: "Leykoz",
                    symptoms: "🦠 <b>Turi:</b> Qon yaratish tizimining surunkali o'sma kasalligi.<br>🩺 <b>Belgilari:</b> Limfa tugunlarining shishishi, ko'zlarning bo'rtib chiqishi.",
                    details: "⚠️ <b>Asorati:</b> Davosi yo'q. Mahsuldorlik tushadi.<br>💊 <b>Davosi:</b> Davosi yo'q.<br>❗ <b>Chora:</b> Kasal hayvonlar podadan chiqariladi. Buzoqlar onasidan alohida boqiladi."
                },
                qq: {
                    name: "Leykoz",
                    symptoms: "🦠 <b>Túri:</b> Qan jaratıw sistemasınıń sozılmalı isik keselligi.<br>🩺 <b>Belgileri:</b> Limfa túyinleriniń isip ketiwi, kózlerdiń bórtip shıǵıwı.",
                    details: "⚠️ <b>Asıreti:</b> Emi joq. Ónimdarlıq túsip ketedi.<br>💊 <b>Emlew:</b> Emi joq.<br>❗ <b>Shara:</b> Kesellengen qaramallar padadan shıǵarıladı."
                },
                ru: {
                    name: "Лейкоз",
                    symptoms: "🦠 <b>Тип:</b> Хроническое опухолевое заболевание кровеносной системы.<br>🩺 <b>Симптомы:</b> Увеличение лимфоузлов, пучеглазие.",
                    details: "⚠️ <b>Осложнения:</b> Неизлечимо. Снижение продуктивности.<br>💊 <b>Лечение:</b> Не лечится.<br>❗ <b>Меры:</b> Инфицированные животные выбраковываются."
                },
                en: {
                    name: "Bovine Leukosis",
                    symptoms: "🦠 <b>Type:</b> Chronic neoplastic disease of the blood-forming tissues.<br>🩺 <b>Symptoms:</b> Swollen lymph nodes, bulging eyes.",
                    details: "⚠️ <b>Complications:</b> Incurable. Decreased productivity.<br>💊 <b>Treatment:</b> No treatment.<br>❗ <b>Action:</b> Culling of infected animals from the herd."
                }
            },
            'telyazioz': {
                uz: {
                    name: "Telyazioz (Ko'z qurti)",
                    symptoms: "🦠 <b>Turi:</b> Ko'z shilliq pardasiga parazit tushishi.<br>🩺 <b>Belgilari:</b> Ko'zdan yosh oqishi, yorug'likdan qo'rqish, ko'zning xiralashishi.",
                    details: "⚠️ <b>Asorati:</b> Ko'zning butunlay ko'r bo'lib qolishi, yiringli infeksiyalar.<br>💊 <b>Davosi:</b> Ko'z 3% borat kislotasi bilan yuviladi. Ivermek inyeksiya qilinadi.<br>🛡️ <b>Qo'shimcha:</b> Tetratsiklin mazi surtiladi."
                },
                qq: {
                    name: "Telyazioz (Kóz qurtı)",
                    symptoms: "🦠 <b>Túri:</b> Kózdiń silekey qabatına parazit tisiwi.<br>🩺 <b>Belgileri:</b> Kózden jas aǵıwı, jaqtılıqtan qorqıw, kózdiń xiralasıwı.",
                    details: "⚠️ <b>Asıreti:</b> Kózdiń tolıq soqır bolıwı, irińli infekciyalar.<br>💊 <b>Emlew:</b> Kóz 3% borat kislotası menen juwıladı. Ivermek shanshiladı.<br>🛡️ <b>Qosımsha:</b> Tetratsiklin mazı súrtiledi."
                },
                ru: {
                    name: "Телязиоз (Глазной червь)",
                    symptoms: "🦠 <b>Тип:</b> Паразитарное поражение слизистой оболочки глаза.<br>🩺 <b>Симптомы:</b> Слезотечение, светобоязнь, помутнение роговицы.",
                    details: "⚠️ <b>Осложнения:</b> Полная слепота, вторичные гнойные инфекции.<br>💊 <b>Лечение:</b> Промывание глаз 3% борной кислотой. Инъекции Ивермека.<br>🛡️ <b>Дополнительно:</b> Тетрациклиновая мазь."
                },
                en: {
                    name: "Thelaziasis (Eyeworm)",
                    symptoms: "🦠 <b>Type:</b> Parasitic infection of the eye's mucous membranes.<br>🩺 <b>Symptoms:</b> Tearing, photophobia, corneal opacity.",
                    details: "⚠️ <b>Complications:</b> Complete blindness, secondary purulent infections.<br>💊 <b>Treatment:</b> Eye wash with 3% boric acid. Ivermectin injections.<br>🛡️ <b>Extra:</b> Tetracycline eye ointment."
                }
            }
        };

        document.getElementById('diseaseSelect').addEventListener('change', function(e) {
            const key = e.target.value;
            if (!key) return;
            
            const chatBox = document.getElementById('symptomChatBox');
            const lang = localStorage.getItem('appLang') || 'uz';
            const data = diseaseDB[key][lang] || diseaseDB[key]['uz'];
            
            // Add User msg
            const userDiv = document.createElement('div');
            userDiv.className = 'chat-msg user-msg';
            userDiv.textContent = e.target.options[e.target.selectedIndex].text + " ?";
            chatBox.appendChild(userDiv);
            
            // Add AI msg with hidden details and a reveal button
            const aiDiv = document.createElement('div');
            aiDiv.className = 'chat-msg ai-msg';
            
            const reqId = Date.now();
            let btnText = "Davosi va asoratlarini ko'rish";
            if (lang === 'qq') btnText = "Emlew hám asıretlerin kóriw";
            if (lang === 'ru') btnText = "Показать лечение и осложнения";
            if (lang === 'en') btnText = "Show treatment & complications";

            aiDiv.innerHTML = `
                <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; color: var(--primary-color);">📌 ${data.name}</div>
                <div style="margin-bottom: 10px;">${data.symptoms}</div>
                <button id="btn_${reqId}" class="btn" style="background: rgba(139, 92, 246, 0.2); border: 1px solid var(--primary-color); color: white; padding: 5px 12px; font-size: 0.9rem; border-radius: 6px; cursor: pointer; margin-bottom: 5px;">
                    <i class="fas fa-plus-circle"></i> ${btnText}
                </button>
                <div id="details_${reqId}" style="display: none; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 10px;">
                    ${data.details}
                </div>
            `;
            
            chatBox.appendChild(aiDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Attach event
            document.getElementById(`btn_${reqId}`).addEventListener('click', function() {
                document.getElementById(`details_${reqId}`).style.display = 'block';
                this.style.display = 'none';
                chatBox.scrollTop = chatBox.scrollHeight;
            });
            
            // Reset select
            e.target.value = '';
        });
"""

# replace the old diseaseDatabase code
html = re.sub(r'const diseaseDatabase = \{.*?\n        \};\n\n        document\.getElementById\(\'diseaseSelect\'\)\.addEventListener\(\'change\', function\(e\) \{.*?\}\);', script_insertion.strip(), html, flags=re.DOTALL)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated ai_diagnosis.html with translated hide-reveal functionality.")
