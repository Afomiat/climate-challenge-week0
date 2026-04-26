# Climate Challenge: Week 0 - African Climate EDA

This repository contains the environment setup, data preprocessing, and exploratory data analysis (EDA) for the 10 Academy Climate Challenge. The goal of this project is to analyze climate trends across five African nations (Ethiopia, Kenya, Sudan, Tanzania, and Nigeria) to generate negotiation-grade insights for the upcoming COP32 climate reporting project.

## 🌟 Project Implementation & Contributions

Our implementation successfully processed raw NASA POWER climate datasets through a structured pipeline:

1. **Robust Environment Setup (Task 1)**: 
   - Initialized a standardized data science folder structure.
   - Established an isolated Python virtual environment (`venv`).
   - Configured `.gitignore` to keep raw and clean CSV datasets out of version control for security and efficiency.
   - Implemented a CI/CD pipeline via GitHub Actions to automatically verify the environment integrity on push.

2. **Data Cleaning & Profiling (Task 2)**: 
   - Handled NASA's `-999.0` sentinel missing values properly by converting them to `NaN`.
   - Forward-filled isolated missing values and dropped duplicates.
   - Profiled statistical outliers (Z-score > 3) and strategically retained them, recognizing that extreme weather spikes represent genuine climate anomalies essential for COP32 analysis.

3. **Exploratory Data Analysis (EDA)**: 
   - **Time Series**: Identified distinct wet/dry seasons and hottest/coolest months across 2015–2026.
   - **Correlation**: Highlighted highly correlated variables (e.g., negative correlation between temperature and relative humidity).
   - **Distributions**: Used logarithmic scaling on precipitation histograms and plotted 3D bubble charts to map heavy storm events to humidity and temperature thresholds.

4. **Automated Pipeline Generation**:
   - Engineered a custom Python automation script to use Ethiopia's notebook as a master template.
   - Dynamically generated identical, executed EDA notebooks for Kenya, Sudan, Tanzania, and Nigeria with stripped Python comments and precise, dynamically-calculated markdown statistics.

## 📂 Repository Structure

```
├── .github/workflows/   # Continuous Integration (CI) actions
├── data/                # Raw and cleaned CSV files (Ignored by Git)
├── notebooks/           # Jupyter notebooks for EDA
│   ├── ethiopia_eda.ipynb  # Master commented template
│   ├── kenya_eda.ipynb     # Automated generation
│   ├── nigeria_eda.ipynb   # Automated generation
│   ├── sudan_eda.ipynb     # Automated generation
│   └── tanzania_eda.ipynb  # Automated generation
├── scripts/             # Python automation and utility scripts
├── requirements.txt     # Project dependencies
├── report.md            # Comprehensive project summary report
└── README.md            # Project documentation
```

## 🛠️ Reproducing the Environment

To reproduce this environment and run the analyses locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Afomiat/climate-challenge-week0.git
   cd climate-challenge-week0
   ```

2. **Create a Python Virtual Environment:**
   Run the following command to create an isolated Python environment named `venv`:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - **Windows:**
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   With the virtual environment activated, install the required packages using:
   ```bash
   pip install -r requirements.txt
   ```
