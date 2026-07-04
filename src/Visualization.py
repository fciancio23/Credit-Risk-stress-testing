import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Load dataset

df = pd.read_csv(".../Credit Risk Project/data/processed/companies_final_df.csv")
#output_path --> replace "..." with personal path

#Medians calculation

median_vol = df["Volatility_1Y"].median()
median_debt = df["Debt_to_EBITDA"].median()

# <editor-fold desc="First figure">
#1. Risk Matrix

sns.set_style("whitegrid")

plt.figure(figsize=(12,8))

sns.scatterplot(data = df, x = "Volatility_1Y", y = "Debt_to_EBITDA",
                hue = "Sector", palette = "tab10", s=80, edgecolor="black", alpha=0.85)

plt.axvline(median_vol, linestyle="--")
plt.axhline(median_debt, linestyle="--")

plt.yscale("log") #Puma case

#Highlight main Debt/EBITDA - Volatility
outliers = ["Puma", "Prosus", "Kering",
            "Nokia", "ASML",
            "RWE"]

for _, row in df.iterrows():
 if row["Company"] in outliers:

  plt.annotate(row["Company"],
               (row["Volatility_1Y"],row["Debt_to_EBITDA"])
               )

plt.title("Risk Matrix: Financial Risk vs Market Risk")
plt.xlabel("Annual Volatility (1Y)")
plt.ylabel("Debt / EBITDA (log scale)")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(".../Credit Risk Project/Outputs/figure/risk_matrix.png",
            dpi=300,
            bbox_inches="tight")
#replace "..." with personal path
plt.show()
# </editor-fold>

# <editor-fold desc="second figure">
#2. Average Debt/EBITDA by sector

sector_debt = (df.groupby("Sector")["Debt_to_EBITDA"]
               .median()
               .sort_values(ascending=False))
sector_count = (df.groupby("Sector").size())
labels = [f"{sector}\n(n={sector_count[sector]})"
          for sector in sector_debt.index]

sns.set_style("whitegrid")

plt.figure(figsize=(14,8))
ax = sns.barplot(
    x = sector_debt.index,
    y = sector_debt.values
)

for i, value in enumerate(sector_debt.values):

    ax.text(
        i,
        value,
        f"{value:.1f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
    )
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels)

plt.title("Sector financial risk profile", fontsize=16)
plt.xlabel("Sector")
plt.ylabel("Debt / EBITDA")
plt.tight_layout()
plt.savefig(".../Credit Risk Project/Outputs/figure/Sector_risk.png",
            dpi=300,
            bbox_inches="tight")
#replace "..." with personal path
plt.show()
# </editor-fold>

# <editor-fold desc="Table">
#3. Top 10 stressed companies

top10 = (
    df.sort_values(
        by="Debt_EBITDA_change",
        ascending=False
    )
    .head(10)
    .copy()
)

top10.insert(
    0,
    "Rank",
    range(1, len(top10) + 1)
)

top10_table = top10[
    [
        "Rank",
        "Company",
        "Sector",
        "Debt_to_EBITDA",
        "Stress_Debt_to_EBITDA",
        "Debt_EBITDA_change"
    ]
]

top10_table[
    [
        "Debt_to_EBITDA",
        "Stress_Debt_to_EBITDA",
        "Debt_EBITDA_change"
    ]
] = top10_table[
    [
        "Debt_to_EBITDA",
        "Stress_Debt_to_EBITDA",
        "Debt_EBITDA_change"
    ]
].round(2)

print("\nTop 10 stress test table:")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(top10_table)

top10_table.to_csv(".../Credit Risk Project/Outputs/table/Top_10_stressed_companies.csv",
                   index=False)
#replace "..." with personal path
# </editor-fold>
