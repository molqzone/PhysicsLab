# src/scripts/process_sucrose_polarimetry.py

from pathlib import Path
from physicslab.data_utils import load_csv
from physicslab.plot_utils import setup_plot_style
from physicslab.sucrose_polarimetry.processing import (
    analyze_average_angle_deg,
    plot_average_angle_vs_concentration,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROTATION_ANGLES_CSV = (
    PROJECT_ROOT / "data/raw/sucrose_polarimetry/rotation_angles.csv"
)
PROCESSED_CSV = (
    PROJECT_ROOT / "data/processed/sucrose_polarimetry/processed_data.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "output/sucrose_polarimetry/"

def main() -> None:
    print("Starting the Sucrose Polarimetry data processing workflow...")

    setup_plot_style()

    print(
        f"\n--> Step 1: Loading raw data from '{ROTATION_ANGLES_CSV.name}'..."
    )
    raw_df = load_csv(ROTATION_ANGLES_CSV)
    if raw_df.empty:
        print(f"Error: No valid data found in '{ROTATION_ANGLES_CSV.name}'.")
        return

    print("\n--> Step 2: Analyzing data...")
    processed_df = analyze_average_angle_deg(raw_df)

    print(f"\n--> Step 3: Saving processed data to '{PROCESSED_CSV.name}'...")
    PROCESSED_CSV.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(PROCESSED_CSV, index=False)
    print(f"Processed data saved to '{PROCESSED_CSV}'.")

    print("\n--> Step 4: Plotting and saving figures...")
    plot_average_angle_vs_concentration(processed_df, OUTPUT_DIR)

    print("\nSucrose Polarimetry data processing workflow completed successfully!")

if __name__ == "__main__":
    main()
