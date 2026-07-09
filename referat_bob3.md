# III-BOB. TIZIMNI AMALGA OSHIRISH NATIJALARI VA TAHLIL

Uchinchi bob qog'ozdagi nazariya va arxitektura qarorlarining haqiqiy dasturga aylanishi haqida. Bu yerda tizim interfeysi sinab ko'riladi, modelning integratsiyasi tahlil qilinadi va eng muhimi — CattleActiv-ML veb-platformasi real sharoitda qanday ishlashi namoyish etiladi. Ushbu bobda faqat nazariy jadvallar emas, balki bevosita o'zimiz yaratgan dasturning (Flask va SQLite asosidagi) arxitekturasi, sayt menyulari va ishlash mexanizmlari yoritilgan.

## 3.1. Dastlabki ma'lumotlar (Dataset) va Belgilar (Features)
Loyihada murakkab va serverni og'irlashtiruvchi o'nlab parametrlardan voz kechilib, amaliyotda eng ko'p axborot beruvchi **5 ta asosiy IoT datchik ko'rsatkichlari (features)** tanlab olindi. Bular qoramol bo'yinturug'idan real vaqtda kelishi rejalashtirilgan eng muhim metrikalardir:
1. `steps` (Qadamlar soni)
2. `movement_time` (Harakatlanish vaqti, daqiqa)
3. `rumination_minutes` (Kavsh qaytarish vaqti, daqiqa)
4. `temperature` (Tana harorati, °C)
5. `distance_from_herd` (Podadan uzoqligi, metr)

Aynan shu 5 ta parametr kompyuter resurslarini tejaydi va modelning juda tez (millisoniyalar ichida) xulosa chiqarishini ta'minlaydi. Model jami **8 xil holatni (sinfni)** tasniflashga o'rgatildi: Normal (Sog'lom), Mastit (Infeksiya), Ketoz (Acidosis), Lameness (Oqsoqlik), Estrus (Qizish), Hypocalcemia (Sut isitmasi), Heat Stress (Issiqlik stresi) va BRD (Pnevmoniya).

## 3.2. Sun'iy Intellekt va Qoidalar bazasi (Gibrid yondashuv)
Haqiqiy chorvachilik tizimlarida faqatgina "Qora quti" (Black-box) bo'lgan ML modellariga ishonish xavfli bo'lishi mumkin. Shu sababli, bizning prototipda **Gibrid yondashuv** qo'llanildi:
1. **Rule-based (Qoidalar asosida) tahlil:** Dasturimizda Maxsus Python mantiqi (`rules.py`) yozilgan bo'lib, u bevosita veterinar shifokorlar ishlatadigan qat'iy tibbiy shartlarni o'z ichiga oladi (Masalan, agar harorat > 39.5 bo'lsa, tana isitmasi).
2. **Machine Learning (Tasodifiy O'rmon - Random Forest) tahlili:** Qoidalardan tashqari, tizim ma'lumotlarni oldindan o'qitilgan `model.pkl` orqali o'tkazadi va umumiy patternlarga qarab xulosa beradi.

Bu orqali fermer ma'lumotlar bazasida (`cattle_activity` jadvalida) bir vaqtning o'zida ham qat'iy matematik xulosani (`rule_result`), ham sun'iy intellekt bashoratini (`ml_result`) ko'ra oladi.

## 3.3. Dasturiy tizim va Veb-Interfeys (Sayt menyulari)
Loyihaning ko'zga ko'rinadigan qismi — barcha qurilmalarga moslashuvchan (Responsive) zamonaviy veb-sayt ko'rinishida ishlab chiqildi. Interfeys foydalanuvchilar (fermer va veterinarlar) uchun imkon qadar sodda loyihalashtirilgan. Tizim quyidagi 6 ta asosiy menyudan iborat:

### 3.3.1. Bosh sahifa (Splash/Index)
Tizimning kirish qismi bo'lib, loyihaning maqsadi va asosiy yo'nalishlarini vizual jihatdan chiroyli animatsiyalar bilan taqdim etadi. Bu yerda foydalanuvchi tizimning umumiy ruhiyatini his qiladi va tezkor navigatsiya tugmalari orqali kerakli bo'limga o'tishi mumkin.

### 3.3.2. Bosh panel (Dashboard)
Eng ko'p ishlatiladigan markaziy oyna. 
* **Funksiyasi:** Barcha qoramollarning umumiy holatini bitta ekranda real vaqt rejimida ko'rsatish.
* **Mexanizmi:** Orqa fonda `/api/data` so'rovi ishlash orqali bazadan (`get_latest_status_by_cow()`) har bir qoramolning eng oxirgi sensor ko'rsatkichlari, harorati va sun'iy intellekt qo'ygan tashxisi yuklanadi. Qizil (xavf) va yashil (sog'lom) rangli indikatorlar orqali fermer podaning holatini soniyalarda tushuna oladi.

### 3.3.3. Qoramollar bazasi (Cows Profile)
Chorva mollari pasportizatsiyasi bo'limi.
* **Funksiyasi:** Yangi tug'ilgan yoki sotib olingan mollarni tizimga kiritish, ularning rasm va biometrik ma'lumotlarini (zoti, yoshi, vazni, sut unumdorligi) saqlash.
* **Mexanizmi:** Bu sahifa orqali ma'lumot kiritilganda dastur `/api/add_cow` manziliga murojaat qilib, rasmni mahalliy `uploads` papkasiga yuklaydi, qolgan ma'lumotlarni esa SQLite ma'lumotlar bazasining `cows_profile` jadvaliga yozadi. Qoramollarni tahrirlash va o'chirish (yo'q qilish) imkoniyatlari ham to'liq integratsiya qilingan.

### 3.3.4. IoT Simulyatsiya (Sensor Input)
Dasturning apparat (hardware) qismini sinovdan o'tkazish xonasi.
* **Funksiyasi:** Real datchiklar o'rnatilmagan paytda ham istalgan qoramol ID sini tanlab, qo'lda sensor ko'rsatkichlarini yuborish va model qanday javob qaytarishini sinash.
* **Mexanizmi:** Ma'lumotlar `/api/predict` manziliga yuboriladi, `joblib` yordamida yuklangan Random Forest modeli natija chiqaradi va ma'lumot tarixlari bazada saqlanadi. Keyinchalik ushbu bo'lim ESP32 kabi real platalar bilan ulash uchun API gateway vazifasini o'taydi.

### 3.3.5. AI Veterinar (AI Diagnosis)
Loyihaning eng noyob interaktiv bo'limlaridan biri.
* **Funksiyasi:** Chatbot ko'rinishidagi sun'iy intellekt yordamchisi. Fermer o'z qoramolining ID sini kiritib so'rov yuborganida, tizim avtomatik ravishda uning bazadagi so'nggi harorati va harakatlarini o'qib, o'zbek/qoraqalpoq tillarida matnli maslahat shakllantiradi (Masalan: *"Sizning qoramolingizda ketoz alomatlari sezilyapti, shoshilinch uglevodli ozuqa bering"*).
* **Mexanizmi:** Orqa fonda maxsus lug'at (Dictionary) va qat'iy mantiq yordamida tilga moslashtirilgan javoblar qaytariladi. Shuningdek, matnli simptom (masalan, "ishtahasi yo'q, holsiz") kiritilganda kalit so'zlar bo'yicha kasallik turini topish mexanizmi qo'shilgan.

### 3.3.6. Loyiha haqida (About)
Ushbu bo'lim loyiha mualliflari, tizimning yaratilish texnologiyalari va umumiy qoidalar haqida axborot beruvchi statik sahifadir.

## 3.4. Tizimning ishlash tezligi va ma'lumotlar bazasi ko'rsatkichlari
Ishlab chiqilgan arxitektura o'zining yengilligi bilan ajralib turadi:
* **Ma'lumotlar bazasi (SQLite):** Murakkab so'rovlar yuborilmagani va faylli tizimda ishlagani sababli ma'lumotlarni o'qish/yozish tezligi lokal kompyuterda mikrosaniyalar miqdorini tashkil etadi. Pythonning `sqlite3` kutubxonasi hech qanday qo'shimcha drayverlarsiz mukammal ishladi.
* **Bashorat tezligi (Latency):** Random Forest (`model.pkl`) modeli orqali bitta oynani (5 ta parametrdan iborat vektor) bashorat qilish o'rtacha 2-5 millisoniyani oladi. Bu degani, bir soniya ichida yuzlab qoramollar holatini qotishlarsiz tahlil qilish mumkin.
* **Tarqatish qulayligi:** Loyiha faqat veb-serverda emas, balki `PyInstaller` orqali to'g'ridan-to'g'ri mustaqil bajariluvchi (executable .exe) dastur sifatida kompilyatsiya qilinishga moslashtirildi. Bu internet aloqasi yo'q chekka hududlardagi fermalarda ham dasturni mahalliy tarmoqda ishlatish kafolatini beradi.

## 3.5. Xulosa va istiqboldagi rivojlanish yo'nalishlari
Ushbu uchinchi bob prototipning to'liq va funksional ishlashini amalda tasdiqladi. Dastur sensor ma'lumotlarni qabul qila oladi, AI va qoidalar asosida kaskadli analiz o'tkazib, natijalarni chiroyli interfeysda (Dashboard) fermerga yetkazadi.

Garchi hozirgi versiya SQLite va Flask orqali prototip darajasida ideal ishlayotgan bo'lsa-da, kelajakda (masalan, 10 000 dan ortiq hayvonlar tarmog'i ulanganda) tizimni mass-scaling qilish rejalashtirilgan. Kelgusidagi optimizatsiya bosqichida tizim **FastAPI** asinxron dvigateliga o'tkazilishi, sensor ma'lumotlarining xronologik tarixini tezkor tahlil qilish uchun esa **PostgreSQL va TimescaleDB** arxitekturasiga ko'chirilishi mo'ljallanmoqda. Bu yondashuv loyihaning nafaqat bugungi kundagi muammolarni hal qilishini, balki uzoq kelajakdagi sanoat darajasidagi yuklamalarga ham tayyor ekanligini ko'rsatadi.
