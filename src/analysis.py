"""Análise descritiva de risco e retorno do Bitcoin."""
from pathlib import Path
import pandas as pd
from src.metrics import add_market_metrics, annualized_volatility, cagr, max_drawdown

ROOT=Path(__file__).resolve().parents[1]
DATA_PATH=ROOT/"data"/"raw"/"bitcoin_daily_2017_2022.csv"

def main() -> None:
    raw=pd.read_csv(DATA_PATH)
    df=add_market_metrics(raw)
    days=(df["Date"].iloc[-1]-df["Date"].iloc[0]).days
    print("=== BITCOIN | AMOSTRA HISTÓRICA ===")
    print(f"Observações: {len(df)}")
    print(f"Período: {df['Date'].min().date()} a {df['Date'].max().date()}")
    print(f"Preço inicial: {df['Adj Close'].iloc[0]:.2f}")
    print(f"Preço final: {df['Adj Close'].iloc[-1]:.2f}")
    print(f"Retorno no período: {df['cumulative_return'].iloc[-1]:.2%}")
    print(f"CAGR: {cagr(df['Adj Close'].iloc[0],df['Adj Close'].iloc[-1],days):.2%}")
    print(f"Volatilidade anualizada: {annualized_volatility(df['daily_return']):.2%}")
    print(f"Drawdown máximo: {max_drawdown(df['Adj Close']):.2%}")
    best=df["daily_return"].idxmax()
    worst=df["daily_return"].idxmin()
    print("\n=== EXTREMOS DIÁRIOS ===")
    print("Melhor dia:",df.loc[best,"Date"].date(),f"{df.loc[best,'daily_return']:.2%}")
    print("Pior dia:",df.loc[worst,"Date"].date(),f"{df.loc[worst,'daily_return']:.2%}")
    print("\n=== RETORNO POR ANO DA AMOSTRA ===")
    yearly=df.set_index("Date")["Adj Close"].resample("YE").agg(["first","last"])
    yearly["return"]=yearly["last"]/yearly["first"]-1
    print((yearly["return"]*100).round(2).to_string())

if __name__=="__main__":
    main()
