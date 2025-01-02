import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data from the uploaded CSV file
df = pd.read_csv('fifa_world_cup_data .csv')

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "🌍 FIFA World Cup Performance Dashboard 🏆",
        style={
            "textAlign": "center",
            "color": "#000000",
            "padding": "20px",
            "borderRadius": "15px",
            "background": "linear-gradient(90deg, #4CAF50, #FF9880)",
            "boxShadow": "0px 4px 8px rgba(255, 255, 255, 0.2)"
        }
    ),

    html.Div([
        html.Div([
            html.Label("📈 Select Metric for Line Plot:", style={"color": "#FFFFFF", "fontWeight": "bold", "fontSize": "16px"}),
            dcc.Dropdown(
                id='line-metric-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns if col not in ['Country']],
                value=df.columns[1],
                style={"border": "1px solid #4CAF50", "borderRadius": "5px", "fontSize": "14px"}
            ),
            dcc.Graph(id='line-plot', style={"padding": "10px"})
        ], style={"flex": "1", "margin": "10px", "background": "#222222", "borderRadius": "10px", "padding": "20px", "boxShadow": "0px 4px 6px rgba(255, 255, 255, 0.1)"}),

        html.Div([
            html.Label("📊 Select Metric for Bar Plot:", style={"color": "#FFFFFF", "fontWeight": "bold", "fontSize": "16px"}),
            dcc.Dropdown(
                id='bar-metric-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns if col not in ['Country']],
                value=df.columns[2],
                style={"border": "1px solid #FF9800", "borderRadius": "5px", "fontSize": "14px"}
            ),
            dcc.Graph(id='bar-plot', style={"padding": "10px"})
        ], style={"flex": "1", "margin": "10px", "background": "#222222", "borderRadius": "10px", "padding": "20px", "boxShadow": "0px 4px 6px rgba(255, 255, 255, 0.1)"}),

        html.Div([
            html.Label("🎯 Select Country for Pie Chart:", style={"color": "#FFFFFF", "fontWeight": "bold"}),
            dcc.Dropdown(
                id='pie-country-dropdown',
                options=[{'label': country, 'value': country} for country in df['Country']],
                value=df['Country'][0],
                style={"border": "1px solid #FF4500", "borderRadius": "5px"}
            ),
            dcc.Graph(id='pie-chart', style={"padding": "10px"})
        ], style={"flex": "1", "margin": "10px", "background": "#222222", "borderRadius": "10px", "padding": "20px", "boxShadow": "0px 4px 6px rgba(255, 255, 255, 0.1)"}),

    ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "space-around", "background": "#333333", "padding": "20px", "borderRadius": "10px", "boxShadow": "0px 4px 6px rgba(255, 255, 255, 0.1)"})

], style={"background": "#000000", "padding": "30px"})

@app.callback(
    Output('line-plot', 'figure'),
    Input('line-metric-dropdown', 'value')
)
def update_line_plot(selected_metric):
    fig = px.line(
        df,
        x='Country',
        y=selected_metric,
        title=f'{selected_metric} Across Countries',
        markers=True
    )
    fig.update_traces(line=dict(width=3, color="#FFD700"), marker=dict(size=10, color="#FF4500"))
    fig.update_layout(
        plot_bgcolor="#222222",
        paper_bgcolor="#222222",
        font_color="#FFFFFF",
        title_font_size=20,
        font=dict(size=14)
    )
    return fig

@app.callback(
    Output('bar-plot', 'figure'),
    Input('bar-metric-dropdown', 'value')
)
def update_bar_plot(selected_metric):
    fig = px.bar(
        df,
        x='Country',
        y=selected_metric,
        title=f'{selected_metric} Comparison by Country',
        text=selected_metric
    )
    fig.update_traces(marker_color="#32CD32", texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        plot_bgcolor="#222222",
        paper_bgcolor="#222222",
        font_color="#FFFFFF",
        title_font_size=20,
        font=dict(size=14)
    )
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    Input('pie-country-dropdown', 'value')
)
def update_pie_chart(selected_country):
    country_data = df[df['Country'] == selected_country].iloc[0]
    values = [
        country_data['Wins'],
        country_data['Finals'] - country_data['Wins'],
        country_data['Matches Played'] - country_data['Finals']
    ]
    labels = ['Wins', 'Finals Without Wins', 'Matches Without Finals']
    
    # Define a custom color sequence: blue, red, yellow
    custom_colors = ['#0000FF', '#FF0000', '#FFFF00']
    
    fig = px.pie(
        names=labels,
        values=values,
        title=f'Performance Breakdown for {selected_country}',
        color_discrete_sequence=custom_colors  # Apply the custom colors here
    )
    
    fig.update_layout(
        plot_bgcolor="#222222",
        paper_bgcolor="#222222",
        font_color="#FFFFFF",
        title_font_size=20,
        font=dict(size=14)
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)