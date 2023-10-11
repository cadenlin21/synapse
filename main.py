import pandas as pd
import plotly.graph_objs as go
import plotly as plt

# # Sample data
# Sample data
data = {
    'city_name': ['Dallas', 'Plano', 'Arlington', 'Frisco', 'Denton', 'Richardson', 'Irving'],
    'latitude': [32.7767, 33.0198, 32.7357, 33.1507, 33.2148, 32.9483, 32.8140],
    'longitude': [-96.7970, -96.6989, -97.1081, -96.8236, -97.1331, -96.7283, -96.9498],
    'population': [1341000, 288000, 398000, 200000, 141000, 120000, 240000],
    'median_income': [50000, 85000, 56000, 120000, 49000, 77000, 58000],
    'growth_rate': [0.015, 0.020, 0.017, 0.035, 0.020, 0.022, 0.018],
    'intersections': [500, 200, 300, 180, 170, 190, 220],
    'traffic_spending': [3000000, 800000, 1000000, 750000, 400000, 600000, 1100000]
}

df = pd.DataFrame(data)

# Define max size for markers
MAX_SIZE = 50

# Calculate normalized sizes for each metric
df['population_size'] = (df['population'] / df['population'].max()) * MAX_SIZE
df['median_income_size'] = (df['median_income'] / df['median_income'].max()) * MAX_SIZE
df['growth_rate_size'] = (df['growth_rate'] / df['growth_rate'].max()) * MAX_SIZE
df['intersections_size'] = (df['intersections'] / df['intersections'].max()) * MAX_SIZE
df['traffic_spending_size'] = (df['traffic_spending'] / df['traffic_spending'].max()) * MAX_SIZE

# Scattermapbox trace
trace = go.Scattermapbox(
    lat=df['latitude'],
    lon=df['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=df['population_size'],
        color=df['population'],
        colorscale="RdBu",  # Red to Blue colorscale
        sizemode='diameter',
        colorbar=dict(title="Metric Value")
    ),
    text=df['city_name'],
    customdata=df['population'],
    hovertemplate="<b>%{text}</b><br><b>Population:</b> %{customdata}",
)

layout = go.Layout(
    mapbox=dict(
        style="open-street-map",
        zoom=9,
        center=dict(lat=32.7767, lon=-96.7970)
    ),
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[{"marker.size": df['population_size'].tolist(), "marker.color": df['population'].tolist(), "customdata": df['population'].tolist(), "hovertemplate": "<b>%{text}</b><br><b>Population:</b> %{customdata}", "marker.colorbar.title": "Population"}],
                    label="Population",
                    method="restyle"
                ),
                dict(
                    args=[{"marker.size": df['median_income_size'].tolist(), "marker.color": df['median_income'].tolist(), "customdata": df['median_income'].tolist(), "hovertemplate": "<b>%{text}</b><br><b>Median Income:</b> $%{customdata}", "marker.colorbar.title": "Median Income ($)"}],
                    label="Median Income",
                    method="restyle"
                ),
                dict(
                    args=[{"marker.size": df['growth_rate_size'].tolist(), "marker.color": df['growth_rate'].tolist(), "customdata": df['growth_rate'].tolist(), "hovertemplate": "<b>%{text}</b><br><b>Growth Rate:</b> %{customdata}", "marker.colorbar.title": "Growth Rate"}],
                    label="Growth Rate",
                    method="restyle"
                ),
                dict(
                    args=[{"marker.size": df['intersections_size'].tolist(), "marker.color": df['intersections'].tolist(), "customdata": df['intersections'].tolist(), "hovertemplate": "<b>%{text}</b><br><b>Intersections:</b> %{customdata}", "marker.colorbar.title": "Number of Intersections"}],
                    label="Intersections",
                    method="restyle"
                ),
                dict(
                    args=[{"marker.size": df['traffic_spending_size'].tolist(), "marker.color": df['traffic_spending'].tolist(), "customdata": df['traffic_spending'].tolist(), "hovertemplate": "<b>%{text}</b><br><b>Traffic Spending:</b> $%{customdata}", "marker.colorbar.title": "Traffic Spending ($)"}],
                    label="Traffic Spending",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ]
)

fig = go.Figure(data=[trace], layout=layout)
plt.offline.plot(fig, 'heatmap.html')