#!/usr/bin/python3

""" All constants for Jupyter Notebook testing """
DEFAULT_WAIT_PERIOD = 10
START_SERVER_WAIT_PERIOD = 60
DATAHUB_DEV_URL = "http://datahub-dev.berkeley.edu"
NBPULLER_ROUTE = "/interact"
JPY_USER_ROUTE = "/user/peterkangveerman"
TEST_1_PARAMS = "repo=data8assets&path=materials/sp17/lab/lab02"
TEST_1_FILES = [
    'tests',
    'lab02.ipynb',
    'array_logarithm.jpg',
    'array_multiplication.jpg',
    'chaining_method_calls.jpg',
    'excel_array.jpg',
    'lab02.ok',
    'more_restaurant_bills.csv',
    'restaurant_bills.csv',
    'statement.jpg',
    'world_population.csv',
]
TEST_1_REDIRECT_PATH = '/tree/data8assets/materials/sp17/lab/lab02'
MALFORMED_LINK_MESSAGE = "Looks like your request was malformed."

""" Keywords that appear in different redirect page titles """
GOOGLE_PAGE_TITLE = "Google"
CALNET_PAGE_TITLE = "CalNet"
SERVER_PAGE_TITLE = "Jupyter"
GDRIVE_PAGE_TITLE = "Request"
NOTEBOOK_PAGE_TITLE = "Home"
