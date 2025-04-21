import datetime
import pandas as pd


def train_test_split(df: pd.DataFrame, cut_off_date, target_col_name: str):
    train = df.loc[df['pickup_hour'] < cut_off_date]
    test = df.loc[df['pickup_hour'] >= cut_off_date]

    X_train = train.drop(target_col_name, axis=1)
    y_train = train[target_col_name]

    X_test = test.drop(target_col_name, axis=1)
    y_test = test[target_col_name]

    return X_train, y_train, X_test, y_test