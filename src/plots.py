import numpy as np, pandas as pd
import plotly.express as px
from typing import Optional
import datetime

def plot_one_example(
        features:pd.DataFrame, 
        targets:pd.Series, 
        example_id:int, 
        predictions:Optional[pd.Series]=None
        ):
    
    feature_ = features.iloc[example_id]
    target_ = targets.iloc[example_id]
    pickup_hour = feature_['pickup_hour']
    col_names = feature_.index
    
    rides= feature_.loc[[ride for ride in col_names if ride.startswith('rides_in_past')]]
    starting_hour = pickup_hour - datetime.timedelta(hours=len(rides))
    hours_range = pd.date_range(starting_hour, pickup_hour, freq='h')
    fig = px.line(y=rides, x=hours_range[:-1] , markers=True)
    fig.show()

def plot_one_sample(features:pd.DataFrame, 
        targets:pd.Series, 
        example_id:int, 
        predictions:Optional[pd.Series]=None):
    
     feature_ = features.iloc[example_id]
     target_ = targets.iloc[example_id]
     ts_columns = [col for col in feature_.index if col.startswith('rides_in_past')]
     ts_values = [feature_[col] for col in ts_columns] + [target_]
     ts_dates = pd.date_range(feature_['pickup_hour'] - datetime.timedelta(hours=len(ts_columns)), 
                              feature_['pickup_hour'], freq='h')
     
     fig = px.line(x=ts_dates, y=ts_values, markers=True)
     fig.add_scatter(x=[feature_['pickup_hour']], y=[target_], mode='markers', name='actual_value')
     
     if predictions is not None:
          prediction_ = predictions.iloc[example_id]
          fig.add_scatter(x=[feature_['pickup_hour']], y=[prediction_])
          
     
     fig.show()


     
     






     






