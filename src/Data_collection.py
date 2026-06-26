import yfinance as yf
import pandas as pd

tickers = ["SHEL", "BP", "TTE.PA", "ENI.MI", "IBE.MC", "ENEL.MI", "ENGI.PA", "RWE.DE",
    "SIE.DE", "SU.PA", "SAF.PA", "VOW3.DE", "BMW.DE", "MBG.DE", "STLA.MI",
    "VOLV-B.ST", "RR.L", "ABB",
    "NESN.SW", "ULVR.L", "OR.PA", "DANO.PA", "DGE.L", "HEIA.AS",
    "ADS.DE", "PUM.DE", "EL.PA", "KER.PA",
    "ASML.AS", "SAP.DE", "STM.PA", "NOKIA.HE", "ERIC-B.ST", "PRX.AS",
    "VNA.DE", "LEG.DE"]

data = []
for ticker in tickers:

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        company_data = {
            "Ticker": ticker,
            "Company": info.get("shortName"),
            "Sector": info.get("sector"),
            "Country": info.get("country"),
            "MarketCap": info.get("marketCap"),
            "TotalDebt": info.get("totalDebt"),
            "Revenue": info.get("totalRevenue"),
            "EBITDA": info.get("ebitda")
        }

        data.append(company_data)

        print(f"downloaded: {ticker}")

    except Exception as e:
        print(f"Error with {ticker}: {e}")



df = pd.DataFrame(data)

numeric_cols = [
    "MarketCap",
    "TotalDebt",
    "Revenue",
    "EBITDA"
]

df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

#Dataset clean:
    #Ent without EBITDA, Total debt, company name, ecc...

df = df.dropna(
    subset=[
        "Company",
        "MarketCap",
        "Revenue",
        "EBITDA"
    ]
)

#Saving dataset
output_path = "C:/Users/KJ9115/Desktop/Restaurant/Candidature/Portfolio/Credit Risk Project/data/raw/european_companies.csv"
#output_path = "...data/raw/european_companies.csv" ---> replace "..." with personal path
df.to_csv(output_path, index=False)

print("\nDataset salvato correttamente")
print(df.head())
print(len(df))