import xgboost as xgb
from sklearn.model_selection import cross_validate,cross_val_predict, StratifiedKFold
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Activation

def train_cnn(train_x, train_y,test_x, test_y):
    # モデルの作成
    model = Sequential()
    model.add(Dense(3, input_dim=len(train_x.columns)))    # 入力層2ノード, 隠れ層に3ノード, 全結合
    model.add(Activation("sigmoid"))    # 活性化関数はsigmoid
    model.add(Dense(1)) # 出力層2ノード,全結合
    model.add(Activation("sigmoid"))

    model.compile(loss="binary_crossentropy",   # 誤差関数
              optimizer="adam",     # 最適化手法
              metrics=['accuracy'])

    # 訓練
    history = model.fit(train_x, train_y, epochs=200, batch_size=32) # 学習

    plt.plot(history.epoch, history.history["accuracy"], label="acc")
    plt.plot(history.epoch, history.history["loss"], label="loss")
    plt.xlabel("epoch")
    plt.legend()
    plt.show()
    
    # 評価
    score = model.evaluate(test_x, test_y, verbose=1)

    # print("Test score", score[0])
    print("Test accuracy", score[1])

    return pd.DataFrame(["Test accuracy", score[1]])

def train_logistic(train_x, train_y,test_x, test_y):
    """
    ロジスティック回帰で学習する
    """
    model = LogisticRegression()
    model.fit(train_x, train_y)

    pred_y = model.predict(test_x)
    print('logistic_score:', accuracy_score(test_y, pred_y))

    return pd.DataFrame(['logistic_score:', accuracy_score(test_y, pred_y)])

def train_GBDT(train_x, train_y,test_x, test_y):
    # ハイパーパラメータを指定して学習実行
    train_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'learning_rate': 0.01,
        'max_depth': 4,
        'n_estimators': 60,
        'colsample_bytree': 0.6
    }
    clf = xgb.XGBClassifier(**train_params)

    clf.fit(train_x, train_y, eval_set=[[test_x, test_y]])

    model = xgb.XGBClassifier(n_estimators=20, random_state=71)
    model.fit(train_x, train_y)
    
    # 出力(1): 検証用データに対する精度を確認
    booster = clf.get_booster()
    dtest = xgb.DMatrix(test_x, label=test_y)
    y_test_pred_prob = booster.predict(dtest)
    y_test_pred = np.where(y_test_pred_prob > 0.5, 1, 0)
    acc = sklearn.metrics.accuracy_score(test_y, y_test_pred)

    print("GBDT_score", acc)

    """
    # 出力(2): 特徴量の重要度を描画
    _, ax = plt.subplots(figsize=(12, 12))
    xgb.plot_importance(booster,
                        ax=ax,
                        importance_type='gain',
                        show_values=False)
    
    # plt.show()
    """
    return pd.DataFrame(["GBDT_score", acc])