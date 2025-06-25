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
    # Main container for overall page styling
    html.Div([
        # Main Dashboard Title
        html.H1('Temperature and Humidity Dashboard', style={
            'textAlign': 'center',
            'color': '#2c3e50',  # Darker blue-grey for heading
            'marginBottom': '30px',
            'fontSize': '2.8em',  # Larger font size
            'fontWeight': '700',  # Bolder
            'textShadow': '1px 1px 2px rgba(0,0,0,0.1)', # Subtle text shadow
            'paddingTop': '20px' # Add some top padding
        }),
        
        # Debug info container
        html.Div(id='debug-info', style={
            'textAlign': 'center',
            'padding': '15px',
            'marginBottom': '30px',  # More space below
            'backgroundColor': '#e3f2fd',  # Softer blue background
            'border': '1px solid #90caf9',  # Lighter, subtle border
            'borderRadius': '8px',  # More rounded corners
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', # Subtle box shadow
            'color': '#1a237e',  # Dark blue text
            'maxWidth': '600px',  # Limit width for better readability
            'margin': '20px auto', # Center horizontally
            'fontSize': '0.95em'
        }),

        # Humidity display container (circular gauge)
        html.Div([
            html.Div([
                html.Div(id='humidity-value', style={
                    'fontSize': '38px',  # Larger font for the humidity value
                    'color': 'white',
                    'textAlign': 'center',
                    'lineHeight': '150px', # Keep text vertically centered
                    'fontWeight': 'bold',
                    'textShadow': '1px 1px 3px rgba(0,0,0,0.3)' # Text shadow for pop
                })
            ], style={
                'width': '180px',  # Slightly larger circle
                'height': '180px',
                'borderRadius': '50%',
                'background': 'linear-gradient(145deg, #4FC3F7, #2196F3)', # Diagonal gradient for depth
                'margin': 'auto',
                'boxShadow': '0 8px 16px rgba(0, 123, 255, 0.3), 0 3px 6px rgba(0, 123, 255, 0.2)', # More prominent shadow
                'display': 'flex', # Use flexbox to center content
                'alignItems': 'center',
                'justifyContent': 'center',
                'transition': 'all 0.3s ease-in-out' # Smooth transitions for any potential future interactivity
            }),
            html.Div("Humidity", style={
                'textAlign': 'center',
                'marginTop': '15px',  # More space below the circle
                'fontSize': '22px',  # Larger font for the label
                'color': '#555',  # Softer black text
                'fontWeight': '600' # Bolder text for the label
            })
        ], style={'marginBottom': '50px', 'padding': '20px'}), # More space below humidity section, slight padding

        # Chart containers for temperature and humidity
        # Wrapped in a flex container to allow side-by-side display on larger screens
        html.Div([
            # Temperature chart container
            html.Div([
                dcc.Graph(id='temperature-chart', config={'displayModeBar': False}), # Hide Plotly's default modebar for cleaner look
            ], style={
                'flex': '1', # Allow chart to take available space
                'minWidth': '300px', # Minimum width before wrapping on smaller screens
                'backgroundColor': '#ffffff', # White background for charts
                'borderRadius': '10px', # Rounded corners for the chart container
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', # Subtle shadow
                'padding': '20px',
                'marginBottom': '30px', # Space between charts if stacked
                'marginRight': '15px', # Space between charts if side-by-side
                'flexGrow': 1 # Allow the chart container to grow
            }),
            
            # Humidity chart container
            html.Div([
                dcc.Graph(id='humidity-chart', config={'displayModeBar': False}), # Hide Plotly's default modebar
            ], style={
                'flex': '1',
                'minWidth': '300px',
                'backgroundColor': '#ffffff',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
                'padding': '20px',
                'marginBottom': '30px',
                'marginLeft': '15px', # Space between charts if side-by-side
                'flexGrow': 1
            }),
        ], style={
            'display': 'flex',
            'flexWrap': 'wrap', # Allow charts to wrap to the next line on smaller screens
            'justifyContent': 'center', # Center items in the flex container
            'gap': '30px' # Gap between chart containers
        }),

        # Fast update for testing (no visual changes to this element itself, it's just the interval component)
        dcc.Interval(id='interval', interval=2000, n_intervals=0), 
    ], style={
        'fontFamily': '"Inter", sans-serif', # Apply Inter font - ensure it's loaded in your assets/index.html
        'backgroundColor': "#092043", # Light grey-blue background for the entire page
        'color': '#333', # Default text color
        'padding': '20px',
        'minHeight': '100vh', # Ensure the page takes at least the full viewport height
        'boxSizing': 'border-box' # Include padding in element's total width and height
    })
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
