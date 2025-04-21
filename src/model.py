import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
import lightgbm as lgbm


def average_rides_last_4_weeks(X: pd.DataFrame):
        

        X['avg_rides_last_4_weeks'] = 0.25 * (
        X[f'rides_in_past_{24*7}_hours'] +
        X[f'rides_in_past_{2*24*7}_hours']+
        X[f'rides_in_past_{3*24*7}_hours']+
        X[f'rides_in_past_{4*24*7}_hours'])
        return X

def temporal_features_engineer(X: pd.DataFrame):

    X['hour_of_day'] = X['pickup_hour'].dt.hour
    X['day_of_week'] = X['pickup_hour'].dt.day_of_week

    return X.drop(['location_id','pickup_hour'],axis=1)

def get_pipeline(hyperparameters):

    add_feature_average_rides_last_4_weeks = FunctionTransformer(average_rides_last_4_weeks,validate=False)
    add_feature_temporal_features_engineer = FunctionTransformer(temporal_features_engineer, validate=False)


    return make_pipeline(
         add_feature_average_rides_last_4_weeks,
         add_feature_temporal_features_engineer,
         lgbm.LGBMRegressor(**hyperparameters)
    )