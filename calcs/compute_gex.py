CONTRACT_SIZE = 100

def compute_total_gex(spot, data):
    """Compute dealers' total GEX"""
    data["GEX_volume"] = spot * data['gamma'] * data['volume'] * CONTRACT_SIZE * spot * 0.01
    data["GEX_oi"] = spot * data['gamma'] * data['open_interest'] * CONTRACT_SIZE * spot * 0.01

    # For put option we assume negative gamma, i.e. dealers sell puts and buy calls
    data["GEX_volume"] = data.apply(lambda x: -x['GEX_volume'] if x['type'] == "P" else x['GEX_volume'], axis=1)
    data["GEX_oi"] = data.apply(lambda x: -x['GEX_oi'] if x['type'] == "P" else x['GEX_oi'], axis=1)

    gex_oi_notional = round(data['GEX_oi'].sum() / 10 ** 9, 4)
    gex_volume_notional = round(data['GEX_volume'].sum() / 10 ** 9, 4)

    return gex_oi_notional, gex_volume_notional

    