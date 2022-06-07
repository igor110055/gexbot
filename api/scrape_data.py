import requests
import pandas as pd

def scrape_data(ticker):
    """
    scrapes cboe website
    saves option data as df to hdf file
    """
    data = requests.get(
        f"https://cdn.cboe.com/api/global/delayed_quotes/options/{ticker}.json"
    )
    data = pd.DataFrame.from_dict(data.json())
    spot_price = data.loc["current_price", "data"]
    timestamp = pd.to_datetime(data["timestamp"].iloc[0]).tz_localize('UTC').tz_convert("US/Eastern")
    option_data = pd.DataFrame(data.loc["options", "data"])
    df = fix_option_data(option_data)

    return spot_price, df, timestamp

def fix_option_data(data):
    """
    Fix option data columns.

    From the name of the option derive type of option, expiration and strike price
    """
    data["type"] = data.option.str.extract(r"\d([A-Z])\d")
    data["strike"] = data.option.str.extract(r"\d[A-Z](\d+)\d\d\d").astype(int)
    data["expiration"] = data.option.str.extract(r"[A-Z](\d+)").astype(str)
    # Convert expiration to datetime format
    data["expiration"] = pd.to_datetime(data["expiration"], format="%y%m%d")
    return data