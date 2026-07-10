import os
import pandas as pd

from src import preprocessing, eda, covid_analysis


def main():
    if not os.path.exists(preprocessing.RAW_PATH):
        print("Raw data not found — generating synthetic dataset...")
        from src.generate_data import generate
        os.makedirs("data/raw", exist_ok=True)
        generate().to_csv(preprocessing.RAW_PATH, index=False)

    print("Step 1/3: Cleaning data...")
    df = preprocessing.load_and_clean()
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(preprocessing.PROCESSED_PATH, index=False)
    print(f"   -> {len(df):,} rows cleaned, saved to {preprocessing.PROCESSED_PATH}")

    os.makedirs("outputs/figures", exist_ok=True)

    print("\nStep 2/3: Running general EDA...")
    eda.run_eda(df)

    print("\nStep 3/3: Running COVID lockdown analysis...")
    covid_analysis.run_covid_analysis(df)

    print("\nAll done! Check the outputs/figures/ folder for charts.")


if __name__ == "__main__":
    main()
