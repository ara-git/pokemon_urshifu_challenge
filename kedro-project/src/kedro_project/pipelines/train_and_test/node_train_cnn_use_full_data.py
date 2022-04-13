import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

def train_cnn_full_data(df, param_cnn_hidden_node_num, param_cnn_epoch_num, param_cnn_batch_size):
    # 説明変数・被説明変数を定義
    y = df["target"]
    x = df[df.columns[df.columns != 'target']]
    
    # 学習データと検証データに分割する(ホールドアウト法)
    train_x, valid_x, train_y, valid_y = train_test_split(x, y,                # 訓練データとテストデータに分割する
                                                        test_size = 0.2,       # テストデータの割合
                                                        shuffle=True,        # シャッフルする
                                                        random_state=0) 


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
        train_x,
        train_y,
        epochs=param_cnn_epoch_num,
        batch_size=param_cnn_batch_size,
        validation_data=[valid_x, valid_y],
        callbacks=[early_stopping],
        verbose=0) # 学習
    
    model.save("data/06_models/trained_model_cnn.h5")
    return None