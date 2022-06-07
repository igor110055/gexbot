import time
import pandas as pd

from api.scrape_data import scrape_data

from calcs.compute_gex import compute_total_gex
from calcs.gex_by_strike import compute_gex_by_strike


def draw_graphs(spot, option_data):
    gex_oi, gex_volume = compute_total_gex(spot, option_data)
    compute_gex_by_strike(ticker, spot, option_data, gex_oi, gex_volume)


if __name__ == "__main__":
    ticker = '_SPX'
    # ticker = 'SPY'
    spot, option_data = scrape_data(ticker)
    
    draw_graphs(spot, option_data)