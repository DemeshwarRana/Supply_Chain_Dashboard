import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
file_path = 'Supply_chain_predictive_model.csv'
df = pd.read_csv(file_path)
origin_col = 'Origin_Port'
dest_col = 'Destination_Port'
target_col = 'Predicted_Lead_Time'
app = dash.Dash(__name__)
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '40px', 'backgroundColor': '#f4f7f6'}, children=[
    html.Div(style={'maxWidth': '1100px', 'margin': '0 auto', 'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        
        html.H1("Supply Chain Predictive Analytics", style={'textAlign': 'center', 'color': '#2d3436'}),
        html.P("XGBoost Simulation: Lead Time Forecasting by Route", style={'textAlign': 'center', 'color': '#636e72', 'marginBottom': '40px'}),
        html.Div([
            html.Div([
                html.Label("Select Origin Port:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='origin-dropdown',
                    options=[{'label': i, 'value': i} for i in sorted(df[origin_col].unique())],
                    value=df[origin_col].unique()[0],
                    clearable=False
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),

            html.Div([
                html.Label("Simulate Risk Score (%):", style={'fontWeight': 'bold'}),
                dcc.Slider(
                    id='risk-slider',
                    min=0, max=100, step=5, value=0,
                    marks={i: f'{i}%' for i in range(0, 101, 20)}
                ),
            ], style={'width': '45%', 'float': 'right', 'display': 'inline-block'}),
        ], style={'marginBottom': '50px'}),
        html.Div([
            html.H3(id='kpi-value', style={'color': '#e67e22', 'margin': '0'}),
            html.P("Projected Average Lead Time", style={'fontSize': '12px', 'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '15px', 'border': '1px solid #ddd', 'borderRadius': '8px', 'width': '30%', 'margin': '0 auto 30px auto'}),
        dcc.Graph(id='main-prediction-chart'),
        html.Hr(style={'margin': '40px 0'}),
        html.H3("Lead Time Risk Distribution", style={'textAlign': 'center', 'color': '#2d3436'}),
        dcc.Graph(id='distribution-chart'),
        html.Div(style={'marginTop': '30px', 'paddingTop': '20px', 'borderTop': '1px solid #eee', 'display': 'flex', 'justifyContent': 'space-between'}, children=[
            html.Div(f"Source: {file_path}", style={'fontSize': '12px', 'color': '#b2bec3'}),
            html.Div("Developed by Demeshwar Rana", 
                     style={'fontSize': '13px', 'fontWeight': 'bold', 'color': '#2d3436'})
        ])
    ])
])

@app.callback(
    [Output('main-prediction-chart', 'figure'),
     Output('distribution-chart', 'figure'),
     Output('kpi-value', 'children')],
    [Input('origin-dropdown', 'value'),
     Input('risk-slider', 'value')]
)
def update_dashboard(selected_origin, risk_pct):
    filtered_df = df[df[origin_col] == selected_origin].copy()
    base_df = filtered_df.copy()
    base_df['Scenario'] = 'Baseline (Normal)'
    risk_df = filtered_df.copy()
    impact = 1 + (risk_pct / 100)
    risk_df[target_col] = risk_df[target_col] * impact
    risk_df['Scenario'] = f'With {risk_pct}% Risk'
    
    combined_df = pd.concat([base_df, risk_df])
    y_limit = combined_df[target_col].max() * 1.2
    fig1 = px.histogram(
        combined_df, x=dest_col, y=target_col, color='Scenario',
        barmode='group', histfunc='avg', template='simple_white',
        color_discrete_map={'Baseline (Normal)': '#3498db', f'With {risk_pct}% Risk': '#e67e22'}
    )
    
    fig1.update_layout(
        title=f"Lead Time Comparison: {selected_origin}",
        yaxis_title="Average Days",
        xaxis_title="Destination Port",
        yaxis=dict(range=[0,90]),
        xaxis={'categoryorder':'total descending'}
    )
    fig2 = px.box(
        combined_df, x=dest_col, y=target_col, color='Scenario',
        template='simple_white',
        color_discrete_map={'Baseline (Normal)': '#3498db', f'With {risk_pct}% Risk': '#e67e22'}
    )
    fig2.update_layout(
        title="Risk Variance per Route",
        yaxis_title="Days",
        xaxis_title="Destination Port",
        yaxis=dict(range=[0, y_limit]),
        xaxis={'categoryorder':'total descending'}
    )

    kpi_text = f"{risk_df[target_col].mean():.1f} Days"
    return fig1, fig2, kpi_text
if __name__ == '__main__':
    app.run(debug=True, port=8050)