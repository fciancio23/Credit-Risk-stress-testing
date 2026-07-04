import yfinance as yf
import pandas as pd
import numpy as np

#Load dataset

df = pd.read_csv(".../Credit Risk Project/data/processed/companies_risk_metrics.csv")
#output_path --> replace "..." with personal path

#Function: Max Drawdown

def calculate_max_drawdown(prices):
    running_max = prices.cummax()
    drawdowns = (prices - running_max) / running_max
    return drawdowns.min()

#List for metrics, cycle and calculation of metrics

volatility_list = []
drawdown_list = []

for ticker in df['Ticker']:

    try:

        prices = yf.download(ticker,
                             period="1y",
                             progress=False,
                             auto_adjust=True
                             )["Close"].squeeze()

        daily_returns = prices.pct_change().dropna()
        annual_volatility = daily_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(prices)

        volatility_list.append(float(annual_volatility))
        drawdown_list.append(float(max_drawdown))

        print(f"{ticker}: {annual_volatility:.4f}, {max_drawdown:.4f}")

    except Exception as e:

        print(f"{ticker}: ERROR - {e}")
        volatility_list.append(np.nan)
        drawdown_list.append(np.nan)

df["Volatility_1Y"] = volatility_list
df["Max_Drawdown_1Y"] = drawdown_list

#Summary statistics

print(df[
    [
        "Volatility_1Y",
        "Max_Drawdown_1Y",
    ]
      ].describe())

#Export dataset

output_path = (".../Credit Risk Project/data/processed/companies_market_metrics.csv")
#output_path --> replace "..." with personal path

df.to_csv(output_path, index=False)
print("\nMarket metrics calculated successfully.")
print(f"Number of companies: {len(df)}")
