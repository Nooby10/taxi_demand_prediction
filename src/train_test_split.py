import pandas as pd, numpy as np


def train_test_split(data: pd.DataFrame, cutoff_percent: int, target_col_name: str ):

    cutoff_ratio = round(len(data) * (cutoff_percent/100))
    training_data = data.iloc[:cutoff_ratio]
    test_data = data.iloc[cutoff_ratio:]

    X_train = training_data.drop(target_col_name, axis=1)
    y_train = training_data[target_col_name]

    X_test = test_data.drop(target_col_name, axis=1)
    y_test = test_data[target_col_name]
    
    
    return X_train, y_train, X_test, y_test
