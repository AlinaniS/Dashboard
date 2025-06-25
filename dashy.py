import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Temperature and Humidity Dashboard - LIVE TEST', style={'textAlign': 'center'}),
    
    # Debug info
    html.Div(id='debug-info', style={
        'textAlign': 'center',
        'padding': '10px',
        'marginBottom': '20px',
        'backgroundColor': '#e8f4fd',
        'border': '2px solid #2196F3',
        'borderRadius': '5px'
    }),

    # Humidity display
    html.Div([
        html.Div([
            html.Div(id='humidity-value', style={
                'fontSize': '30px',
                'color': 'white',
                'textAlign': 'center',
                'lineHeight': '150px',
                'fontWeight': 'bold'
            })
        ], style={
            'width': '150px',
            'height': '150px',
            'borderRadius': '50%',
            'background': 'linear-gradient(to top, #4FC3F7 0%, #29B6F6 100%)',
            'margin': 'auto',
            'boxShadow': '0 0 15px rgba(0, 123, 255, 0.5)',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }),
        html.Div("Humidity", style={
            'textAlign': 'center',
            'marginTop': '10px',
            'fontSize': '20px',
            'color': '#333'
        })
    ], style={'marginBottom': '40px'}),

    # Temperature chart
    dcc.Graph(id='temperature-chart'),
    
    # Humidity chart
    dcc.Graph(id='humidity-chart'),

    # Fast update for testing
    dcc.Interval(id='interval', interval=2000, n_intervals=0),  # every 2 seconds
])

def generate_live_data(n_intervals):
    """Generate data that definitely changes every update"""
    now = datetime.now()
    
    # Create 20 data points over the last 20 minutes
    data = []
    for i in range(20, 0, -1):
        timestamp = now - timedelta(minutes=i)
        
        # Create sinusoidal patterns that change over time
        time_factor = (n_intervals + i) * 0.1
        
        # Temperature: 20°C base + sine wave + some noise
        temp = 20 + 5 * math.sin(time_factor) + np.random.normal(0, 0.5)
        
        # Humidity: 50% base + cosine wave + some noise  
        humidity = 50 + 20 * math.cos(time_factor * 0.7) + np.random.normal(0, 2)
        humidity = max(20, min(80, humidity))  # Clamp between 20-80%
        
        data.append({
            'timestamp': timestamp,
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1)
        })
    
    return pd.DataFrame(data)

@app.callback(
    [Output('humidity-value', 'children'),
     Output('temperature-chart', 'figure'),
     Output('humidity-chart', 'figure'),
     Output('debug-info', 'children')],
    Input('interval', 'n_intervals')
)
def update_dashboard(n):
    print(f"\n🔄 Update #{n} - Generating new data...")
    
    try:
        # Generate fresh data every time
        df = generate_live_data(n)
        
        # Get latest values
        latest = df.iloc[-1]
        current_temp = latest['temperature']
        current_humidity = latest['humidity']
        
        print(f"📊 Latest: {current_temp}°C, {current_humidity}%")
        print(f"📊 Data range - Temp: {df['temperature'].min():.1f} to {df['temperature'].max():.1f}")
        print(f"📊 Data range - Humidity: {df['humidity'].min():.1f} to {df['humidity'].max():.1f}")
        
        # Temperature chart with markers to show individual points
        temp_fig = px.line(
            df, 
            x='timestamp', 
            y='temperature',
            title=f'🌡️ Temperature Over Time (Update #{n})',
            markers=True
        )
        temp_fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6)
        )
        temp_fig.update_layout(
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            height=400,
            showlegend=False
        )
        
        # Humidity chart
        humidity_fig = px.line(
            df, 
            x='timestamp', 
            y='humidity',
            title=f'💧 Humidity Over Time (Update #{n})',
            markers=True,
            color_discrete_sequence=['#29B6F6']
        )
        humidity_fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6)
        )
        humidity_fig.update_layout(
            xaxis_title='Time',
            yaxis_title='Humidity (%)',
            height=400,
            showlegend=False
        )
        
        # Debug info
        debug_text = html.Div([
            html.P(f"🔄 Update #{n} at {datetime.now().strftime('%H:%M:%S')}", 
                   style={'margin': '0', 'fontWeight': 'bold'}),
            html.P(f"📊 Current: {current_temp}°C, {current_humidity}%", 
                   style={'margin': '0'}),
            html.P(f"📈 Temp Range: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C", 
                   style={'margin': '0'}),
            html.P(f"💧 Humidity Range: {df['humidity'].min():.1f}% to {df['humidity'].max():.1f}%", 
                   style={'margin': '0'})
        ])
        
        print(f"✅ Update #{n} completed")
        
        return f"{current_humidity:.1f}%", temp_fig, humidity_fig, debug_text
        
    except Exception as e:
        print(f"❌ Error in update #{n}: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error state
        error_fig = go.Figure()
        error_fig.update_layout(title=f'Error: {str(e)}')
        
        error_debug = html.P(f"❌ Error in update #{n}: {str(e)}", 
                           style={'color': 'red', 'fontWeight': 'bold'})
        
        return "Error", error_fig, error_fig, error_debug

if __name__ == '__main__':
    print("🧪 Starting LIVE TEST dashboard...")
    print("📍 Dashboard: http://127.0.0.1:8052")
    print("🔄 Data changes every 2 seconds - you should see the graphs move!")
    
    app.run(debug=True, host='127.0.0.1', port=8052)