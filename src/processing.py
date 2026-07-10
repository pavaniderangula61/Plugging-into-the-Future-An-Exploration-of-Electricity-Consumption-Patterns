import pandas as pd

RAW_PATH = "data/raw/long_data_.csv"
PROCESSED_PATH = "data/processed/clean_data.csv"

LOCKDOWN_START = pd.Timestamp("2020-03-25")
LOCKDOWN_END = pd.Timestamp("2020-06-08")


def label_phase(date):
    if date < LOCKDOWN_START:
        return "Pre-Lockdown"
    elif date <= LOCKDOWN_END:
        return "Lockdown"
    else:
        return "Post-Lockdown"


def load_and_clean(path=RAW_PATH):
    df = pd.read_csv(path)

    # Basic cleaning
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.dropna(subset=["Usage"])
    df = df[df["Usage"] >= 0]
    df = df.drop_duplicates()

    # Feature engineering
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.month_name()
    df["Weekday"] = df["Date"].dt.day_name()
    df["Phase"] = df["Date"].apply(label_phase)

    df = df.sort_values(["States", "Date"]).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = load_and_clean()
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Cleaned data saved -> {PROCESSED_PATH}")
    print(f"Rows: {len(df):,}  |  States: {df['States'].nunique()}  |  Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(df.head())
