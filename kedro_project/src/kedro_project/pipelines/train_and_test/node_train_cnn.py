from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import EarlyStopping
from pandas.core.common import flatten

def train_cnn(train_x, train_y, test_x, param_cnn_hidden_node_num, param_cnn_epoch_num, param_cnn_batch_size):
    # クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    pred_y_list = []
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
        # 学習記録を出力する
        plt.plot(history.epoch, history.history["accuracy"], label="acc")
        plt.plot(history.epoch, history.history["loss"], label="loss")
        plt.xlabel("epoch")
        plt.legend()
        plt.show()
        """

        """
        # 評価
        score = model.evaluate(test_x, test_y, verbose=1)[1]
        score_list.append(score)
        """
        # 予測値を計算し、リスト化して保存する
        pred_y = model.predict(test_x)
        pred_y = np.array(list(flatten(pred_y)))
        pred_y = list((pred_y > 0.5).astype(int))
        pred_y_list.append(pred_y)

    # dataframeに変更する
    pred_y_df = pd.DataFrame(pred_y_list).T
    pred_y_df.columns = ["pred"] * len(pred_y_df.columns)

    return pred_y_df