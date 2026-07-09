from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for, flash
import joblib
import numpy as np
import random
import sklearn
import sklearn.ensemble
from database import init_db, save_prediction, get_all_records, get_latest_status_by_cow, get_all_cows, add_cow_profile, update_cow_profile, delete_cow_profile, check_password, update_password
from rules import analyze_cattle_activity
import os
from werkzeug.utils import secure_filename
import sys
import os
from ai_translations import disease_data_multi, ai_responses

# PyInstaller uchun yo'llarni to'g'rilash
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    application_path = os.path.dirname(sys.executable)
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__)

# Uploads folder .exe turgan joyda bo'lishi kerak, to'liq saqlanib qolishi uchun
UPLOAD_FOLDER = os.path.join(application_path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Modelni yuklash
if getattr(sys, 'frozen', False):
    MODEL_PATH = os.path.join(sys._MEIPASS, 'model.pkl')
else:
    MODEL_PATH = os.path.join(application_path, 'model.pkl')

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# Baza yaratish
init_db()

app.secret_key = 'cattle_activ_super_secret_key'

@app.before_request
def require_login():
    allowed_routes = ['login', 'static', 'serve_manifest', 'serve_sw', 'serve_uploads']
    if request.endpoint not in allowed_routes and 'logged_in' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password(password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Parol noto'g'ri!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        if check_password(old_password):
            update_password(new_password)
            return render_template('settings.html', success="Parol muvaffaqiyatli o'zgartirildi!")
        else:
            return render_template('settings.html', error="Eski parol noto'g'ri!")
    return render_template('settings.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_input')
def sensor_input():
    return render_template('sensor_input.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/cows')
def cows():
    return render_template('cows.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ai_diagnosis')
def ai_diagnosis():
    return render_template('ai_diagnosis.html')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/cows', methods=['GET'])
def api_cows():
    cows = get_all_cows()
    return jsonify({'success': True, 'cows': cows})

@app.route('/api/add_cow', methods=['POST'])
def add_cow():
    # Handle both multipart/form-data (with image) and application/json
    if request.is_json:
        data = request.json
        cow_id = data.get('cow_id')
        breed = data.get('breed', "Noma'lum")
        age = data.get('age', 2)
        weight = data.get('weight', 400)
        milk_yield_str = data.get('milk_yield')
        milk_yield = float(milk_yield_str) if milk_yield_str else 0
        image_filename = 'cow1.png'
    else:
        # Form data (with possible file upload)
        data = request.form
        cow_id = data.get('cow_id')
        breed = data.get('breed', "Noma'lum")
        age = data.get('age', 2)
        weight = data.get('weight', 400)
        milk_yield_str = data.get('milk_yield')
        milk_yield = float(milk_yield_str) if milk_yield_str else 0
        
        image_filename = 'cow1.png'
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(f"cow_{cow_id}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = f"/{filename}"

    if not cow_id:
        return jsonify({'success': False, 'message': 'Qoramol ID si kiritilmagan'})
        
    # Check if the image filename starts with '/' indicating it's an uploaded image.
    # We will let the frontend resolve it properly, but in database it stores just the path
    if image_filename.startswith('/'):
        db_image_path = f"uploads{image_filename}"
    else:
        db_image_path = image_filename
        
    success = add_cow_profile(cow_id, breed, age, weight, milk_yield, db_image_path)
    if success:
        return jsonify({'success': True, 'message': 'Qoramol muvaffaqiyatli qo\'shildi!'})
    else:
        return jsonify({'success': False, 'message': 'Ushbu ID dagi qoramol allaqachon mavjud!'})

@app.route('/api/update_cow/<int:cow_id>', methods=['POST'])
def update_cow(cow_id):
    data = request.form
    breed = data.get('breed')
    age = data.get('age')
    weight = data.get('weight')
    milk_yield_str = data.get('milk_yield')
    milk_yield = float(milk_yield_str) if milk_yield_str else 0
    
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(f"cow_{cow_id}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = f"uploads/{filename}"

    success = update_cow_profile(cow_id, breed, age, weight, milk_yield, image_filename)
    if success:
        return jsonify({'success': True, 'message': 'Qoramol muvaffaqiyatli yangilandi!'})
    else:
        return jsonify({'success': False, 'message': 'Qoramol topilmadi!'})

@app.route('/api/delete_cow/<int:cow_id>', methods=['DELETE'])
def delete_cow(cow_id):
    success = delete_cow_profile(cow_id)
    if success:
        return jsonify({'success': True, 'message': 'Qoramol o\'chirildi!'})
    else:
        return jsonify({'success': False, 'message': 'Qoramol topilmadi!'})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        cow_id = int(data.get('cow_id', 0))
        steps = int(data.get('steps', 0))
        movement_time = float(data.get('movement', 0.0))
        rumination_minutes = int(data.get('rumination', 0))
        temperature = float(data.get('temperature', 0.0))
        distance_from_herd = float(data.get('distance', 0.0))
        lat = float(data.get('lat', 41.3))
        lng = float(data.get('lng', 69.2))

        # 1. Rule-based analiz
        rule_result = analyze_cattle_activity(steps, movement_time, rumination_minutes, temperature, distance_from_herd)

        # 2. ML model analizi
        ml_result = "Model mavjud emas"
        if model is not None:
            features = np.array([[steps, movement_time, rumination_minutes, temperature, distance_from_herd]])
            prediction = model.predict(features)[0]
            
            classes = {
                0: "Normal",
                1: "Mastit / Infeksiya",
                2: "Ketoz / Acidosis",
                3: "Lameness (Oyoq og'rig'i)",
                4: "Estrus (Qizish)",
                5: "Hypocalcemia (Sut isitmasi)",
                6: "Heat Stress (Issiqlik stresi)",
                7: "BRD (Pnevmoniya)"
            }
            ml_result = classes.get(prediction, "Noma'lum holat")

        # 3. Natijani DB ga saqlash
        save_prediction(cow_id, steps, movement_time, rumination_minutes, temperature, distance_from_herd, lat, lng, rule_result, ml_result)

        return jsonify({
            'success': True,
            'rule_result': rule_result,
            'ml_result': ml_result
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data', methods=['GET'])
def get_data():
    records = get_all_records()
    latest_cows = get_latest_status_by_cow()
    return jsonify({
        'history': records,
        'latest_cows': latest_cows
    })

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    """
    Simulated AI Veterinary Assistant.
    Uses Rule-Based logic combined with pre-defined natural language responses
    to mimic an LLM assistant analyzing the cow's latest data.
    """
    data = request.json
    question = data.get('question', '').lower()
    cow_id = data.get('cow_id', None)
    lang = data.get('lang', 'uz')
    
    # Get latest data for this cow
    latest_cows = get_latest_status_by_cow()
    cow_data = next((c for c in latest_cows if str(c['cow_id']) == str(cow_id)), None)
    
    if not cow_data:
        return jsonify({'response': ai_responses['not_found'].get(lang, ai_responses['not_found']['uz'])})
    
    temp = cow_data['temperature']
    rum = cow_data['rumination_minutes']
    ml = cow_data['ml_prediction']
    
    # Generate simple LLM-like response
    response_header = ai_responses['analysis_header'].get(lang, ai_responses['analysis_header']['uz']).format(cow_id=cow_id, temp=temp, rum=rum)
    response = response_header
    
    if "mastit" in ml.lower() or "infeksiya" in ml.lower():
        response += ai_responses['mastitis'].get(lang, ai_responses['mastitis']['uz'])
    elif "ketoz" in ml.lower():
        response += ai_responses['ketosis'].get(lang, ai_responses['ketosis']['uz'])
    elif "lameness" in ml.lower() or "oyoq" in ml.lower():
        response += ai_responses['lameness'].get(lang, ai_responses['lameness']['uz'])
    elif "estrus" in ml.lower() or "qizish" in ml.lower():
        response += ai_responses['estrus'].get(lang, ai_responses['estrus']['uz'])
    elif "hypocalcemia" in ml.lower() or "sut isitmasi" in ml.lower():
        response += ai_responses['hypocalcemia'].get(lang, ai_responses['hypocalcemia']['uz'])
    elif "heat stress" in ml.lower() or "issiqlik" in ml.lower():
        response += ai_responses['heat_stress'].get(lang, ai_responses['heat_stress']['uz'])
    elif "brd" in ml.lower() or "pnevmoniya" in ml.lower():
        response += ai_responses['brd'].get(lang, ai_responses['brd']['uz'])
    else:
        response += ai_responses['normal'].get(lang, ai_responses['normal']['uz'])
        
    return jsonify({'response': response})

@app.route('/api/symptom_chat', methods=['POST'])
def symptom_chat():
    """
    Symptom-based AI diagnostic. 
    Analyses user input for keywords and provides veterinary advice.
    """
    data = request.json
    question = data.get('question', '').lower()
    lang = data.get('lang', 'uz')
    
    if not question:
        return jsonify({'response': ai_responses['empty_query'].get(lang, ai_responses['empty_query']['uz'])})
        
    best_match = None
    max_score = 0
    
    for key, d_data in disease_data_multi.items():
        score = sum(1 for kw in d_data['keywords'] if kw in question)
        if score > max_score:
            max_score = score
            best_match = key
            
    if best_match:
        response = disease_data_multi[best_match]['response'].get(lang, disease_data_multi[best_match]['response']['uz'])
    else:
        response = ai_responses['no_match'].get(lang, ai_responses['no_match']['uz'])

    return jsonify({'response': response})

if __name__ == '__main__':
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    # Brauzerni 1.5 soniyadan keyin ochish
    Timer(1.5, open_browser).start()
    
    # debug=False qilib qo'yamiz, chunki .exe da kerak emas
    app.run(host='0.0.0.0', port=5000, debug=False)
