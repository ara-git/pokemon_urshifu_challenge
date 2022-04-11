import pandas as pd

def merge_raw_data(dark_urshifu_data, water_urshifu_data, dark_urshifu_data_sd, water_urshifu_data_sd):
    """
    悪、水ウーラオスのデータを結合する
    showdownのデータとぽけっとふぁんくしょんのデータを使う
    """
    merged_df = pd.concat([dark_urshifu_data, water_urshifu_data, dark_urshifu_data_sd, water_urshifu_data_sd])
    return merged_df