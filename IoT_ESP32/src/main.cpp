#include <DHT.h>

// DHT11 sensor setup
#define DHT_PIN 14        // GPIO pin connected to DHT11 data pin
#define DHT_TYPE DHT11   // DHT11 sensor type

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize DHT sensor
  dht.begin();
  
  Serial.println("ESP32 DHT11 Temperature & Humidity Sensor");
  Serial.println("==========================================");
  delay(2000); // Wait for sensor to stabilize
}

void loop() {
  // Read humidity and temperature
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // Celsius
  float temperatureF = dht.readTemperature(true); // Fahrenheit
  
  // Check if readings are valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }
  
  // Calculate heat index (feels like temperature)
  float heatIndex = dht.computeHeatIndex(temperatureF, humidity);
  float heatIndexC = dht.computeHeatIndex(temperature, humidity, false);
  
  // Print readings to Serial Monitor
  Serial.println("--- Sensor Readings ---");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  
  Serial.print("Temperature: ");
  Serial.print(temperatureF);
  Serial.println(" °F");
  
  Serial.print("Heat Index: ");
  Serial.print(heatIndexC);
  Serial.println(" °C");
  
  Serial.print("Heat Index: ");
  Serial.print(heatIndex);
  Serial.println(" °F");
  
  Serial.println(""); // Empty line for readability
  
  // Wait 2 seconds between readings
  delay(2000);
}

// Optional: Function to print sensor info
void printSensorInfo() {
  Serial.println("DHT11 Sensor Information:");
  Serial.println("- Temperature range: 0-50°C (±2°C accuracy)");
  Serial.println("- Humidity range: 20-90% RH (±5% accuracy)");
  Serial.println("- Sampling rate: 1Hz (once per second)");
}