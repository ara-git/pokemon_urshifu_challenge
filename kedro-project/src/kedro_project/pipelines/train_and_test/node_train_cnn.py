import xgboost as xgb
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation

def train_cnn(df, param_cnn_hidden_node_num, param_cnn_epoch_num, param_cnn_batch_size):
    # 説明変数・被説明変数を定義
    y = df["target"]
    x = df[df.columns[df.columns != 'target']]

    # クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    score_list = []
    for fold_id, (train_index, test_index) in enumerate(cv.split(x, y)):
        # 学習データと検証データに分割する
        train_x = x.iloc[train_index, : ]
        test_x = x.iloc[test_index, : ]
        train_y = y.iloc[train_index]
        test_y = y.iloc[test_index]
        
        # モデルの作成
        model = Sequential()
        model.add(Dense(param_cnn_hidden_node_num, input_dim=len(train_x.columns)))    # 入力層2ノード, 隠れ層に3ノード, 全結合
        model.add(Activation("sigmoid"))    # 活性化関数はsigmoid
        model.add(Dense(1)) # 出力層2ノード,全結合
        model.add(Activation("sigmoid"))

        model.compile(loss="binary_crossentropy",   # 誤差関数
                optimizer="adam",     # 最適化手法
                metrics=['accuracy'])

        # 訓練
        model.fit(train_x, train_y, epochs=param_cnn_epoch_num, batch_size=param_cnn_batch_size, verbose=0) # 学習

        """
        plt.plot(history.epoch, history.history["accuracy"], label="acc")
        plt.plot(history.epoch, history.history["loss"], label="loss")
        plt.xlabel("epoch")
        plt.legend()
        plt.show()
        """

        # 評価
        score = model.evaluate(test_x, test_y, verbose=1)[1]
        score_list.append(score)

    # 平均スコアを計算する
    score_list = np.array(score_list)
    average_score = np.average(score_list)
    print("cnn_score:", average_score)

    return pd.DataFrame([average_score], columns = ["score"])