import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

# Set plot style
plt.style.use("seaborn-dark")
for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
    plt.rcParams[param] = "#212946"
for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
    plt.rcParams[param] = "0.9"

def compute_gex_by_strike(ticker, spot, data, gex_oi, gex_volume, timestamp):
    """Compute and plot GEX by strike"""
    # Compute total GEX by strike
    gex_oi_by_strike = data.groupby("strike")["GEX_oi"].sum() / 10 ** 9
    gex_vol_by_strike = data.groupby("strike")["GEX_volume"].sum() / 10 ** 9

    # Limit data to +- 25% from spot price
    limit_criteria = (gex_oi_by_strike.index > spot * 0.75) & (gex_oi_by_strike.index < spot * 1.25)
    limit_criteria = (gex_vol_by_strike.index > spot * 0.75) & (gex_vol_by_strike.index < spot * 1.25)

    fig = plt.figure(figsize=(12.0, 7.0))
    if ticker == '_SPX':
        width_oi = 4
        width_vol = 3
    else:
        width_oi = 1
        width_vol = 0.8
    # Plot GEX by strike
    plt.bar(
        gex_oi_by_strike.loc[limit_criteria].index,
        gex_oi_by_strike.loc[limit_criteria],
        width=width_oi,
        color="#021ffa",
        alpha=0.8,
        label="GEX by OI"
    )
    plt.bar(
        gex_vol_by_strike.loc[limit_criteria].index,
        gex_vol_by_strike.loc[limit_criteria],
        width=width_vol,
        color="#ff00f2",
        alpha=0.8,
        label="GEX by Volume"
    )
    if ticker == "_SPX":
        ticker = "SPX"
        bottom = gex_oi_by_strike.loc[limit_criteria].index.min() - 50
        step = 25 # points
        top = gex_oi_by_strike.loc[limit_criteria].index.max() + 50

        bottom = round(bottom / 25) * 25
        top = round(top / 25) * 25

        xticks = np.arange(bottom, top, 25)
        plt.tick_params(labelsize=6.5)

    else:
        bottom = gex_oi_by_strike.loc[limit_criteria].index.min()
        step = 5 # points
        top = gex_oi_by_strike.loc[limit_criteria].index.max()

        bottom = round(bottom / 5) * 5
        top = round(top / 5) * 5

        xticks = np.arange(bottom, top, 5)
        plt.tick_params(labelsize=5)
        

    plt.grid(color="#2A3459")
    plt.xticks(fontweight="heavy")
    plt.xticks(xticks)
    plt.xticks(rotation=90)
    plt.yticks(fontweight="heavy")
    plt.xlabel("Strike", fontweight="heavy")
    plt.ylabel("Gamma Exposure (Bn$ / %)", fontweight="heavy")
    plt.title(f"{ticker} GEX by Strike", fontweight="heavy")
    plt.legend()
    plt.figtext(
        0.15,
        0.8,
        f"GEX Notional by OI: ${gex_oi} Bn\nGEX Notional by Volume: ${gex_volume} Bn\nUpdated as of {timestamp.month}/{timestamp.day} {timestamp.hour}:{timestamp.minute}:{timestamp.second} EST")
    plt.savefig(f"img/{ticker}_gex_by_strike.png", bbox_inches='tight', dpi=800)
    plt.close(fig)
