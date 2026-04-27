import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
        try:
            path = f'data/{country.lower()}_clean.csv'
            df = pd.read_csv(path)
            df['Country'] = country
            df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
            dfs.append(df)
        except FileNotFoundError:
            st.error(f"Data for {country} not found at {path}")
    
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)

def filter_data(df, year_range):
    """Filters dataframe by a range of years."""
    return df[(df['YEAR'] >= year_range[0]) & (df['YEAR'] <= year_range[1])]

def plot_line_chart(df, variable, countries):
    """Generates a multi-country line chart for a specific variable."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for country in countries:
        df_c = df[df['Country'] == country].copy()
        if not df_c.empty:
            # Resample to month end for smoothness
            df_monthly = df_c.set_index('Date').resample('ME')[variable].mean()
            ax.plot(df_monthly.index, df_monthly.values, 
                    label=country, color=COLORS.get(country), linewidth=1.5)
    
    ax.set_title(f"Monthly Average {variable} Over Time", fontsize=14, fontweight='bold')
    ax.set_ylabel(variable)
    ax.legend(title="Country", loc='upper right')
    plt.xticks(rotation=45)
    return fig

def plot_boxplot(df, variable):
    """Generates side-by-side boxplots for the selected variable."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x='Country', y=variable, palette=COLORS, ax=ax, hue='Country', legend=False)
    ax.set_title(f"{variable} Distribution by Country", fontsize=14, fontweight='bold')
    return fig

def get_summary_stats(df, variable):
    """Returns a summary stats table for the selected variable."""
    stats = df.groupby('Country')[variable].agg(['mean', 'median', 'std']).round(2)
    stats.columns = ['Mean', 'Median', 'Std Dev']
    return stats
