# scripts/process_thermal_resistor.py

from pathlib import Path

from physicslab.data_utils import (
    load_transposed_csv,
    check_missing_data,
    save_processed_data,
)
from physicslab.plot_utils import setup_plot_style
from physicslab.thermal_resistor.processing import (
    analyze_thermal_data,
    plot_thermal_curves,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = PROJECT_ROOT / "data/raw/thermal_resistor/source_data.csv"
PROCESSED_CSV = PROJECT_ROOT / "data/processed/thermal_resistor/processed_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs/thermal_resistor/"


def main() -> None:
    print("Starting the Thermal Resistor data processing workflow...")

    setup_plot_style()

    print(f"\n--> Step 1: Loading and validating raw data from '{INPUT_CSV.name}'...")
    raw_df = load_transposed_csv(INPUT_CSV)

    if raw_df.empty:
        print(f"Error: No valid data found in '{INPUT_CSV.name}'.")
        return

    check_missing_data(raw_df, "Raw Data")

    print("\n--> Step 2: Analyzing thermal data...")
    process_df = analyze_thermal_data(raw_df)

    check_missing_data(process_df, "Processed Data")

    print("\n--> Step 3: Saving processed data...")
    save_processed_data(process_df, PROCESSED_CSV)

    print(f"\n--> Step 4: Plotting thermal curves and saving to '{OUTPUT_DIR}'...")
    plot_thermal_curves(process_df, OUTPUT_DIR)

    print("\nThermal Resistor data processing workflow completed successfully!")


if __name__ == "__main__":
    main()
