def analyze_cattle_activity(steps, movement_time, rumination_minutes, temperature, distance_from_herd):
    """
    Qoramol kasalliklarini kompleks IoT sensorlari yordamida aniqlash.
    """
    alerts = []

    # 1. Haroratga asoslangan kasalliklar
    if temperature >= 40.5:
        alerts.append("🔴 XAVFLI: Harorat o'ta yuqori. Issiqlik stresi (Heat Stress) yoki Og'ir Infeksiya ehtimoli.")
    elif temperature >= 39.5:
        if rumination_minutes < 300:
            alerts.append("🔴 XAVFLI: Yuqori isitma va chaynashning keskin kamayishi (Infeksiya, Mastit yoki Pnevmoniya (BRD) ehtimoli).")
        else:
            alerts.append("🟠 OGOHLANTIRISH: Tana harorati yuqori (Mastit yoki Pnevmoniya boshlang'ich belgisi).")
    elif temperature < 37.5:
        if steps < 500:
            alerts.append("🔴 XAVFLI: Harorat me'yordan past va harakat umuman yo'q (Sut isitmasi - Hypocalcemia xavfi!).")
        else:
            alerts.append("🟡 DIQQAT: Harorat me'yordan past (Gipotermiya yoki umumiy holsizlik).")

    # 2. Chaynash (Rumination) asosida (Ketoz, Acidosis)
    # Normal chaynash vaqti: 400 - 500 daqiqa (kuniga)
    if rumination_minutes < 250:
        if movement_time < 2:
            alerts.append("🔴 XAVFLI: Chaynash deyarli to'xtagan va qoramol yotib qolgan (Og'ir Ketoz / Acidosis xavfi).")
        else:
            alerts.append("🟠 OGOHLANTIRISH: Chaynash vaqti keskin kam (Oshqozon kasalligi yoki Stress).")
    
    # 3. Faollik (Harakat) asosida (Lameness, Estrus)
    # Normal yurish vaqti: 4-6 soat
    if steps < 1000 or movement_time < 1:
        alerts.append("🔴 XAVFLI: Harakat keskin kamaygan, qoramol uzoq yotibdi (Lameness / Oyoq og'rig'i ehtimoli).")
    elif steps > 7000 and movement_time > 10:
        if temperature > 38.5:
            alerts.append("🟢 ESTRUS: Harakatning keskin oshishi (Qizish davri yoki bezovtalik).")

    # 4. Joylashuv (GPS) asosida
    # Podadan ajralish masofasi: > 50 metr shubhali
    if distance_from_herd > 100:
        alerts.append("🟠 OGOHLANTIRISH: GPS bo'yicha qoramol podadan juda uzoqda (Kasallik tufayli yolg'izlanish yoki O'g'irlik xavfi).")

    # Xulosa qilish
    if not alerts:
        return "✅ NORMAL HOLAT: Barcha ko'rsatkichlar me'yorda. Qoramol sog'lom."
    
    return " | ".join(alerts)
