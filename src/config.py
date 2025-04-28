import os
from dotenv import load_dotenv
from src.paths import PARENT_DIR

HOPSWORK_PROJECT_NAME = 'taxi_demand_service'

try:
    HOPSWORK_API_KEY = os.environ['HOPSWORK_API_KEY']
except Exception:
    print('Create a .env file in the project root with the Hopsworks API key')

    
FEATURE_GROUP_NAME = 'time_series_data_hourly_feature_group'
FEATURE_GROUP_VERSION = '1'




