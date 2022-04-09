from sklearn.model_selection import train_test_split

def split_data(df, selected_feature_name_df):
    # 使う特徴量を抽出する
    #selected_feature_name_list = list(selected_feature_name_df["feature name"])
    #df = df[["target"] + selected_feature_name_list]

    train, test = train_test_split(df, random_state = 0, test_size = 0.2)
    
    # 説明変数・被説明変数を定義
    train_y = train["target"]
    train_x = train[df.columns[df.columns != 'target']]
    
    test_y = test["target"]
    test_x = test[df.columns[df.columns != 'target']]

    return train_x, train_y, test_x, test_y