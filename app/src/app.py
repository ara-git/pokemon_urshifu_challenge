"""
streamlit appのためのファイル
"""
import pandas as pd
import streamlit as st
import warnings
import pickle
from keras.models import load_model
import yaml


# 強引に上位ディレクトリ内のモジュールをインポートする
import sys
sys.path.append('kedro_project/src/kedro_project/pipelines/preprocess')
import node_make_used_pokemon_feature
import node_make_used_type_feature
import node_make_opponent_advantage_feature
import node_merge_features

warnings.simplefilter("ignore")

# タイトル
st.title("ウーラオスの型判別AI")

# 学習済みモデルを読み込む
model_gbdt = pickle.load(open('./kedro_project/data/06_models/trained_model_gbdt.pkl', 'rb'))
model_cnn = load_model('./kedro_project/data/06_models/trained_model_cnn.h5')
model_logistic = pickle.load(open('./kedro_project/data/06_models/trained_model_logistic.pkl', 'rb'))

# csv, yamlファイルを複数読み込む
## 全ポケモンの名称が入ったリストを解凍する
poke_data_sheet = pd.read_csv("./kedro_project/data/01_raw/pokemon_data_sheet.csv")
poke_name_list = [None] + list(poke_data_sheet["名前"])

## 高頻度ポケモンのリストを解凍する
frequent_pokemon_df = pd.read_csv("./kedro_project/data/02_intermediate/frequent_pokemon_list.csv")

## 仮想敵のタイプ有利度に関するdfを解凍する
opponent_compatibility_df = pd.read_csv("./kedro_project/data/02_intermediate/opponent_compatibility.csv")

## パラメータに関するymlファイルを解凍する
with open('kedro_project/conf/base/parameters.yml', 'r', encoding= "utf-8") as yml:
    parameters = yaml.safe_load(yml)

## 使用する特徴量のリストを解凍する
selected_feature_name_df = pd.read_csv("./kedro_project/data/01_raw/selected_features_name.csv")

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

if len(input_poke_name_list) == 5:
    """
    入力したポケモンの数が５体の時のみ実行する
    """
    # 一時敵に"悪ウーラオス"をリストに追加する
    input_poke_name_list.append("ウーラオス悪")
    input_poke_name_df = pd.DataFrame(input_poke_name_list).T
    input_poke_name_df.columns = ["p1", "p2", "p3", "p4", "p5", "p6"]

    # 特徴量を計算する
    used_pokemon_feature = node_make_used_pokemon_feature.make_used_pokemon_feature(input_poke_name_df, frequent_pokemon_df)
    type_frequency_feature = node_make_used_type_feature.make_used_type_feature(input_poke_name_df, poke_data_sheet)
    opponent_advantage_feature = node_make_opponent_advantage_feature.make_opponent_advantage_feature(type_frequency_feature, opponent_compatibility_df)
    
    """
    st.write(used_pokemon_feature)
    st.write(type_frequency_feature)
    st.write(opponent_advantage_feature)
    """

    #特徴量を結合し、"target"列だけ抜く
    merged_features = node_merge_features.merge_features(used_pokemon_feature, type_frequency_feature, opponent_advantage_feature, selected_feature_name_df, parameters)
    x = merged_features[merged_features.columns[merged_features.columns != "target"]]
    
    # 予測を行う
    prediction_result_list = []

    ## gbdt
    pred_y_gbdt = model_gbdt.predict(x)
    prediction_result_list.append(round(pred_y_gbdt))
    
    ## cnn
    pred_y_cnn = model_cnn.predict(x)
    prediction_result_list.append(round(float(pred_y_cnn)))
    
    ## logistic
    pred_y_logistic = model_logistic.predict(x)
    prediction_result_list.append(round(pred_y_logistic))

    # 結果をまとめ、予測結果を出力する
    prediction_result_df = pd.DataFrame(prediction_result_list).T
    prediction_result_df.columns=["gbdt", "cnn", "logistic"]
    prediction_result_df = prediction_result_df.replace({0: "水ウーラオス", 1: "悪ウーラオス"})
    
    st.write("ジャッジ１(light GBM gbdt)：", str(prediction_result_df["gbdt"][0]))
    st.write("ジャッジ２(keras cnn)：", str(prediction_result_df["cnn"][0]))
    st.write("ジャッジ３(sklearn logistic)：", str(prediction_result_df["logistic"][0]))


else:
    st.write("左のバーにウーラオス以外のポケモン（５体）を入力してください。")