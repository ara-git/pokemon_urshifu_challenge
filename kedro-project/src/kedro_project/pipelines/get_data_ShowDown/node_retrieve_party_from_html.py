import pandas as pd
import bs4
import os
import pandas as pd

def retrieve_party_from_html(htmls, poke_data_sheet_df):
    poke_name_jp_en_dict = dict(zip(poke_data_sheet_df["英語名"], poke_data_sheet_df["名前"]))

    return None