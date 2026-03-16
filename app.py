from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('training_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

training_types = df['Training_Type'].unique()

app = Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    
    html.H1("Muay Thai Performance Dashboard 🥊", style={'textAlign': 'center'}),
    
    html.P("Select a training type to filter the metrics:", style={'textAlign': 'center'}),
    
    html.Div(
        dcc.Dropdown(
            id='training-filter',
            options=[{'label': t, 'value': t} for t in training_types],
            value=training_types[0],
            clearable=False
        ),
        style={'width': '50%', 'margin': '0 auto', 'paddingBottom': '20px'}
    ),
    
    dcc.Graph(id='performance-graph')
])
@app.callback(
    Output('performance-graph', 'figure'),
    Input('training-filter', 'value')
)
def update_graph(selected_training):
    filtered_df = df[df['Training_Type'] == selected_training]
    
    fig = px.line(
        filtered_df, 
        x='Date', 
        y='Calories_Burned', 
        markers=True,
        title=f"Calories Burned Over Time: {selected_training}",
        labels={"Calories_Burned": "Calories (kcal)", "Date": "Training Date"}
    )
    
    fig.update_layout(template='plotly_white')
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)