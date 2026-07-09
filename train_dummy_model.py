import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def create_advanced_model():
    print("Advanced AI Model o'qitilmoqda (Mastit, Ketoz, Lameness, Estrus)...")
    
    # Features: [steps, movement_time, rumination_minutes, temperature, distance_from_herd]
    np.random.seed(42)
    
    # 0. Normal holat: O'rtacha parametrlar
    normal = np.c_[
        np.random.randint(2500, 4500, 200),      # steps
        np.random.uniform(4, 7, 200),            # movement_time
        np.random.randint(400, 550, 200),        # rumination
        np.random.uniform(38.0, 39.2, 200),      # temp
        np.random.uniform(0, 20, 200),           # distance
        np.zeros(200)                            # label 0
    ]
    
    # 1. Mastit/Infeksiya: Yuqori isitma, biroz kam chaynash
    mastitis = np.c_[
        np.random.randint(1500, 3000, 100),
        np.random.uniform(3, 5, 100),
        np.random.randint(300, 400, 100),
        np.random.uniform(39.5, 41.0, 100),
        np.random.uniform(10, 40, 100),
        np.ones(100)                             # label 1
    ]
    
    # 2. Ketoz/Acidosis: Chaynash keskin past, harorat normal
    ketosis = np.c_[
        np.random.randint(1000, 2500, 100),
        np.random.uniform(2, 4, 100),
        np.random.randint(100, 250, 100),        # chaynash keskin past
        np.random.uniform(37.5, 38.8, 100),
        np.random.uniform(20, 60, 100),
        np.full(100, 2)                          # label 2
    ]
    
    # 3. Lameness (Oyoq og'rig'i): Qadamlar kam, yotish ko'p
    lameness = np.c_[
        np.random.randint(200, 800, 100),        # qadamlar kam
        np.random.uniform(0.5, 2, 100),
        np.random.randint(350, 450, 100),
        np.random.uniform(38.0, 39.0, 100),
        np.random.uniform(50, 150, 100),         # podadan ortda qoladi
        np.full(100, 3)                          # label 3
    ]
    
    # 4. Estrus (Qizish): Harakat keskin ko'p
    estrus = np.c_[
        np.random.randint(6000, 10000, 100),     # juda faol
        np.random.uniform(9, 14, 100),
        np.random.randint(350, 450, 100),
        np.random.uniform(38.5, 39.5, 100),
        np.random.uniform(10, 50, 100),
        np.full(100, 4)                          # label 4
    ]
    
    # 5. Hypocalcemia (Sut isitmasi): Past harorat, harakat deyarli yo'q
    hypocalcemia = np.c_[
        np.random.randint(50, 300, 100),
        np.random.uniform(0.1, 1, 100),
        np.random.randint(100, 200, 100),
        np.random.uniform(36.0, 37.5, 100),
        np.random.uniform(50, 150, 100),
        np.full(100, 5)                          # label 5
    ]
    
    # 6. Heat Stress (Issiqlik stresi): Juda yuqori harorat, chaynash past
    heat_stress = np.c_[
        np.random.randint(2000, 4000, 100),
        np.random.uniform(3, 6, 100),
        np.random.randint(200, 300, 100),
        np.random.uniform(40.5, 42.0, 100),
        np.random.uniform(0, 30, 100),
        np.full(100, 6)                          # label 6
    ]
    
    # 7. BRD (Pnevmoniya): Harorat baland, harakat va chaynash past
    brd = np.c_[
        np.random.randint(500, 1500, 100),
        np.random.uniform(1, 3, 100),
        np.random.randint(150, 250, 100),
        np.random.uniform(39.8, 41.0, 100),
        np.random.uniform(20, 80, 100),
        np.full(100, 7)                          # label 7
    ]
    
    # Birlashtirish
    dataset = np.vstack((normal, mastitis, ketosis, lameness, estrus, hypocalcemia, heat_stress, brd))
    
    X = dataset[:, :-1]
    y = dataset[:, -1]
    
    # Modelni o'qitish
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X, y)
    
    # Modelni saqlash
    joblib.dump(rf_model, 'model.pkl')
    print("Advanced Model muvaffaqiyatli saqlandi (model.pkl)")

if __name__ == "__main__":
    create_advanced_model()
