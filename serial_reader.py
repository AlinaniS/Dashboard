import serial
import serial.tools.list_ports
import threading
import time
import pandas as pd
import re

def read_serial(port='COM3', baudrate=9600):
    """Minimal serial reader"""
    try:
        # Try to connect
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"✅ Connected to {port}")
        
        # Buffer for collecting lines
        line_buffer = []
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if line:
                    print(f"📥 Received: {line}")  # Debug: show what we're receiving
                    line_buffer.append(line)
                    
                    # Look for humidity and temperature in the buffer
                    humidity = None
                    temperature = None
                    
                    for buffered_line in line_buffer:
                        if buffered_line.startswith("Humidity:"):
                            match = re.search(r'(\d+\.?\d*)', buffered_line)
                            if match:
                                humidity = float(match.group(1))
                                print(f"🌊 Found humidity: {humidity}%")
                        
                        elif buffered_line.startswith("Temperature:") and "°C" in buffered_line:
                            match = re.search(r'(\d+\.?\d*)', buffered_line)
                            if match:
                                temperature = float(match.group(1))
                                print(f"🌡️ Found temperature: {temperature}°C")
                    
                    # If we have both values, save them
                    if humidity is not None and temperature is not None:
                        try:
                            # FIXED: Import the module and modify the df attribute directly
                            import data_store
                            
                            new_data = pd.DataFrame({
                                'timestamp': [pd.Timestamp.now()],
                                'temperature': [temperature],
                                'humidity': [humidity]
                            })
                            
                            # FIXED: Use pd.concat and assign back to the module attribute
                            data_store.df = pd.concat([data_store.df, new_data], ignore_index=True)
                            
                            # Keep only last 50 readings
                            if len(data_store.df) > 50:
                                data_store.df = data_store.df.tail(50).reset_index(drop=True)
                            
                            print(f"💾 Data saved: {temperature}°C, {humidity}% RH (Total rows: {len(data_store.df)})")
                            
                            # Clear buffer after successful parse
                            line_buffer = []
                            
                        except Exception as e:
                            print(f"❌ Error saving data: {e}")
                    
                    # Prevent buffer from growing too large
                    if len(line_buffer) > 10:
                        line_buffer = line_buffer[-5:]  # Keep only last 5 lines
            
            time.sleep(0.1)
            
    except serial.SerialException as e:
        print(f"❌ Serial error: {e}")
        print("💡 Check if the device is connected and the port is correct")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

def start_serial_reader(port='COM3', baudrate=9600):
    """Start serial reader in background thread"""
    # Find available ports if default doesn't work
    available_ports = [p.device for p in serial.tools.list_ports.comports()]
    print(f"🔍 Available ports: {available_ports}")
    
    if port not in available_ports and available_ports:
        port = available_ports[0]  # Use first available port
        print(f"🔄 Using {port} instead of COM3")
    elif not available_ports:
        print("⚠️ No serial ports found!")
        return None
    
    thread = threading.Thread(target=read_serial, args=(port, baudrate), daemon=True)
    thread.start()
    print(f"🚀 Serial reader thread started for {port}")
    return thread

# Test function
def test_serial():
    """Test the serial connection"""
    ports = [p.device for p in serial.tools.list_ports.comports()]
    print(f"🔍 Available ports: {ports}")
    
    if ports:
        print("🧪 Starting test...")
        start_serial_reader(ports[0])
        
        # Let it run for a bit
        for i in range(10):
            time.sleep(1)
            try:
                import data_store
                if not data_store.df.empty:
                    print(f"📊 DataFrame has {len(data_store.df)} rows")
                    print(f"📈 Latest: {data_store.df.tail(1).to_dict('records')[0]}")
                else:
                    print(f"⏳ No data yet... (attempt {i+1}/10)")
            except Exception as e:
                print(f"❌ Error accessing DataFrame: {e}")
    else:
        print("❌ No serial ports available for testing")

if __name__ == "__main__":
    test_serial()