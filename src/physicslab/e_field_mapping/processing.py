# src/physicslab/e_field_mapping/processing.py

import os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import matplotlib.pyplot as plt
from physicslab.plot_utils import create_figure, save_figure


def analyze_e_field_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze electric field mapping data to compute necessary parameters.

    Parameters:
    raw_df (pd.DataFrame): DataFrame containing raw data with columns 'X', 'Y', 'V'.

    Returns:
    pd.DataFrame: DataFrame with computed electric field parameters.
    """
    df = raw_df.copy()

    # For equipotential mapping data
    d_cols = [f"d{i}_cm" for i in range(1, 6)]
    if all(col in df.columns for col in d_cols):
        # Fill d_bar_cm as mean of d1_cm to d5_cm
        df["d_bar_cm"] = df[d_cols].mean(axis=1)
        # Fill r_bar_cm as d_bar_cm / 2
        df["r_bar_cm"] = df["d_bar_cm"] / 2
        # Fill ln_r as ln(r_bar_cm)
        df["ln_r"] = np.log(df["r_bar_cm"])
        # Fill ln_r_over_ln_7 as ln(r_bar_cm) / ln(7)
        ln_7 = np.log(7)
        df["ln_r_over_ln_7"] = df["ln_r"] / ln_7
        # 保留两位小数
        df["d_bar_cm"] = df["d_bar_cm"].round(2)
        df["r_bar_cm"] = df["r_bar_cm"].round(2)
        df["ln_r"] = df["ln_r"].round(2)
        df["ln_r_over_ln_7"] = df["ln_r_over_ln_7"].round(2)

    return df


def plot_V_r_over_V_B_vs_ln_r_over_ln_7(
    processed_df: pd.DataFrame, output_dir: str | Path
):
    """
    Plot V_R/V_B vs ln(r)/ln(7) and save the figure.
    """
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    df1 = processed_df.dropna(subset=["V_R_over_V_B", "ln_r_over_ln_7"])
    x1 = df1["ln_r_over_ln_7"]
    y1 = df1["V_R_over_V_B"]

    fig, ax1 = create_figure(
        title="$V_r/V_B$ - $log(\\bar{r})/log(7)$ 直线图",
        xlabel=r"$log(\bar{r})/log(7)$",
        ylabel=r"$V_r/V_B$",
    )
    ax1.scatter(x1, y1, color="b", label="实验数据")

    def linear_func(x, k, b):
        return k * x + b

    popt, pcov = curve_fit(linear_func, x1, y1)
    k, b = popt
    x_fit = np.linspace(x1.min(), x1.max(), 100)
    y_fit = linear_func(x_fit, k, b)

    def format_float(val):
        s = f"{val:+.2f}"
        if s.endswith(".00"):
            s = s[:-3]
        return s

    k_str = f"{k:.4f}".replace(",", ".")
    b_str = format_float(b)
    ax1.plot(
        x_fit,
        y_fit,
        "r-",
        label=rf"拟合: $V_R/V_B = {k_str} \cdot \log({{r}})/\log(7) {b_str}$",
    )
    ax1.legend()
    save_figure(fig, output_dir / "V_R_over_V_B_vs_ln_r_over_ln_7.png")
