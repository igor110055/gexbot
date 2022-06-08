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
    low_gamma = data.loc[(data['strike'] >= spot - 20) & (data['strike'] <= spot + 20)].copy()
    if ticker == '_SPX':
        low_gamma['mean_volume'] = low_gamma['GEX_volume'].rolling(10).mean()
        n = low_gamma.shape[0]
        mid = int(n / 2)
        flip_idx = np.where(np.diff(np.sign(low_gamma['mean_volume'].iloc[mid-10:mid+10])))[0]
        flip_strike = low_gamma['strike'].values[flip_idx[0]]

    if ticker == 'SPY':
        low_gamma = data.loc[(data['strike'] >= spot - 5) & (data['strike'] <= spot + 5)].copy()
        low_gamma['mean_volume'] = low_gamma['GEX_volume'].rolling(3).mean()
        n = low_gamma.shape[0]
        mid = int(n / 2)
        flip_idx = np.where(np.diff(np.sign(low_gamma['mean_volume'].iloc[mid-2:mid+2])))[0]
        flip_strike_SPY = low_gamma['strike'].values[flip_idx[0]]

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
        

    plt.grid(axis="x", color="#2A3459")
    plt.xticks(fontweight="heavy")
    plt.xticks(xticks)
    plt.xticks(rotation=70)

    ax = plt.gca()
    for i,(g,tick) in enumerate(zip(xticks, ax.get_xticklabels())):
        if ticker == 'SPX' and g <= flip_strike:
            tick.set_ha('left')
            tick.set_va('bottom')
            tick.set_position((i, 0.05))
        elif ticker == 'SPX' and g > flip_strike:
            tick.set_ha('right')
            tick.set_va('top')
            tick.set_position((i, -0.05))
        elif ticker == 'SPY' and g <= flip_strike_SPY:
            tick.set_ha('left')
            tick.set_va('bottom')
            tick.set_position((i, 0.05))
        elif ticker == 'SPY' and g > flip_strike_SPY:
            tick.set_ha('right')
            tick.set_va('top')
            tick.set_position((i, -0.05))
        tick.set_rotation_mode('anchor')
        tick.set_transform(ax.transData)

    for (i, axis) in enumerate(ax.get_xgridlines()):
        if i % 2 == 0:
            axis.set_color("#252e50")

    plt.yticks(fontweight="heavy")
    plt.xlabel("Strike", fontweight="heavy", labelpad=8)
    plt.ylabel("Gamma Exposure (Bn$ / %)", fontweight="heavy")
    plt.title(f"{ticker} GEX by Strike", fontweight="heavy")
    plt.legend()
    plt.figtext(
        0.15,
        0.8,
        f"Spot Price: ${spot}\nGEX Notional by OI: ${gex_oi} Bn\nGEX Notional by Volume: ${gex_volume} Bn\nUpdated as of {timestamp.month}/{timestamp.day} {timestamp.hour}:{timestamp.minute}:{timestamp.second} EST")
    plt.savefig(f"img/{ticker}_gex_by_strike.png", bbox_inches='tight', dpi=800)
    plt.close(fig)
