from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import EarlyStopping

def train_cnn(train_x, train_y, test_x, test_y, param_cnn_hidden_node_num, param_cnn_epoch_num, param_cnn_batch_size):
    # クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    score_list = []

    for fold_id, (train_index, valid_index) in enumerate(cv.split(train_x, train_y)):
        # 学習データと検証データに分割する
        train_cv_x = train_x.iloc[train_index, : ]
        valid_x = train_x.iloc[valid_index, : ]
        train_cv_y = train_y.iloc[train_index]
        valid_y = train_y.iloc[valid_index]
    
        
        # モデルの作成
        model = Sequential()
        model.add(Dense(param_cnn_hidden_node_num, input_dim=len(train_x.columns)))    # 入力層2ノード, 隠れ層に3ノード, 全結合
        model.add(Activation("sigmoid"))    # 活性化関数はsigmoid
        model.add(Dense(1)) # 出力層2ノード,全結合
        model.add(Activation("sigmoid"))

        model.compile(loss="binary_crossentropy",   # 誤差関数
                optimizer="adam",     # 最適化手法
                metrics=['accuracy'])

        # EaelyStoppingの設定
        early_stopping =  EarlyStopping(
                                    monitor='val_loss',
                                    min_delta=0.0,
                                    patience=2,
        )

        # 訓練
        model.fit(
            train_cv_x,
            train_cv_y,
            epochs=param_cnn_epoch_num,
            batch_size=param_cnn_batch_size,
            validation_data=[valid_x, valid_y],
            callbacks=[early_stopping],
            verbose=0) # 学習

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