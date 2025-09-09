# scripts/process_e-beam_deflection_analysis.py

from pathlib import Path

from physicslab.data_utils import load_csv
from physicslab.plot_utils import setup_plot_style
from physicslab.e_beam_deflection_analysis.processing import (
    plot_D_Y_vs_V_d,
    plot_D_vs_I,
    count_mass_to_charge_ratio,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ELECTRIC_DEFLECTION_VERTICAL_MEASUREMENT_CSV = (
    PROJECT_ROOT / "data/raw/e_beam_deflection_analysis/elec_deflection_y_data.csv"
)
MAGNETIC_DEFLECTION_MEASUREMENT_CSV = (
    PROJECT_ROOT / "data/raw/e_beam_deflection_analysis/mag_deflection_data.csv"
)
EM_RATIO_MAG_FOCUS_CSV = (
    PROJECT_ROOT / "data/raw/e_beam_deflection_analysis/em_ratio_mag_focus.csv"
)
PROCESSED_CSV = (
    PROJECT_ROOT / "data/processed/e_beam_deflection_analysis/processed_data.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "output/e_beam_deflection_analysis/"


def main() -> None:
    print("Starting the E-Beam Deflection Analysis data processing workflow...")

    setup_plot_style()

    print(
        f"\n--> Step 1: Loading raw data from '{ELECTRIC_DEFLECTION_VERTICAL_MEASUREMENT_CSV.name}' and '{MAGNETIC_DEFLECTION_MEASUREMENT_CSV.name}'..."
    )
    electric_raw_df = load_csv(ELECTRIC_DEFLECTION_VERTICAL_MEASUREMENT_CSV)
    magnetic_raw_df = load_csv(MAGNETIC_DEFLECTION_MEASUREMENT_CSV)
    em_ratio_raw_df = load_csv(EM_RATIO_MAG_FOCUS_CSV)

    if electric_raw_df.empty:
        print(
            f"Error: No valid data found in '{ELECTRIC_DEFLECTION_VERTICAL_MEASUREMENT_CSV.name}'."
        )
        return

    print("\n--> Step 2: Plotting and saving figures...")
    plot_D_Y_vs_V_d(electric_raw_df, OUTPUT_DIR)
    plot_D_vs_I(magnetic_raw_df, OUTPUT_DIR)

    print(f"\n--> Step 3: Calculating e/m ratios from '{EM_RATIO_MAG_FOCUS_CSV.name}'...")
    ratio_dict = count_mass_to_charge_ratio(em_ratio_raw_df)
    print("Calculated e/m ratios:", ratio_dict)
    

    print(
        "\nE-Beam Deflection Analysis data processing workflow completed successfully!"
    )


if __name__ == "__main__":
    main()
