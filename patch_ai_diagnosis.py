import re

file_path = 'd:/Diplom1/templates/ai_diagnosis.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the chat input area
old_input_area = """                <div class="chat-input-area" style="margin-top: 1rem; display: flex; gap: 10px;">
                    <input type="text" id="symptomInput" class="modern-select" style="flex: 1; border-radius: 8px; font-size: 1rem;" placeholder="Kasallik belgilarini yozing..." data-i18n="diag_placeholder">
                    <button class="btn primary-btn chat-btn" onclick="askSymptomAi()" style="border-radius: 8px; background: var(--primary-color); padding: 0 1.5rem;"><i class="fas fa-paper-plane"></i> <span data-i18n="diag_ask">So'rash</span></button>
                </div>"""

new_input_area = """                <div class="chat-input-area" style="margin-top: 1rem; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
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
                </div>"""

html = html.replace(old_input_area, new_input_area)

# Add the diseaseDatabase and the select listener to the <script> block
script_insertion = """        const diseaseDatabase = {
            'oqsil': `📌 Kasallik nomi: Oqsil (Yashur)
🦠 Turi: Bu virusli va juda yuqumli kasallik bo'lib, asosan og'iz bo'shlig'i, tili va tuyoqlariga zarar yetkazadi.
🩺 Belgilari: Isitma, og'izdan so'lak oqishi, til va lablarda pufakchalar paydo bo'lishi.
⚠️ Asorati: Hayvonning yurak mushaklari shikastlanishi (miokardit), sut mahsuldorligining keskin kamayishi, buzovlarning ommaviy o'limi va tuyoqlar tushib ketishi natijasida cho'loqlik.
💊 Davosi: Maxsus davosi yo'q (virusli bo'lgani uchun), asosan simptomatik davolanadi.
🛠️ Davolash: Og'iz bo'shlig'i 2% li borat kislotasi yoki margansovka eritmasi bilan yuviladi. Tuyoqlarga mis kuporosi yoki qatron (degtyar) surtiladi.
🛡️ Profilaktika: Faqat emlash (vaksinatsiya) orqali oldi olinadi.`,

            'kuydirgi': `📌 Kasallik nomi: Kuydirgi (Sibir yarasi)
🦠 Turi: Odamlar uchun ham o'ta xavfli bo'lgan o'tkir yuqumli kasallik.
🩺 Belgilari: Tana haroratining keskin ko'tarilishi, tabiiy teshiklardan (burun, og'iz, orqa chiqaruv a'zosi) qora qon kelishi.
⚠️ Asorati: Ko'pincha o'lim bilan tugaydi. Kasallik o'chog'i bo'lgan joylarda sporalar o'nlab yillar davomida tuproqda saqlanib qolishi mumkin.
💊 Davosi: Kasallikning ilk bosqichida kuydirgi o'tiga qarshi maxsus zardob va katta dozada antibiotiklar (penitsillin guruhi) qo'llaniladi.
❗ Eslatma: Kasallik o'ta xavfli bo'lgani uchun hayvon o'lsa, uni yormasdan kuydirib ko'mish shart.`,

            'brutsellyoz': `📌 Kasallik nomi: Brutsellyoz
🦠 Turi: Surunkali kechuvchi kasallik bo'lib, hayvonning ko'payish organlariga ta'sir qiladi.
🩺 Belgilari: Ko'pincha sezilarli belgisiz o'tadi, asosan abort (bolatashlash) orqali bilinadi.
⚠️ Asorati: Urg'ochi hayvonlarning bepusht bo'lib qolishi, yo'ldoshning ushlanib qolishi va sutning iste'molga yaroqsiz bo'lishi. Insonlarga ham oson yuqadi.
💊 Davosi: Afsuski, qoramollarda brutsellyozni davolash iqtisodiy jihatdan samarasiz va xavfli hisoblanadi.
❗ Chora: Kasal hayvonlar aniqlansa, ular alohida ajratiladi va so'yishga yuboriladi. Podani sog'lomlashtirish uchun muntazam qon tahlili o'tkaziladi.`,

            'qoraopka': `📌 Kasallik nomi: Qorao'pka (Pasterellyoz)
🦠 Turi: Nafas yo'llari va o'pkaning yallig'lanishi bilan kechadigan infeksiya.
🩺 Belgilari: Yo'tal, burundan yiringli suyuqlik kelishi, nafas qisishi.
⚠️ Asorati: O'pkaning yiringli yallig'lanishi (plevropnevmoniya) va hayvonning ozib ketishi, o'lim ko'rsatkichining yuqoriligi.
💊 Davosi: Pasterellyozga qarshi maxsus zardob (giperimmun zardob) va keng spektrli antibiotiklar (Terramitsin, Enrofloksatsin) qo'llaniladi.
🛡️ Qo'shimcha: Hayvonga vitaminlar va nafas olishni osonlashtiruvchi dorilar beriladi.`,

            'qutirish': `📌 Kasallik nomi: Qutirish (Beshenstvo)
🦠 Turi: Markaziy asab tizimiga ta'sir qiluvchi virusli kasallik.
🩺 Belgilari: Tajovuzkorlik yoki haddan tashqari qo'rquv, yutish qobiliyatining yo'qolishi, falajlik.
⚠️ Asorati: Davosi yo'q, hayvon har doim o'ladi. Odamlar uchun hayotiy xavf tug'diradi.
💊 Davosi: Davosi yo'q.
❗ Chora: Kasal hayvon darhol yo'q qilinadi. Oldini olishning yagona chorasi — har yili itlar va chorva hayvonlarini profilaktik emlash.`,

            'mastit': `📌 Kasallik nomi: Mastit
🦠 Turi: Sut bezlarining yallig'lanishi. Ko'pincha noto'g'ri sog'ish yoki gigiyena qoidalariga amal qilmaslikdan kelib chiqadi.
🩺 Belgilari: Yelinning shishishi, qizarishi, sutning tarkibi o'zgarishi (qon yoki yiring aralashishi).
⚠️ Asorati: Yelinning bir qismi yoki hammasining ishdan chiqishi (atrofiya), sutning butunlay yo'qolishi.
💊 Davosi: Yelin ichiga yuboriladigan maxsus antibiotikli shprits-tubalar (Mastisan, Mastiyet-forte) qo'llaniladi.
🛡️ Qo'shimcha: Yelinni massaj qilish (faqat yiringli bo'lmasa), tez-tez sog'ib tashlash va hayvonni quruq joyda saqlash.`,

            'ketoz': `📌 Kasallik nomi: Ketoz
🦠 Turi: Modda almashinuvi buzilishi bilan bog'liq kasallik (asosan yuqori mahsuldor sigirlarda).
🩺 Belgilari: Ishtahaning yo'qolishi, sut va siydikdan atseton hidi kelishi.
⚠️ Asorati: Jigar semirishi, bepushtlik va immunitetning keskin tushishi natijasida boshqa kasalliklarga beriluvchanlik.
💊 Davosi: Qondagi qand miqdorini oshirish uchun vena ichiga 40% li glyukoza eritmasi yuboriladi.
🍲 Parhez: Ratsiondagi konsentrat (kunjara) yemlarni kamaytirib, sifatli pishloq, sabzi va qand lavlagi ko'paytiriladi. Ichishga ichimlik sodasi eritmasi beriladi.`,

            'timpaniya': `📌 Kasallik nomi: Timpaniya (Qorin dam bo'lishi)
🦠 Turi: Katta qorinning gazlar bilan to'lib ketishi.
🩺 Belgilari: Qorinning chap tomoni shishishi, hayvonning bezovtalanishi, nafas olishning qiyinlashishi.
⚠️ Asorati: Agar tez yordam ko'rsatilmasa (gaz chiqarilmasa), hayvon bo'g'ilib o'ladi (yurak va o'pkaning siqilishi natijasida).
💊 Davosi: Zudlik bilan gazni chiqarish uchun og'iz orqali Timpanol yoki o'simlik yog'i ichiriladi.
❗ Favqulodda chora: Agar dori yordam bermasa, veterinar tomonidan troakar bilan chap yonboshdan teshilib, gaz chiqarib yuboriladi.`,

            'leykoz': `📌 Kasallik nomi: Leykoz
🦠 Turi: Qon yaratish tizimining surunkali o'sma kasalligi.
🩺 Belgilari: Tashqi bezlarning (limfa tugunlarining) shishishi, ko'zlarning bo'rtib chiqishi.
⚠️ Asorati: Davosi yo'q. Mahsuldorlik tushadi, hayvon go'shti va suti faqat texnik qayta ishlashga yuboriladi yoki yo'q qilinadi.
💊 Davosi: Davosi yo'q.
❗ Chora: Kasallik genetik darajada va qon orqali o'tishi sababli, Leykoz bilan kasallangan hayvonlar podadan chiqariladi. Sog'lom buzoqlarni saqlab qolish uchun ularni onasidan alohida boqish tavsiya etiladi.`,

            'telyazioz': `📌 Kasallik nomi: Telyazioz (Ko'z qurti)
🦠 Turi: Ko'zning shilliq pardasiga parazit chuvalchanglarning tushishi.
🩺 Belgilari: Ko'zdan yosh oqishi, yorug'likdan qo'rqish, ko'zning xiralashishi.
⚠️ Asorati: Ko'zning butunlay ko'r bo'lib qolishi va ikkinchi darajali yiringli infeksiyalar rivojlanishi.
💊 Davosi: Ko'z xaltachasi 3% li borat kislotasi eritmasi bilan yuviladi. Chuvalchanglarni o'ldirish uchun Ivermek yoki shunga o'xshash preparatlar inyeksiya qilinadi.
🛡️ Qo'shimcha: Ko'zga tetratsiklin mazini surtish orqali yallig'lanish olinadi.`
        };

        document.getElementById('diseaseSelect').addEventListener('change', function(e) {
            const key = e.target.value;
            if (!key) return;
            
            const chatBox = document.getElementById('symptomChatBox');
            
            // Add User msg for the selection
            const userDiv = document.createElement('div');
            userDiv.className = 'chat-msg user-msg';
            userDiv.textContent = e.target.options[e.target.selectedIndex].text + " haqida to'liq ma'lumot bering.";
            chatBox.appendChild(userDiv);
            
            // Add AI msg
            const aiDiv = document.createElement('div');
            aiDiv.className = 'chat-msg ai-msg';
            aiDiv.style.whiteSpace = 'pre-line';
            aiDiv.textContent = diseaseDatabase[key];
            chatBox.appendChild(aiDiv);
            
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // reset select
            e.target.value = '';
        });
"""

html = html.replace("    <script>\n        async function askSymptomAi() {", "    <script>\n" + script_insertion + "\n        async function askSymptomAi() {")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("ai_diagnosis.html updated.")
