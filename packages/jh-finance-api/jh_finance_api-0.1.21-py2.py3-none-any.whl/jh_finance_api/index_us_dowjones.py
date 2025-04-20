import sys; sys.dont_write_bytecode=True
import warnings
import pandas as pd

warnings.filterwarnings('ignore')


endpoint = lambda: f'https://proj-finance-backend.onrender.com/index-us-dowjones'


def get(): 
    return pd.read_json(endpoint())


sample_req = 'https://proj-finance-backend.onrender.com/index-us-dowjones'

sample_res = [
  {
    "#": 1,
    "Company": "Unitedhealth Group Inc",
    "Symbol": "UNH",
    "Weight": 8.192351,
    "Price": 525.05,
    "Chg": -15.39,
    "% Chg": "(-2.85%)"
  },
  {
    "#": 2,
    "Company": "Goldman Sachs Group Inc",
    "Symbol": "GS",
    "Weight": 7.749566,
    "Price": 470.81,
    "Chg": -40.42,
    "% Chg": "(-7.91%)"
  },
  {
    "#": 3,
    "Company": "Microsoft Corp",
    "Symbol": "MSFT",
    "Weight": 5.655851,
    "Price": 359.84,
    "Chg": -13.27,
    "% Chg": "(-3.56%)"
  },
  {
    "#": 4,
    "Company": "Home Depot Inc",
    "Symbol": "HD",
    "Weight": 5.395122,
    "Price": 353.9,
    "Chg": -2.01,
    "% Chg": "(-0.56%)"
  },
  {
    "#": 5,
    "Company": "Sherwin Williams Co",
    "Symbol": "SHW",
    "Weight": 5.163801,
    "Price": 332.06,
    "Chg": -8.59,
    "% Chg": "(-2.52%)"
  },
  {
    "#": 6,
    "Company": "Visa Inc Class A Shares",
    "Symbol": "V",
    "Weight": 5.144701,
    "Price": 313.13,
    "Chg": -26.26,
    "% Chg": "(-7.74%)"
  },
  {
    "#": 7,
    "Company": "Mcdonald S Corp",
    "Symbol": "MCD",
    "Weight": 4.82455,
    "Price": 300.11,
    "Chg": -18.16,
    "% Chg": "(-5.71%)"
  },
  {
    "#": 8,
    "Company": "Amgen Inc",
    "Symbol": "AMGN",
    "Weight": 4.696914,
    "Price": 294.39,
    "Chg": -15.46,
    "% Chg": "(-4.99%)"
  },
  {
    "#": 9,
    "Company": "Caterpillar Inc",
    "Symbol": "CAT",
    "Weight": 4.634915,
    "Price": 288.08,
    "Chg": -17.68,
    "% Chg": "(-5.78%)"
  },
  {
    "#": 10,
    "Company": "Travelers Cos Inc",
    "Symbol": "TRV",
    "Weight": 3.988246,
    "Price": 242.26,
    "Chg": -20.84,
    "% Chg": "(-7.92%)"
  },
  {
    "#": 11,
    "Company": "Salesforce Inc",
    "Symbol": "CRM",
    "Weight": 3.868947,
    "Price": 240.76,
    "Chg": -14.47,
    "% Chg": "(-5.67%)"
  },
  {
    "#": 12,
    "Company": "American Express Co",
    "Symbol": "AXP",
    "Weight": 3.744191,
    "Price": 233.68,
    "Chg": -14.14,
    "% Chg": "(-5.71%)"
  },
  {
    "#": 13,
    "Company": "Intl Business Machines Corp",
    "Symbol": "IBM",
    "Weight": 3.690984,
    "Price": 227.48,
    "Chg": -16.01,
    "% Chg": "(-6.58%)"
  },
  {
    "#": 14,
    "Company": "Jpmorgan Chase & Co",
    "Symbol": "JPM",
    "Weight": 3.445414,
    "Price": 210.28,
    "Chg": -18.41,
    "% Chg": "(-8.05%)"
  },
  {
    "#": 15,
    "Company": "Honeywell International Inc",
    "Symbol": "HON",
    "Weight": 3.132994,
    "Price": 190.99,
    "Chg": -15.69,
    "% Chg": "(-7.59%)"
  },
  {
    "#": 16,
    "Company": "Apple Inc",
    "Symbol": "AAPL",
    "Weight": 3.08009,
    "Price": 188.38,
    "Chg": -14.81,
    "% Chg": "(-7.29%)"
  },
  {
    "#": 17,
    "Company": "Amazon.com Inc",
    "Symbol": "AMZN",
    "Weight": 2.704458,
    "Price": 171,
    "Chg": -7.41,
    "% Chg": "(-4.15%)"
  },
  {
    "#": 18,
    "Company": "Procter & Gamble Co",
    "Symbol": "PG",
    "Weight": 2.613203,
    "Price": 163.75,
    "Chg": -8.64,
    "% Chg": "(-5.01%)"
  },
  {
    "#": 19,
    "Company": "Johnson & Johnson",
    "Symbol": "JNJ",
    "Weight": 2.422658,
    "Price": 153.24,
    "Chg": -6.58,
    "% Chg": "(-4.12%)"
  },
  {
    "#": 20,
    "Company": "Chevron Corp",
    "Symbol": "CVX",
    "Weight": 2.366571,
    "Price": 143.28,
    "Chg": -12.84,
    "% Chg": "(-8.22%)"
  },
  {
    "#": 21,
    "Company": "Boeing Co",
    "Symbol": "BA",
    "Weight": 2.287595,
    "Price": 136.59,
    "Chg": -14.32,
    "% Chg": "(-9.49%)"
  },
  {
    "#": 22,
    "Company": "3m Co",
    "Symbol": "MMM",
    "Weight": 2.118272,
    "Price": 126.91,
    "Chg": -12.83,
    "% Chg": "(-9.18%)"
  },
  {
    "#": 23,
    "Company": "Nvidia Corp",
    "Symbol": "NVDA",
    "Weight": 1.543152,
    "Price": 94.31,
    "Chg": -7.49,
    "% Chg": "(-7.36%)"
  },
  {
    "#": 24,
    "Company": "Walt Disney Co",
    "Symbol": "DIS",
    "Weight": 1.346696,
    "Price": 83.53,
    "Chg": -5.31,
    "% Chg": "(-5.98%)"
  },
  {
    "#": 25,
    "Company": "Walmart Inc",
    "Symbol": "WMT",
    "Weight": 1.322745,
    "Price": 83.19,
    "Chg": -4.07,
    "% Chg": "(-4.66%)"
  },
  {
    "#": 26,
    "Company": "Merck & Co. Inc.",
    "Symbol": "MRK",
    "Weight": 1.309557,
    "Price": 81.47,
    "Chg": -4.92,
    "% Chg": "(-5.70%)"
  },
  {
    "#": 27,
    "Company": "Coca Cola Co",
    "Symbol": "KO",
    "Weight": 1.109311,
    "Price": 69.93,
    "Chg": -3.25,
    "% Chg": "(-4.44%)"
  },
  {
    "#": 28,
    "Company": "Cisco Systems Inc",
    "Symbol": "CSCO",
    "Weight": 0.868743,
    "Price": 54.54,
    "Chg": -2.77,
    "% Chg": "(-4.83%)"
  },
  {
    "#": 29,
    "Company": "Nike Inc Cl B",
    "Symbol": "NKE",
    "Weight": 0.842519,
    "Price": 57.25,
    "Chg": 1.67,
    "% Chg": "(3.00%)"
  },
  {
    "#": 30,
    "Company": "Verizon Communications Inc",
    "Symbol": "VZ",
    "Weight": 0.691538,
    "Price": 43.03,
    "Chg": -2.59,
    "% Chg": "(-5.68%)"
  }
]