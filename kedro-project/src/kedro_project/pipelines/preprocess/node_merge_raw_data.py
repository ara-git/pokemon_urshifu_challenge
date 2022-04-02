import pandas as pd

def merge_raw_data(dark_urshifu_data, water_urshifu_data):
    """
    悪、水ウーラオスのデータを結合する
    """
    merged_df = pd.concat([dark_urshifu_data, water_urshifu_data])
    return merged_df