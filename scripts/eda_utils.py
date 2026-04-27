import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

SENTINEL = -999.0

COLORS = {
    "Ethiopia": "#E63946",
    "Kenya":    "#2A9D8F",
    "Sudan":    "#E9C46A",
    "Tanzania": "#F4A261",
    "Nigeria":  "#457B9D",
}


def load_and_clean(filepath: str, country: str) -> pd.DataFrame:
    """
    Load a NASA POWER CSV, replace sentinel values, parse dates,
    drop duplicates, and forward-fill isolated missing values.
    """
    df = pd.read_csv(filepath)
    df.replace(SENTINEL, np.nan, inplace=True)
    df["Date"] = pd.to_datetime(df["YEAR"] * 1000 + df["DOY"], format="%Y%j")
    df["Month"] = df["Date"].dt.month
    df.drop_duplicates(inplace=True)
    df.ffill(inplace=True)
    df["Country"] = country
    return df


def profile_dataframe(df: pd.DataFrame) -> None:
    """
    Print a standardized data profile:
    shape, duplicates, missing values, and data types.
    """
    print("=" * 50)
    print(f"Shape            : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Duplicate rows   : {df.duplicated().sum()}")
    print(f"\nMissing Values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nData Types:\n{df.dtypes}")
    print("=" * 50)


def detect_outliers(df: pd.DataFrame, cols: list) -> None:
    """
    Detect and report statistical outliers using Z-score method (|Z| > 3).
    Outliers are retained as they represent genuine climate extremes.
    """
    numeric_df = df[cols].dropna()
    z_scores = np.abs(stats.zscore(numeric_df))
    outlier_mask = (z_scores > 3).any(axis=1)
    count = outlier_mask.sum()
    print(f"Outliers (|Z| > 3): {count} rows ({count / len(df) * 100:.2f}%)")
    print("Note: Outliers retained — represent genuine climate extremes for COP32.")


def plot_time_series(df: pd.DataFrame, col: str, country: str) -> None:
    """
    Plot a monthly-resampled time series for a given column and country.
    """
    color = COLORS.get(country, "#888888")
    fig, ax = plt.subplots(figsize=(14, 5))
    monthly = df.set_index("Date").resample("ME")[col].mean()
    ax.plot(monthly.index, monthly.values, color=color, linewidth=1.8)
    ax.set_title(f"{country} — Monthly Avg {col} (2015–2026)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel(col, fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df: pd.DataFrame, cols: list, country: str) -> None:
    """
    Plot a correlation heatmap for the specified numeric columns.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df[cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, ax=ax)
    ax.set_title(f"{country} — Variable Correlation Heatmap",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def summary_statistics(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Return a clean summary table: mean, median, std for the given columns.
    """
    return df[cols].agg(["mean", "median", "std"]).round(2).T.rename(
        columns={"mean": "Mean", "median": "Median", "std": "Std Dev"}
    )
