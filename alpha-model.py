import ib_insync


def generate_signal(asset_a: Asset, asset_b: Asset):

    delta = asset_a.quote - alpha - beta * asset_b.quote # TODO Model parameter ergänzen
    
    if delta < 0 and delta < threshold:
        output_signal = {asset_b.symbol : "BUY",
                         asset_a.symbol : "SELL"}

    else:
        output_signal = {asset_b.symbol : "BUY",
                         asset_a.symbol : "SELL"}

    print("Signal updated")
