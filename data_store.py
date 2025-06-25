import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Simple global DataFrame
df = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity'])

# Add some initial test data
def initialize_test_data():
    global df
    print("🧪 Initializing with test data...")
    
    now = datetime.now()
    test_data = []
    
    for i in range(20, 0, -1):  # 20 data points, newest first
        timestamp = now - timedelta(minutes=i)
        temperature = 20 + np.random.normal(0, 1)  # Around 20°C ± 1°C
        humidity = 50 + np.random.normal(0, 5)     # Around 50% ± 5%
        humidity = max(20, min(80, humidity))      # Clamp between 20-80%
        
        test_data.append({
            'timestamp': timestamp,
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1)
        })
    
    df = pd.DataFrame(test_data)
    print(f"✅ Test data created: {len(df)} rows")
    return df

# Initialize on import
initialize_test_data()

def add_reading(temperature, humidity):
    """Add a new reading to the DataFrame"""
    global df
    
    try:
        new_row = pd.DataFrame({
            'timestamp': [datetime.now()],
            'temperature': [float(temperature)],
            'humidity': [float(humidity)]
        })
        
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Keep only last 50 readings
        if len(df) > 50:
            df = df.tail(50).reset_index(drop=True)
            
        print(f"📊 Added reading: {temperature}°C, {humidity}% (Total: {len(df)})")
        return True
        
    except Exception as e:
        print(f"❌ Error adding reading: {e}")
        return False

if __name__ == "__main__":
    print("Testing minimal data store...")
    print(f"DataFrame shape: {df.shape}")
    print("Sample data:")
    print(df.head())
    
    # Test adding data
    print("\nTesting add_reading...")
    add_reading(25.5, 60.0)
    print(f"New shape: {df.shape}")
    print("Latest reading:")
    print(df.tail(1))