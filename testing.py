import dash
from dash import dcc
from dash import html, exceptions, callback_context
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Sample data
# data = {
#     'City': ['Dallas', 'Plano', 'Irving', 'Arlington', 'Frisco'],
#     'latitude': [32.7767, 33.0198, 32.8140, 32.7357, 33.1507],
#     'longitude': [-96.7970, -96.6989, -96.9553, -97.1081, -96.8236],
#     'population': [1343573, 288539, 240373, 398854, 200490],
#     'growth rate': [1.1, 2.3, 1.7, 1.4, 3.8],
#     'median income': [55047, 92266, 60458, 57432, 130464]
# }
websites = {
    'Fort Worth': 'https://www.fortworthtexas.gov/departments/development-services/infrastructure',
    'Dallas': 'https://dallascityhall.com/departments/transportation/Pages/default.aspx',
    'McKinney': 'https://www.mckinneytexas.org/3339/Infrastructure',
    'Frisco': 'https://www.friscotexas.gov/423/Capital-Improvement-Projects',
    'Plano': 'https://www.plano.gov/425/Traffic-Transportation'
}

data = pd.read_excel('dallas metro data.xlsx', sheet_name=1)
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Population', 'value': 'Population'},
                    {'label': 'Growth Rate', 'value': 'Growth Rate'},
                    {'label': 'Median Individual Income', 'value': 'Median Individual Income'},
                    {'label': 'Signalized Intersections', 'value': 'Signalized Intersections'},
                    {'label': 'Annual Traffic Spending', 'value': 'Annual Traffic Spending'}
                ],
                value='Population'  # default value
            )
        ], width={'size': 6, 'offset': 3}, style={'marginTop': 30}),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map')
        ], width=8),
        dbc.Col([
            dcc.Graph(id='bar-chart')
        ], width=4)
    ], style={'marginTop': 30}),
    dbc.Row([
        dbc.Col([
            html.Div(id='popup-content')
        ], width={'size': 8, 'offset': 2}, style={'marginTop': 30}),
    ])
], fluid=True)


# Callback function to update map
@app.callback(
    [Output('map', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('dropdown', 'value')]
)
def update_map(selected_value):
    # Create Map
    try:
        fig_map = px.scatter_mapbox(df,
                                    lat='Latitude',
                                    lon='Longitude',
                                    size=selected_value,
                                    color=selected_value,
                                    hover_name='City',
                                    hover_data=['Population', 'Growth Rate', 'Median Individual Income',
                                                'Signalized Intersections', 'Annual Traffic Spending'],
                                    title=f'Cities in the Dallas Region by {selected_value.title()}',
                                    mapbox_style="open-street-map",
                                    color_continuous_scale='Rainbow',
                                    size_max=50,
                                    zoom=8,
                                    center={"lat": 32.7767, "lon": -96.7970})
        fig_map.update_layout(
            # ... other layout configurations ...
            height=800  # Specifying the height
        )
        fig_map.update_traces(
            hovertemplate="<b>%{hovertext}</b><br><br>" +
                          "Population: %{customdata[0]:,.0f}<br>" +
                          "Growth Rate: %{customdata[1]:.2f}%<br>" +
                          "Median Individual Income: $%{customdata[2]:,.2f}<br>" +
                          "Signalized Intersections: %{customdata[3]:,.0f}<br>" +
                          "Annual Traffic Spending: $%{customdata[4]:,.0f}<br>" +
                          "<extra></extra>"
        )

        # Create Bar Chart
        fig_bar = px.bar(df, x='City', y=selected_value, title=f'{selected_value.title()} by City')
        fig_bar.update_layout(
            # ... other layout configurations ...
            height=800  # Specifying the height
        )
        return fig_map, fig_bar  # Return figures to respective output components
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise exceptions.PreventUpdate("Failed to create the map. If you're on Chrome, do you have WebGL enabled? If you're not sure:\n"
                                       "1) Visit chrome://flags/ and enable WebGL and WebGL2."
                                       "2) Visit chrome://gpu/ and ensure that WebGL and WebGL2 are available and hardware-accelerated.\n"
                                       "3) If they're not, go to Chrome settings -> Advanced -> System and ensure that Use hardware acceleration when available is enabled.\n"
                                       "If this doesn't work, try another browser.")


# Callback function to display popup
@app.callback(
    Output('popup-content', 'children'),
    [Input('map', 'clickData')]
)
def display_popup(clickData):
    if clickData is None:
        return html.Div([
            html.P(
                "Click on a city for more info. If you can't see the map and you're on Chrome, do you have WebGL enabled?"),
            html.P("If you're not sure:"),
            html.Ol([
                html.Li("Visit chrome://flags/ and enable WebGL and WebGL2."),
                html.Li("Visit chrome://gpu/ and ensure that WebGL and WebGL2 are available and hardware-accelerated."),
                html.Li(
                    "If they're not, go to Chrome settings -> Advanced -> System and ensure that Use hardware acceleration when available is enabled."),
            ]),
            html.P("If this doesn't work, try another browser.")
        ])

    point_data = clickData['points'][0]
    city_name = point_data['hovertext']

    content = [
        html.H4(city_name),
        html.P(f"Population: {point_data['customdata'][0]:,.0f}"),
        html.P(f"Growth Rate: {point_data['customdata'][1]:.2f}%"),
        html.P(f"Median Individual Income: ${point_data['customdata'][2]:,.0f}"),
        html.P(f"Signalized Intersections: {point_data['customdata'][3]:,.0f}"),
        html.P(f"Annual Traffic Spending: ${point_data['customdata'][4]:,.0f}"),
        html.A(f"Visit {city_name} Website", href=websites[city_name], target="_blank")
    ]

    return content

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)