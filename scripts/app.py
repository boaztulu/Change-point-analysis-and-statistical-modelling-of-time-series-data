#!/usr/bin/env python3
# app.py

import pandas as pd
import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load data
df_prices = pd.read_csv('BrentOilPrices.csv', parse_dates=['Date'])
df_events = pd.read_csv('BrentOilEvents.csv', parse_dates=['Date'])

# Preprocessing
df_prices.sort_values('Date', inplace=True)
df_prices.set_index('Date', inplace=True)
# Compute log returns
df_prices['LogReturn'] = np.log(df_prices['Price']).diff()

# Align event prices (forward fill to next trading day)
df_events.sort_values('Date', inplace=True)
df_events = pd.merge_asof(df_events,
                          df_prices[['Price']].reset_index(),
                          on='Date',
                          direction='forward')

# Initialize Dash app
app = Dash(__name__)
app.title = "Brent Oil Price Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Brent Crude Oil Price Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df_prices.index.min().date(),
                max_date_allowed=df_prices.index.max().date(),
                start_date=df_prices.index.min().date(),
                end_date=df_prices.index.max().date(),
                display_format='YYYY-MM-DD',
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Events:"),
            dcc.Dropdown(
                id='event-select',
                options=[{'label': ev, 'value': ev} for ev in df_events['Event']],
                value=list(df_events['Event']),
                multi=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'padding': '10px 0px'}),
    dcc.Graph(id='price-chart'),
    dcc.Graph(id='returns-chart'),
])

# Callbacks to update charts
@app.callback(
    Output('price-chart', 'figure'),
    Output('returns-chart', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('event-select', 'value'),
)
def update_charts(start_date, end_date, selected_events):
    # Filter by date
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    mask = (df_prices.index >= start) & (df_prices.index <= end)
    df_filt = df_prices.loc[mask]

    # Filter events
    df_evt = df_events[(df_events['Date'] >= start) & (df_events['Date'] <= end)]
    if selected_events:
        df_evt = df_evt[df_evt['Event'].isin(selected_events)]

    # Price chart
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=df_filt.index, y=df_filt['Price'],
        mode='lines', name='Price'
    ))
    if not df_evt.empty:
        fig_price.add_trace(go.Scatter(
            x=df_evt['Date'], y=df_evt['Price'],
            mode='markers', name='Events',
            marker=dict(symbol='x', size=10, color='red'),
            text=df_evt['Event'],
            hovertemplate="%{x|%Y-%m-%d}<br>%{text}<extra></extra>"
        ))
    fig_price.update_layout(
        title="Brent Crude Oil Price",
        xaxis_title="Date",
        yaxis_title="Price (USD per barrel)",
        hovermode="x unified"
    )

    # Returns chart
    fig_returns = go.Figure()
    fig_returns.add_trace(go.Scatter(
        x=df_filt.index, y=df_filt['LogReturn'],
        mode='lines', name='Log Return'
    ))
    fig_returns.update_layout(
        title="Daily Log Returns",
        xaxis_title="Date",
        yaxis_title="Log Return",
        hovermode="x unified"
    )

    return fig_price, fig_returns

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
