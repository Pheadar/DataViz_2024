import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

alo_data = pd.read_csv('DataViz_2024/treated_data/ALO_data_tableau.csv')

alo_data['start.season'] = pd.to_datetime(alo_data['start.season'].astype(str), format='%Y')
alo_data['End.season'] = pd.to_datetime(alo_data['End.season'].astype(str), format='%Y')

color_map = {
    "Minardi": "black", 
    "Renault": "#fcd205", # renault yellow
    "McLaren": "#E56717", # papaya orange
    "Ferrari": "#F70D1A", # Ferrari red
    "Alpine": "#2673E2", # Alpine blue
    "Aston Martin": "#004225" # british racing green
}

text_color_map = {
    "Minardi": "gold",
    "Renault": "grey",
    "McLaren": "black",
    "Ferrari": "yellow",
    "Alpine": "white",
    "Aston Martin": "white"
}

# Assuming alo_data is already loaded and processed
current_year = datetime.now().year

# Create the Gantt chart with Plotly Express
fig = px.timeline(
    alo_data,
    x_start="start.season",
    x_end="End.season",
    y="Constructors",
    color="Constructors",
    color_discrete_map=color_map
)

# Convert Plotly Express figure to Plotly Graph Objects figure for custom adjustments
fig = go.Figure(fig)

# Adjusting the opacity for each trace based on the 'End.season' year
for trace in fig.data:
    end_years = alo_data[alo_data['Constructors'] == trace.name]['End.season'].dt.year
    opacities = [0.66 if year > 2024 else 1 for year in end_years]
    trace.marker.opacity = opacities

# Customize text color to contrast with the bar color and add annotations
for index, row in alo_data.iterrows():
    text_position = row['End.season'] - ((row['End.season'] - row['start.season']) / 10)
    fig.add_annotation(
        x=text_position, y=row['Constructors'],
        text=row['Constructors'],
        showarrow=False,
        font=dict(
            color=text_color_map[row['Constructors']],
        ),
        xanchor='right',
        align='right'
    )

# Reverse the y-axis
fig.update_yaxes(autorange="reversed")

# Hide the legend as it's redundant now
fig.update_layout(showlegend=False)

fig.add_shape(
    # Line Horizontal
    type="line",
    x0="2005-01-01", x1="2005-01-01",
    y0=-0.5, y1=len(alo_data['Constructors'].unique()) - 0.5,  # Span full height of plot
    line=dict(
        color="red",
        width=1
    )
)

fig.add_shape(
    # Line Horizontal
    type="line",
    x0="2006-01-01", x1="2006-01-01",
    y0=-0.5, y1=len(alo_data['Constructors'].unique()) - 0.5,  # Span full height of plot
    line=dict(
        color="red",
        width=1
    )
)

# Adjust x-axis ticks to show every year and set an upper limit for the x-axis
fig.update_xaxes(
    tickmode='linear',
    dtick="M12",
    range=["2001-01-01", "2025-12-31"]
)
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='gantt-chart',
        figure=fig
    ),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    Input('gantt-chart', 'clickData')
)
def display_click_data(clickData):
    # Logic to determine if the red line was clicked (needs refinement based on clickData structure)
    if clickData:
        return 'The red line was clicked. Displaying new visualization or information.'
    return 'Click on the chart to interact.'

if __name__ == '__main__':
    app.run_server(debug=True)
