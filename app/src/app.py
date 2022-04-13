"""
streamlit appのためのファイル
"""
import pandas as pd
import streamlit as st
import warnings
import pickle
import os
from keras.models import load_model

warnings.simplefilter("ignore")

# 学習済みモデルを読み込む
model_gmbt = pickle.load(open('./kedro-project/data/06_models/trained_model_gbdt.pkl', 'rb'))
model_cnn = load_model('./kedro-project/data/06_models/trained_model_cnn.h5')

# 全ポケモンの名称が入ったリストを解凍する
poke_data_sheet = pd.read_csv("./kedro-project/data/01_raw/pokemon_data_sheet.csv")
poke_name_list = [None] + list(poke_data_sheet["名前"])

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