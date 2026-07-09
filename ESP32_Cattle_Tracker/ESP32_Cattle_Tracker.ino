#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <TinyGPSPlus.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ==========================================
// 1. WiFi VA SERVER SOZLAMALARI
// ==========================================
const char* ssid = "WIFI_NOMI";       // O'zingizning WiFi nomingizni yozing
const char* password = "WIFI_PAROLI"; // WiFi parolingizni yozing

// Kompyuteringizning IP manzili (cmd orqali ipconfig deb bilib olishingiz mumkin)
// Masalan: "http://192.168.1.100:5000/api/predict"
const char* serverUrl = "http://KOMPYUTER_IP_MANZILI:5000/api/predict";

// ==========================================
// 2. QORAMOL SOZLAMALARI
// ==========================================
const int COW_ID = 1; // Qaysi qoramolga taqilgan bo'lsa, o'shaning ID raqami

// ==========================================
// 3. DATCHIKLAR SOZLAMALARI
// ==========================================
// 3.1. MPU6050 (Akselerometr va Giroskop - I2C orqali ulanadi: SDA, SCL)
Adafruit_MPU6050 mpu;

// 3.2. Neo-6M GPS (UART2 orqali ulanadi: RX, TX)
#define RXD2 16
#define TXD2 17
HardwareSerial gpsSerial(2);
TinyGPSPlus gps;

// 3.3. DS18B20 Harorat Datchigi (OneWire orqali)
#define ONE_WIRE_BUS 4 // ESP32 ning 4-piniga ulanadi
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);

// ==========================================
// 4. VAQT VA MA'LUMOT YIG'ISH O'ZGARUVCHILARI
// ==========================================
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 60000; // Har 60 soniyada serverga jo'natish (1 daqiqa)

// Yig'ilgan ma'lumotlar (jo'natilgandan so'ng nolga tushadi)
int stepsAccumulated = 0;
float movementAccumulated = 0.0;
int ruminationAccumulated = 0;

void setup() {
  Serial.begin(115200);
  
  // Wi-Fi ga ulanish
  WiFi.begin(ssid, password);
  Serial.print("WiFi tarmog'iga ulanmoqda");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi ga muvaffaqiyatli ulandi!");
  Serial.print("IP Manzil: ");
  Serial.println(WiFi.localIP());

  // Datchiklarni ishga tushirish
  // 1. Harorat datchigi
  tempSensor.begin();
  Serial.println("Harorat datchigi sozlandi.");

  // 2. MPU6050 (Harakat datchigi)
  if (!mpu.begin()) {
    Serial.println("MPU6050 topilmadi! Simlarni tekshiring.");
  } else {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    Serial.println("MPU6050 harakat datchigi sozlandi.");
  }

  // 3. GPS moduli
  gpsSerial.begin(9600, SERIAL_8N1, RXD2, TXD2);
  Serial.println("GPS moduli sozlandi.");
}

void loop() {
  // ---------------------------------------------------------
  // 1-QADAM: DATCHIKLARDAN DOIMIY MA'LUMOT O'QISH
  // ---------------------------------------------------------
  
  // GPS dan o'qish
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  // MPU6050 dan o'qish
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  
  // Harakat kuchi (Akseleratsiya) hisoblash (x, y, z o'qlari bo'yicha)
  float acceleration = sqrt(a.acceleration.x * a.acceleration.x + 
                            a.acceleration.y * a.acceleration.y + 
                            a.acceleration.z * a.acceleration.z);
                            
  // Qadamlarni hisoblash algoritmi (Agar kuch 12 m/s^2 dan oshsa, qadam hisoblanadi)
  if (acceleration > 12.0) {
    stepsAccumulated++;
    movementAccumulated += 0.05; // Yurilgan masofa (soatiga) simulatsiyasi
  }

  // Kavsh qaytarish (Rumination) ni simulatsiya qilish yoki bosh datchigidan hisoblash
  // Real holatda bo'yin harakatlaridan olinadi. 
  if (millis() % 5000 < 50) {
     ruminationAccumulated++;
  }

  // ---------------------------------------------------------
  // 2-QADAM: MA'LUMOTNI MA'LUM VAQT ORALIG'IDA SERVERGA YUBORISH
  // ---------------------------------------------------------
  if (millis() - lastSendTime > sendInterval) {
    lastSendTime = millis();
    
    // Haroratni o'qish
    tempSensor.requestTemperatures(); 
    float bodyTemp = tempSensor.getTempCByIndex(0);
    if(bodyTemp == DEVICE_DISCONNECTED_C) {
      bodyTemp = 38.5; // Agar o'zilsa, standart harorat (qoramol uchun normal harorat)
    }

    // GPS dan Lat/Lng koordinatalarini olish
    float lat = 41.311081; // Standart Toshkent koordinatasi
    float lng = 69.240562;
    if (gps.location.isValid()) {
      lat = gps.location.lat();
      lng = gps.location.lng();
    }

    // Podadan qanchalik uzoqdaligi (Poda markazi bilan masofa hisoblanadi, hozircha taxminiy)
    float distance = random(5, 50) / 1.0; 

    // Serverga jo'natish funksiyasini chaqirish
    sendDataToServer(COW_ID, stepsAccumulated, movementAccumulated, ruminationAccumulated, bodyTemp, distance, lat, lng);
    
    // Keyingi davr uchun o'zgaruvchilarni tozalash
    stepsAccumulated = 0;
    movementAccumulated = 0.0;
    ruminationAccumulated = 0;
  }
  
  delay(100); // Sistemani ortiqcha zo'riqtirmaslik uchun biroz kutish
}

// ---------------------------------------------------------
// SERVERGA POST SO'ROV YUBORUVCHI FUNKSIYA
// ---------------------------------------------------------
void sendDataToServer(int id, int steps, float movement, int rumination, float bodyTemp, float dist, float lat, float lng) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // JSON obyekt yaratish
    StaticJsonDocument<256> doc;
    doc["cow_id"] = id;
    doc["steps"] = steps;
    doc["movement"] = movement;
    doc["rumination"] = rumination;
    doc["temperature"] = bodyTemp;
    doc["distance"] = dist;
    doc["lat"] = lat;
    doc["lng"] = lng;

    String requestBody;
    serializeJson(doc, requestBody);

    Serial.println("=====================================");
    Serial.println("Serverga ma'lumot jo'natilmoqda:");
    Serial.println(requestBody);

    // POST so'rovini yuborish
    int httpResponseCode = http.POST(requestBody);
    
    if (httpResponseCode > 0) {
      Serial.print("Serverdan javob kodi: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Server javobi: " + response);
    } else {
      Serial.print("Xatolik! Kod: ");
      Serial.println(httpResponseCode);
    }
    http.end(); // Ulanishni yopish
  } else {
    Serial.println("XATOLIK: WiFi tarmog'iga ulanmagan!");
  }
}
