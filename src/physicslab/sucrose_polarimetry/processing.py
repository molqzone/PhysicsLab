# src/physicslab/sucrose_polarimetry/processing.py

import os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
from physicslab.plot_utils import create_figure, save_figure


def analyze_average_angle_deg(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze sucrose polarimetry data to compute average angles.

    Parameters:
    raw_df (pd.DataFrame): DataFrame containing raw data with columns 'trial1_deg', 'trial2_deg', 'trial3_deg'.

    Returns:
    pd.DataFrame: DataFrame with computed average angles.
    """
    df = raw_df.copy()
    # Alias for consistency
    if "sucrose_concentration_kg_m3" in df.columns:
        df["sucrose_concentration"] = df["sucrose_concentration_kg_m3"]

    # For sucrose polarimetry data
    trial_cols = ["trial1_deg", "trial2_deg", "trial3_deg"]
    if all(col in df.columns for col in trial_cols):
        # Ignore the first row where sucrose_concentration is 0
        mask = df["sucrose_concentration"] != 0
        # Fill average_angle_deg as mean of trial1_deg, trial2_deg, trial3_deg for rows where sucrose_concentration != 0
        df.loc[mask, "average_angle_deg"] = df.loc[mask, trial_cols].mean(axis=1)
        # Round to two decimal places
        df["average_angle_deg"] = df["average_angle_deg"].round(2)

    return df


def calculate_alpha(B: float, i: float) -> float:
    return B / (i * 1.0)


def calculate_c_x(phi_x: float, phi_0: float, B: float) -> float:
    return (phi_x - phi_0) * B


def plot_average_angle_vs_concentration(
    processed_df: pd.DataFrame, output_dir: str | Path
):
    """
    Plot average angle vs sucrose concentration and save the figure.
    """
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    df = processed_df.copy()
    if "sucrose_concentration_kg_m3" in df.columns:
        df["sucrose_concentration"] = df["sucrose_concentration_kg_m3"]

    # Ensure numeric types and filter out non-numeric rows
    df["sucrose_concentration"] = pd.to_numeric(
        df["sucrose_concentration"], errors="coerce"
    )
    df["average_angle_deg"] = pd.to_numeric(df["average_angle_deg"], errors="coerce")
    df1 = df.dropna(subset=["average_angle_deg", "sucrose_concentration"])
    x1 = df1["sucrose_concentration"]
    y1 = df1["average_angle_deg"]

    fig, ax1 = create_figure(
        title="平均旋光角与蔗糖浓度关系",
        xlabel="$c/(kg/m³)$",
        ylabel="$\phi$",
    )
    ax1.scatter(x1, y1, color="blue", label="数据点")

    # Fit a linear model
    def linear_model(x, m, b):
        return m * x + b

    if len(x1) >= 2:  # Ensure there are enough points to fit
        popt, pcov = curve_fit(linear_model, x1, y1)
        m, b = popt
        x_fit = np.linspace(min(x1), max(x1), 100)
        y_fit = linear_model(x_fit, m, b)
        ax1.plot(x_fit, y_fit, color="red", label=f"拟合: y={m:.2f}x+{b:.2f}")
        ax1.legend()

    save_figure(fig, output_dir / "average_angle_vs_concentration.png")
