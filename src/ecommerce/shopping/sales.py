def calculate_tax(amount_in_taxes):
    return f'tax is {amount_in_taxes}'
#print(__package__)

import sys
from pathlib import Path
sys.path.append(r'c:/Users/pc/Documents/weekly_profile/src')
#print(sys.path)
from ecommerce.customers.contacts import show_contacts
#print('sales module loaded')
print(Path() / Path('__init__.py'))
#print(Path().home())

import os
print(os.environ['PATH'])



    


