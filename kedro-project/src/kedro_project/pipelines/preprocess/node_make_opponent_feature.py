import pandas as pd
import numpy as np

def make_make_opponent_features(type_features_df, opponent_compatibility):
    """
    仮想敵（上位ポケモン）に対する有利度合いを計算する。
    具体的には、攻めのタイプ相性を計算する。
    """
