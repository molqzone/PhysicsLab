# scripts/process_e_field_mapping.py

from pathlib import Path
from physicslab.data_utils import load_csv
from physicslab.plot_utils import setup_plot_style
from physicslab.e_field_mapping.processing import (
    analyze_e_field_data,
    plot_V_r_over_V_B_vs_ln_r_over_ln_7
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EQUIPOTENTIAL_MAPPING_CSV = (
    PROJECT_ROOT / "data/raw/e_field_mapping/equipotential_mapping_data.csv"
)
PROCESSED_CSV = (
    PROJECT_ROOT / "data/processed/e_field_mapping/processed_data.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "output/e_field_mapping/"


def main() -> None:
    print("Starting the E-Field Mapping data processing workflow...")

    setup_plot_style()

    print(
        f"\n--> Step 1: Loading raw data from '{EQUIPOTENTIAL_MAPPING_CSV.name}'..."
    )
    raw_df = load_csv(EQUIPOTENTIAL_MAPPING_CSV)
    if raw_df.empty:
        print(f"Error: No valid data found in '{EQUIPOTENTIAL_MAPPING_CSV.name}'.")
        return

    print("\n--> Step 2: Analyzing data...")
    processed_df = analyze_e_field_data(raw_df)

    print(f"\n--> Step 3: Saving processed data to '{PROCESSED_CSV.name}'...")
    PROCESSED_CSV.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(PROCESSED_CSV, index=False)
    print(f"Processed data saved to '{PROCESSED_CSV}'.")

    print("\n--> Step 4: Plotting and saving figures...")
    plot_V_r_over_V_B_vs_ln_r_over_ln_7(processed_df, OUTPUT_DIR)

    print("\nE-Field Mapping data processing workflow completed successfully!")

if __name__ == "__main__":
    main()
