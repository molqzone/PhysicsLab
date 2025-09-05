# src/physicslab/thermal_resistor/processing.py

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import os

from physicslab.plot_utils import create_figure, save_figure


def analyze_thermal_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze thermal resistor data to compute resistance and temperature coefficients.

    Parameters:
    raw_df (pd.DataFrame): DataFrame containing raw data with columns 'Time', 'Voltage', 'Current', 'Temperature'.

    Returns:
    pd.DataFrame: DataFrame with computed resistance and temperature coefficients.
    """
    df = raw_df.copy()

    if "t/℃" in df.columns:
        df["T/K"] = df["t/℃"] + 273.15

    if "T/K" in df.columns:
        df["1/T (10^-2 K^-1)"] = (1 / df["T/K"]) * 100

    if "R_T/Ω" in df.columns:
        df["ln R_T"] = np.log(df["R_T/Ω"])

    # TODO: Not usable algorithm to figure omega out yet
    # df['-w/(%·K^-1)'] = ...

    return df


def plot_thermal_curves(processed_df: pd.DataFrame, output_dir: str | Path):
    """
    Plot thermal curves based on processed data.

    Parameters:
    processed_df (pd.DataFrame): DataFrame containing processed data with necessary columns.
    output_dir (str): Directory to save the plots.
    """
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # --- Plot 1: ln(R_T) vs 1/T ---
    df1 = processed_df.dropna(subset=["1/T (10^-2 K^-1)", "ln R_T"])
    x1 = df1["1/T (10^-2 K^-1)"] * 1e-2  # Convert to K^-1
    y1 = df1["ln R_T"]

    # Use the create_figure function to create the plot
    fig, ax1 = create_figure(
        title="$\ln R_T$ - $1/T$ 直线图",
        xlabel=r"$1/T\ (\mathrm{K}^{-1})$",
        ylabel=r"$\ln R_T$",
    )
    ax1.scatter(x1, y1, color="b", label="实验数据")

    # Linear fitting
    def linear_func(x, k, b):
        return k * x + b

    popt, pcov = curve_fit(linear_func, x1, y1)
    k, b = popt
    k_err, b_err = np.sqrt(np.diag(pcov))

    x_fit = np.linspace(x1.min(), x1.max(), 100)
    ax1.plot(
        x_fit,
        linear_func(x_fit, k, b),
        "r-",
        label=rf"$\ln R_T = ({k:.2f}\pm{k_err:.2f})x {b:+.2f}\pm{b_err:.2f}$",
    )
    ax1.legend()

    # Use the save_figure utility
    save_figure(fig, output_dir / "ln_R_T_vs_1_T.png")

    # --- Plot 2: N vs T ---
    df2 = processed_df.dropna(subset=["N", "T/K"])
    x2 = df2["T/K"]
    y2 = df2["N"]

    fig, ax2 = create_figure(
        title="$N$ - $T$ 直线图",
        xlabel=r"$T\ (\mathrm{K})$",
        ylabel=r"$N$",
    )
    ax2.scatter(x2, y2, color="g", label="实验数据")

    # Linear fitting
    popt, pcov = curve_fit(linear_func, x2, y2)
    k, b = popt
    k_err, b_err = np.sqrt(np.diag(pcov))

    x_fit = np.linspace(x2.min(), x2.max(), 100)
    ax2.plot(
        x_fit,
        linear_func(x_fit, k, b),
        "r-",
        label=rf"$N = ({k:.2f}\pm{k_err:.2f})x {b:+.2f}\pm{b_err:.2f}$",
    )
    ax2.legend()

    # Use the save_figure utility
    save_figure(fig, output_dir / "N_vs_T.png")
