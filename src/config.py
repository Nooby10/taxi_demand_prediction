import os
from dotenv import load_dotenv
from src.paths import PARENT_DIR

HOPSWORK_PROJECT_NAME = 'taxi_demand_service'

try:
    HOPSWORK_API_KEY = os.environ['HOPSWORK_API_KEY']
except Exception:
    print('There is an error loading the API key. It is now being reloaded')
    load_dotenv(PARENT_DIR / '.env')
    HOPSWORK_API_KEY = os.environ['HOPSWORK_API_KEY']
    
FEATURE_GROUP_NAME = 'time_series_data_hourly_feature_group'
FEATURE_GROUP_VERSION = '1'




