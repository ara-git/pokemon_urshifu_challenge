"""
streamlit appのためのファイル
"""
import pandas as pd
import streamlit as st
import warnings
import pickle
import os
from keras.models import load_model

# 強引に上位ディレクトリ内のモジュールをインポートする
import sys
sys.path.append('kedro_project/src/kedro_project/pipelines/preprocess')
import node_make_used_pokemon_feature
import node_make_used_type_feature
import node_make_opponent_advantage_feature

warnings.simplefilter("ignore")

# 学習済みモデルを読み込む
model_gmbt = pickle.load(open('./kedro_project/data/06_models/trained_model_gbdt.pkl', 'rb'))
model_cnn = load_model('./kedro_project/data/06_models/trained_model_cnn.h5')

# 全ポケモンの名称が入ったリストを解凍する
poke_data_sheet = pd.read_csv("./kedro_project/data/01_raw/pokemon_data_sheet.csv")
poke_name_list = [None] + list(poke_data_sheet["名前"])

# 高頻度ポケモンのリストを解凍する
frequent_pokemon_df = pd.read_csv("./kedro_project/data/02_intermediate/frequent_pokemon_list.csv")

# 仮想敵のタイプ有利度に関するdfを解凍する
opponent_compatibility_df = pd.read_csv("./kedro_project/data/02_intermediate/opponent_compatibility.csv")

# ポケモン名を入力する
input_poke_name_list = []
input_poke_name_list.append(st.sidebar.selectbox("p1", poke_name_list))
input_poke_name_list.append(st.sidebar.selectbox("p2", poke_name_list))
input_poke_name_list.append(st.sidebar.selectbox("p3", poke_name_list))
input_poke_name_list.append(st.sidebar.selectbox("p4", poke_name_list))
input_poke_name_list.append(st.sidebar.selectbox("p5", poke_name_list))

# Noneをリストから除く
input_poke_name_list = list(filter(None, input_poke_name_list))

# 重複を除く
input_poke_name_list = list(set(input_poke_name_list))

st.write(input_poke_name_list)

if len(input_poke_name_list) == 5:
    input_poke_name_list.append("ウーラオス悪")
    input_poke_name_df = pd.DataFrame(input_poke_name_list).T
    input_poke_name_df.columns = ["p1", "p2", "p3", "p4", "p5", "p6"]
    print(input_poke_name_df)

    # 特徴量を計算する
    used_pokemon_feature = node_make_used_pokemon_feature.make_used_pokemon_feature(input_poke_name_df, frequent_pokemon_df)
    used_type_feature = node_make_used_type_feature.make_used_type_feature(input_poke_name_df, poke_data_sheet)
    opponent_advantage_feature = node_make_opponent_advantage_feature.make_opponent_advantage_feature(used_type_feature, opponent_compatibility_df)
    
    st.write(used_pokemon_feature)
    st.write(used_type_feature)
    st.write(opponent_advantage_feature)