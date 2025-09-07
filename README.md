# GDUT University Physics Lab - Data Processing Toolkit

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Managed with PDM](https://img.shields.io/badge/managed%20by-PDM-29A4D5.svg)](https://pdm-project.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of Python scripts designed to automate calculations and generate plots for the Guangdong University of Technology's University Physics Lab course.

---

## 🌟 Key Features

* **Automated Processing**: Standardized pipeline for processing raw experimental data.
* **Modular Design**: Reusable utilities for data I/O and plotting, with experiment-specific logic clearly separated.
* **High-Quality Visualization**: Generates consistent, report-ready plots using Matplotlib.
* **Reproducible Environment**: Managed by **PDM**, ensuring a consistent environment and dependencies via a lockfile.

## 📂 Project Structure

The project follows a modern, standard Python source layout for clarity and scalability.

```
PhysicsLab/
├── .venv/                     # PDM-managed virtual environment (ignored by Git)
├── data/                      # All data files
│   ├── processed/             # Sub-directory for processed data
│   └── raw/                   # Sub-directory for original, immutable raw data
├── notebooks/                 # Directory for exploratory Jupyter Notebooks
├── outputs/                   # Directory for all generated outputs (plots, reports)
├── scripts/                   # Executable "driver" scripts to run the full workflow for each experiment
├── src/                       # All installable Python source code lives here
│   └── physicslab/
│       ├── __init__.py
│       ├── data_utils.py      # General utilities for data loading/saving
│       ├── plot_utils.py      # General utilities for plot styling
│       └── experiments/       # Sub-package for experiment-specific logic
│           ├── __init__.py
│           ├── thermal_resistor.py
│           └── ...            # Logic for other experiments
├── .gitignore                 # Specifies files for Git to ignore
├── pdm.lock                   # PDM lockfile for reproducible installs
└── pyproject.toml             # Project metadata and dependencies for PDM
```

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

* Python 3.11+
* [Git](https://git-scm.com/)
* [PDM](https://pdm-project.org/) (Follow the official guide for installation)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/PhysicsLab.git](https://github.com/your-username/PhysicsLab.git)
    cd PhysicsLab
    ```

2.  **Install dependencies using PDM:**
    This single command will create a `.venv` virtual environment in the project directory and install all the necessary packages specified in `pyproject.toml` and `pdm.lock`.
    ```bash
    pdm install
    ```

## ⚙️ Usage

The main workflow involves running "driver scripts" from the `scripts/` directory. Each script corresponds to a complete analysis for one experiment.

### Running a Full Analysis

To run the analysis for a specific experiment (e.g., the Thermal Resistor), execute its corresponding script using `pdm run`.

```bash
# Example for the Thermal Resistor experiment
pdm run python scripts/process_thermal_resistor.py
```

The script will:
1.  Load the raw data from `data/raw/`.
2.  Perform all calculations.
3.  Save the processed data to `data/processed/`.
4.  Generate and save all plots to `outputs/`.

### Interactive Exploration

If you want to explore the data or test functions interactively, you can use the IPython console within the project's virtual environment.

```bash
pdm run ipython
```
Inside IPython, you can then import your utility and processing functions:
```python
from physicslab.data_utils import load_transposed_csv
from physicslab.experiments.thermal_resistor import analyze_thermal_data

df = load_transposed_csv("data/raw/thermal_resistor/source_data.csv")
processed_df = analyze_thermal_data(df)
print(processed_df.head())
```

## ✨ Adding a New Experiment

The project is designed to be easily extensible. To add a new experiment (e.g., "ViscosityMeasurement"), follow these steps:

1.  **Add Raw Data**
    Create a new directory for your experiment inside `data/raw/` and place your source data file(s) there.
    * Example: `data/raw/viscosity_measurement/fall_times.csv`

2.  **Create the Logic Module**
    Create a new Python file inside the `src/physicslab/experiments/` directory. This file will contain all the specific calculations and plotting functions for this new experiment.
    * Example: `src/physicslab/experiments/viscosity_measurement.py`

3.  **Create the Driver Script**
    The easiest way is to copy an existing script from the `scripts/` directory and modify it.
    * Copy `scripts/process_thermal_resistor.py` to `scripts/process_viscosity_measurement.py`.
    * Inside the new script, change the `import` statements to pull functions from your new logic module (e.g., `from physicslab.experiments.viscosity_measurement import ...`).
    * Update the file paths at the top of the script to point to the correct data and output directories.

4.  **Run the New Analysis**
    You can now run the complete workflow for your new experiment with a single command:
    ```bash
    pdm run python scripts/process_viscosity_measurement.py
    ```

## 🛠️ Tools Used

* [Python](https://www.python.org/)
* [PDM](https://pdm-project.org/) - Dependency Management
* [Pandas](https://pandas.pydata.org/) - Data Manipulation
* [NumPy](https://numpy.org/) - Numerical Computation
* [Matplotlib](https://matplotlib.org/) - Plotting
* [SciPy](https://scipy.org/) - Scientific Computing

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.