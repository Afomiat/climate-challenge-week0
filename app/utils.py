import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Standard color palette from our notebook
COLORS = {
    "Ethiopia": "#E63946",
    "Kenya":    "#2A9D8F",
    "Sudan":    "#E9C46A",
    "Tanzania": "#F4A261",
    "Nigeria":  "#457B9D",
}

@st.cache_data
def load_data(countries):
    """Loads and concatenates the selected countries' clean CSVs."""
    dfs = []
    for country in countries:
        # 1. Try primary data folder
        path = f'data/processed/{country.lower()}_clean.csv'
        if not os.path.exists(path):
            # 2. Try sample data folder (for cloud deployment)
            path = f'app/sample_data/{country.lower()}_clean.csv'
            
        try:
            df = pd.read_csv(path)
            df['Country'] = country
            df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
            dfs.append(df)
        except Exception:
            continue 
    
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)

def filter_data(df, year_range):
    """Filters dataframe by a range of years."""
    return df[(df['YEAR'] >= year_range[0]) & (df['YEAR'] <= year_range[1])]

def plot_interactive_line(df, variable, countries):
    """Generates a Premium Plotly Line Chart."""
    # Resample each country separately to maintain color mapping
    plot_df_list = []
    for country in countries:
        df_c = df[df['Country'] == country].copy()
        if not df_c.empty:
            df_m = df_c.set_index('Date').resample('ME')[variable].mean().reset_index()
            df_m['Country'] = country
            plot_df_list.append(df_m)
    
    if not plot_df_list:
        return None
        
    plot_df = pd.concat(plot_df_list)
    
    fig = px.line(
        plot_df, x='Date', y=variable, color='Country',
        color_discrete_map=COLORS,
        template='plotly_dark',
        title=f'Monthly Avg {variable} (2015–2026)'
    )
    fig.update_layout(
        font_family="Inter, sans-serif",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_interactive_box(df, variable):
    """Generates a Premium Plotly Box Plot."""
    fig = px.box(
        df, x='Country', y=variable, color='Country',
        color_discrete_map=COLORS,
        template='plotly_dark',
        title=f'{variable} Distribution & Outliers'
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def calculate_vulnerability(df):
    """Calculates a real-time 'Risk Score' based on selected filter."""
    if df.empty: return None
    
    # Simple risk heuristic: (Heat + Dryness) / (Stability)
    stats = df.groupby('Country').agg({
        'T2M': 'mean',
        'PRECTOTCORR': 'std'
    }).reset_index()
    
    # Normalized score logic
    stats['Risk'] = (stats['T2M'] * 0.5) + (stats['PRECTOTCORR'] * 0.5)
    most_at_risk = stats.sort_values('Risk', ascending=False).iloc[0]['Country']
    return most_at_risk
