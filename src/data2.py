import sys
sys.path.append('C:/Users/pc/Documents/weekly_profile')
import requests
import pandas as pd, numpy as np
from pathlib import Path
from typing import Optional, List
from src.paths import RAW_DATA_DIR



def download_one_file_of_raw_data(year:int, month:int):
     
     URL = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month: 02d}.parquet'
     response = requests.get(URL)
     file_path = RAW_DATA_DIR / f'rides{year}_{month:02d}'
     
     if response.status_code == 200:
          file_path.write_bytes(response.content)
          return file_path
     else:
          raise Exception('file not found')
     


def validate_raw_data(rides:pd.DataFrame, year:int, month:int):
     
     this_month_starts = f'{year}-{month:02d}-01'
     next_month_starts = f'{year}-{month + 1:02d}-01' if month < 12 else f'{year+1}-01-01'


     rides = rides[['tpep_pickup_datetime', 'PULocationID']]
     rides = rides.rename(columns={'tpep_pickup_datetime':'pickup_datetime','PULocationID':'location_id'})
     validated_rides=rides.loc[rides['pickup_datetime'] >= this_month_starts]
     validated_rides=validated_rides.loc[validated_rides['pickup_datetime'] < next_month_starts]
     
     return validated_rides



def load_raw_data(year:int, months:Optional[List[int]]=None):
    
    rides = pd.DataFrame()

    if months is None:
          months = np.arange(12) + 1
          
    else:
         months = [months] if type(months) == int else months

    for month in months:
         path = RAW_DATA_DIR / f'rides_{year}_{month:02d}.parquet'
         
         
         if not path.exists():
              print(f'downloading data for {month:02d}, {year}')
              try:
                download_one_file_of_raw_data(year, month)
              except Exception:
                   print(f'file not available for {month:02d}, {year}')
                   continue
        
         else:
              print(f'file already existed on disk for {month:02d}, {year}')
        
         data_month_i = pd.read_parquet(path)
         data_month_i = validate_raw_data(data_month_i, year, month)
         rides = pd.concat([rides,data_month_i])
    
    return rides



def add_missing_slots(agg_rides: pd.DataFrame):
     
    
     full_range_dates = pd.date_range(agg_rides.pickup_hour.min(), agg_rides.pickup_hour.max(), freq='h') 
     location_ids = agg_rides.location_id.unique()
     output = pd.DataFrame()

     for loc_id in location_ids:
          agg_rides_i = agg_rides.loc[agg_rides['location_id'] == loc_id][['pickup_hour','rides']]
          agg_rides_i.set_index('pickup_hour', inplace= True)
          agg_rides_i.index = pd.DatetimeIndex(agg_rides_i.index)
          agg_rides_i = agg_rides_i.reindex(full_range_dates, fill_value=0)
          agg_rides_i['location_id'] = loc_id
          output = pd.concat([output,agg_rides_i])
     output = output.reset_index().rename(columns={'index':'pickup_hour'})
     
     return output


def transform_raw_data_into_ts(rides: pd.DataFrame):
      rides['pickup_hour'] = rides['pickup_datetime'].dt.floor(freq='h')
      agg_rides = rides.groupby(['pickup_hour', 'location_id']).size()
      agg_rides = agg_rides.reset_index().rename(columns={0:'rides'})
      agg_rides_all_slots = add_missing_slots(agg_rides)
      return agg_rides_all_slots



def get_cutoff_indices(data:pd.DataFrame, no_features:int, step_size:int):
     
     indices_list = []
     stop_point = len(data) - 1

     first_sub = 0
     mid_sub = no_features
     last_sub = mid_sub + 1

     while first_sub + no_features < stop_point:
          indices_list.append((first_sub,mid_sub,last_sub))
          first_sub += step_size
          mid_sub += step_size
          last_sub += step_size
     return indices_list


def transform_ts_data_into_fatures_and_targets(rides:pd.DataFrame, no_features:int, step_size:int):
     
     location_ids = rides.location_id.unique()
     features = pd.DataFrame()
     targets = pd.DataFrame()

     for loc_id in location_ids:

        
        rides_i_location = rides.loc[rides['location_id'] == loc_id]
        indices = get_cutoff_indices(rides_i_location, no_features, step_size)
        no_observations = len(indices)
        pickup_hours = []
        x = np.random.random([no_observations,no_features])
        y = np.random.random(no_observations)
        
        for counter, idx in enumerate(indices):
             x[counter,:] = rides_i_location.iloc[idx[0]:idx[1]]['rides'].values
             y[counter] = rides_i_location.iloc[idx[1]:idx[2]]['rides'].values[0]
             pickup_hours.append(rides_i_location.iloc[idx[1]]['pickup_hour'])

        features_i_location = pd.DataFrame(x)
        features_i_location['pickup_hour'] = pickup_hours
        features = pd.concat([features,features_i_location])

        targets_i_location = pd.DataFrame(y, columns =['target_ride_next_hour'])
        targets = pd.concat([targets,targets_i_location])
        
     features = features.reset_index(drop=True)
     features = features.rename(columns=dict(zip(features.columns,[f'rides_in_past_{hr + 1}_hour' for hr in reversed(range(no_features))])))
     
     targets = targets.reset_index(drop=True)

    
     return features,targets










      



          
     
     
    

