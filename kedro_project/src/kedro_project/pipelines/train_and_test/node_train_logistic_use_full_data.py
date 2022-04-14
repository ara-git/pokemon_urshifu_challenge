"""
ロジスティック回帰で学習する
"""
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train_logistic_full_data(df):
    # 説明変数・被説明変数を定義
    y = df["target"]
    x = df[df.columns[df.columns != 'target']]

    # 学習データと検証データに分割する(ホールドアウト法)
    train_x, valid_x, train_y, valid_y = train_test_split(x, y,                # 訓練データとテストデータに分割する
                                                        test_size = 0.2,       # テストデータの割合
                                                        shuffle=True,        # シャッフルする
                                                        random_state=0) 

    model = LogisticRegression(verbose=0)

    # 学習
    model.fit(train_x, train_y)

    # 学習済みモデルをpickleファイルで保存する
    file = "data/06_models/trained_model_logistic.pkl"
    pickle.dump(model, open(file, "wb"))

    return None