"""
light gbmを使って、gbdtモデルの二値分類を行い、計算した重みを出力する。

尚、early stoppingを実装するためにホールドアウト法でデータを分割する。
"""
import lightgbm as lgb
import pickle
from sklearn.model_selection import train_test_split

def train_gbdt_full_data(df, pram_gbdt_max_bin, pram_gbdt_num_leaves):
    # 説明変数・被説明変数を定義
    y = df["target"]
    x = df[df.columns[df.columns != 'target']]

    # 学習データと検証データに分割する(ホールドアウト法)
    train_x, test_x, train_y, test_y = train_test_split(x, y,                # 訓練データとテストデータに分割する
                                                        test_size = 0.2,       # テストデータの割合
                                                        shuffle=True,        # シャッフルする
                                                        random_state=0) 

    # 学習
    lgb_train = lgb.Dataset(train_x, train_y)
    lgb_test = lgb.Dataset(test_x, test_y, reference=lgb_train)

    params = {
        "objective": "binary",
        "max_bin": pram_gbdt_max_bin,
        "num_leaves": pram_gbdt_num_leaves
    }

    model = lgb.train(params, 
    lgb_train, 
    valid_sets=[lgb_train, lgb_test],
    verbose_eval=False,
    num_boost_round=1000, 
    early_stopping_rounds=10)

    # 学習済みモデルをpickleファイルで保存する
    file = "trained_model_gbdt.pkl"
    pickle.dump(model, open(file, "wb"))

    return None