import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import os
import numpy as np

# Load the processed data
base_path = os.path.join(os.curdir, 'treated_data', 'pickles')
df = pd.read_pickle(os.path.join(base_path, '2005_timeline_short.pkl'))

# Extract the race names and driver names, excluding 'constructorId'
race_names = df.columns[3:]  # Assuming the first three columns are driverId, driverName, constructorId
race_names = [col for col in race_names if col != 'constructorId']
driver_names = df['driverName'].tolist()

# Create initial figure
fig = go.Figure()

# Add initial traces (first race)
for driver in df.index:
    driver_name = df.at[driver, 'driverName']
    fig.add_trace(go.Scatter(
        x=[race_names[0]],
        y=[df.loc[driver, race_names[0]]],
        mode='lines+markers',
        name=driver_name
    ))

# Generate interpolated frames for smoother animation
frames = []
num_interp_frames = 50  # Number of interpolated frames between each race

for i in range(1, len(race_names)):
    for j in range(num_interp_frames):
        frame_data = []
        for driver in df.index:
            driver_name = df.at[driver, 'driverName']
            start_y = df.loc[driver, race_names[:i]].values
            end_y = df.loc[driver, race_names[i]]
            interp_y = np.linspace(start_y[-1], end_y, num_interp_frames + 1)[j + 1]
            frame_data.append(go.Scatter(
                x=race_names[:i] + [race_names[i]],
                y=np.append(start_y, interp_y),
                mode='lines+markers',
                name=driver_name
            ))
        frames.append(go.Frame(data=frame_data, name=f"{i}-{j}"))

fig.update(frames=frames)

# Add play button with smoother transition settings
fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 50, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 50, "easing": "linear"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate"}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
)

# Set layout and axis titles
fig.update_layout(
    title='2005 Formula 1 Championship',
    xaxis={'title': 'Grand Prix'},
    yaxis={'title': 'Points'},
    margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
    legend={'x': 0, 'y': 1},
    hovermode='closest',
    transition={'duration': 50, 'easing': 'linear'}  # Smoother transition settings
)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='points-graph', figure=fig)  # Directly set the figure in the layout
])

if __name__ == '__main__':
    app.run_server(debug=True)
