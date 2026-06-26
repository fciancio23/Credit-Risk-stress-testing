import pandas as pd
df = pd.read_csv("C:/Users/KJ9115/Desktop/Restaurant/Candidature/Portfolio/Credit Risk Project/data/processed/companies_market_metrics.csv")

#Hypotesis of recession scenario

sector_shock = {"Consumer Cyclical": 0.30,
    "Technology": 0.25,
    "Industrials": 0.20,
    "Real Estate": 0.20,
    "Energy": 0.15,
    "Consumer Defensive": 0.10,
    "Utilities": 0.10,
    "Healthcare": 0.10}

df["sector_shock"] = df["Sector"].map(sector_shock)

#Stressed statistics:
df["Stress_EBITDA"] = (df["EBITDA"] * (1 - df["sector_shock"]))
df["Stress_Debt_to_EBITDA"] = (df["TotalDebt"] / df["Stress_EBITDA"]) #Stressed Leverage
df["Debt_EBITDA_change"] = (df["Stress_Debt_to_EBITDA"] - df["Debt_to_EBITDA"]) #Deterioration

#Top stressed companies

stress_ranking = (df.sort_values(by="Debt_EBITDA_change", ascending=False))
print("\nTop 10 stressed companies:\n")
print(stress_ranking[
    [
        "Company",
        "Sector",
        "Debt_to_EBITDA",
        "Stress_Debt_to_EBITDA",
        "Debt_EBITDA_change",
    ]
      ].head(10))

#Sector analysis

sector_stress = (
    df.groupby("Sector")
    [
        [
            "Debt_to_EBITDA",
            "Stress_Debt_to_EBITDA"
        ]
    ].mean())

sector_stress["Increase"] = (sector_stress["Stress_Debt_to_EBITDA"] - sector_stress["Debt_to_EBITDA"])
print("\nSector stress result:\n")
print(
    sector_stress.sort_values(
        by="Increase",
        ascending=False))

#Export dataset

output_path = ("C:/Users/KJ9115/Desktop/Restaurant/Candidature/Portfolio/Credit Risk Project/data/processed/companies_final_df.csv")

df.to_csv(output_path, index=False)
print("\nStress test completed successfully.")
print(f"Number of companies: {len(df)}")
