let mapInstance = null;
let markers = {};

document.addEventListener('DOMContentLoaded', () => {
    const activityForm = document.getElementById('activityForm');
    const addCowForm = document.getElementById('addCowForm');
    
    if (addCowForm) {
        addCowForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(addCowForm);
            
            try {
                const response = await fetch('/api/add_cow', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.success) {
                    Toastify({
                        text: "Yangi qoramol muvaffaqiyatli qo'shildi!",
                        duration: 3000,
                        gravity: "top",
                        position: "right",
                        style: { background: "var(--success-color)" },
                    }).showToast();
                    addCowForm.reset();
                } else {
                    Toastify({
                        text: "Xatolik: " + result.message,
                        duration: 3000,
                        gravity: "top",
                        position: "right",
                        style: { background: "var(--danger-color)" },
                    }).showToast();
                }
            } catch (err) {
                console.error(err);
            }
        });
    }

    if (activityForm) {
        activityForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const cow_id = document.getElementById('cow_id').value;
            const steps = document.getElementById('steps').value;
            const movement = document.getElementById('movement').value;
            const rumination = document.getElementById('rumination').value;
            const temperature = document.getElementById('temperature').value;
            // Generate random GPS and distance since they are removed from UI
            const distance = Math.floor(Math.random() * 20) + 5; // 5-25m
            const lat = 44.1000 + (Math.random() - 0.5) * 0.01;
            const lng = 59.3500 + (Math.random() - 0.5) * 0.01;
            
            const data = { cow_id, steps, movement, rumination, temperature, distance, lat, lng };

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('rule-result').innerHTML = formatRuleResult(result.rule_result);
                    let mlIcon = '<i class="fas fa-check-circle" style="color:var(--accent-color)"></i>';
                    if (result.ml_result !== "Normal") {
                        mlIcon = '<i class="fas fa-exclamation-triangle" style="color:var(--danger-color)"></i>';
                    }
                    document.getElementById('ml-result').innerHTML = `${mlIcon} ${result.ml_result}`;
                    
                    document.getElementById('result-container').classList.remove('hidden');
                    showSuccess(`Diagnostika yakunlandi (Cow #${cow_id})`);
                } else {
                    showError(result.error);
                }
            } catch (err) {
                showError("Server xatosi");
            }
        });
    }
});

function formatRuleResult(text) {
    if (text.includes("✅")) return `<div style="color: var(--accent-color);">${text}</div>`;
    const alerts = text.split(" | ");
    let html = "";
    alerts.forEach(alert => {
        let color = "var(--text-main)";
        if (alert.includes("🔴")) color = "var(--danger-color)";
        else if (alert.includes("🟠")) color = "var(--warning-color)";
        else if (alert.includes("🟢")) color = "var(--accent-color)";
        html += `<div style="color: ${color}; margin-bottom: 5px;">${alert}</div>`;
    });
    return html;
}

function showError(msg) {
    if (typeof Toastify !== 'undefined') {
        Toastify({ text: msg, duration: 3000, style: { background: "#ef4444" } }).showToast();
    }
}
function showSuccess(msg) {
    if (typeof Toastify !== 'undefined') {
        Toastify({ text: msg, duration: 3000, style: { background: "#10b981" } }).showToast();
    }
}

/* Dashboard Logic */
async function initDashboard() {
    // Initialize Map
    const mapDiv = document.getElementById('farmMap');
    if (mapDiv) {
        mapInstance = L.map('farmMap').setView([44.1000, 59.3500], 12); // Jiltirbas batqaqligi
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(mapInstance);
    }
    
    await fetchCowsList();
    await fetchAndUpdate();
    setInterval(fetchAndUpdate, 5000);
}

async function fetchCowsList() {
    try {
        const response = await fetch('/api/cows');
        const data = await response.json();
        if (data.success && data.cows) {
            const select = document.getElementById('chatCowId');
            if (select) {
                select.innerHTML = '';
                data.cows.forEach(cow => {
                    const option = document.createElement('option');
                    option.value = cow.cow_id;
                    option.textContent = `Cow #${cow.cow_id} (${cow.breed})`;
                    select.appendChild(option);
                });
            }
        }
    } catch (e) {
        console.error("Qoramollar ro'yxatini yuklashda xatolik:", e);
    }
}

async function fetchAndUpdate() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            updateTable(data.history);
        }
        
        if (data.latest_cows && data.latest_cows.length > 0) {
            updateCowCards(data.latest_cows);
            updateMap(data.latest_cows);
        }
    } catch (err) {
        console.error(err);
    }
}

function updateTable(history) {
    const tbody = document.querySelector('#dataTable tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    history.forEach(row => {
        const date = new Date(row.timestamp);
        const dateStr = `${date.getHours()}:${date.getMinutes() < 10 ? '0' : ''}${date.getMinutes()}`;
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${dateStr}</td>
            <td><strong>#${row.cow_id}</strong></td>
            <td>${row.temperature}°C</td>
            <td>${row.rumination_minutes} min</td>
            <td>${row.movement_time}h</td>
            <td>${row.distance_from_herd} m</td>
            <td style="color:${row.ml_prediction === 'Normal' ? 'var(--accent-color)' : 'var(--danger-color)'}">${row.ml_prediction}</td>
        `;
        tbody.appendChild(tr);
    });
}

function updateCowCards(latest_cows) {
    const container = document.getElementById('cow-cards-container');
    if (!container) return;
    container.innerHTML = '';
    
    latest_cows.forEach(cow => {
        const isSick = cow.ml_prediction !== "Normal";
        const cardClass = isSick ? "cow-card sick" : "cow-card";
        const statusText = isSick ? cow.ml_prediction : "Sog'lom";
        const icon = isSick ? '<i class="fas fa-exclamation-circle"></i>' : '<i class="fas fa-check-circle"></i>';
        
        const card = document.createElement('div');
        card.className = cardClass;
        card.innerHTML = `
            <h3><span>Cow #${cow.cow_id}</span> <span class="status">${icon} ${statusText}</span></h3>
            <div class="cow-stat"><span>Harorat:</span> <strong>${cow.temperature}°C</strong></div>
            <div class="cow-stat"><span>Chaynash:</span> <strong>${cow.rumination_minutes} min</strong></div>
            <div class="cow-stat"><span>Faollik:</span> <strong>${cow.movement_time}h yurish</strong></div>
            <div class="cow-stat"><span>GPS Masofa:</span> <strong>${cow.distance_from_herd} m</strong></div>
        `;
        container.appendChild(card);
    });
}

function updateMap(latest_cows) {
    if (!mapInstance) return;
    
    latest_cows.forEach(cow => {
        if (cow.lat && cow.lng) {
            const isSick = cow.ml_prediction !== "Normal";
            const color = isSick ? "red" : "green";
            
            // Custom marker icon based on health
            const markerIcon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>`,
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });
            
            if (markers[cow.cow_id]) {
                markers[cow.cow_id].setLatLng([cow.lat, cow.lng]);
                markers[cow.cow_id].setIcon(markerIcon);
                if(markers[cow.cow_id].getTooltip()) {
                    markers[cow.cow_id].setTooltipContent(`<b>Cow #${cow.cow_id}</b><br>Holat: ${cow.ml_prediction}`);
                }
            } else {
                markers[cow.cow_id] = L.marker([cow.lat, cow.lng], {icon: markerIcon})
                    .addTo(mapInstance)
                    .bindTooltip(`<b>Cow #${cow.cow_id}</b><br>Holat: ${cow.ml_prediction}`, {
                        direction: 'top',
                        offset: [0, -10]
                    });
            }
        }
    });
}

// AI Chat Feature
async function askAiVet() {
    const cow_id = document.getElementById('chatCowId').value;
    const chatBox = document.getElementById('chatBox');
    
    // User Message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user-msg';
    userMsg.innerText = `Cow #${cow_id} holatini tahlil qilib bering.`;
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
    
    try {
        const lang = localStorage.getItem('appLang') || 'uz';
        const response = await fetch('/api/ai_chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cow_id: cow_id, question: "tahlil qil", lang: lang })
        });
        
        const result = await response.json();
        
        // AI Message
        const aiMsg = document.createElement('div');
        aiMsg.className = 'chat-msg ai-msg';
        aiMsg.innerText = result.response;
        chatBox.appendChild(aiMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
        
    } catch (err) {
        console.error(err);
    }
}

// Map Fullscreen Toggle
function toggleMapFullscreen() {
    const panel = document.getElementById('mapPanel');
    if (!panel) return;

    if (!document.fullscreenElement && !document.webkitFullscreenElement) {
        if (panel.requestFullscreen) {
            panel.requestFullscreen().catch(err => console.error(err));
        } else if (panel.webkitRequestFullscreen) {
            panel.webkitRequestFullscreen();
        } else {
            // Fallback to CSS only
            panel.classList.toggle('fullscreen-map');
            updateMapBtnUI();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else {
            // Fallback
            panel.classList.remove('fullscreen-map');
            updateMapBtnUI();
        }
    }
}

function updateMapBtnUI() {
    const panel = document.getElementById('mapPanel');
    const btn = document.getElementById('mapToggleBtn');
    const farmMap = document.getElementById('farmMap');
    if (!panel || !btn || !farmMap) return;

    if (document.fullscreenElement || document.webkitFullscreenElement || panel.classList.contains('fullscreen-map')) {
        panel.classList.add('fullscreen-map');
        // Absolute pixel calculation for maximum reliability
        farmMap.style.setProperty('height', (window.innerHeight - 100) + 'px', 'important');
        btn.innerHTML = '<i class="fas fa-compress"></i> Kichiklashtirish';
    } else {
        panel.classList.remove('fullscreen-map');
        farmMap.style.setProperty('height', '500px', 'important'); // Reset to original height (now 500px)
        btn.innerHTML = '<i class="fas fa-expand"></i> Kattalashtirish';
    }

    if (mapInstance) {
        setTimeout(() => {
            mapInstance.invalidateSize();
        }, 100);
    }
}

document.addEventListener('fullscreenchange', updateMapBtnUI);
document.addEventListener('webkitfullscreenchange', updateMapBtnUI);

// Cow Cards Toggle Function
function toggleCowCards() {
    const wrapper = document.getElementById('cow-cards-wrapper');
    const btn = document.getElementById('toggleCardsBtn');
    
    if (wrapper.style.display === 'none') {
        wrapper.style.display = 'block';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i> Ro\'yxatini yashirish';
        btn.style.background = 'var(--panel-bg)';
        btn.style.border = '1px solid var(--border-color)';
        btn.style.color = 'var(--text-main)';
        btn.style.boxShadow = 'none';
    } else {
        wrapper.style.display = 'none';
        btn.innerHTML = '<i class="fas fa-layer-group"></i> Barcha qoramollar holatini ko\'rish (10 ta)';
        btn.style.background = '#1e293b';
        btn.style.border = '1px solid #38bdf8';
        btn.style.color = '#38bdf8';
        btn.style.boxShadow = '0 4px 15px rgba(56, 189, 248, 0.3)';
    }
}

// History Table Toggle Function
function toggleHistoryTable() {
    const wrapper = document.getElementById('history-table-wrapper');
    const btn = document.getElementById('toggleHistoryBtn');
    
    if (!wrapper || !btn) return;

    if (wrapper.style.display === 'none') {
        wrapper.style.display = 'block';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i> Tarixni Yashirish';
        btn.style.background = 'var(--panel-bg)';
        btn.style.border = '1px solid var(--border-color)';
        btn.style.color = 'var(--text-main)';
    } else {
        wrapper.style.display = 'none';
        btn.innerHTML = '<i class="fas fa-eye"></i> Tarixni Ko\'rsatish';
        btn.style.background = '#1e293b';
        btn.style.border = '1px solid #38bdf8';
        btn.style.color = '#38bdf8';
        btn.style.boxShadow = '0 4px 15px rgba(56, 189, 248, 0.3)';
    }
}

// AI Chat Toggle Function
function toggleAiChat() {
    const wrapper = document.getElementById('ai-chat-wrapper');
    const btn = document.getElementById('toggleAiBtn');
    
    if (!wrapper || !btn) return;

    if (wrapper.style.display === 'none') {
        wrapper.style.display = 'block';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i> Assistentni Yashirish';
        btn.style.background = 'var(--panel-bg)';
        btn.style.border = '1px solid var(--border-color)';
        btn.style.color = 'var(--text-main)';
        btn.style.boxShadow = 'none';
    } else {
        wrapper.style.display = 'none';
        btn.innerHTML = '<i class="fas fa-comment-medical"></i> Assistentni Ochish';
        btn.style.background = '#8b5cf6';
        btn.style.border = 'none';
        btn.style.color = 'white';
        btn.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.4)';
    }
}

// Clear AI Chat History Function
function clearAiChat() {
    const chatBox = document.getElementById('chatBox');
    if (chatBox) {
        chatBox.innerHTML = '<div class="chat-msg ai-msg" data-i18n="vet_greet">Assalomu alaykum! Men AI Veterinarmon. Yangitdan savol berishingiz mumkin.</div>';
        if (typeof applyTranslations === "function") applyTranslations();
    }
}

// SIMULATION LOGIC FOR MOVING COWS
let simulationInterval = null;

async function toggleSimulation() {
    const btn = document.getElementById('simBtn');
    if (!btn) return;
    
    if (simulationInterval) {
        clearInterval(simulationInterval);
        simulationInterval = null;
        btn.innerHTML = '<i class="fas fa-play"></i> Simulyatsiya';
        btn.style.background = '#eab308';
        btn.style.borderColor = '#ca8a04';
        if (typeof Toastify !== 'undefined') {
            Toastify({ text: "Simulyatsiya to'xtatildi", duration: 3000, style: { background: "#f59e0b" } }).showToast();
        }
    } else {
        simulationInterval = setInterval(simulateAllCows, 6000); // Har 6 soniyada harakatlanadi
        simulateAllCows(); // Birinchi marta darhol chaqirish
        btn.innerHTML = '<i class="fas fa-pause"></i> To\'xtatish';
        btn.style.background = '#ef4444';
        btn.style.borderColor = '#dc2626';
        if (typeof Toastify !== 'undefined') {
            Toastify({ text: "Simulyatsiya boshlandi! Mollar xaritada harakatlanmoqda...", duration: 3000, style: { background: "#10b981" } }).showToast();
        }
    }
}

async function simulateAllCows() {
    try {
        const response = await fetch('/api/cows');
        const data = await response.json();
        
        if (data.success && data.cows) {
            // Har bir qoramol uchun yangi tasodifiy ma'lumot jo'natamiz
            data.cows.forEach(cow => {
                // Harakat animatsiyasi uchun eski koordinatalarni olib ozgina o'zgartiramiz
                let currentLat = 44.1000;
                let currentLng = 59.3500;
                
                if (markers[cow.cow_id]) {
                    const pos = markers[cow.cow_id].getLatLng();
                    currentLat = pos.lat;
                    currentLng = pos.lng;
                }
                
                // Kichik qadamlar bilan harakatlantirish
                const lat = currentLat + (Math.random() - 0.5) * 0.003;
                const lng = currentLng + (Math.random() - 0.5) * 0.003;
                
                let steps, movement, rumination, temperature, distance;
                
                // Qoramol ID siga qarab turli holatlarni simulyatsiya qilish:
                if (cow.cow_id % 2 !== 0) {
                    // NORMAL (Sog'lom qoramollar: 1, 3, 5, 7, 9)
                    steps = Math.floor(Math.random() * 2000) + 3000; // 3000-5000
                    movement = (Math.random() * 3 + 4).toFixed(1); // 4-7 hours
                    rumination = Math.floor(Math.random() * 100) + 400; // 400-500 min
                    temperature = (38.0 + Math.random() * 1.0).toFixed(1); // 38.0-39.0 C
                    distance = Math.floor(Math.random() * 30) + 10;
                } else if (cow.cow_id === 2) {
                    // MASTIT / INFECTION (Isitma, chaynash kam)
                    steps = Math.floor(Math.random() * 1000) + 1500; 
                    movement = (Math.random() * 2 + 2).toFixed(1); 
                    rumination = Math.floor(Math.random() * 50) + 200; // < 300
                    temperature = (39.6 + Math.random() * 0.8).toFixed(1); // > 39.5
                    distance = Math.floor(Math.random() * 20) + 10;
                } else if (cow.cow_id === 4) {
                    // LAMENESS (Oyoq og'rig'i - harakat juda kam)
                    steps = Math.floor(Math.random() * 400) + 300; // < 1000
                    movement = (Math.random() * 0.5 + 0.3).toFixed(1); // < 1 h
                    rumination = Math.floor(Math.random() * 100) + 350; 
                    temperature = (38.0 + Math.random() * 1.0).toFixed(1); 
                    distance = Math.floor(Math.random() * 10) + 5;
                } else if (cow.cow_id === 6) {
                    // KETOZ (Oshqozon ishlashi susaygan)
                    steps = Math.floor(Math.random() * 1000) + 1500; 
                    movement = (Math.random() * 0.5 + 1.0).toFixed(1); // < 2 h
                    rumination = Math.floor(Math.random() * 30) + 150; // < 250
                    temperature = (38.0 + Math.random() * 1.0).toFixed(1); 
                    distance = Math.floor(Math.random() * 20) + 10;
                } else if (cow.cow_id === 8) {
                    // ESTRUS (Qizish - harakat keskin oshgan)
                    steps = Math.floor(Math.random() * 2000) + 7500; // > 7000
                    movement = (Math.random() * 3 + 11).toFixed(1); // > 10 h
                    rumination = Math.floor(Math.random() * 50) + 350; 
                    temperature = (38.6 + Math.random() * 0.8).toFixed(1); // > 38.5
                    distance = Math.floor(Math.random() * 30) + 10;
                } else {
                    // HYPOCALCEMIA (Sut isitmasi - harorat past, yotib qolgan)
                    // ID == 10 yoki undan kattalari
                    steps = Math.floor(Math.random() * 300) + 100; // < 500
                    movement = (Math.random() * 0.5 + 0.1).toFixed(1); 
                    rumination = Math.floor(Math.random() * 50) + 300; 
                    temperature = (36.5 + Math.random() * 0.8).toFixed(1); // < 37.5
                    distance = Math.floor(Math.random() * 10) + 5;
                }
                
                const payload = { cow_id: cow.cow_id, steps, movement, rumination, temperature, distance, lat, lng };
                
                fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
            });
            
            // 1 soniyadan keyin jadvalni yangilash
            setTimeout(fetchAndUpdate, 1000);
        }
    } catch (e) {
        console.error("Simulyatsiyada xatolik:", e);
    }
}
