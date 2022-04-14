import pandas as pd

def merge_raw_data(dark_urshifu_data, water_urshifu_data, dark_urshifu_data_sd, water_urshifu_data_sd):
    """
    悪、水ウーラオスのデータを結合する
    showdownのデータとぽけっとふぁんくしょんのデータを使う
    """
    dark_urshifu_data = dark_urshifu_data[["p1", "p2", "p3", "p4", "p5", "p6"]]
    water_urshifu_data = water_urshifu_data[["p1", "p2", "p3", "p4", "p5", "p6"]]
    merged_df = pd.concat([dark_urshifu_data, water_urshifu_data, dark_urshifu_data_sd, water_urshifu_data_sd])
    return merged_df