import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")
FIG_DIR = "outputs/figures"


def phase_comparison(df):
    phase_avg = df.groupby(["Regions", "Phase"])["Usage"].mean().unstack()
    phase_avg = phase_avg[["Pre-Lockdown", "Lockdown", "Post-Lockdown"]]
    print("\n--- Average Usage by Region & Lockdown Phase (MU) ---")
    print(phase_avg.round(1))
    return phase_avg


def percent_change_lockdown(df):
    pre = df[df["Phase"] == "Pre-Lockdown"].groupby("States")["Usage"].mean()
    during = df[df["Phase"] == "Lockdown"].groupby("States")["Usage"].mean()
    pct = ((during - pre) / pre * 100).sort_values()
    print("\n--- % Change in Usage: Pre-Lockdown -> Lockdown ---")
    print(pct.round(1))
    return pct


def plot_phase_comparison(phase_avg):
    phase_avg.plot(kind="bar", figsize=(12, 6), colormap="coolwarm")
    plt.title("Average Electricity Usage by Region: Lockdown Phases")
    plt.ylabel("Average Usage (MU)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/05_phase_comparison.png", dpi=150)
    plt.close()


def plot_percent_change(pct):
    plt.figure(figsize=(9, 10))
    colors = ["#d62728" if v < 0 else "#2ca02c" for v in pct.values]
    plt.barh(pct.index, pct.values, color=colors)
    plt.title("% Change in Electricity Usage (Pre-Lockdown -> Lockdown)")
    plt.xlabel("% Change")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/06_percent_change_by_state.png", dpi=150)
    plt.close()


def plot_lockdown_zoom(df):
    zoom = df[(df["Date"] >= "2020-02-01") & (df["Date"] <= "2020-07-15")]
    daily = zoom.groupby("Date")["Usage"].sum().reset_index()
    plt.figure(figsize=(14, 5))
    plt.plot(daily["Date"], daily["Usage"], color="#333")
    plt.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-06-08"),
                color="red", alpha=0.15, label="Lockdown Period")
    plt.title("National Electricity Usage: Zoomed on Lockdown Period")
    plt.xlabel("Date")
    plt.ylabel("Usage (MU)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/07_lockdown_zoom.png", dpi=150)
    plt.close()


def run_covid_analysis(df):
    phase_avg = phase_comparison(df)
    pct = percent_change_lockdown(df)
    plot_phase_comparison(phase_avg)
    plot_percent_change(pct)
    plot_lockdown_zoom(df)
    print(f"\nFigures saved in {FIG_DIR}/")


if __name__ == "__main__":
    df = pd.read_csv("data/processed/clean_data.csv", parse_dates=["Date"])
    run_covid_analysis(df)
