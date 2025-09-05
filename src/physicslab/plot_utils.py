# src/physicslab/plot_utils.py

import matplotlib.pyplot as plt
from typing import Tuple


def setup_plot_style() -> None:
    """
    Set up the plot style for Matplotlib.
    """
    # Set font to support Chinese characters (add more as needed)
    plt.rcParams["font.sans-serif"] = [
        "Arial Unicode MS",
        "Noto Sans SC",
        "STSong",
        "sans-serif",
    ]
    # Ensure the minus sign displays correctly
    plt.rcParams["axes.unicode_minus"] = False
    # Set a default figure size
    plt.rcParams["figure.figsize"] = (8, 6)
    # Set a default DPI for saved figures
    plt.rcParams["savefig.dpi"] = 300
    print("🎨 Plot style configured for professional output.")


def create_figure(
    title: str,
    xlabel: str,
    ylabel: str,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a Matplotlib figure with a title and axis labels.

    Parameters:
    - title (str): The title of the plot.
    - xlabel (str): The label for the x-axis.
    - ylabel (str): The label for the y-axis.

    Returns:
    - Tuple[plt.Figure, plt.Axes]: The created figure and axes.
    """
    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    return fig, ax


def save_figure(fig: plt.Figure, filepath: str) -> None:
    """
    Save a Matplotlib figure to a file.

    Parameters:
    - fig (plt.Figure): The figure to save.
    - filename (str): The filename (including path) to save the figure to.
    """
    fig.savefig(filepath, bbox_inches="tight")
    plt.close(fig)  # Close the figure to free up memory
    print(f"📈 Figure saved to {filepath}")
