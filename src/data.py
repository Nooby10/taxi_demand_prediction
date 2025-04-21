


import sys
sys.path.append('C:/Users/pc/Documents/weekly_profile')
from src.paths import RAW_DATA_DIR
import requests
import numpy as np, pandas as pd
from typing import Optional, List





def download_one_file_of_raw_data(year:int, month:int):

    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'

    path = RAW_DATA_DIR / f'rides_{year}_{month:02d}.parquet'

    response = requests.get(url)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        return path
    else:
        raise Exception(f'{url} is not available')
    


    


    
def validate_raw_data(data: pd.DataFrame, year:int, month:int):

    data = data[['tpep_pickup_datetime', 'PULocationID']]
    data = data.rename(columns={'tpep_pickup_datetime':'pickup_time', 'PULocationID':'location_id'})

    data = data.loc[
        (data.pickup_time >= f'{year}-{month:02d}-01') & 
        (data.pickup_time < f'{year}-{month+1 :02d}-1') if month < 12 else (data.pickup_time <= f'{year}-{month:02d}-31')]
    return data







def load_raw_data(year:int, months: Optional[List[int]] = None):

    validated_data_all_month = pd.DataFrame()

    
    if not months:
        months = np.arange(1,13)
    else:
        months = [months] if type(months) == int else months

    for month in months:
        path = RAW_DATA_DIR / f'rides_{year}_{month:02d}.parquet'

        if not path.exists():
            try:
                print(f'downloading file for {month:02d}, {year}')
                download_one_file_of_raw_data(year, month)
            except:
                print('file not available')
                continue
            
        else:
            print(f'file for {month:02d}, {year} already exists on disk')
        raw_data_one_month = pd.read_parquet(path)
        
        validated_data_one_month = validate_raw_data(raw_data_one_month, year, month)

        validated_data_all_month = pd.concat([validated_data_all_month, validated_data_one_month])
    
    
    return validated_data_all_month






def transform_raw_into_ts_data(data: pd.DataFrame):
    
    data['pickup_hour'] = data.pickup_time.dt.floor(freq='h')
    data = data.groupby(['pickup_hour', 'location_id']).size().reset_index().rename(columns={0: 'rides'})
    full_time_range = pd.date_range(data.pickup_hour.min(), data.pickup_hour.max(), freq='h')
    location_ids = data.location_id.unique()
    data_all_location = pd.DataFrame()

    for location in location_ids:
        data_one_location = data.loc[data.location_id == location][['pickup_hour','rides']]
        indexed_data = data_one_location.set_index('pickup_hour')
        indexed_data.index = pd.DatetimeIndex(indexed_data.index)
        indexed_data = indexed_data.reindex(full_time_range, fill_value=0)
        indexed_data['location_id'] = location
        data_all_location = pd.concat([data_all_location, indexed_data])
        
    data_all_location =data_all_location.reset_index().rename(columns={'index':'pickup_hour'})
    
    return data_all_location






def get_cutoff_indices(data:pd.DataFrame, n_feat: int, step_size:int):

    indices_list = []
    stop_position = len(data) - 1
    first_sub = 0
    mid_sub = n_feat
    last_sub = mid_sub + 1

    while first_sub + n_feat <= stop_position:
        indices_list.append((first_sub,mid_sub,last_sub))
        first_sub += step_size
        mid_sub += step_size
        last_sub += step_size
    return indices_list





def transform_ts_into_tabular_data(data: pd.DataFrame, num_feat: int, step_size: int):

    data_all_location = pd.DataFrame()
    location_ids = data.location_id.unique()


    for location in location_ids:
        data_one_location = data.loc[data.location_id == location]
        indices = get_cutoff_indices(data_one_location, num_feat, step_size)

        num_observation = len(indices)
        x = np.zeros((num_observation, num_feat))
        y = np.zeros(num_observation)
        pickup_time_list = []

        for counter, ind in enumerate(indices):
            x[counter] = data.rides.iloc[ind[0]:ind[1]].values
            y[counter] = data.rides.iloc[ind[1]:ind[2]].values[0]
            pickup_time_list.append(data.pickup_hour.iloc[ind[1]])

        final_ts_df_one_location = pd.DataFrame(x)
        final_ts_df_one_location['target_pickup_time'] = pickup_time_list
        final_ts_df_one_location['location_id'] = location
        final_ts_df_one_location['target_ride_next_hour'] = y
        data_all_location = pd.concat([data_all_location, final_ts_df_one_location])


    return data_all_location.rename(columns=
        dict(zip(data_all_location.columns[:-3],[f'rides_past_{hr+1}_hour' for hr in reversed(range(len(data_all_location.columns[:-3])))]))).reset_index(drop=True)
   


    



