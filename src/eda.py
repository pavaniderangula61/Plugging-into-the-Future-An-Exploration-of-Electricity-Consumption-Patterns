import matplotlib
matplotlib.use("Agg")  # safe for headless environments
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")
FIG_DIR = "outputs/figures"


def summary_stats(df):
    print("\n--- Dataset Overview ---")
    print(df.describe(include="all").T)

    print("\n--- Total Usage by Region (MU) ---")
    print(df.groupby("Regions")["Usage"].sum().sort_values(ascending=False))

    print("\n--- Top 5 States by Average Daily Usage ---")
    print(df.groupby("States")["Usage"].mean().sort_values(ascending=False).head())


def plot_national_trend(df):
    daily = df.groupby("Date")["Usage"].sum().reset_index()
    plt.figure(figsize=(14, 5))
    plt.plot(daily["Date"], daily["Usage"], color="#1f77b4", linewidth=1)
    plt.title("India: Total Daily Electricity Consumption (2019-2020)")
    plt.xlabel("Date")
    plt.ylabel("Usage (MU)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/01_national_daily_trend.png", dpi=150)
    plt.close()


def plot_region_comparison(df):
    region_month = df.groupby([df["Date"].dt.to_period("M"), "Regions"])["Usage"].sum().reset_index()
    region_month["Date"] = region_month["Date"].dt.to_timestamp()
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=region_month, x="Date", y="Usage", hue="Regions", marker="o")
    plt.title("Monthly Electricity Usage by Region")
    plt.xlabel("Month")
    plt.ylabel("Usage (MU)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/02_region_monthly_comparison.png", dpi=150)
    plt.close()


def plot_top_states(df):
    top_states = df.groupby("States")["Usage"].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_states.values, y=top_states.index, hue=top_states.index, palette="viridis", legend=False)
    plt.title("Top 10 States by Average Daily Electricity Usage")
    plt.xlabel("Average Usage (MU)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/03_top10_states.png", dpi=150)
    plt.close()


def plot_weekday_pattern(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_avg = df.groupby("Weekday")["Usage"].mean().reindex(order)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=weekday_avg.index, y=weekday_avg.values, hue=weekday_avg.index, palette="mako", legend=False)
    plt.title("Average Electricity Usage by Day of Week")
    plt.ylabel("Average Usage (MU)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/04_weekday_pattern.png", dpi=150)
    plt.close()


def run_eda(df):
    summary_stats(df)
    plot_national_trend(df)
    plot_region_comparison(df)
    plot_top_states(df)
    plot_weekday_pattern(df)
    print(f"\nFigures saved in {FIG_DIR}/")


if __name__ == "__main__":
    df = pd.read_csv("data/processed/clean_data.csv", parse_dates=["Date"])
    run_eda(df)
