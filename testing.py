import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample data
data = {
    'city_name': ['Dallas', 'Plano', 'Irving', 'Arlington', 'Frisco'],
    'latitude': [32.7767, 33.0198, 32.8140, 32.7357, 33.1507],
    'longitude': [-96.7970, -96.6989, -96.9553, -97.1081, -96.8236],
    'population': [1343573, 288539, 240373, 398854, 200490],
    'growth rate': [1.1, 2.3, 1.7, 1.4, 3.8],
    'median income': [55047, 92266, 60458, 57432, 130464]
}

df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Population', 'value': 'population'},
            {'label': 'Growth Rate', 'value': 'growth rate'},
            {'label': 'Median Income', 'value': 'median income'},
        ],
        value='population'  # default value
    ),
    dcc.Graph(id='map')
], style={'display': 'flex', 'flex-direction': 'column'})

# Callback function to update map
@app.callback(
    Output('map', 'figure'),
    [Input('dropdown', 'value')]
)
def update_map(selected_value):
    fig = px.scatter_mapbox(df,
                            lat='latitude',
                            lon='longitude',
                            size=selected_value,
                            color=selected_value,
                            hover_name='city_name',
                            hover_data=['population', 'growth rate', 'median income'],
                            title=f'Cities in the Dallas Region by {selected_value.title()}',
                            mapbox_style="open-street-map",
                            color_continuous_scale='Viridis',
                            size_max=30,  # max size of circle markers
                            zoom=8,  # zoom level
                            center={"lat": 32.7767, "lon": -96.7970})  # center on Dallas
    # Customize hovertemplate
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>" +
                      "Population: %{customdata[0]:,.0f}<br>" +
                      "Growth Rate: %{customdata[1]:.2f}%<br>" +
                      "Median Income: $%{customdata[2]:,.2f}<br>" +
                      "<extra></extra>"  # this line removes the default trace info in the hover
    )
    fig.update_layout(
        width=1200,
        height=800,
        margin={"r": 100, "t": 100, "l": 100, "b": 100},
        legend_title_text = f'City by {selected_value.title()}',
        legend = dict(
            bgcolor='LightSteelBlue',
            bordercolor='Black',
            borderwidth=2,
            font=dict(
                family="Arial",
                size=12,
                color="RebeccaPurple"
            )
        )
    )

    return fig

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)