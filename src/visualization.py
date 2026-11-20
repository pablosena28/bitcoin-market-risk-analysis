"""Geração das visualizações refinadas do projeto."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "bitcoin_daily_2017_2022.csv"
FIGURES = ROOT / "reports" / "figures"

PLOT_BG = "#e7eff8"
TEXT = "#0b2a4a"
GRID = "#ffffff"


def _base_ax(title: str, subtitle: str = ""):
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor(PLOT_BG)
    ax.grid(True, color=GRID, linewidth=1)
    ax.set_title(title, loc="left", fontsize=18, color=TEXT, pad=18)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=10, color="#53677d")
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig, ax


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"]).sort_values("Date")
    df["daily_return"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = df["Adj Close"] / df["Adj Close"].iloc[0] - 1
    df["sma_30"] = df["Close"].rolling(30).mean()
    df["sma_90"] = df["Close"].rolling(90).mean()
    df["volume_sma_30"] = df["Volume"].rolling(30).mean()
    peak = df["Adj Close"].cummax()
    df["drawdown"] = df["Adj Close"] / peak - 1
    df["rolling_vol_30"] = df["daily_return"].rolling(30).std() * np.sqrt(365)

    fig, ax = _base_ax(
        "Análise do fechamento Bitcoin",
        "Fechamento diário, média móvel de 30 dias e tendência de 90 dias",
    )
    ax.plot(df["Date"], df["Close"], label="Fechamento", linewidth=1.2)
    ax.plot(df["Date"], df["sma_30"], label="Média móvel (30d)", linewidth=1.8)
    ax.plot(df["Date"], df["sma_90"], label="Tendência (90d)", linewidth=2.0)
    ax.set_ylabel("Preço de fechamento")
    ax.set_xlabel("Período histórico")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "price_trend.svg", bbox_inches="tight")
    plt.close(fig)

    fig, ax = _base_ax("Retorno acumulado do Bitcoin")
    y = df["cumulative_return"] * 100
    ax.plot(df["Date"], y, linewidth=2)
    ax.fill_between(df["Date"], 0, y, alpha=0.18)
    ax.set_ylabel("Retorno acumulado (%)")
    fig.tight_layout()
    fig.savefig(FIGURES / "cumulative_return.svg", bbox_inches="tight")
    plt.close(fig)

    fig, ax = _base_ax("Drawdown do Bitcoin")
    y = df["drawdown"] * 100
    ax.plot(df["Date"], y, linewidth=1.8)
    ax.fill_between(df["Date"], 0, y, alpha=0.20)
    ax.set_ylabel("Drawdown (%)")
    fig.tight_layout()
    fig.savefig(FIGURES / "drawdown.svg", bbox_inches="tight")
    plt.close(fig)

    fig, ax = _base_ax("Volatilidade móvel do Bitcoin", "Janela de 30 dias, anualizada com √365")
    ax.plot(df["Date"], df["rolling_vol_30"] * 100, linewidth=1.8)
    ax.set_ylabel("Volatilidade anualizada (%)")
    fig.tight_layout()
    fig.savefig(FIGURES / "rolling_volatility_30d.svg", bbox_inches="tight")
    plt.close(fig)

    fig, ax = _base_ax("Volume diário do Bitcoin")
    ax.plot(df["Date"], df["Volume"] / 1e9, alpha=0.45, label="Volume diário")
    ax.plot(df["Date"], df["volume_sma_30"] / 1e9, linewidth=2, label="Média móvel (30d)")
    ax.set_ylabel("Volume (bilhões)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "volume.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
