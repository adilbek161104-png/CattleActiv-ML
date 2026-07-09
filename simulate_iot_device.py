import time
import random
import requests

API_URL = "http://127.0.0.1:5000/api/predict"

# Global o'zgaruvchi: Har bir molning oxirgi pozitsiyasini saqlab turamiz
cow_positions = {}

def generate_random_sensor_data(cow_id, lat, lng, is_sick=False, disease_type=None):
    """
    Simulates real IoT sensor inputs for a specific cow.
    """
    if not is_sick:
        return {
            "cow_id": cow_id,
            "steps": random.randint(3000, 4000),
            "movement": round(random.uniform(4, 6), 1),
            "rumination": random.randint(450, 500),
            "temperature": round(random.uniform(38.0, 39.0), 1),
            "distance": random.randint(5, 20),
            "lat": lat,
            "lng": lng
        }
    else:
        if disease_type == "ketosis":
            return {
                "cow_id": cow_id,
                "steps": random.randint(1500, 2500),
                "movement": round(random.uniform(2, 4), 1),
                "rumination": random.randint(150, 200),
                "temperature": round(random.uniform(38.0, 38.5), 1),
                "distance": random.randint(30, 60),
                "lat": lat,
                "lng": lng
            }
        else: # mastitis
            return {
                "cow_id": cow_id,
                "steps": random.randint(2000, 3000),
                "movement": round(random.uniform(3, 5), 1),
                "rumination": random.randint(350, 400),
                "temperature": round(random.uniform(39.6, 40.5), 1),
                "distance": random.randint(10, 40),
                "lat": lat,
                "lng": lng
            }

def run_simulation():
    print("[IoT] ESP32 simulyatsiyasi ishga tushdi...")
    print("Har 5 soniyada qoramollar xaritada real yuradi va ma'lumot jo'natiladi.\n")
    
    # Jiltirbas batqaqligi markazi
    farm_lat = 44.1000
    farm_lng = 59.3500

    try:
        while True:
            try:
                cows_res = requests.get("http://127.0.0.1:5000/api/cows")
                cows_data = cows_res.json()
                registered_cows = cows_data.get('cows', [])
            except Exception as e:
                print(f"Baza ulanishda xato: {e}")
                registered_cows = []
            
            if not registered_cows:
                print("[Kutilmoqda] Bizada qoramol yo'q...")
                time.sleep(5)
                continue
                
            for cow in registered_cows:
                cow_id = cow['cow_id']
                
                # Agar mol birinchi marta xaritaga chiqayotgan bo'lsa, uni boshlang'ich nuqtaga qo'yamiz
                if cow_id not in cow_positions:
                    cow_positions[cow_id] = {
                        "lat": farm_lat + random.uniform(-0.005, 0.005),
                        "lng": farm_lng + random.uniform(-0.005, 0.005)
                    }
                else:
                    # Molni silliq "yurgizish" (har safar kichkina masofaga suriladi)
                    # 0.0001 gradus taxminan 10 metrga teng
                    cow_positions[cow_id]["lat"] += random.uniform(-0.0002, 0.0002)
                    cow_positions[cow_id]["lng"] += random.uniform(-0.0002, 0.0002)
                
                current_lat = cow_positions[cow_id]["lat"]
                current_lng = cow_positions[cow_id]["lng"]

                if cow_id == 4:
                    data = generate_random_sensor_data(cow_id, current_lat, current_lng, is_sick=True, disease_type="ketosis")
                elif cow_id == 7:
                    data = generate_random_sensor_data(cow_id, current_lat, current_lng, is_sick=True, disease_type="mastitis")
                else:
                    data = generate_random_sensor_data(cow_id, current_lat, current_lng, is_sick=(random.random() < 0.05), disease_type="mastitis")
                
                print(f"[Yuborilmoqda] Cow #{data['cow_id']} | GPS: {round(current_lat, 4)}, {round(current_lng, 4)}")
                
                try:
                    response = requests.post(API_URL, json=data)
                    result = response.json()
                    if result.get("success"):
                        print(f"  -> [OK] AI Tashxisi: {result['ml_result']}")
                    else:
                        print(f"  -> [XATO] Xatolik: {result.get('error')}")
                except requests.exceptions.ConnectionError:
                    print("  -> [XATO] Serverga ulanib bo'lmadi! Flask ishlayotganiga ishonch hosil qiling.")
            
            print("-" * 40)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[To'xtatildi] Simulyatsiya to'xtatildi.")

if __name__ == "__main__":
    run_simulation()
