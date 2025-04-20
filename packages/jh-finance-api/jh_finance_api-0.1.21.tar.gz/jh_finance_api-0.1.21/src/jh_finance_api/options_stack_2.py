import warnings
import pandas as pd

warnings.filterwarnings('ignore')


endpoint = lambda TICKER: f'https://proj-finance-backend.onrender.com/options-stack-2/{TICKER}'


def get(TICKER='MSFT'):
    return pd.read_json(endpoint(TICKER))


sample_req = 'https://proj-finance-backend.onrender.com/options-stack-2/MSFT'
sample_res = [
 {'Code': 'MSFT250411C00230000',
  'Ticker': 'MSFT',
  'Price': 351,
  'Option': 'CALL',
  'Expiry': '2025-04-11',
  'Strike': 230.0,
  'Volume': 0,
  'OI': 3,
  'Ask': 119.1,
  'Mid': 120.9,
  'Bid': 122.7},
 {'Code': 'MSFT250411C00240000',
  'Ticker': 'MSFT',
  'Price': 351,
  'Option': 'CALL',
  'Expiry': '2025-04-11',
  'Strike': 240.0,
  'Volume': 0,
  'OI': 0,
  'Ask': 109.2,
  'Mid': 110.72,
  'Bid': 112.25},
 {'Code': 'MSFT250411C00250000',
  'Ticker': 'MSFT',
  'Price': 351,
  'Option': 'CALL',
  'Expiry': '2025-04-11',
  'Strike': 250.0,
  'Volume': 0,
  'OI': 0,
  'Ask': 99.35,
  'Mid': 101.08,
  'Bid': 102.8},
 {'Code': 'MSFT250411C00260000',
  'Ticker': 'MSFT',
  'Price': 351,
  'Option': 'CALL',
  'Expiry': '2025-04-11',
  'Strike': 260.0,
  'Volume': 0,
  'OI': 1,
  'Ask': 89.35,
  'Mid': 90.88,
  'Bid': 92.4},
 {'Code': 'MSFT250411C00270000',
  'Ticker': 'MSFT',
  'Price': 351,
  'Option': 'CALL',
  'Expiry': '2025-04-11',
  'Strike': 270.0,
  'Volume': 0,
  'OI': 0,
  'Ask': 79.55,
  'Mid': 81.28,
  'Bid': 83.0}
]