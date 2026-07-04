import pandas as pd

#Load dataset
df = pd.read_csv(".../Credit Risk Project/data/raw/european_companies.csv")
#output_path --> replace "..." with personal path

#Financial risk metrics

df["Debt_to_EBITDA"] = (df["TotalDebt"] / df["EBITDA"])
df["EBITDA_Margin"] = (df["EBITDA"] / df["Revenue"])
df["Debt_to_Revenue"] = (df["TotalDebt"] / df["Revenue"])

#Summary statistics

print(df[
    [
        "Debt_to_EBITDA",
        "EBITDA_Margin",
        "Debt_to_Revenue",
    ]
      ].describe())

#Export dataset

output_path = (".../Credit Risk Project/data/processed/companies_risk_metrics.csv")
#output_path --> replace "..." with personal path
df.to_csv(output_path, index=False)
print("\nRisk metrics calculated successfully.")
print(f"Number of companies: {len(df)}")