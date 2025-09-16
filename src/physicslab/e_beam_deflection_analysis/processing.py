# src/physicslab/e-beam_deflection_analysis/processing.py

import os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import matplotlib.pyplot as plt
from physicslab.plot_utils import create_figure, save_figure


def plot_D_Y_vs_V_d(processed_df: pd.DataFrame, output_dir: str | Path):
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    df1 = processed_df.dropna(subset=["V2_V", "Vd_V", "Dy_mm"])
    fig, ax1 = create_figure(
        title="$D_Y$ - $V_d$ 直线图", xlabel="$V_d$ (mm)", ylabel="$D_Y$ (V)"
    )
    colors = plt.cm.tab10.colors
    for idx, (v2_v, group) in enumerate(df1.groupby("V2_V")):
        x = group["Vd_V"]
        y = group["Dy_mm"]
        ax1.scatter(x, y, color=colors[idx % len(colors)], label=rf"$V_2={{{v2_v}}}$")

        def linear_func(x, k, b):
            return k * x + b

        try:
            popt, _ = curve_fit(linear_func, x, y)
            k, b = popt
            x_fit = np.linspace(x.min(), x.max(), 100)
            y_fit = linear_func(x_fit, k, b)
            # Format legend with period as decimal separator and proper sign
            k_str = f"{k:.4f}".replace(",", ".")
            b_str = f"{b:+.4f}".replace(",", ".")
            ax1.plot(
                x_fit,
                y_fit,
                "-",
                color=colors[idx % len(colors)],
                label=rf"$V_d = {k_str} D_Y {b_str}$",
            )
        except Exception as e:
            ax1.plot(
                [],
                [],
                color=colors[idx % len(colors)],
                label=rf"$V_2={{{v2_v}}}$ 拟合失败: {e}",
            )
    ax1.legend()
    save_figure(fig, output_dir / "V_d_vs_D_Y.png")


def plot_D_B_vs_I(processed_df: pd.DataFrame, output_dir: str | Path):
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    df2 = processed_df.dropna(subset=["V2_V", "I_mA", "Db_mm"])
    fig, ax2 = create_figure(
        title="$D_B$ - $I$ 直线图", xlabel="$I$ (mA)", ylabel="$D_B$ (mm)"
    )
    colors = plt.cm.tab10.colors
    for idx, (v2_v, group) in enumerate(df2.groupby("V2_V")):
        x = group["I_mA"]
        y = group["Db_mm"]
        ax2.scatter(x, y, color=colors[idx % len(colors)], label=rf"$V_2={{{v2_v}}}$")

        def linear_func(x, k, b):
            return k * x + b

        try:
            popt, _ = curve_fit(linear_func, x, y)
            k, b = popt
            x_fit = np.linspace(x.min(), x.max(), 100)
            y_fit = linear_func(x_fit, k, b)
            # Format legend with period as decimal separator and proper sign
            k_str = f"{k:.4f}".replace(",", ".")
            b_str = f"{b:+.4f}".replace(",", ".")
            ax2.plot(
                x_fit,
                y_fit,
                "-",
                color=colors[idx % len(colors)],
                label=rf"$D = {k_str} I {b_str}$",
            )
        except Exception as e:
            ax2.plot(
                [],
                [],
                color=colors[idx % len(colors)],
                label=rf"$V_2={{{v2_v}}}$ 拟合失败: {e}",
            )
    ax2.legend()
    save_figure(fig, output_dir / "I_vs_D.png")


def count_mass_to_charge_ratio(processed_df: pd.DataFrame) -> None:
    """
    Calculate the mass-to-charge ratio of the electron for each $V_2$ value in the DataFrame.

    Args:
        processed_df (pd.DataFrame): DataFrame containing columns 'V_V' and 'I_avg_A'.

    Returns:
        list[dict]: List of dicts with keys 'V_2', 'I_avg', and 'em_ratio'.
    """
    mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability (H/m)
    L_N = 0.234  # m
    N = 1550
    D_N = 0.090  # m
    h = 0.145  # m (use h_Y as default, adjust if needed)
    results = []
    for _, row in processed_df.iterrows():
        V_2 = float(row["V_V"])
        I_avg = float(row["I_avg_A"])
        numerator = 8 * np.pi**2 * V_2 * (L_N**2 + D_N**2)
        denominator = mu_0**2 * N**2 * h**2 * I_avg**2
        em_ratio = numerator / denominator
        results.append({"V_2": V_2, "I_avg": I_avg, "em_ratio": em_ratio})
    return results
