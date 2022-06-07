import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime, timedelta

# Set plot style
plt.style.use("seaborn-dark")
for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
    plt.rcParams[param] = "#212946"
for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
    plt.rcParams[param] = "0.9"


def print_gex_surface(ticker, spot, data):
    """Plot 3D surface"""
    # Limit data to 1 year and +- 15% from ATM
    selected_date = datetime.today() + timedelta(days=365)
    limit_criteria = (
            (data.expiration < selected_date)
            & (data.strike > spot * 0.85)
            & (data.strike < spot * 1.15)
    )
    data = data.loc[limit_criteria]

    # Compute GEX by expiration and strike
    data = data.groupby(["expiration", "strike"])["GEX"].sum() / 10 ** 6
    data = data.reset_index()

    # Plot 3D surface
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(
        data["strike"],
        dates.date2num(data["expiration"]),
        data["GEX"],
        cmap="seismic_r",
    )
    ax.yaxis.set_major_formatter(dates.AutoDateFormatter(ax.xaxis.get_major_locator()))
    ax.set_ylabel("Expiration date", fontweight="heavy")
    ax.set_xlabel("Strike Price", fontweight="heavy")
    ax.set_zlabel("Gamma (M$ / %)", fontweight="heavy")
    plt.title(f"{ticker} GEX Surface", fontweight="heavy")
    plt.legend()
    plt.savefig(f"img/{ticker}_gex_surface.png", bbox_inches='tight')
    plt.show()