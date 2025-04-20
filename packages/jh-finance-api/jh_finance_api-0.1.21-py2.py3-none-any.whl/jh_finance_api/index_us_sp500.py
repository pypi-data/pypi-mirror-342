import sys; sys.dont_write_bytecode=True
import warnings
import pandas as pd

warnings.filterwarnings('ignore')


endpoint = lambda: f'https://proj-finance-backend.onrender.com/index-us-sp500'


def get(): 
    return pd.read_json(endpoint())


sample_req = 'https://proj-finance-backend.onrender.com/index-us-sp500'

sample_res = [
  {
    "#": 1,
    "Company": "Apple Inc.",
    "Symbol": "AAPL",
    "Weight": "6.67%",
    "Price": 188.38,
    "Chg": -14.81,
    "% Chg": "(-7.29%)"
  },
  {
    "#": 2,
    "Company": "Microsoft Corp",
    "Symbol": "MSFT",
    "Weight": "6.06%",
    "Price": 359.84,
    "Chg": -13.27,
    "% Chg": "(-3.56%)"
  },
  {
    "#": 3,
    "Company": "Nvidia Corp",
    "Symbol": "NVDA",
    "Weight": "5.45%",
    "Price": 94.31,
    "Chg": -7.49,
    "% Chg": "(-7.36%)"
  },
  {
    "#": 4,
    "Company": "Amazon.com Inc",
    "Symbol": "AMZN",
    "Weight": "3.68%",
    "Price": 171,
    "Chg": -7.41,
    "% Chg": "(-4.15%)"
  },
  {
    "#": 5,
    "Company": "Meta Platforms, Inc. Class A",
    "Symbol": "META",
    "Weight": "2.54%",
    "Price": 504.73,
    "Chg": -26.89,
    "% Chg": "(-5.06%)"
  },
  {
    "#": 6,
    "Company": "Berkshire Hathaway Class B",
    "Symbol": "BRK.B",
    "Weight": "2.12%",
    "Price": 493.54,
    "Chg": -36.62,
    "% Chg": "(-6.91%)"
  },
  {
    "#": 7,
    "Company": "Alphabet Inc. Class A",
    "Symbol": "GOOGL",
    "Weight": "1.92%",
    "Price": 145.6,
    "Chg": -5.12,
    "% Chg": "(-3.40%)"
  },
  {
    "#": 8,
    "Company": "Tesla, Inc.",
    "Symbol": "TSLA",
    "Weight": "1.63%",
    "Price": 239.43,
    "Chg": -27.85,
    "% Chg": "(-10.42%)"
  },
  {
    "#": 9,
    "Company": "Broadcom Inc.",
    "Symbol": "AVGO",
    "Weight": "1.58%",
    "Price": 146.29,
    "Chg": -7.72,
    "% Chg": "(-5.01%)"
  },
  {
    "#": 10,
    "Company": "Alphabet Inc. Class C",
    "Symbol": "GOOG",
    "Weight": "1.58%",
    "Price": 147.74,
    "Chg": -4.89,
    "% Chg": "(-3.20%)"
  },
  {
    "#": 11,
    "Company": "Jpmorgan Chase & Co.",
    "Symbol": "JPM",
    "Weight": "1.39%",
    "Price": 210.28,
    "Chg": -18.41,
    "% Chg": "(-8.05%)"
  },
  {
    "#": 12,
    "Company": "Eli Lilly & Co.",
    "Symbol": "LLY",
    "Weight": "1.36%",
    "Price": 738.21,
    "Chg": -50.88,
    "% Chg": "(-6.45%)"
  },
  {
    "#": 13,
    "Company": "Visa Inc.",
    "Symbol": "V",
    "Weight": "1.28%",
    "Price": 313.13,
    "Chg": -26.26,
    "% Chg": "(-7.74%)"
  },
  {
    "#": 14,
    "Company": "Unitedhealth Group Incorporated",
    "Symbol": "UNH",
    "Weight": "1.09%",
    "Price": 525.05,
    "Chg": -15.39,
    "% Chg": "(-2.85%)"
  },
  {
    "#": 15,
    "Company": "Exxon Mobil Corporation",
    "Symbol": "XOM",
    "Weight": "1.07%",
    "Price": 104.34,
    "Chg": -8.09,
    "% Chg": "(-7.20%)"
  },
  {
    "#": 16,
    "Company": "Mastercard Incorporated",
    "Symbol": "MA",
    "Weight": "0.94%",
    "Price": 489.77,
    "Chg": -40.78,
    "% Chg": "(-7.69%)"
  },
  {
    "#": 17,
    "Company": "Costco Wholesale Corp",
    "Symbol": "COST",
    "Weight": "0.94%",
    "Price": 916.48,
    "Chg": -50.6,
    "% Chg": "(-5.23%)"
  },
  {
    "#": 18,
    "Company": "Procter & Gamble Company",
    "Symbol": "PG",
    "Weight": "0.88%",
    "Price": 163.75,
    "Chg": -8.64,
    "% Chg": "(-5.01%)"
  },
  {
    "#": 19,
    "Company": "Netflix Inc",
    "Symbol": "NFLX",
    "Weight": "0.86%",
    "Price": 855.86,
    "Chg": -61.19,
    "% Chg": "(-6.67%)"
  },
  {
    "#": 20,
    "Company": "Johnson & Johnson",
    "Symbol": "JNJ",
    "Weight": "0.84%",
    "Price": 153.24,
    "Chg": -6.58,
    "% Chg": "(-4.12%)"
  },
  {
    "#": 21,
    "Company": "Walmart Inc.",
    "Symbol": "WMT",
    "Weight": "0.83%",
    "Price": 83.19,
    "Chg": -4.07,
    "% Chg": "(-4.66%)"
  },
  {
    "#": 22,
    "Company": "Abbvie Inc.",
    "Symbol": "ABBV",
    "Weight": "0.78%",
    "Price": 186.96,
    "Chg": -14.68,
    "% Chg": "(-7.28%)"
  },
  {
    "#": 23,
    "Company": "Home Depot, Inc.",
    "Symbol": "HD",
    "Weight": "0.77%",
    "Price": 353.9,
    "Chg": -2.01,
    "% Chg": "(-0.56%)"
  },
  {
    "#": 24,
    "Company": "Coca-Cola Company",
    "Symbol": "KO",
    "Weight": "0.62%",
    "Price": 69.93,
    "Chg": -3.25,
    "% Chg": "(-4.44%)"
  },
  {
    "#": 25,
    "Company": "Chevron Corporation",
    "Symbol": "CVX",
    "Weight": "0.57%",
    "Price": 143.28,
    "Chg": -12.84,
    "% Chg": "(-8.22%)"
  },
  {
    "#": 26,
    "Company": "Philip Morris International Inc.",
    "Symbol": "PM",
    "Weight": "0.55%",
    "Price": 150.62,
    "Chg": -11.45,
    "% Chg": "(-7.06%)"
  },
  {
    "#": 27,
    "Company": "Bank of America Corporation",
    "Symbol": "BAC",
    "Weight": "0.54%",
    "Price": 34.39,
    "Chg": -2.83,
    "% Chg": "(-7.60%)"
  },
  {
    "#": 28,
    "Company": "Salesforce, Inc.",
    "Symbol": "CRM",
    "Weight": "0.53%",
    "Price": 240.76,
    "Chg": -14.47,
    "% Chg": "(-5.67%)"
  },
  {
    "#": 29,
    "Company": "Abbott Laboratories",
    "Symbol": "ABT",
    "Weight": "0.50%",
    "Price": 124.44,
    "Chg": -7.19,
    "% Chg": "(-5.46%)"
  },
  {
    "#": 30,
    "Company": "Cisco Systems, Inc.",
    "Symbol": "CSCO",
    "Weight": "0.50%",
    "Price": 54.54,
    "Chg": -2.77,
    "% Chg": "(-4.83%)"
  },
  {
    "#": 31,
    "Company": "Mcdonald's Corporation",
    "Symbol": "MCD",
    "Weight": "0.50%",
    "Price": 300.11,
    "Chg": -18.16,
    "% Chg": "(-5.71%)"
  },
  {
    "#": 32,
    "Company": "International Business Machines Corporation",
    "Symbol": "IBM",
    "Weight": "0.49%",
    "Price": 227.48,
    "Chg": -16.01,
    "% Chg": "(-6.58%)"
  },
  {
    "#": 33,
    "Company": "Oracle Corp",
    "Symbol": "ORCL",
    "Weight": "0.49%",
    "Price": 128.27,
    "Chg": -8.96,
    "% Chg": "(-6.53%)"
  },
  {
    "#": 34,
    "Company": "Linde Plc",
    "Symbol": "LIN",
    "Weight": "0.49%",
    "Price": 437.96,
    "Chg": -29.26,
    "% Chg": "(-6.26%)"
  },
  {
    "#": 35,
    "Company": "Merck & Co., Inc.",
    "Symbol": "MRK",
    "Weight": "0.48%",
    "Price": 81.47,
    "Chg": -4.92,
    "% Chg": "(-5.70%)"
  },
  {
    "#": 36,
    "Company": "Wells Fargo & Co.",
    "Symbol": "WFC",
    "Weight": "0.47%",
    "Price": 60.98,
    "Chg": -4.69,
    "% Chg": "(-7.14%)"
  },
  {
    "#": 37,
    "Company": "Pepsico, Inc.",
    "Symbol": "PEP",
    "Weight": "0.45%",
    "Price": 146.61,
    "Chg": -4.76,
    "% Chg": "(-3.14%)"
  },
  {
    "#": 38,
    "Company": "At&t Inc.",
    "Symbol": "T",
    "Weight": "0.45%",
    "Price": 26.64,
    "Chg": -1.96,
    "% Chg": "(-6.85%)"
  },
  {
    "#": 39,
    "Company": "Ge Aerospace",
    "Symbol": "GE",
    "Weight": "0.44%",
    "Price": 166.81,
    "Chg": -20.82,
    "% Chg": "(-11.10%)"
  },
  {
    "#": 40,
    "Company": "Verizon Communications",
    "Symbol": "VZ",
    "Weight": "0.42%",
    "Price": 43.03,
    "Chg": -2.59,
    "% Chg": "(-5.68%)"
  },
  {
    "#": 41,
    "Company": "Accenture Plc",
    "Symbol": "ACN",
    "Weight": "0.41%",
    "Price": 285.06,
    "Chg": -16.4,
    "% Chg": "(-5.44%)"
  },
  {
    "#": 42,
    "Company": "Thermo Fisher Scientific, Inc.",
    "Symbol": "TMO",
    "Weight": "0.39%",
    "Price": 437.91,
    "Chg": -32.12,
    "% Chg": "(-6.83%)"
  },
  {
    "#": 43,
    "Company": "Intuitive Surgical Inc.",
    "Symbol": "ISRG",
    "Weight": "0.39%",
    "Price": 451.58,
    "Chg": -43.03,
    "% Chg": "(-8.70%)"
  },
  {
    "#": 44,
    "Company": "Rtx Corporation",
    "Symbol": "RTX",
    "Weight": "0.38%",
    "Price": 117.45,
    "Chg": -12.78,
    "% Chg": "(-9.81%)"
  },
  {
    "#": 45,
    "Company": "Palantir Technologies Inc. Class A",
    "Symbol": "PLTR",
    "Weight": "0.37%",
    "Price": 74.01,
    "Chg": -9.59,
    "% Chg": "(-11.47%)"
  },
  {
    "#": 46,
    "Company": "Progressive Corporation",
    "Symbol": "PGR",
    "Weight": "0.37%",
    "Price": 257.64,
    "Chg": -29.36,
    "% Chg": "(-10.23%)"
  },
  {
    "#": 47,
    "Company": "Intuit Inc",
    "Symbol": "INTU",
    "Weight": "0.37%",
    "Price": 561.53,
    "Chg": -37,
    "% Chg": "(-6.18%)"
  },
  {
    "#": 48,
    "Company": "Amgen Inc",
    "Symbol": "AMGN",
    "Weight": "0.36%",
    "Price": 294.39,
    "Chg": -15.46,
    "% Chg": "(-4.99%)"
  },
  {
    "#": 49,
    "Company": "The Walt Disney Company",
    "Symbol": "DIS",
    "Weight": "0.35%",
    "Price": 83.53,
    "Chg": -5.31,
    "% Chg": "(-5.98%)"
  },
  {
    "#": 50,
    "Company": "Adobe Inc.",
    "Symbol": "ADBE",
    "Weight": "0.35%",
    "Price": 349.07,
    "Chg": -18.18,
    "% Chg": "(-4.95%)"
  },
  {
    "#": 51,
    "Company": "Servicenow, Inc.",
    "Symbol": "NOW",
    "Weight": "0.35%",
    "Price": 721.65,
    "Chg": -52.42,
    "% Chg": "(-6.77%)"
  },
  {
    "#": 52,
    "Company": "Goldman Sachs Group Inc.",
    "Symbol": "GS",
    "Weight": "0.35%",
    "Price": 470.81,
    "Chg": -40.42,
    "% Chg": "(-7.91%)"
  },
  {
    "#": 53,
    "Company": "Qualcomm Inc",
    "Symbol": "QCOM",
    "Weight": "0.34%",
    "Price": 127.46,
    "Chg": -11.96,
    "% Chg": "(-8.58%)"
  },
  {
    "#": 54,
    "Company": "S&p Global Inc.",
    "Symbol": "SPGI",
    "Weight": "0.34%",
    "Price": 451.5,
    "Chg": -37.88,
    "% Chg": "(-7.74%)"
  },
  {
    "#": 55,
    "Company": "Advanced Micro Devices",
    "Symbol": "AMD",
    "Weight": "0.33%",
    "Price": 85.76,
    "Chg": -8.04,
    "% Chg": "(-8.57%)"
  },
  {
    "#": 56,
    "Company": "Texas Instruments Incorporated",
    "Symbol": "TXN",
    "Weight": "0.33%",
    "Price": 151.39,
    "Chg": -12.81,
    "% Chg": "(-7.80%)"
  },
  {
    "#": 57,
    "Company": "Nextra Energy, Inc.",
    "Symbol": "NEE",
    "Weight": "0.32%",
    "Price": 66.91,
    "Chg": -5.23,
    "% Chg": "(-7.25%)"
  },
  {
    "#": 58,
    "Company": "Booking Holdings Inc.",
    "Symbol": "BKNG",
    "Weight": "0.32%",
    "Price": 4284.02,
    "Chg": -166.51,
    "% Chg": "(-3.74%)"
  },
  {
    "#": 59,
    "Company": "Caterpillar Inc.",
    "Symbol": "CAT",
    "Weight": "0.32%",
    "Price": 288.08,
    "Chg": -17.68,
    "% Chg": "(-5.78%)"
  },
  {
    "#": 60,
    "Company": "Uber Technologies, Inc.",
    "Symbol": "UBER",
    "Weight": "0.32%",
    "Price": 64.62,
    "Chg": -5.23,
    "% Chg": "(-7.49%)"
  },
  {
    "#": 61,
    "Company": "Boston Scientific Corp.",
    "Symbol": "BSX",
    "Weight": "0.32%",
    "Price": 89.7,
    "Chg": -8.8,
    "% Chg": "(-8.93%)"
  },
  {
    "#": 62,
    "Company": "Tjx Companies, Inc.",
    "Symbol": "TJX",
    "Weight": "0.31%",
    "Price": 122.16,
    "Chg": -3.27,
    "% Chg": "(-2.61%)"
  },
  {
    "#": 63,
    "Company": "Gilead Sciences Inc",
    "Symbol": "GILD",
    "Weight": "0.31%",
    "Price": 107.25,
    "Chg": -5.14,
    "% Chg": "(-4.57%)"
  },
  {
    "#": 64,
    "Company": "Pfizer Inc.",
    "Symbol": "PFE",
    "Weight": "0.30%",
    "Price": 22.97,
    "Chg": -1.32,
    "% Chg": "(-5.43%)"
  },
  {
    "#": 65,
    "Company": "American Express Company",
    "Symbol": "AXP",
    "Weight": "0.30%",
    "Price": 233.68,
    "Chg": -14.14,
    "% Chg": "(-5.71%)"
  },
  {
    "#": 66,
    "Company": "Union Pacific Corp.",
    "Symbol": "UNP",
    "Weight": "0.30%",
    "Price": 213.26,
    "Chg": -10.71,
    "% Chg": "(-4.78%)"
  },
  {
    "#": 67,
    "Company": "Comcast Corp",
    "Symbol": "CMCSA",
    "Weight": "0.29%",
    "Price": 33.38,
    "Chg": -2.34,
    "% Chg": "(-6.55%)"
  },
  {
    "#": 68,
    "Company": "Honeywell International, Inc.",
    "Symbol": "HON",
    "Weight": "0.29%",
    "Price": 190.99,
    "Chg": -15.69,
    "% Chg": "(-7.59%)"
  },
  {
    "#": 69,
    "Company": "Morgan Stanley",
    "Symbol": "MS",
    "Weight": "0.29%",
    "Price": 99.83,
    "Chg": -8.1,
    "% Chg": "(-7.50%)"
  },
  {
    "#": 70,
    "Company": "Blackrock, Inc.",
    "Symbol": "BLK",
    "Weight": "0.28%",
    "Price": 822.62,
    "Chg": -65.03,
    "% Chg": "(-7.33%)"
  },
  {
    "#": 71,
    "Company": "T-Mobile Us, Inc.",
    "Symbol": "TMUS",
    "Weight": "0.28%",
    "Price": 248.11,
    "Chg": -19.78,
    "% Chg": "(-7.38%)"
  },
  {
    "#": 72,
    "Company": "The Charles Schwab Corporation",
    "Symbol": "SCHW",
    "Weight": "0.28%",
    "Price": 69.06,
    "Chg": -5.81,
    "% Chg": "(-7.76%)"
  },
  {
    "#": 73,
    "Company": "Danaher Corporation",
    "Symbol": "DHR",
    "Weight": "0.28%",
    "Price": 181.77,
    "Chg": -16.13,
    "% Chg": "(-8.15%)"
  },
  {
    "#": 74,
    "Company": "Stryker Corporation",
    "Symbol": "SYK",
    "Weight": "0.28%",
    "Price": 345.8,
    "Chg": -22.35,
    "% Chg": "(-6.07%)"
  },
  {
    "#": 75,
    "Company": "Lowe's Companies Inc.",
    "Symbol": "LOW",
    "Weight": "0.27%",
    "Price": 223.29,
    "Chg": 0.77,
    "% Chg": "(0.35%)"
  },
  {
    "#": 76,
    "Company": "Vertex Pharmaceuticals Inc",
    "Symbol": "VRTX",
    "Weight": "0.27%",
    "Price": 474.62,
    "Chg": -9.39,
    "% Chg": "(-1.94%)"
  },
  {
    "#": 77,
    "Company": "Automatic Data Processing",
    "Symbol": "ADP",
    "Weight": "0.27%",
    "Price": 286.13,
    "Chg": -19.26,
    "% Chg": "(-6.31%)"
  },
  {
    "#": 78,
    "Company": "Fiserv, Inc.",
    "Symbol": "FI",
    "Weight": "0.27%",
    "Price": 198.6,
    "Chg": -18.3,
    "% Chg": "(-8.44%)"
  },
  {
    "#": 79,
    "Company": "Conocophillips",
    "Symbol": "COP",
    "Weight": "0.27%",
    "Price": 86.29,
    "Chg": -8.96,
    "% Chg": "(-9.41%)"
  },
  {
    "#": 80,
    "Company": "Marsh & Mclennan Companies, Inc.",
    "Symbol": "MMC",
    "Weight": "0.26%",
    "Price": 230.2,
    "Chg": -14.07,
    "% Chg": "(-5.76%)"
  },
  {
    "#": 81,
    "Company": "Citigroup Inc.",
    "Symbol": "C",
    "Weight": "0.26%",
    "Price": 58.13,
    "Chg": -4.92,
    "% Chg": "(-7.80%)"
  },
  {
    "#": 82,
    "Company": "Bristol-Myers Squibb Co.",
    "Symbol": "BMY",
    "Weight": "0.25%",
    "Price": 55.3,
    "Chg": -2.52,
    "% Chg": "(-4.36%)"
  },
  {
    "#": 83,
    "Company": "Deere & Company",
    "Symbol": "DE",
    "Weight": "0.25%",
    "Price": 429.86,
    "Chg": -17.59,
    "% Chg": "(-3.93%)"
  },
  {
    "#": 84,
    "Company": "Boeing Company",
    "Symbol": "BA",
    "Weight": "0.25%",
    "Price": 136.59,
    "Chg": -14.32,
    "% Chg": "(-9.49%)"
  },
  {
    "#": 85,
    "Company": "Chubb Limited",
    "Symbol": "CB",
    "Weight": "0.25%",
    "Price": 280.68,
    "Chg": -21.78,
    "% Chg": "(-7.20%)"
  },
  {
    "#": 86,
    "Company": "Medtronic Plc",
    "Symbol": "MDT",
    "Weight": "0.25%",
    "Price": 82.88,
    "Chg": -5.01,
    "% Chg": "(-5.70%)"
  },
  {
    "#": 87,
    "Company": "Applied Materials Inc",
    "Symbol": "AMAT",
    "Weight": "0.24%",
    "Price": 126.95,
    "Chg": -8.56,
    "% Chg": "(-6.32%)"
  },
  {
    "#": 88,
    "Company": "Palo Alto Networks, Inc.",
    "Symbol": "PANW",
    "Weight": "0.24%",
    "Price": 153.57,
    "Chg": -11.6,
    "% Chg": "(-7.02%)"
  },
  {
    "#": 89,
    "Company": "American Tower Corporation",
    "Symbol": "AMT",
    "Weight": "0.23%",
    "Price": 220.17,
    "Chg": -8.02,
    "% Chg": "(-3.51%)"
  },
  {
    "#": 90,
    "Company": "Elevance Health, Inc.",
    "Symbol": "ELV",
    "Weight": "0.23%",
    "Price": 428.89,
    "Chg": -23.8,
    "% Chg": "(-5.26%)"
  },
  {
    "#": 91,
    "Company": "Eaton Corporation, Plcs",
    "Symbol": "ETN",
    "Weight": "0.23%",
    "Price": 246.52,
    "Chg": -14.33,
    "% Chg": "(-5.49%)"
  },
  {
    "#": 92,
    "Company": "The Southern Company",
    "Symbol": "SO",
    "Weight": "0.22%",
    "Price": 88.94,
    "Chg": -3.62,
    "% Chg": "(-3.91%)"
  },
  {
    "#": 93,
    "Company": "Starbucks Corp",
    "Symbol": "SBUX",
    "Weight": "0.22%",
    "Price": 82.1,
    "Chg": -6.16,
    "% Chg": "(-6.98%)"
  },
  {
    "#": 94,
    "Company": "Altria Group, Inc.",
    "Symbol": "MO",
    "Weight": "0.21%",
    "Price": 56.07,
    "Chg": -1.82,
    "% Chg": "(-3.14%)"
  },
  {
    "#": 95,
    "Company": "Blackstone Inc.",
    "Symbol": "BX",
    "Weight": "0.21%",
    "Price": 125.04,
    "Chg": -8.06,
    "% Chg": "(-6.06%)"
  },
  {
    "#": 96,
    "Company": "Intel Corp",
    "Symbol": "INTC",
    "Weight": "0.21%",
    "Price": 19.85,
    "Chg": -2.58,
    "% Chg": "(-11.50%)"
  },
  {
    "#": 97,
    "Company": "Cme Group Inc.",
    "Symbol": "CME",
    "Weight": "0.21%",
    "Price": 254.46,
    "Chg": -13.9,
    "% Chg": "(-5.18%)"
  },
  {
    "#": 98,
    "Company": "Duke Energy Corporation",
    "Symbol": "DUK",
    "Weight": "0.21%",
    "Price": 118.93,
    "Chg": -5.12,
    "% Chg": "(-4.13%)"
  },
  {
    "#": 99,
    "Company": "Intercontinental Exchange Inc.",
    "Symbol": "ICE",
    "Weight": "0.21%",
    "Price": 156.74,
    "Chg": -10.82,
    "% Chg": "(-6.46%)"
  },
  {
    "#": 100,
    "Company": "Lockheed Martin Corp.",
    "Symbol": "LMT",
    "Weight": "0.21%",
    "Price": 432.15,
    "Chg": -22.63,
    "% Chg": "(-4.98%)"
  },
  {
    "#": 101,
    "Company": "Prologis, Inc.",
    "Symbol": "PLD",
    "Weight": "0.21%",
    "Price": 98.23,
    "Chg": -3.36,
    "% Chg": "(-3.31%)"
  },
  {
    "#": 102,
    "Company": "Welltower Inc.",
    "Symbol": "WELL",
    "Weight": "0.20%",
    "Price": 143.29,
    "Chg": -9.14,
    "% Chg": "(-6.00%)"
  },
  {
    "#": 103,
    "Company": "The Cigna Group",
    "Symbol": "CI",
    "Weight": "0.20%",
    "Price": 322.4,
    "Chg": -16.05,
    "% Chg": "(-4.74%)"
  },
  {
    "#": 104,
    "Company": "Mckesson Corporation",
    "Symbol": "MCK",
    "Weight": "0.20%",
    "Price": 683.11,
    "Chg": -33.82,
    "% Chg": "(-4.72%)"
  },
  {
    "#": 105,
    "Company": "Analog Devices, Inc.",
    "Symbol": "ADI",
    "Weight": "0.20%",
    "Price": 164.6,
    "Chg": -16.28,
    "% Chg": "(-9.00%)"
  },
  {
    "#": 106,
    "Company": "Mondelez International, Inc. Class A",
    "Symbol": "MDLZ",
    "Weight": "0.19%",
    "Price": 66.31,
    "Chg": -1.59,
    "% Chg": "(-2.34%)"
  },
  {
    "#": 107,
    "Company": "Arthur J. Gallagher & Co.",
    "Symbol": "AJG",
    "Weight": "0.19%",
    "Price": 319.25,
    "Chg": -25.15,
    "% Chg": "(-7.30%)"
  },
  {
    "#": 108,
    "Company": "Waste Management, Inc.",
    "Symbol": "WM",
    "Weight": "0.19%",
    "Price": 225.2,
    "Chg": -11.63,
    "% Chg": "(-4.91%)"
  },
  {
    "#": 109,
    "Company": "Crowdstrike Holdings, Inc. Class A",
    "Symbol": "CRWD",
    "Weight": "0.19%",
    "Price": 321.63,
    "Chg": -25.76,
    "% Chg": "(-7.42%)"
  },
  {
    "#": 110,
    "Company": "Aon Plc Class A",
    "Symbol": "AON",
    "Weight": "0.19%",
    "Price": 375.76,
    "Chg": -18.53,
    "% Chg": "(-4.70%)"
  },
  {
    "#": 111,
    "Company": "Cvs Health Corporation",
    "Symbol": "CVS",
    "Weight": "0.19%",
    "Price": 63.66,
    "Chg": -3.85,
    "% Chg": "(-5.70%)"
  },
  {
    "#": 112,
    "Company": "Lam Research Corp",
    "Symbol": "LRCX",
    "Weight": "0.18%",
    "Price": 59.09,
    "Chg": -6.13,
    "% Chg": "(-9.40%)"
  },
  {
    "#": 113,
    "Company": "O'reilly Automotive, Inc.",
    "Symbol": "ORLY",
    "Weight": "0.18%",
    "Price": 1389.87,
    "Chg": -52.02,
    "% Chg": "(-3.61%)"
  },
  {
    "#": 114,
    "Company": "Micron Technology, Inc.",
    "Symbol": "MU",
    "Weight": "0.18%",
    "Price": 64.72,
    "Chg": -9.62,
    "% Chg": "(-12.94%)"
  },
  {
    "#": 115,
    "Company": "Kla Corporation",
    "Symbol": "KLAC",
    "Weight": "0.18%",
    "Price": 576.53,
    "Chg": -44.29,
    "% Chg": "(-7.13%)"
  },
  {
    "#": 116,
    "Company": "Ge Vernova Inc.",
    "Symbol": "GEV",
    "Weight": "0.18%",
    "Price": 271.48,
    "Chg": -26.18,
    "% Chg": "(-8.80%)"
  },
  {
    "#": 117,
    "Company": "The Sherwin-Williams Company",
    "Symbol": "SHW",
    "Weight": "0.17%",
    "Price": 332.06,
    "Chg": -8.59,
    "% Chg": "(-2.52%)"
  },
  {
    "#": 118,
    "Company": "Equinix, Inc. Reit",
    "Symbol": "EQIX",
    "Weight": "0.17%",
    "Price": 766.21,
    "Chg": -35.23,
    "% Chg": "(-4.40%)"
  },
  {
    "#": 119,
    "Company": "Colgate-Palmolive Company",
    "Symbol": "CL",
    "Weight": "0.17%",
    "Price": 91.66,
    "Chg": -4.34,
    "% Chg": "(-4.52%)"
  },
  {
    "#": 120,
    "Company": "Transdigm Group Incorporated",
    "Symbol": "TDG",
    "Weight": "0.17%",
    "Price": 1237.85,
    "Chg": -125.57,
    "% Chg": "(-9.21%)"
  },
  {
    "#": 121,
    "Company": "Amphenol Corporation",
    "Symbol": "APH",
    "Weight": "0.17%",
    "Price": 59.09,
    "Chg": -3.57,
    "% Chg": "(-5.70%)"
  },
  {
    "#": 122,
    "Company": "3m Company",
    "Symbol": "MMM",
    "Weight": "0.17%",
    "Price": 126.91,
    "Chg": -12.83,
    "% Chg": "(-9.18%)"
  },
  {
    "#": 123,
    "Company": "Trane Technologies Plc",
    "Symbol": "TT",
    "Weight": "0.16%",
    "Price": 318.11,
    "Chg": -12.93,
    "% Chg": "(-3.91%)"
  },
  {
    "#": 124,
    "Company": "Arista Networks",
    "Symbol": "ANET",
    "Weight": "0.16%",
    "Price": 64.37,
    "Chg": -6.9,
    "% Chg": "(-9.68%)"
  },
  {
    "#": 125,
    "Company": "United Parcel Service, Inc. Class B",
    "Symbol": "UPS",
    "Weight": "0.16%",
    "Price": 97.71,
    "Chg": -2.41,
    "% Chg": "(-2.41%)"
  },
  {
    "#": 126,
    "Company": "Motorola Solutions, Inc.",
    "Symbol": "MSI",
    "Weight": "0.16%",
    "Price": 402.13,
    "Chg": -33.37,
    "% Chg": "(-7.66%)"
  },
  {
    "#": 127,
    "Company": "Williams Companies Inc.",
    "Symbol": "WMB",
    "Weight": "0.16%",
    "Price": 54.57,
    "Chg": -4.46,
    "% Chg": "(-7.56%)"
  },
  {
    "#": 128,
    "Company": "Parker-Hannifin Corporation",
    "Symbol": "PH",
    "Weight": "0.16%",
    "Price": 517.23,
    "Chg": -39.47,
    "% Chg": "(-7.09%)"
  },
  {
    "#": 129,
    "Company": "Zoetis Inc.",
    "Symbol": "ZTS",
    "Weight": "0.16%",
    "Price": 151.73,
    "Chg": -7.88,
    "% Chg": "(-4.94%)"
  },
  {
    "#": 130,
    "Company": "Cintas Corp",
    "Symbol": "CTAS",
    "Weight": "0.15%",
    "Price": 190.33,
    "Chg": -14.52,
    "% Chg": "(-7.09%)"
  },
  {
    "#": 131,
    "Company": "Northrop Grumman Corp.",
    "Symbol": "NOC",
    "Weight": "0.15%",
    "Price": 485.52,
    "Chg": -29.65,
    "% Chg": "(-5.76%)"
  },
  {
    "#": 132,
    "Company": "Kkr & Co. Inc.",
    "Symbol": "KKR",
    "Weight": "0.15%",
    "Price": 92.79,
    "Chg": -9.76,
    "% Chg": "(-9.52%)"
  },
  {
    "#": 133,
    "Company": "Moody's Corporation",
    "Symbol": "MCO",
    "Weight": "0.15%",
    "Price": 402.43,
    "Chg": -39.96,
    "% Chg": "(-9.03%)"
  },
  {
    "#": 134,
    "Company": "General Dynamics Corporation",
    "Symbol": "GD",
    "Weight": "0.15%",
    "Price": 250.01,
    "Chg": -19.61,
    "% Chg": "(-7.27%)"
  },
  {
    "#": 135,
    "Company": "Cadence Design Systems",
    "Symbol": "CDNS",
    "Weight": "0.15%",
    "Price": 232.88,
    "Chg": -16.03,
    "% Chg": "(-6.44%)"
  },
  {
    "#": 136,
    "Company": "Chipotle Mexican Grill, Inc.",
    "Symbol": "CMG",
    "Weight": "0.15%",
    "Price": 47.29,
    "Chg": -2.79,
    "% Chg": "(-5.57%)"
  },
  {
    "#": 137,
    "Company": "Eog Resources, Inc.",
    "Symbol": "EOG",
    "Weight": "0.15%",
    "Price": 110.55,
    "Chg": -9.34,
    "% Chg": "(-7.79%)"
  },
  {
    "#": 138,
    "Company": "Nike, Inc.",
    "Symbol": "NKE",
    "Weight": "0.14%",
    "Price": 57.25,
    "Chg": 1.67,
    "% Chg": "(3.00%)"
  },
  {
    "#": 139,
    "Company": "Synopsys Inc",
    "Symbol": "SNPS",
    "Weight": "0.14%",
    "Price": 388.13,
    "Chg": -29.63,
    "% Chg": "(-7.09%)"
  },
  {
    "#": 140,
    "Company": "Regeneron Pharmaceuticals Inc",
    "Symbol": "REGN",
    "Weight": "0.14%",
    "Price": 573.45,
    "Chg": -37.19,
    "% Chg": "(-6.09%)"
  },
  {
    "#": 141,
    "Company": "Autozone, Inc.",
    "Symbol": "AZO",
    "Weight": "0.14%",
    "Price": 3653.24,
    "Chg": -172.91,
    "% Chg": "(-4.52%)"
  },
  {
    "#": 142,
    "Company": "Illinois Tool Works Inc.",
    "Symbol": "ITW",
    "Weight": "0.14%",
    "Price": 225.57,
    "Chg": -13.87,
    "% Chg": "(-5.79%)"
  },
  {
    "#": 143,
    "Company": "Pnc Financial Services Group",
    "Symbol": "PNC",
    "Weight": "0.14%",
    "Price": 153.1,
    "Chg": -8.19,
    "% Chg": "(-5.08%)"
  },
  {
    "#": 144,
    "Company": "Becton, Dickinson and Co.",
    "Symbol": "BDX",
    "Weight": "0.14%",
    "Price": 207.34,
    "Chg": -14.25,
    "% Chg": "(-6.43%)"
  },
  {
    "#": 145,
    "Company": "Ecolab, Inc.",
    "Symbol": "ECL",
    "Weight": "0.14%",
    "Price": 237.77,
    "Chg": -12.47,
    "% Chg": "(-4.98%)"
  },
  {
    "#": 146,
    "Company": "Air Products & Chemicals, Inc.",
    "Symbol": "APD",
    "Weight": "0.14%",
    "Price": 263.47,
    "Chg": -19.73,
    "% Chg": "(-6.97%)"
  },
  {
    "#": 147,
    "Company": "Capital One Financial",
    "Symbol": "COF",
    "Weight": "0.14%",
    "Price": 150.57,
    "Chg": -13.47,
    "% Chg": "(-8.21%)"
  },
  {
    "#": 148,
    "Company": "Hca Healthcare, Inc.",
    "Symbol": "HCA",
    "Weight": "0.14%",
    "Price": 331.65,
    "Chg": -17.49,
    "% Chg": "(-5.01%)"
  },
  {
    "#": 149,
    "Company": "Roper Technologies, Inc.",
    "Symbol": "ROP",
    "Weight": "0.14%",
    "Price": 541.8,
    "Chg": -37.9,
    "% Chg": "(-6.54%)"
  },
  {
    "#": 150,
    "Company": "Paypal Holdings, Inc.",
    "Symbol": "PYPL",
    "Weight": "0.13%",
    "Price": 58.37,
    "Chg": -3.34,
    "% Chg": "(-5.41%)"
  },
  {
    "#": 151,
    "Company": "U.S. Bancorp",
    "Symbol": "USB",
    "Weight": "0.13%",
    "Price": 36.83,
    "Chg": -1.96,
    "% Chg": "(-5.05%)"
  },
  {
    "#": 152,
    "Company": "The Travelers Companies, Inc.",
    "Symbol": "TRV",
    "Weight": "0.13%",
    "Price": 242.26,
    "Chg": -20.84,
    "% Chg": "(-7.92%)"
  },
  {
    "#": 153,
    "Company": "Constellation Energy Corporation",
    "Symbol": "CEG",
    "Weight": "0.13%",
    "Price": 170.96,
    "Chg": -19.28,
    "% Chg": "(-10.13%)"
  },
  {
    "#": 154,
    "Company": "Doordash, Inc. Class A",
    "Symbol": "DASH",
    "Weight": "0.13%",
    "Price": 163.16,
    "Chg": -10.83,
    "% Chg": "(-6.22%)"
  },
  {
    "#": 155,
    "Company": "American Electric Power Company, Inc.",
    "Symbol": "AEP",
    "Weight": "0.13%",
    "Price": 104.48,
    "Chg": -4.63,
    "% Chg": "(-4.24%)"
  },
  {
    "#": 156,
    "Company": "Oneok, Inc.",
    "Symbol": "OKE",
    "Weight": "0.13%",
    "Price": 80.86,
    "Chg": -11.84,
    "% Chg": "(-12.77%)"
  },
  {
    "#": 157,
    "Company": "Emerson Electric Co.",
    "Symbol": "EMR",
    "Weight": "0.13%",
    "Price": 94.57,
    "Chg": -7.32,
    "% Chg": "(-7.18%)"
  },
  {
    "#": 158,
    "Company": "Bank of New York Mellon Corporation",
    "Symbol": "BK",
    "Weight": "0.13%",
    "Price": 73.31,
    "Chg": -6.6,
    "% Chg": "(-8.26%)"
  },
  {
    "#": 159,
    "Company": "Fortinet, Inc.",
    "Symbol": "FTNT",
    "Weight": "0.12%",
    "Price": 84.71,
    "Chg": -4.73,
    "% Chg": "(-5.29%)"
  },
  {
    "#": 160,
    "Company": "Autodesk Inc",
    "Symbol": "ADSK",
    "Weight": "0.12%",
    "Price": 245.51,
    "Chg": -11.64,
    "% Chg": "(-4.53%)"
  },
  {
    "#": 161,
    "Company": "Aflac Inc.",
    "Symbol": "AFL",
    "Weight": "0.12%",
    "Price": 101.98,
    "Chg": -9.77,
    "% Chg": "(-8.74%)"
  },
  {
    "#": 162,
    "Company": "Apollo Global Management, Inc.",
    "Symbol": "APO",
    "Weight": "0.12%",
    "Price": 108.68,
    "Chg": -14.77,
    "% Chg": "(-11.96%)"
  },
  {
    "#": 163,
    "Company": "Newmont Corporation",
    "Symbol": "NEM",
    "Weight": "0.12%",
    "Price": 44.18,
    "Chg": -4.15,
    "% Chg": "(-8.59%)"
  },
  {
    "#": 164,
    "Company": "Schlumberger Limited",
    "Symbol": "SLB",
    "Weight": "0.12%",
    "Price": 34.78,
    "Chg": -4.43,
    "% Chg": "(-11.30%)"
  },
  {
    "#": 165,
    "Company": "The Allstate Corporation",
    "Symbol": "ALL",
    "Weight": "0.12%",
    "Price": 186.57,
    "Chg": -18.75,
    "% Chg": "(-9.13%)"
  },
  {
    "#": 166,
    "Company": "Csx Corporation",
    "Symbol": "CSX",
    "Weight": "0.12%",
    "Price": 27.21,
    "Chg": -0.78,
    "% Chg": "(-2.79%)"
  },
  {
    "#": 167,
    "Company": "Kinder Morgan, Inc.",
    "Symbol": "KMI",
    "Weight": "0.12%",
    "Price": 25.29,
    "Chg": -2.43,
    "% Chg": "(-8.77%)"
  },
  {
    "#": 168,
    "Company": "Hilton Worldwide Holdings Inc.",
    "Symbol": "HLT",
    "Weight": "0.11%",
    "Price": 208.85,
    "Chg": -8.53,
    "% Chg": "(-3.92%)"
  },
  {
    "#": 169,
    "Company": "Marriot International Class A",
    "Symbol": "MAR",
    "Weight": "0.11%",
    "Price": 214.58,
    "Chg": -10.04,
    "% Chg": "(-4.47%)"
  },
  {
    "#": 170,
    "Company": "American International Group, Inc.",
    "Symbol": "AIG",
    "Weight": "0.11%",
    "Price": 78.95,
    "Chg": -7.25,
    "% Chg": "(-8.41%)"
  },
  {
    "#": 171,
    "Company": "Johnson Controls International Plc",
    "Symbol": "JCI",
    "Weight": "0.11%",
    "Price": 71.7,
    "Chg": -5.53,
    "% Chg": "(-7.16%)"
  },
  {
    "#": 172,
    "Company": "Howmet Aerospace Inc.",
    "Symbol": "HWM",
    "Weight": "0.11%",
    "Price": 112.33,
    "Chg": -12.67,
    "% Chg": "(-10.14%)"
  },
  {
    "#": 173,
    "Company": "Republic Services Inc.",
    "Symbol": "RSG",
    "Weight": "0.11%",
    "Price": 235.42,
    "Chg": -13.02,
    "% Chg": "(-5.24%)"
  },
  {
    "#": 174,
    "Company": "Norfolk Southern Corp.",
    "Symbol": "NSC",
    "Weight": "0.11%",
    "Price": 210.93,
    "Chg": -9.81,
    "% Chg": "(-4.44%)"
  },
  {
    "#": 175,
    "Company": "Cencora, Inc.",
    "Symbol": "COR",
    "Weight": "0.11%",
    "Price": 278.39,
    "Chg": -10.97,
    "% Chg": "(-3.79%)"
  },
  {
    "#": 176,
    "Company": "Realty Income Corporation",
    "Symbol": "O",
    "Weight": "0.11%",
    "Price": 55.15,
    "Chg": -1.91,
    "% Chg": "(-3.35%)"
  },
  {
    "#": 177,
    "Company": "Copart Inc",
    "Symbol": "CPRT",
    "Weight": "0.11%",
    "Price": 54.51,
    "Chg": -2.13,
    "% Chg": "(-3.76%)"
  },
  {
    "#": 178,
    "Company": "Airbnb, Inc. Class A",
    "Symbol": "ABNB",
    "Weight": "0.11%",
    "Price": 106.66,
    "Chg": -7.31,
    "% Chg": "(-6.41%)"
  },
  {
    "#": 179,
    "Company": "Paychex Inc",
    "Symbol": "PAYX",
    "Weight": "0.11%",
    "Price": 143.32,
    "Chg": -10.21,
    "% Chg": "(-6.65%)"
  },
  {
    "#": 180,
    "Company": "Carrier Global Corporation",
    "Symbol": "CARR",
    "Weight": "0.11%",
    "Price": 57.18,
    "Chg": -3.54,
    "% Chg": "(-5.83%)"
  },
  {
    "#": 181,
    "Company": "Workday, Inc. Class A",
    "Symbol": "WDAY",
    "Weight": "0.11%",
    "Price": 217.14,
    "Chg": -11.19,
    "% Chg": "(-4.90%)"
  },
  {
    "#": 182,
    "Company": "Truist Financial Corporation",
    "Symbol": "TFC",
    "Weight": "0.11%",
    "Price": 34.79,
    "Chg": -2.25,
    "% Chg": "(-6.07%)"
  },
  {
    "#": 183,
    "Company": "Paccar Inc",
    "Symbol": "PCAR",
    "Weight": "0.11%",
    "Price": 90.88,
    "Chg": -1.48,
    "% Chg": "(-1.60%)"
  },
  {
    "#": 184,
    "Company": "Kimberly-Clark Corp.",
    "Symbol": "KMB",
    "Weight": "0.11%",
    "Price": 137.91,
    "Chg": -7.31,
    "% Chg": "(-5.03%)"
  },
  {
    "#": 185,
    "Company": "Freeport-Mcmoran Inc.",
    "Symbol": "FCX",
    "Weight": "0.11%",
    "Price": 29.15,
    "Chg": -4.36,
    "% Chg": "(-13.01%)"
  },
  {
    "#": 186,
    "Company": "Fedex Corporation",
    "Symbol": "FDX",
    "Weight": "0.10%",
    "Price": 210.12,
    "Chg": -5.74,
    "% Chg": "(-2.66%)"
  },
  {
    "#": 187,
    "Company": "Exelon Corporation",
    "Symbol": "EXC",
    "Weight": "0.10%",
    "Price": 45.35,
    "Chg": -1.88,
    "% Chg": "(-3.98%)"
  },
  {
    "#": 188,
    "Company": "Dominion Energy, Inc.",
    "Symbol": "D",
    "Weight": "0.10%",
    "Price": 52.73,
    "Chg": -3.52,
    "% Chg": "(-6.26%)"
  },
  {
    "#": 189,
    "Company": "The Kroger Co.",
    "Symbol": "KR",
    "Weight": "0.10%",
    "Price": 67.18,
    "Chg": -3.56,
    "% Chg": "(-5.03%)"
  },
  {
    "#": 190,
    "Company": "Simon Property Group, Inc.",
    "Symbol": "SPG",
    "Weight": "0.10%",
    "Price": 146.05,
    "Chg": -7.13,
    "% Chg": "(-4.65%)"
  },
  {
    "#": 191,
    "Company": "Royal Caribbean Group",
    "Symbol": "RCL",
    "Weight": "0.10%",
    "Price": 177.93,
    "Chg": -10.72,
    "% Chg": "(-5.68%)"
  },
  {
    "#": 192,
    "Company": "Crown Castle Inc.",
    "Symbol": "CCI",
    "Weight": "0.10%",
    "Price": 100.98,
    "Chg": -6.08,
    "% Chg": "(-5.68%)"
  },
  {
    "#": 193,
    "Company": "Public Storage",
    "Symbol": "PSA",
    "Weight": "0.10%",
    "Price": 284.53,
    "Chg": -10.21,
    "% Chg": "(-3.46%)"
  },
  {
    "#": 194,
    "Company": "General Motors Company",
    "Symbol": "GM",
    "Weight": "0.10%",
    "Price": 44.18,
    "Chg": -1.72,
    "% Chg": "(-3.75%)"
  },
  {
    "#": 195,
    "Company": "Kenvue Inc.",
    "Symbol": "KVUE",
    "Weight": "0.10%",
    "Price": 22.33,
    "Chg": -1.29,
    "% Chg": "(-5.46%)"
  },
  {
    "#": 196,
    "Company": "Yum! Brands, Inc.",
    "Symbol": "YUM",
    "Weight": "0.10%",
    "Price": 147.83,
    "Chg": -13.62,
    "% Chg": "(-8.44%)"
  },
  {
    "#": 197,
    "Company": "Sempra",
    "Symbol": "SRE",
    "Weight": "0.10%",
    "Price": 65.88,
    "Chg": -4.85,
    "% Chg": "(-6.86%)"
  },
  {
    "#": 198,
    "Company": "Fastenal Co",
    "Symbol": "FAST",
    "Weight": "0.10%",
    "Price": 74.42,
    "Chg": -3.59,
    "% Chg": "(-4.60%)"
  },
  {
    "#": 199,
    "Company": "Digital Realty Trust, Inc.",
    "Symbol": "DLR",
    "Weight": "0.10%",
    "Price": 137.5,
    "Chg": -3.59,
    "% Chg": "(-2.54%)"
  },
  {
    "#": 200,
    "Company": "Phillips 66",
    "Symbol": "PSX",
    "Weight": "0.10%",
    "Price": 98.81,
    "Chg": -8.37,
    "% Chg": "(-7.81%)"
  },
  {
    "#": 201,
    "Company": "Metlife, Inc.",
    "Symbol": "MET",
    "Weight": "0.10%",
    "Price": 69.07,
    "Chg": -6.84,
    "% Chg": "(-9.01%)"
  },
  {
    "#": 202,
    "Company": "Fair Isaac Corporation",
    "Symbol": "FICO",
    "Weight": "0.10%",
    "Price": 1673.98,
    "Chg": -127.07,
    "% Chg": "(-7.06%)"
  },
  {
    "#": 203,
    "Company": "Ameriprise Financial, Inc.",
    "Symbol": "AMP",
    "Weight": "0.10%",
    "Price": 422.19,
    "Chg": -33.62,
    "% Chg": "(-7.38%)"
  },
  {
    "#": 204,
    "Company": "Nxp Semiconductors N.v.",
    "Symbol": "NXPI",
    "Weight": "0.10%",
    "Price": 160.81,
    "Chg": -11.07,
    "% Chg": "(-6.44%)"
  },
  {
    "#": 205,
    "Company": "Ross Stores Inc",
    "Symbol": "ROST",
    "Weight": "0.09%",
    "Price": 130.31,
    "Chg": -0.9,
    "% Chg": "(-0.69%)"
  },
  {
    "#": 206,
    "Company": "Target Corporation",
    "Symbol": "TGT",
    "Weight": "0.09%",
    "Price": 95.72,
    "Chg": 1.44,
    "% Chg": "(1.53%)"
  },
  {
    "#": 207,
    "Company": "W.W. Grainger, Inc.",
    "Symbol": "GWW",
    "Weight": "0.09%",
    "Price": 942.43,
    "Chg": -30.98,
    "% Chg": "(-3.18%)"
  },
  {
    "#": 208,
    "Company": "Verisk Analytics, Inc.",
    "Symbol": "VRSK",
    "Weight": "0.09%",
    "Price": 284.99,
    "Chg": -20.1,
    "% Chg": "(-6.59%)"
  },
  {
    "#": 209,
    "Company": "Edwards Lifesciences Corp",
    "Symbol": "EW",
    "Weight": "0.09%",
    "Price": 69.36,
    "Chg": -3.62,
    "% Chg": "(-4.96%)"
  },
  {
    "#": 210,
    "Company": "Keurig Dr Pepper Inc.",
    "Symbol": "KDP",
    "Weight": "0.09%",
    "Price": 33.81,
    "Chg": -1.82,
    "% Chg": "(-5.11%)"
  },
  {
    "#": 211,
    "Company": "Msci, Inc.",
    "Symbol": "MSCI",
    "Weight": "0.09%",
    "Price": 507.44,
    "Chg": -36.74,
    "% Chg": "(-6.75%)"
  },
  {
    "#": 212,
    "Company": "Corteva, Inc.",
    "Symbol": "CTVA",
    "Weight": "0.09%",
    "Price": 55.79,
    "Chg": -5.51,
    "% Chg": "(-8.99%)"
  },
  {
    "#": 213,
    "Company": "Monster Beverage Corporation",
    "Symbol": "MNST",
    "Weight": "0.09%",
    "Price": 57.08,
    "Chg": -2.57,
    "% Chg": "(-4.31%)"
  },
  {
    "#": 214,
    "Company": "Xcel Energy, Inc.",
    "Symbol": "XEL",
    "Weight": "0.09%",
    "Price": 67.89,
    "Chg": -4.25,
    "% Chg": "(-5.89%)"
  },
  {
    "#": 215,
    "Company": "Otis Worldwide Corporation",
    "Symbol": "OTIS",
    "Weight": "0.09%",
    "Price": 94.97,
    "Chg": -9.33,
    "% Chg": "(-8.95%)"
  },
  {
    "#": 216,
    "Company": "Hess Corporation",
    "Symbol": "HES",
    "Weight": "0.09%",
    "Price": 133.56,
    "Chg": -14.82,
    "% Chg": "(-9.99%)"
  },
  {
    "#": 217,
    "Company": "Public Service Enterprise Group Incorporated",
    "Symbol": "PEG",
    "Weight": "0.09%",
    "Price": 77.73,
    "Chg": -3.82,
    "% Chg": "(-4.68%)"
  },
  {
    "#": 218,
    "Company": "Marathon Petroleum Corporation",
    "Symbol": "MPC",
    "Weight": "0.09%",
    "Price": 121.07,
    "Chg": -7.52,
    "% Chg": "(-5.85%)"
  },
  {
    "#": 219,
    "Company": "Cummins Inc.",
    "Symbol": "CMI",
    "Weight": "0.09%",
    "Price": 277.62,
    "Chg": -17.73,
    "% Chg": "(-6.00%)"
  },
  {
    "#": 220,
    "Company": "Discover Financial Services",
    "Symbol": "DFS",
    "Weight": "0.09%",
    "Price": 147.04,
    "Chg": -14.22,
    "% Chg": "(-8.82%)"
  },
  {
    "#": 221,
    "Company": "Baker Hughes Company",
    "Symbol": "BKR",
    "Weight": "0.09%",
    "Price": 35.41,
    "Chg": -5.45,
    "% Chg": "(-13.34%)"
  },
  {
    "#": 222,
    "Company": "L3harris Technologies, Inc.",
    "Symbol": "LHX",
    "Weight": "0.09%",
    "Price": 202.06,
    "Chg": -7.88,
    "% Chg": "(-3.75%)"
  },
  {
    "#": 223,
    "Company": "Fidelity National Information Services, Inc.",
    "Symbol": "FIS",
    "Weight": "0.09%",
    "Price": 69.9,
    "Chg": -4.61,
    "% Chg": "(-6.19%)"
  },
  {
    "#": 224,
    "Company": "Targa Resources Corp.",
    "Symbol": "TRGP",
    "Weight": "0.09%",
    "Price": 161.19,
    "Chg": -19.53,
    "% Chg": "(-10.81%)"
  },
  {
    "#": 225,
    "Company": "Axon Enterprise, Inc.",
    "Symbol": "AXON",
    "Weight": "0.09%",
    "Price": 497.13,
    "Chg": -42.56,
    "% Chg": "(-7.89%)"
  },
  {
    "#": 226,
    "Company": "Consolidated Edison, Inc.",
    "Symbol": "ED",
    "Weight": "0.09%",
    "Price": 109.32,
    "Chg": -3.4,
    "% Chg": "(-3.02%)"
  },
  {
    "#": 227,
    "Company": "Te Connectivity Plc",
    "Symbol": "TEL",
    "Weight": "0.08%",
    "Price": 122,
    "Chg": -7.98,
    "% Chg": "(-6.14%)"
  },
  {
    "#": 228,
    "Company": "United Rentals, Inc.",
    "Symbol": "URI",
    "Weight": "0.08%",
    "Price": 564.57,
    "Chg": -26.6,
    "% Chg": "(-4.50%)"
  },
  {
    "#": 229,
    "Company": "Pg&e Corporation",
    "Symbol": "PCG",
    "Weight": "0.08%",
    "Price": 16.44,
    "Chg": -0.81,
    "% Chg": "(-4.70%)"
  },
  {
    "#": 230,
    "Company": "Ametek, Inc.",
    "Symbol": "AME",
    "Weight": "0.08%",
    "Price": 152.66,
    "Chg": -8.83,
    "% Chg": "(-5.47%)"
  },
  {
    "#": 231,
    "Company": "Quanta Services, Inc.",
    "Symbol": "PWR",
    "Weight": "0.08%",
    "Price": 239.47,
    "Chg": -12.57,
    "% Chg": "(-4.99%)"
  },
  {
    "#": 232,
    "Company": "Ford Motor Company",
    "Symbol": "F",
    "Weight": "0.08%",
    "Price": 9.58,
    "Chg": 0.04,
    "% Chg": "(0.42%)"
  },
  {
    "#": 233,
    "Company": "Prudential Financial, Inc.",
    "Symbol": "PRU",
    "Weight": "0.08%",
    "Price": 96.53,
    "Chg": -8.26,
    "% Chg": "(-7.88%)"
  },
  {
    "#": 234,
    "Company": "Vistra Corp.",
    "Symbol": "VST",
    "Weight": "0.08%",
    "Price": 98.07,
    "Chg": -10.14,
    "% Chg": "(-9.37%)"
  },
  {
    "#": 235,
    "Company": "Sysco Corporation",
    "Symbol": "SYY",
    "Weight": "0.08%",
    "Price": 71.44,
    "Chg": -3.97,
    "% Chg": "(-5.26%)"
  },
  {
    "#": 236,
    "Company": "Cbre Group, Inc.",
    "Symbol": "CBRE",
    "Weight": "0.08%",
    "Price": 118.08,
    "Chg": -5.76,
    "% Chg": "(-4.65%)"
  },
  {
    "#": 237,
    "Company": "Entergy Corporation",
    "Symbol": "ETR",
    "Weight": "0.08%",
    "Price": 79.03,
    "Chg": -6.03,
    "% Chg": "(-7.09%)"
  },
  {
    "#": 238,
    "Company": "Cognizant Technology Solutions",
    "Symbol": "CTSH",
    "Weight": "0.08%",
    "Price": 68.74,
    "Chg": -4.53,
    "% Chg": "(-6.18%)"
  },
  {
    "#": 239,
    "Company": "Valero Energy Corporation",
    "Symbol": "VLO",
    "Weight": "0.08%",
    "Price": 104.69,
    "Chg": -9.6,
    "% Chg": "(-8.40%)"
  },
  {
    "#": 240,
    "Company": "Arch Capital Group Ltd",
    "Symbol": "ACGL",
    "Weight": "0.08%",
    "Price": 87.83,
    "Chg": -8.45,
    "% Chg": "(-8.78%)"
  },
  {
    "#": 241,
    "Company": "Charter Comm Inc Del Cl a",
    "Symbol": "CHTR",
    "Weight": "0.08%",
    "Price": 338.29,
    "Chg": -30.11,
    "% Chg": "(-8.17%)"
  },
  {
    "#": 242,
    "Company": "The Hartford Financial Services Group, Inc.",
    "Symbol": "HIG",
    "Weight": "0.08%",
    "Price": 113.57,
    "Chg": -9.87,
    "% Chg": "(-8.00%)"
  },
  {
    "#": 243,
    "Company": "D.R. Horton Inc.",
    "Symbol": "DHI",
    "Weight": "0.08%",
    "Price": 127.87,
    "Chg": 5.56,
    "% Chg": "(4.55%)"
  },
  {
    "#": 244,
    "Company": "Electronic Arts Inc",
    "Symbol": "EA",
    "Weight": "0.08%",
    "Price": 135.34,
    "Chg": -9.51,
    "% Chg": "(-6.57%)"
  },
  {
    "#": 245,
    "Company": "Wec Energy Group, Inc.",
    "Symbol": "WEC",
    "Weight": "0.08%",
    "Price": 104.36,
    "Chg": -4.17,
    "% Chg": "(-3.84%)"
  },
  {
    "#": 246,
    "Company": "Take-Two Interactive Software Inc",
    "Symbol": "TTWO",
    "Weight": "0.07%",
    "Price": 194.58,
    "Chg": -14.35,
    "% Chg": "(-6.87%)"
  },
  {
    "#": 247,
    "Company": "Idexx Laboratories Inc",
    "Symbol": "IDXX",
    "Weight": "0.07%",
    "Price": 393.73,
    "Chg": -17.03,
    "% Chg": "(-4.15%)"
  },
  {
    "#": 248,
    "Company": "General Mills, Inc.",
    "Symbol": "GIS",
    "Weight": "0.07%",
    "Price": 59.61,
    "Chg": -1.36,
    "% Chg": "(-2.23%)"
  },
  {
    "#": 249,
    "Company": "Vici Properties Inc.",
    "Symbol": "VICI",
    "Weight": "0.07%",
    "Price": 30.59,
    "Chg": -1.07,
    "% Chg": "(-3.38%)"
  },
  {
    "#": 250,
    "Company": "Cardinal Health, Inc.",
    "Symbol": "CAH",
    "Weight": "0.07%",
    "Price": 129.63,
    "Chg": -7.46,
    "% Chg": "(-5.44%)"
  },
  {
    "#": 251,
    "Company": "Willis Towers Watson Public Limited Companys",
    "Symbol": "WTW",
    "Weight": "0.07%",
    "Price": 308.8,
    "Chg": -23.61,
    "% Chg": "(-7.10%)"
  },
  {
    "#": 252,
    "Company": "Ge Healthcare Technologies Inc.",
    "Symbol": "GEHC",
    "Weight": "0.07%",
    "Price": 60.51,
    "Chg": -11.49,
    "% Chg": "(-15.96%)"
  },
  {
    "#": 253,
    "Company": "Corning Incorporated",
    "Symbol": "GLW",
    "Weight": "0.07%",
    "Price": 39.07,
    "Chg": -3.22,
    "% Chg": "(-7.61%)"
  },
  {
    "#": 254,
    "Company": "Costar Group Inc",
    "Symbol": "CSGP",
    "Weight": "0.07%",
    "Price": 72.62,
    "Chg": -3.73,
    "% Chg": "(-4.89%)"
  },
  {
    "#": 255,
    "Company": "Humana Inc.",
    "Symbol": "HUM",
    "Weight": "0.07%",
    "Price": 253.77,
    "Chg": -11.71,
    "% Chg": "(-4.41%)"
  },
  {
    "#": 256,
    "Company": "Centene Corporation",
    "Symbol": "CNC",
    "Weight": "0.07%",
    "Price": 61.93,
    "Chg": -2.36,
    "% Chg": "(-3.67%)"
  },
  {
    "#": 257,
    "Company": "Ebay Inc",
    "Symbol": "EBAY",
    "Weight": "0.07%",
    "Price": 62.4,
    "Chg": -3.96,
    "% Chg": "(-5.97%)"
  },
  {
    "#": 258,
    "Company": "Resmed Inc.",
    "Symbol": "RMD",
    "Weight": "0.07%",
    "Price": 205.17,
    "Chg": -8.18,
    "% Chg": "(-3.83%)"
  },
  {
    "#": 259,
    "Company": "Vulcan Materials Company",
    "Symbol": "VMC",
    "Weight": "0.07%",
    "Price": 230.74,
    "Chg": -6.44,
    "% Chg": "(-2.72%)"
  },
  {
    "#": 260,
    "Company": "Agilent Technologies Inc.",
    "Symbol": "A",
    "Weight": "0.07%",
    "Price": 103,
    "Chg": -6.67,
    "% Chg": "(-6.08%)"
  },
  {
    "#": 261,
    "Company": "Gartner, Inc.",
    "Symbol": "IT",
    "Weight": "0.07%",
    "Price": 383.24,
    "Chg": -21.71,
    "% Chg": "(-5.36%)"
  },
  {
    "#": 262,
    "Company": "Eqt Corp",
    "Symbol": "EQT",
    "Weight": "0.07%",
    "Price": 46.11,
    "Chg": -5.98,
    "% Chg": "(-11.48%)"
  },
  {
    "#": 263,
    "Company": "Extra Space Storage, Inc.",
    "Symbol": "EXR",
    "Weight": "0.07%",
    "Price": 138.21,
    "Chg": -5.95,
    "% Chg": "(-4.13%)"
  },
  {
    "#": 264,
    "Company": "Nasdaq, Inc.",
    "Symbol": "NDAQ",
    "Weight": "0.07%",
    "Price": 68.25,
    "Chg": -5.54,
    "% Chg": "(-7.51%)"
  },
  {
    "#": 265,
    "Company": "Ventas, Inc.",
    "Symbol": "VTR",
    "Weight": "0.07%",
    "Price": 65.51,
    "Chg": -4.09,
    "% Chg": "(-5.88%)"
  },
  {
    "#": 266,
    "Company": "Tractor Supply Co",
    "Symbol": "TSCO",
    "Weight": "0.07%",
    "Price": 52.4,
    "Chg": -3.37,
    "% Chg": "(-6.04%)"
  },
  {
    "#": 267,
    "Company": "Wabtec Inc.",
    "Symbol": "WAB",
    "Weight": "0.06%",
    "Price": 160.95,
    "Chg": -12.63,
    "% Chg": "(-7.28%)"
  },
  {
    "#": 268,
    "Company": "Martin Marietta Materials",
    "Symbol": "MLM",
    "Weight": "0.06%",
    "Price": 470.7,
    "Chg": -14.27,
    "% Chg": "(-2.94%)"
  },
  {
    "#": 269,
    "Company": "Occidental Petroleum Corporation",
    "Symbol": "OXY",
    "Weight": "0.06%",
    "Price": 40.54,
    "Chg": -3.36,
    "% Chg": "(-7.65%)"
  },
  {
    "#": 270,
    "Company": "Ingersoll Rand Inc.",
    "Symbol": "IR",
    "Weight": "0.06%",
    "Price": 69.7,
    "Chg": -3.82,
    "% Chg": "(-5.20%)"
  },
  {
    "#": 271,
    "Company": "American Water Works Company, Inc",
    "Symbol": "AWK",
    "Weight": "0.06%",
    "Price": 147.23,
    "Chg": -4.73,
    "% Chg": "(-3.11%)"
  },
  {
    "#": 272,
    "Company": "Brown & Brown, Inc.",
    "Symbol": "BRO",
    "Weight": "0.06%",
    "Price": 115.01,
    "Chg": -9.42,
    "% Chg": "(-7.57%)"
  },
  {
    "#": 273,
    "Company": "Old Dominion Freight Line",
    "Symbol": "ODFL",
    "Weight": "0.06%",
    "Price": 152.06,
    "Chg": -3.69,
    "% Chg": "(-2.37%)"
  },
  {
    "#": 274,
    "Company": "Avalonbay Communities, Inc.",
    "Symbol": "AVB",
    "Weight": "0.06%",
    "Price": 191.7,
    "Chg": -14.16,
    "% Chg": "(-6.88%)"
  },
  {
    "#": 275,
    "Company": "Dte Energy Company",
    "Symbol": "DTE",
    "Weight": "0.06%",
    "Price": 131.8,
    "Chg": -7.69,
    "% Chg": "(-5.51%)"
  },
  {
    "#": 276,
    "Company": "Equifax, Incorporated",
    "Symbol": "EFX",
    "Weight": "0.06%",
    "Price": 210.07,
    "Chg": -21.73,
    "% Chg": "(-9.37%)"
  },
  {
    "#": 277,
    "Company": "Lululemon Athletica Inc.",
    "Symbol": "LULU",
    "Weight": "0.06%",
    "Price": 263.7,
    "Chg": 8.05,
    "% Chg": "(3.15%)"
  },
  {
    "#": 278,
    "Company": "Garmin Ltd",
    "Symbol": "GRMN",
    "Weight": "0.06%",
    "Price": 178.46,
    "Chg": -6.88,
    "% Chg": "(-3.71%)"
  },
  {
    "#": 279,
    "Company": "Dupont De Nemours, Inc.",
    "Symbol": "DD",
    "Weight": "0.06%",
    "Price": 59.14,
    "Chg": -8.64,
    "% Chg": "(-12.75%)"
  },
  {
    "#": 280,
    "Company": "Constellation Brands, Inc.",
    "Symbol": "STZ",
    "Weight": "0.06%",
    "Price": 173.86,
    "Chg": -7.63,
    "% Chg": "(-4.20%)"
  },
  {
    "#": 281,
    "Company": "Broadridge Financial Solutions Inc",
    "Symbol": "BR",
    "Weight": "0.06%",
    "Price": 225.04,
    "Chg": -14.87,
    "% Chg": "(-6.20%)"
  },
  {
    "#": 282,
    "Company": "Iqvia Holdings Inc.",
    "Symbol": "IQV",
    "Weight": "0.06%",
    "Price": 154.73,
    "Chg": -12.96,
    "% Chg": "(-7.73%)"
  },
  {
    "#": 283,
    "Company": "Ameren Corporation",
    "Symbol": "AEE",
    "Weight": "0.06%",
    "Price": 95.79,
    "Chg": -5.89,
    "% Chg": "(-5.79%)"
  },
  {
    "#": 284,
    "Company": "Ansys Inc",
    "Symbol": "ANSS",
    "Weight": "0.06%",
    "Price": 286.85,
    "Chg": -23.6,
    "% Chg": "(-7.60%)"
  },
  {
    "#": 285,
    "Company": "M&t Bank Corp.",
    "Symbol": "MTB",
    "Weight": "0.06%",
    "Price": 157.02,
    "Chg": -6.34,
    "% Chg": "(-3.88%)"
  },
  {
    "#": 286,
    "Company": "Church & Dwight Co., Inc.",
    "Symbol": "CHD",
    "Weight": "0.06%",
    "Price": 106.09,
    "Chg": -4.67,
    "% Chg": "(-4.22%)"
  },
  {
    "#": 287,
    "Company": "Rockwell Automation, Inc.",
    "Symbol": "ROK",
    "Weight": "0.06%",
    "Price": 227.11,
    "Chg": -12.05,
    "% Chg": "(-5.04%)"
  },
  {
    "#": 288,
    "Company": "Xylem Inc",
    "Symbol": "XYL",
    "Weight": "0.06%",
    "Price": 104.6,
    "Chg": -6.39,
    "% Chg": "(-5.76%)"
  },
  {
    "#": 289,
    "Company": "The Kraft Heinz Company",
    "Symbol": "KHC",
    "Weight": "0.06%",
    "Price": 29.68,
    "Chg": -1.13,
    "% Chg": "(-3.67%)"
  },
  {
    "#": 290,
    "Company": "Ppl Corporation",
    "Symbol": "PPL",
    "Weight": "0.06%",
    "Price": 34.46,
    "Chg": -1.77,
    "% Chg": "(-4.89%)"
  },
  {
    "#": 291,
    "Company": "Diamondback Energy, Inc.",
    "Symbol": "FANG",
    "Weight": "0.06%",
    "Price": 123.37,
    "Chg": -17.91,
    "% Chg": "(-12.68%)"
  },
  {
    "#": 292,
    "Company": "International Paper Co.",
    "Symbol": "IP",
    "Weight": "0.06%",
    "Price": 47.98,
    "Chg": -1.2,
    "% Chg": "(-2.44%)"
  },
  {
    "#": 293,
    "Company": "Nucor Corporation",
    "Symbol": "NUE",
    "Weight": "0.06%",
    "Price": 103.22,
    "Chg": -6.57,
    "% Chg": "(-5.98%)"
  },
  {
    "#": 294,
    "Company": "Lennar Corporation Class A",
    "Symbol": "LEN",
    "Weight": "0.06%",
    "Price": 111.03,
    "Chg": 2.63,
    "% Chg": "(2.43%)"
  },
  {
    "#": 295,
    "Company": "Godaddy Inc",
    "Symbol": "GDDY",
    "Weight": "0.05%",
    "Price": 164.42,
    "Chg": -13.25,
    "% Chg": "(-7.46%)"
  },
  {
    "#": 296,
    "Company": "Delta Air Lines, Inc.",
    "Symbol": "DAL",
    "Weight": "0.05%",
    "Price": 37.25,
    "Chg": -1.46,
    "% Chg": "(-3.77%)"
  },
  {
    "#": 297,
    "Company": "Sba Communications Corp",
    "Symbol": "SBAC",
    "Weight": "0.05%",
    "Price": 219.91,
    "Chg": -10.96,
    "% Chg": "(-4.75%)"
  },
  {
    "#": 298,
    "Company": "The Hershey Company",
    "Symbol": "HSY",
    "Weight": "0.05%",
    "Price": 162.24,
    "Chg": -4.59,
    "% Chg": "(-2.75%)"
  },
  {
    "#": 299,
    "Company": "Atmos Energy Corporation",
    "Symbol": "ATO",
    "Weight": "0.05%",
    "Price": 147.81,
    "Chg": -7.48,
    "% Chg": "(-4.82%)"
  },
  {
    "#": 300,
    "Company": "Iron Mountain Inc.",
    "Symbol": "IRM",
    "Weight": "0.05%",
    "Price": 77.19,
    "Chg": -5.91,
    "% Chg": "(-7.11%)"
  },
  {
    "#": 301,
    "Company": "Tyler Technologies, Inc.",
    "Symbol": "TYL",
    "Weight": "0.05%",
    "Price": 538.24,
    "Chg": -31.44,
    "% Chg": "(-5.52%)"
  },
  {
    "#": 302,
    "Company": "Centerpoint Energy, Inc.",
    "Symbol": "CNP",
    "Weight": "0.05%",
    "Price": 36.08,
    "Chg": -1.28,
    "% Chg": "(-3.43%)"
  },
  {
    "#": 303,
    "Company": "Dexcom, Inc.",
    "Symbol": "DXCM",
    "Weight": "0.05%",
    "Price": 59.83,
    "Chg": -1.97,
    "% Chg": "(-3.19%)"
  },
  {
    "#": 304,
    "Company": "Ppg Industries, Inc.",
    "Symbol": "PPG",
    "Weight": "0.05%",
    "Price": 99.15,
    "Chg": -4.84,
    "% Chg": "(-4.65%)"
  },
  {
    "#": 305,
    "Company": "Dell Technologies Inc.",
    "Symbol": "DELL",
    "Weight": "0.05%",
    "Price": 71.63,
    "Chg": -5.6,
    "% Chg": "(-7.25%)"
  },
  {
    "#": 306,
    "Company": "State Street Corporation",
    "Symbol": "STT",
    "Weight": "0.05%",
    "Price": 76.25,
    "Chg": -6.58,
    "% Chg": "(-7.94%)"
  },
  {
    "#": 307,
    "Company": "Raymond James Financial, Inc.",
    "Symbol": "RJF",
    "Weight": "0.05%",
    "Price": 123.65,
    "Chg": -6.63,
    "% Chg": "(-5.09%)"
  },
  {
    "#": 308,
    "Company": "Monolithic Power Systems, Inc.",
    "Symbol": "MPWR",
    "Weight": "0.05%",
    "Price": 477.39,
    "Chg": -21.29,
    "% Chg": "(-4.27%)"
  },
  {
    "#": 309,
    "Company": "Fifth Third Bancorp",
    "Symbol": "FITB",
    "Weight": "0.05%",
    "Price": 33.75,
    "Chg": -1.72,
    "% Chg": "(-4.85%)"
  },
  {
    "#": 310,
    "Company": "Darden Restaurants, Inc.",
    "Symbol": "DRI",
    "Weight": "0.05%",
    "Price": 192.38,
    "Chg": -8.3,
    "% Chg": "(-4.14%)"
  },
  {
    "#": 311,
    "Company": "Cboe Global Markets, Inc.",
    "Symbol": "CBOE",
    "Weight": "0.05%",
    "Price": 215.09,
    "Chg": -10.71,
    "% Chg": "(-4.74%)"
  },
  {
    "#": 312,
    "Company": "Keysight Technologies, Inc.",
    "Symbol": "KEYS",
    "Weight": "0.05%",
    "Price": 127.02,
    "Chg": -8.71,
    "% Chg": "(-6.42%)"
  },
  {
    "#": 313,
    "Company": "Equity Residential",
    "Symbol": "EQR",
    "Weight": "0.05%",
    "Price": 63.79,
    "Chg": -4.76,
    "% Chg": "(-6.94%)"
  },
  {
    "#": 314,
    "Company": "Expand Energy Corporation",
    "Symbol": "EXE",
    "Weight": "0.05%",
    "Price": 100.01,
    "Chg": -10.54,
    "% Chg": "(-9.53%)"
  },
  {
    "#": 315,
    "Company": "Veralto Corporation",
    "Symbol": "VLTO",
    "Weight": "0.05%",
    "Price": 88.82,
    "Chg": -5.08,
    "% Chg": "(-5.41%)"
  },
  {
    "#": 316,
    "Company": "Fortive Corporation",
    "Symbol": "FTV",
    "Weight": "0.05%",
    "Price": 64.13,
    "Chg": -3.49,
    "% Chg": "(-5.16%)"
  },
  {
    "#": 317,
    "Company": "Global Payments, Inc.",
    "Symbol": "GPN",
    "Weight": "0.05%",
    "Price": 84.88,
    "Chg": -8.1,
    "% Chg": "(-8.71%)"
  },
  {
    "#": 318,
    "Company": "Texas Pacific Land Corporation",
    "Symbol": "TPL",
    "Weight": "0.05%",
    "Price": 1079,
    "Chg": -141.98,
    "% Chg": "(-11.63%)"
  },
  {
    "#": 319,
    "Company": "Mettler-Toledo International",
    "Symbol": "MTD",
    "Weight": "0.05%",
    "Price": 1022.66,
    "Chg": -72.58,
    "% Chg": "(-6.63%)"
  },
  {
    "#": 320,
    "Company": "Archer Daniels Midland Company",
    "Symbol": "ADM",
    "Weight": "0.05%",
    "Price": 43.32,
    "Chg": -4.25,
    "% Chg": "(-8.93%)"
  },
  {
    "#": 321,
    "Company": "Eversource Energy",
    "Symbol": "ES",
    "Weight": "0.05%",
    "Price": 58.34,
    "Chg": -3.58,
    "% Chg": "(-5.78%)"
  },
  {
    "#": 322,
    "Company": "Edison International",
    "Symbol": "EIX",
    "Weight": "0.05%",
    "Price": 54.75,
    "Chg": -3.63,
    "% Chg": "(-6.22%)"
  },
  {
    "#": 323,
    "Company": "Cms Energy Corporation",
    "Symbol": "CMS",
    "Weight": "0.05%",
    "Price": 72.69,
    "Chg": -2.82,
    "% Chg": "(-3.73%)"
  },
  {
    "#": 324,
    "Company": "Cincinnati Financial Corp",
    "Symbol": "CINF",
    "Weight": "0.05%",
    "Price": 131.69,
    "Chg": -13.01,
    "% Chg": "(-8.99%)"
  },
  {
    "#": 325,
    "Company": "Zimmer Biomet Holdings, Inc.",
    "Symbol": "ZBH",
    "Weight": "0.05%",
    "Price": 107.34,
    "Chg": -5.32,
    "% Chg": "(-4.72%)"
  },
  {
    "#": 326,
    "Company": "Dover Corporation",
    "Symbol": "DOV",
    "Weight": "0.05%",
    "Price": 153.55,
    "Chg": -9.18,
    "% Chg": "(-5.64%)"
  },
  {
    "#": 327,
    "Company": "Hp Inc.",
    "Symbol": "HPQ",
    "Weight": "0.05%",
    "Price": 22.61,
    "Chg": -1.17,
    "% Chg": "(-4.92%)"
  },
  {
    "#": 328,
    "Company": "Kellanova",
    "Symbol": "K",
    "Weight": "0.05%",
    "Price": 82.24,
    "Chg": -0.31,
    "% Chg": "(-0.38%)"
  },
  {
    "#": 329,
    "Company": "Corpay, Inc.",
    "Symbol": "CPAY",
    "Weight": "0.05%",
    "Price": 288.57,
    "Chg": -29.06,
    "% Chg": "(-9.15%)"
  },
  {
    "#": 330,
    "Company": "Dow Inc.",
    "Symbol": "DOW",
    "Weight": "0.05%",
    "Price": 28.2,
    "Chg": -3.26,
    "% Chg": "(-10.36%)"
  },
  {
    "#": 331,
    "Company": "Teledyne Technologies Incorporated",
    "Symbol": "TDY",
    "Weight": "0.05%",
    "Price": 436.57,
    "Chg": -35.03,
    "% Chg": "(-7.43%)"
  },
  {
    "#": 332,
    "Company": "Microchip Technology Inc",
    "Symbol": "MCHP",
    "Weight": "0.05%",
    "Price": 36.22,
    "Chg": -4.49,
    "% Chg": "(-11.03%)"
  },
  {
    "#": 333,
    "Company": "Devon Energy Corporation",
    "Symbol": "DVN",
    "Weight": "0.05%",
    "Price": 29.31,
    "Chg": -3.85,
    "% Chg": "(-11.61%)"
  },
  {
    "#": 334,
    "Company": "Steris Plc",
    "Symbol": "STE",
    "Weight": "0.05%",
    "Price": 212.61,
    "Chg": -8.8,
    "% Chg": "(-3.97%)"
  },
  {
    "#": 335,
    "Company": "W.R. Berkley Corporation",
    "Symbol": "WRB",
    "Weight": "0.05%",
    "Price": 65.43,
    "Chg": -4.86,
    "% Chg": "(-6.91%)"
  },
  {
    "#": 336,
    "Company": "Nvr, Inc.",
    "Symbol": "NVR",
    "Weight": "0.05%",
    "Price": 7410.93,
    "Chg": 300.94,
    "% Chg": "(4.23%)"
  },
  {
    "#": 337,
    "Company": "Smurfit Westrock Plc",
    "Symbol": "SW",
    "Weight": "0.05%",
    "Price": 41.06,
    "Chg": -1.65,
    "% Chg": "(-3.86%)"
  },
  {
    "#": 338,
    "Company": "Firstenergy Corp.",
    "Symbol": "FE",
    "Weight": "0.05%",
    "Price": 39.37,
    "Chg": -1.68,
    "% Chg": "(-4.09%)"
  },
  {
    "#": 339,
    "Company": "Verisign Inc",
    "Symbol": "VRSN",
    "Weight": "0.05%",
    "Price": 240.2,
    "Chg": -15.23,
    "% Chg": "(-5.96%)"
  },
  {
    "#": 340,
    "Company": "Dollar General Corp.",
    "Symbol": "DG",
    "Weight": "0.05%",
    "Price": 92.62,
    "Chg": -1.79,
    "% Chg": "(-1.90%)"
  },
  {
    "#": 341,
    "Company": "Waters Corp",
    "Symbol": "WAT",
    "Weight": "0.04%",
    "Price": 324.92,
    "Chg": -20.2,
    "% Chg": "(-5.85%)"
  },
  {
    "#": 342,
    "Company": "Warner Bros. Discovery, Inc. Series a",
    "Symbol": "WBD",
    "Weight": "0.04%",
    "Price": 8.07,
    "Chg": -1.09,
    "% Chg": "(-11.90%)"
  },
  {
    "#": 343,
    "Company": "Mccormick & Company, Incorporated Non-Vtg Cs",
    "Symbol": "MKC",
    "Weight": "0.04%",
    "Price": 76.46,
    "Chg": -4.38,
    "% Chg": "(-5.42%)"
  },
  {
    "#": 344,
    "Company": "Cdw Corporation",
    "Symbol": "CDW",
    "Weight": "0.04%",
    "Price": 144.49,
    "Chg": -7.08,
    "% Chg": "(-4.67%)"
  },
  {
    "#": 345,
    "Company": "Coterra Energy Inc.",
    "Symbol": "CTRA",
    "Weight": "0.04%",
    "Price": 25.12,
    "Chg": -2.24,
    "% Chg": "(-8.19%)"
  },
  {
    "#": 346,
    "Company": "Weyerhaeuser Company",
    "Symbol": "WY",
    "Weight": "0.04%",
    "Price": 26.26,
    "Chg": -1.17,
    "% Chg": "(-4.27%)"
  },
  {
    "#": 347,
    "Company": "United Airlines Holdings, Inc.",
    "Symbol": "UAL",
    "Weight": "0.04%",
    "Price": 57.67,
    "Chg": -2.56,
    "% Chg": "(-4.25%)"
  },
  {
    "#": 348,
    "Company": "Live Nation Entertainment Inc.",
    "Symbol": "LYV",
    "Weight": "0.04%",
    "Price": 120.84,
    "Chg": -5.22,
    "% Chg": "(-4.14%)"
  },
  {
    "#": 349,
    "Company": "Pultegroup, Inc.",
    "Symbol": "PHM",
    "Weight": "0.04%",
    "Price": 101.24,
    "Chg": 3.49,
    "% Chg": "(3.57%)"
  },
  {
    "#": 350,
    "Company": "Molina Healthcare, Inc.",
    "Symbol": "MOH",
    "Weight": "0.04%",
    "Price": 346.71,
    "Chg": -6.53,
    "% Chg": "(-1.85%)"
  },
  {
    "#": 351,
    "Company": "Huntington Bancshares Inc",
    "Symbol": "HBAN",
    "Weight": "0.04%",
    "Price": 12.6,
    "Chg": -0.86,
    "% Chg": "(-6.39%)"
  },
  {
    "#": 352,
    "Company": "International Flavors & Fragrances Inc.",
    "Symbol": "IFF",
    "Weight": "0.04%",
    "Price": 73.12,
    "Chg": -3.33,
    "% Chg": "(-4.36%)"
  },
  {
    "#": 353,
    "Company": "Labcorp Holdings Inc.",
    "Symbol": "LH",
    "Weight": "0.04%",
    "Price": 225,
    "Chg": -8.46,
    "% Chg": "(-3.62%)"
  },
  {
    "#": 354,
    "Company": "Halliburton Company",
    "Symbol": "HAL",
    "Weight": "0.04%",
    "Price": 19.98,
    "Chg": -2.41,
    "% Chg": "(-10.76%)"
  },
  {
    "#": 355,
    "Company": "Invitation Homes Inc.",
    "Symbol": "INVH",
    "Weight": "0.04%",
    "Price": 32.54,
    "Chg": -1.45,
    "% Chg": "(-4.27%)"
  },
  {
    "#": 356,
    "Company": "T Rowe Price Group Inc",
    "Symbol": "TROW",
    "Weight": "0.04%",
    "Price": 82.6,
    "Chg": -3.62,
    "% Chg": "(-4.20%)"
  },
  {
    "#": 357,
    "Company": "Mid-America Apartment Communities, Inc.",
    "Symbol": "MAA",
    "Weight": "0.04%",
    "Price": 153.08,
    "Chg": -10.56,
    "% Chg": "(-6.45%)"
  },
  {
    "#": 358,
    "Company": "Biogen Inc.",
    "Symbol": "BIIB",
    "Weight": "0.04%",
    "Price": 122.98,
    "Chg": -7.73,
    "% Chg": "(-5.91%)"
  },
  {
    "#": 359,
    "Company": "Essex Property Trust, Inc",
    "Symbol": "ESS",
    "Weight": "0.04%",
    "Price": 271.03,
    "Chg": -23.32,
    "% Chg": "(-7.92%)"
  },
  {
    "#": 360,
    "Company": "Quest Diagnostics Inc.",
    "Symbol": "DGX",
    "Weight": "0.04%",
    "Price": 164.18,
    "Chg": -6.45,
    "% Chg": "(-3.78%)"
  },
  {
    "#": 361,
    "Company": "Nrg Energy, Inc.",
    "Symbol": "NRG",
    "Weight": "0.04%",
    "Price": 83.61,
    "Chg": -9.16,
    "% Chg": "(-9.87%)"
  },
  {
    "#": 362,
    "Company": "Expedia Group, Inc.",
    "Symbol": "EXPE",
    "Weight": "0.04%",
    "Price": 141.86,
    "Chg": -10.51,
    "% Chg": "(-6.90%)"
  },
  {
    "#": 363,
    "Company": "Nisource Inc.",
    "Symbol": "NI",
    "Weight": "0.04%",
    "Price": 37.22,
    "Chg": -2.53,
    "% Chg": "(-6.36%)"
  },
  {
    "#": 364,
    "Company": "Clorox Company",
    "Symbol": "CLX",
    "Weight": "0.04%",
    "Price": 143.86,
    "Chg": -4.83,
    "% Chg": "(-3.25%)"
  },
  {
    "#": 365,
    "Company": "Leidos Holdings, Inc.",
    "Symbol": "LDOS",
    "Weight": "0.04%",
    "Price": 133.14,
    "Chg": -6.35,
    "% Chg": "(-4.55%)"
  },
  {
    "#": 366,
    "Company": "Synchrony Financial",
    "Symbol": "SYF",
    "Weight": "0.04%",
    "Price": 43.81,
    "Chg": -2.75,
    "% Chg": "(-5.91%)"
  },
  {
    "#": 367,
    "Company": "Tyson Foods, Inc.",
    "Symbol": "TSN",
    "Weight": "0.04%",
    "Price": 59.81,
    "Chg": -3.75,
    "% Chg": "(-5.90%)"
  },
  {
    "#": 368,
    "Company": "Ptc, Inc",
    "Symbol": "PTC",
    "Weight": "0.04%",
    "Price": 139.77,
    "Chg": -9.76,
    "% Chg": "(-6.53%)"
  },
  {
    "#": 369,
    "Company": "Insulet Corporation",
    "Symbol": "PODD",
    "Weight": "0.04%",
    "Price": 245.26,
    "Chg": -11.54,
    "% Chg": "(-4.49%)"
  },
  {
    "#": 370,
    "Company": "Hewlett Packard Enterprise Company",
    "Symbol": "HPE",
    "Weight": "0.04%",
    "Price": 12.79,
    "Chg": -0.89,
    "% Chg": "(-6.51%)"
  },
  {
    "#": 371,
    "Company": "Carnival Corporation",
    "Symbol": "CCL",
    "Weight": "0.04%",
    "Price": 16.5,
    "Chg": -0.78,
    "% Chg": "(-4.51%)"
  },
  {
    "#": 372,
    "Company": "Regions Financial Corp.",
    "Symbol": "RF",
    "Weight": "0.04%",
    "Price": 18.66,
    "Chg": -0.95,
    "% Chg": "(-4.84%)"
  },
  {
    "#": 373,
    "Company": "Northern Trust Corp",
    "Symbol": "NTRS",
    "Weight": "0.04%",
    "Price": 86.01,
    "Chg": -4.57,
    "% Chg": "(-5.05%)"
  },
  {
    "#": 374,
    "Company": "Lennox International Inc.",
    "Symbol": "LII",
    "Weight": "0.04%",
    "Price": 531.3,
    "Chg": -15.52,
    "% Chg": "(-2.84%)"
  },
  {
    "#": 375,
    "Company": "Hubbell Incorporated",
    "Symbol": "HUBB",
    "Weight": "0.04%",
    "Price": 315.94,
    "Chg": -5.41,
    "% Chg": "(-1.68%)"
  },
  {
    "#": 376,
    "Company": "Snap-on Incorporated",
    "Symbol": "SNA",
    "Weight": "0.04%",
    "Price": 314.99,
    "Chg": -12.46,
    "% Chg": "(-3.81%)"
  },
  {
    "#": 377,
    "Company": "Southwest Airlines Co.",
    "Symbol": "LUV",
    "Weight": "0.04%",
    "Price": 25.87,
    "Chg": -2.99,
    "% Chg": "(-10.36%)"
  },
  {
    "#": 378,
    "Company": "Williams-Sonoma, Inc.",
    "Symbol": "WSM",
    "Weight": "0.04%",
    "Price": 141.68,
    "Chg": 2.82,
    "% Chg": "(2.03%)"
  },
  {
    "#": 379,
    "Company": "Ulta Beauty, Inc.",
    "Symbol": "ULTA",
    "Weight": "0.04%",
    "Price": 359.36,
    "Chg": -8.4,
    "% Chg": "(-2.28%)"
  },
  {
    "#": 380,
    "Company": "Packaging Corp of America",
    "Symbol": "PKG",
    "Weight": "0.04%",
    "Price": 183.42,
    "Chg": -5.74,
    "% Chg": "(-3.03%)"
  },
  {
    "#": 381,
    "Company": "Principal Financial Group, Inc.",
    "Symbol": "PFG",
    "Weight": "0.04%",
    "Price": 72.94,
    "Chg": -6.38,
    "% Chg": "(-8.04%)"
  },
  {
    "#": 382,
    "Company": "Alliant Energy Corporation",
    "Symbol": "LNT",
    "Weight": "0.04%",
    "Price": 61.36,
    "Chg": -3.49,
    "% Chg": "(-5.38%)"
  },
  {
    "#": 383,
    "Company": "Factset Research Systems",
    "Symbol": "FDS",
    "Weight": "0.04%",
    "Price": 416.19,
    "Chg": -20.96,
    "% Chg": "(-4.79%)"
  },
  {
    "#": 384,
    "Company": "Genuine Parts Company",
    "Symbol": "GPC",
    "Weight": "0.04%",
    "Price": 116.81,
    "Chg": -1.87,
    "% Chg": "(-1.58%)"
  },
  {
    "#": 385,
    "Company": "Netapp, Inc",
    "Symbol": "NTAP",
    "Weight": "0.04%",
    "Price": 76.1,
    "Chg": -5.51,
    "% Chg": "(-6.75%)"
  },
  {
    "#": 386,
    "Company": "Steel Dynamics Inc",
    "Symbol": "STLD",
    "Weight": "0.04%",
    "Price": 109.21,
    "Chg": -6.85,
    "% Chg": "(-5.90%)"
  },
  {
    "#": 387,
    "Company": "Lyondellbasell Industries N.v. Class A",
    "Symbol": "LYB",
    "Weight": "0.04%",
    "Price": 57.98,
    "Chg": -5.13,
    "% Chg": "(-8.13%)"
  },
  {
    "#": 388,
    "Company": "Super Micro Computer, Inc.",
    "Symbol": "SMCI",
    "Weight": "0.04%",
    "Price": 29.82,
    "Chg": -2.5,
    "% Chg": "(-7.74%)"
  },
  {
    "#": 389,
    "Company": "Loews Corporation",
    "Symbol": "L",
    "Weight": "0.04%",
    "Price": 83.12,
    "Chg": -7.99,
    "% Chg": "(-8.77%)"
  },
  {
    "#": 390,
    "Company": "Baxter International Inc.",
    "Symbol": "BAX",
    "Weight": "0.04%",
    "Price": 28.79,
    "Chg": -2.56,
    "% Chg": "(-8.17%)"
  },
  {
    "#": 391,
    "Company": "Domino's Pizza Inc.",
    "Symbol": "DPZ",
    "Weight": "0.04%",
    "Price": 444.21,
    "Chg": -19.57,
    "% Chg": "(-4.22%)"
  },
  {
    "#": 392,
    "Company": "West Pharmaceutical Services, Inc.",
    "Symbol": "WST",
    "Weight": "0.03%",
    "Price": 203.21,
    "Chg": -16.76,
    "% Chg": "(-7.62%)"
  },
  {
    "#": 393,
    "Company": "Evergy, Inc.",
    "Symbol": "EVRG",
    "Weight": "0.03%",
    "Price": 66.18,
    "Chg": -3.03,
    "% Chg": "(-4.38%)"
  },
  {
    "#": 394,
    "Company": "Citizens Financial Group, Inc.",
    "Symbol": "CFG",
    "Weight": "0.03%",
    "Price": 34.27,
    "Chg": -1.95,
    "% Chg": "(-5.38%)"
  },
  {
    "#": 395,
    "Company": "Rollins, Inc.",
    "Symbol": "ROL",
    "Weight": "0.03%",
    "Price": 52.21,
    "Chg": -3.69,
    "% Chg": "(-6.60%)"
  },
  {
    "#": 396,
    "Company": "Everest Group, Ltd.",
    "Symbol": "EG",
    "Weight": "0.03%",
    "Price": 337.02,
    "Chg": -24.74,
    "% Chg": "(-6.84%)"
  },
  {
    "#": 397,
    "Company": "The Cooper Companies, Inc.",
    "Symbol": "COO",
    "Weight": "0.03%",
    "Price": 73.77,
    "Chg": -4.4,
    "% Chg": "(-5.63%)"
  },
  {
    "#": 398,
    "Company": "Expeditors International of Washington, Inc.",
    "Symbol": "EXPD",
    "Weight": "0.03%",
    "Price": 108.98,
    "Chg": -1.68,
    "% Chg": "(-1.52%)"
  },
  {
    "#": 399,
    "Company": "Deckers Outdoor Corp",
    "Symbol": "DECK",
    "Weight": "0.03%",
    "Price": 106.02,
    "Chg": 5.14,
    "% Chg": "(5.10%)"
  },
  {
    "#": 400,
    "Company": "Seagate Technology Holdings Plcs",
    "Symbol": "STX",
    "Weight": "0.03%",
    "Price": 66.73,
    "Chg": -4.8,
    "% Chg": "(-6.71%)"
  },
  {
    "#": 401,
    "Company": "Ball Corporation",
    "Symbol": "BALL",
    "Weight": "0.03%",
    "Price": 48.6,
    "Chg": -1.9,
    "% Chg": "(-3.76%)"
  },
  {
    "#": 402,
    "Company": "On Semiconductor Corp",
    "Symbol": "ON",
    "Weight": "0.03%",
    "Price": 33.7,
    "Chg": -1.86,
    "% Chg": "(-5.23%)"
  },
  {
    "#": 403,
    "Company": "Omnicom Group Inc.",
    "Symbol": "OMC",
    "Weight": "0.03%",
    "Price": 72.59,
    "Chg": -2.79,
    "% Chg": "(-3.70%)"
  },
  {
    "#": 404,
    "Company": "Trimble Inc.",
    "Symbol": "TRMB",
    "Weight": "0.03%",
    "Price": 56.51,
    "Chg": -3.77,
    "% Chg": "(-6.25%)"
  },
  {
    "#": 405,
    "Company": "First Solar, Inc.",
    "Symbol": "FSLR",
    "Weight": "0.03%",
    "Price": 128.69,
    "Chg": -7.54,
    "% Chg": "(-5.53%)"
  },
  {
    "#": 406,
    "Company": "Jacobs Solutions Inc.",
    "Symbol": "J",
    "Weight": "0.03%",
    "Price": 111.45,
    "Chg": -7.03,
    "% Chg": "(-5.93%)"
  },
  {
    "#": 407,
    "Company": "F5, Inc.",
    "Symbol": "FFIV",
    "Weight": "0.03%",
    "Price": 239.25,
    "Chg": -11.73,
    "% Chg": "(-4.67%)"
  },
  {
    "#": 408,
    "Company": "Avery Dennison Corp.",
    "Symbol": "AVY",
    "Weight": "0.03%",
    "Price": 170.25,
    "Chg": -6.09,
    "% Chg": "(-3.45%)"
  },
  {
    "#": 409,
    "Company": "Gen Digital Inc.",
    "Symbol": "GEN",
    "Weight": "0.03%",
    "Price": 23.78,
    "Chg": -2.22,
    "% Chg": "(-8.54%)"
  },
  {
    "#": 410,
    "Company": "Keycorp",
    "Symbol": "KEY",
    "Weight": "0.03%",
    "Price": 13.47,
    "Chg": -0.65,
    "% Chg": "(-4.60%)"
  },
  {
    "#": 411,
    "Company": "Cf Industries Holding, Inc.",
    "Symbol": "CF",
    "Weight": "0.03%",
    "Price": 73.07,
    "Chg": -6.79,
    "% Chg": "(-8.50%)"
  },
  {
    "#": 412,
    "Company": "Amcor Plcs",
    "Symbol": "AMCR",
    "Weight": "0.03%",
    "Price": 9.22,
    "Chg": -0.35,
    "% Chg": "(-3.66%)"
  },
  {
    "#": 413,
    "Company": "Hologic Inc",
    "Symbol": "HOLX",
    "Weight": "0.03%",
    "Price": 60.86,
    "Chg": -0.83,
    "% Chg": "(-1.35%)"
  },
  {
    "#": 414,
    "Company": "Builders Firstsource, Inc.",
    "Symbol": "BLDR",
    "Weight": "0.03%",
    "Price": 123.96,
    "Chg": 4.14,
    "% Chg": "(3.46%)"
  },
  {
    "#": 415,
    "Company": "Dollar Tree Inc.",
    "Symbol": "DLTR",
    "Weight": "0.03%",
    "Price": 67.55,
    "Chg": 0.33,
    "% Chg": "(0.49%)"
  },
  {
    "#": 416,
    "Company": "Healthpeak Properties, Inc.",
    "Symbol": "DOC",
    "Weight": "0.03%",
    "Price": 18.43,
    "Chg": -1.03,
    "% Chg": "(-5.29%)"
  },
  {
    "#": 417,
    "Company": "Masco Corporation",
    "Symbol": "MAS",
    "Weight": "0.03%",
    "Price": 62.92,
    "Chg": -1.23,
    "% Chg": "(-1.92%)"
  },
  {
    "#": 418,
    "Company": "The Estee Lauder Companies Inc. Class A",
    "Symbol": "EL",
    "Weight": "0.03%",
    "Price": 52.93,
    "Chg": -5.26,
    "% Chg": "(-9.04%)"
  },
  {
    "#": 419,
    "Company": "Jabil Inc.",
    "Symbol": "JBL",
    "Weight": "0.03%",
    "Price": 116.88,
    "Chg": -6.61,
    "% Chg": "(-5.35%)"
  },
  {
    "#": 420,
    "Company": "Henry (Jack) & Associates",
    "Symbol": "JKHY",
    "Weight": "0.03%",
    "Price": 172.62,
    "Chg": -11.98,
    "% Chg": "(-6.49%)"
  },
  {
    "#": 421,
    "Company": "Kimco Realty Corp.",
    "Symbol": "KIM",
    "Weight": "0.03%",
    "Price": 19.32,
    "Chg": -0.75,
    "% Chg": "(-3.74%)"
  },
  {
    "#": 422,
    "Company": "Pentair Plc",
    "Symbol": "PNR",
    "Weight": "0.03%",
    "Price": 78.76,
    "Chg": -2.78,
    "% Chg": "(-3.41%)"
  },
  {
    "#": 423,
    "Company": "Tapestry, Inc.",
    "Symbol": "TPR",
    "Weight": "0.03%",
    "Price": 62.94,
    "Chg": -2.15,
    "% Chg": "(-3.30%)"
  },
  {
    "#": 424,
    "Company": "Alexandria Real Estate Equities, Inc.",
    "Symbol": "ARE",
    "Weight": "0.03%",
    "Price": 81.28,
    "Chg": -4.97,
    "% Chg": "(-5.76%)"
  },
  {
    "#": 425,
    "Company": "Udr, Inc.",
    "Symbol": "UDR",
    "Weight": "0.03%",
    "Price": 40.44,
    "Chg": -3.26,
    "% Chg": "(-7.46%)"
  },
  {
    "#": 426,
    "Company": "Conagra Brands, Inc.",
    "Symbol": "CAG",
    "Weight": "0.03%",
    "Price": 26.68,
    "Chg": -0.1,
    "% Chg": "(-0.37%)"
  },
  {
    "#": 427,
    "Company": "Idex Corporation",
    "Symbol": "IEX",
    "Weight": "0.03%",
    "Price": 162.49,
    "Chg": -6.19,
    "% Chg": "(-3.67%)"
  },
  {
    "#": 428,
    "Company": "Camden Property Trust",
    "Symbol": "CPT",
    "Weight": "0.03%",
    "Price": 110.43,
    "Chg": -8.46,
    "% Chg": "(-7.12%)"
  },
  {
    "#": 429,
    "Company": "Aptiv Plc",
    "Symbol": "APTV",
    "Weight": "0.03%",
    "Price": 53,
    "Chg": -2.39,
    "% Chg": "(-4.31%)"
  },
  {
    "#": 430,
    "Company": "The J.M. Smucker Company",
    "Symbol": "SJM",
    "Weight": "0.03%",
    "Price": 115.16,
    "Chg": -3.16,
    "% Chg": "(-2.67%)"
  },
  {
    "#": 431,
    "Company": "Las Vegas Sands Corp.",
    "Symbol": "LVS",
    "Weight": "0.03%",
    "Price": 33.37,
    "Chg": -3.04,
    "% Chg": "(-8.35%)"
  },
  {
    "#": 432,
    "Company": "Zebra Technologies Corporation",
    "Symbol": "ZBRA",
    "Weight": "0.03%",
    "Price": 223.49,
    "Chg": -15.01,
    "% Chg": "(-6.29%)"
  },
  {
    "#": 433,
    "Company": "Revvity, Inc.",
    "Symbol": "RVTY",
    "Weight": "0.03%",
    "Price": 94.84,
    "Chg": -5.91,
    "% Chg": "(-5.87%)"
  },
  {
    "#": 434,
    "Company": "Teradyne, Inc.",
    "Symbol": "TER",
    "Weight": "0.03%",
    "Price": 68.72,
    "Chg": -6.37,
    "% Chg": "(-8.48%)"
  },
  {
    "#": 435,
    "Company": "Textron, Inc.",
    "Symbol": "TXT",
    "Weight": "0.03%",
    "Price": 60.72,
    "Chg": -6.15,
    "% Chg": "(-9.20%)"
  },
  {
    "#": 436,
    "Company": "Best Buy Company, Inc.",
    "Symbol": "BBY",
    "Weight": "0.03%",
    "Price": 60.44,
    "Chg": -1.78,
    "% Chg": "(-2.86%)"
  },
  {
    "#": 437,
    "Company": "Pool Corporation",
    "Symbol": "POOL",
    "Weight": "0.03%",
    "Price": 315.05,
    "Chg": 1.2,
    "% Chg": "(0.38%)"
  },
  {
    "#": 438,
    "Company": "Carmax Inc.",
    "Symbol": "KMX",
    "Weight": "0.03%",
    "Price": 75.72,
    "Chg": -0.74,
    "% Chg": "(-0.97%)"
  },
  {
    "#": 439,
    "Company": "Akamai Technologies Inc",
    "Symbol": "AKAM",
    "Weight": "0.03%",
    "Price": 73.69,
    "Chg": -5.09,
    "% Chg": "(-6.46%)"
  },
  {
    "#": 440,
    "Company": "Western Digital Corp.",
    "Symbol": "WDC",
    "Weight": "0.03%",
    "Price": 30.54,
    "Chg": -3.61,
    "% Chg": "(-10.57%)"
  },
  {
    "#": 441,
    "Company": "Regency Centers Corporation",
    "Symbol": "REG",
    "Weight": "0.03%",
    "Price": 68.77,
    "Chg": -3.32,
    "% Chg": "(-4.61%)"
  },
  {
    "#": 442,
    "Company": "Juniper Networks Inc",
    "Symbol": "JNPR",
    "Weight": "0.03%",
    "Price": 33.95,
    "Chg": -1.29,
    "% Chg": "(-3.66%)"
  },
  {
    "#": 443,
    "Company": "Fox Corporation Class A",
    "Symbol": "FOXA",
    "Weight": "0.02%",
    "Price": 49.73,
    "Chg": -2.1,
    "% Chg": "(-4.05%)"
  },
  {
    "#": 444,
    "Company": "C.H. Robinson Worldwide, Inc.",
    "Symbol": "CHRW",
    "Weight": "0.02%",
    "Price": 90.94,
    "Chg": -3.83,
    "% Chg": "(-4.04%)"
  },
  {
    "#": 445,
    "Company": "Universal Health Services, Inc. Class B",
    "Symbol": "UHS",
    "Weight": "0.02%",
    "Price": 174.53,
    "Chg": -14.2,
    "% Chg": "(-7.52%)"
  },
  {
    "#": 446,
    "Company": "Allegion Public Limited Company",
    "Symbol": "ALLE",
    "Weight": "0.02%",
    "Price": 123.64,
    "Chg": -3.57,
    "% Chg": "(-2.81%)"
  },
  {
    "#": 447,
    "Company": "Lkq Corporation",
    "Symbol": "LKQ",
    "Weight": "0.02%",
    "Price": 41.29,
    "Chg": -0.89,
    "% Chg": "(-2.11%)"
  },
  {
    "#": 448,
    "Company": "Jb Hunt Transport Services Inc",
    "Symbol": "JBHT",
    "Weight": "0.02%",
    "Price": 134.66,
    "Chg": -1.57,
    "% Chg": "(-1.15%)"
  },
  {
    "#": 449,
    "Company": "Pinnacle West Capital Corporation",
    "Symbol": "PNW",
    "Weight": "0.02%",
    "Price": 91.09,
    "Chg": -4.12,
    "% Chg": "(-4.33%)"
  },
  {
    "#": 450,
    "Company": "Align Technology Inc",
    "Symbol": "ALGN",
    "Weight": "0.02%",
    "Price": 153.51,
    "Chg": -0.73,
    "% Chg": "(-0.47%)"
  },
  {
    "#": 451,
    "Company": "Molson Coors Beverage Company Class B",
    "Symbol": "TAP",
    "Weight": "0.02%",
    "Price": 61.15,
    "Chg": -1.31,
    "% Chg": "(-2.10%)"
  },
  {
    "#": 452,
    "Company": "Globe Life Inc.",
    "Symbol": "GL",
    "Weight": "0.02%",
    "Price": 117.22,
    "Chg": -10.29,
    "% Chg": "(-8.07%)"
  },
  {
    "#": 453,
    "Company": "Erie Indemnity Co",
    "Symbol": "ERIE",
    "Weight": "0.02%",
    "Price": 396.57,
    "Chg": -24.99,
    "% Chg": "(-5.93%)"
  },
  {
    "#": 454,
    "Company": "Assurant, Inc.",
    "Symbol": "AIZ",
    "Weight": "0.02%",
    "Price": 187.01,
    "Chg": -16.41,
    "% Chg": "(-8.07%)"
  },
  {
    "#": 455,
    "Company": "Bunge Global Sa",
    "Symbol": "BG",
    "Weight": "0.02%",
    "Price": 73.2,
    "Chg": -5,
    "% Chg": "(-6.39%)"
  },
  {
    "#": 456,
    "Company": "Nordson Corp",
    "Symbol": "NDSN",
    "Weight": "0.02%",
    "Price": 176.73,
    "Chg": -9.66,
    "% Chg": "(-5.18%)"
  },
  {
    "#": 457,
    "Company": "Paycom Software, Inc.",
    "Symbol": "PAYC",
    "Weight": "0.02%",
    "Price": 198.11,
    "Chg": -15.32,
    "% Chg": "(-7.18%)"
  },
  {
    "#": 458,
    "Company": "Tko Group Holdings, Inc.",
    "Symbol": "TKO",
    "Weight": "0.02%",
    "Price": 139.58,
    "Chg": -10.86,
    "% Chg": "(-7.22%)"
  },
  {
    "#": 459,
    "Company": "Incyte Genomics Inc",
    "Symbol": "INCY",
    "Weight": "0.02%",
    "Price": 60.58,
    "Chg": -1.88,
    "% Chg": "(-3.01%)"
  },
  {
    "#": 460,
    "Company": "Stanley Black & Decker, Inc.",
    "Symbol": "SWK",
    "Weight": "0.02%",
    "Price": 62.88,
    "Chg": -1.78,
    "% Chg": "(-2.75%)"
  },
  {
    "#": 461,
    "Company": "News Corporation Class A",
    "Symbol": "NWSA",
    "Weight": "0.02%",
    "Price": 24.58,
    "Chg": -1.49,
    "% Chg": "(-5.72%)"
  },
  {
    "#": 462,
    "Company": "Viatris Inc.",
    "Symbol": "VTRS",
    "Weight": "0.02%",
    "Price": 7.62,
    "Chg": -0.54,
    "% Chg": "(-6.62%)"
  },
  {
    "#": 463,
    "Company": "Solventum Corporation",
    "Symbol": "SOLV",
    "Weight": "0.02%",
    "Price": 66.2,
    "Chg": -3.99,
    "% Chg": "(-5.68%)"
  },
  {
    "#": 464,
    "Company": "Host Hotels & Resorts, Inc.",
    "Symbol": "HST",
    "Weight": "0.02%",
    "Price": 13.14,
    "Chg": -0.16,
    "% Chg": "(-1.20%)"
  },
  {
    "#": 465,
    "Company": "Eastman Chemical Company",
    "Symbol": "EMN",
    "Weight": "0.02%",
    "Price": 75.53,
    "Chg": -4.45,
    "% Chg": "(-5.56%)"
  },
  {
    "#": 466,
    "Company": "Hormel Foods Corporation",
    "Symbol": "HRL",
    "Weight": "0.02%",
    "Price": 30.74,
    "Chg": -0.7,
    "% Chg": "(-2.23%)"
  },
  {
    "#": 467,
    "Company": "The Interpublic Group of Companies, Inc.",
    "Symbol": "IPG",
    "Weight": "0.02%",
    "Price": 23.7,
    "Chg": -0.88,
    "% Chg": "(-3.58%)"
  },
  {
    "#": 468,
    "Company": "Bxp, Inc.",
    "Symbol": "BXP",
    "Weight": "0.02%",
    "Price": 60.42,
    "Chg": -2.18,
    "% Chg": "(-3.48%)"
  },
  {
    "#": 469,
    "Company": "Skyworks Solutions Inc",
    "Symbol": "SWKS",
    "Weight": "0.02%",
    "Price": 52.78,
    "Chg": -3.98,
    "% Chg": "(-7.00%)"
  },
  {
    "#": 470,
    "Company": "Dayforce, Inc.",
    "Symbol": "DAY",
    "Weight": "0.02%",
    "Price": 51.49,
    "Chg": -4.77,
    "% Chg": "(-8.48%)"
  },
  {
    "#": 471,
    "Company": "Epam Systems, Inc.",
    "Symbol": "EPAM",
    "Weight": "0.02%",
    "Price": 144.67,
    "Chg": -10.88,
    "% Chg": "(-6.99%)"
  },
  {
    "#": 472,
    "Company": "Moderna, Inc.",
    "Symbol": "MRNA",
    "Weight": "0.02%",
    "Price": 25.11,
    "Chg": -0.62,
    "% Chg": "(-2.41%)"
  },
  {
    "#": 473,
    "Company": "Bio-Techne Corp.",
    "Symbol": "TECH",
    "Weight": "0.02%",
    "Price": 51.72,
    "Chg": -3.14,
    "% Chg": "(-5.72%)"
  },
  {
    "#": 474,
    "Company": "Lamb Weston Holdings, Inc.",
    "Symbol": "LW",
    "Weight": "0.02%",
    "Price": 59,
    "Chg": -0.57,
    "% Chg": "(-0.96%)"
  },
  {
    "#": 475,
    "Company": "Aes Corporation",
    "Symbol": "AES",
    "Weight": "0.02%",
    "Price": 10.78,
    "Chg": -1.12,
    "% Chg": "(-9.41%)"
  },
  {
    "#": 476,
    "Company": "Henry Schein Inc",
    "Symbol": "HSIC",
    "Weight": "0.02%",
    "Price": 65.47,
    "Chg": -1.12,
    "% Chg": "(-1.68%)"
  },
  {
    "#": 477,
    "Company": "The Mosaic Company",
    "Symbol": "MOS",
    "Weight": "0.02%",
    "Price": 23.45,
    "Chg": -2.51,
    "% Chg": "(-9.67%)"
  },
  {
    "#": 478,
    "Company": "Marketaxess Holdings Inc.",
    "Symbol": "MKTX",
    "Weight": "0.02%",
    "Price": 212.94,
    "Chg": -3.21,
    "% Chg": "(-1.49%)"
  },
  {
    "#": 479,
    "Company": "Ralph Lauren Corporation",
    "Symbol": "RL",
    "Weight": "0.02%",
    "Price": 197.62,
    "Chg": -0.27,
    "% Chg": "(-0.14%)"
  },
  {
    "#": 480,
    "Company": "Walgreens Boots Alliance, Inc",
    "Symbol": "WBA",
    "Weight": "0.02%",
    "Price": 10.68,
    "Chg": -0.38,
    "% Chg": "(-3.44%)"
  },
  {
    "#": 481,
    "Company": "Albemarle Corporation",
    "Symbol": "ALB",
    "Weight": "0.02%",
    "Price": 58.51,
    "Chg": -7.99,
    "% Chg": "(-12.02%)"
  },
  {
    "#": 482,
    "Company": "Huntington Ingalls Industries, Inc.",
    "Symbol": "HII",
    "Weight": "0.02%",
    "Price": 184.95,
    "Chg": -14.27,
    "% Chg": "(-7.16%)"
  },
  {
    "#": 483,
    "Company": "The Campbell's Company",
    "Symbol": "CPB",
    "Weight": "0.02%",
    "Price": 38.79,
    "Chg": -1.03,
    "% Chg": "(-2.59%)"
  },
  {
    "#": 484,
    "Company": "Enphase Energy, Inc.",
    "Symbol": "ENPH",
    "Weight": "0.02%",
    "Price": 57.27,
    "Chg": -1.5,
    "% Chg": "(-2.55%)"
  },
  {
    "#": 485,
    "Company": "A.O. Smith Corporation",
    "Symbol": "AOS",
    "Weight": "0.02%",
    "Price": 61.99,
    "Chg": -1.67,
    "% Chg": "(-2.62%)"
  },
  {
    "#": 486,
    "Company": "Match Group, Inc",
    "Symbol": "MTCH",
    "Weight": "0.02%",
    "Price": 28.74,
    "Chg": -1.44,
    "% Chg": "(-4.77%)"
  },
  {
    "#": 487,
    "Company": "Hasbro, Inc.",
    "Symbol": "HAS",
    "Weight": "0.02%",
    "Price": 53.96,
    "Chg": -1.03,
    "% Chg": "(-1.87%)"
  },
  {
    "#": 488,
    "Company": "Charles River Laboratories International, Inc.",
    "Symbol": "CRL",
    "Weight": "0.02%",
    "Price": 136.9,
    "Chg": -4.08,
    "% Chg": "(-2.89%)"
  },
  {
    "#": 489,
    "Company": "Norwegian Cruise Line Holdings Ltd.s",
    "Symbol": "NCLH",
    "Weight": "0.02%",
    "Price": 15.69,
    "Chg": -0.62,
    "% Chg": "(-3.80%)"
  },
  {
    "#": 490,
    "Company": "Federal Realty Investment Trust",
    "Symbol": "FRT",
    "Weight": "0.02%",
    "Price": 89.09,
    "Chg": -3.59,
    "% Chg": "(-3.87%)"
  },
  {
    "#": 491,
    "Company": "Generac Holdings Inc",
    "Symbol": "GNRC",
    "Weight": "0.02%",
    "Price": 111.86,
    "Chg": -3.78,
    "% Chg": "(-3.27%)"
  },
  {
    "#": 492,
    "Company": "Paramount Global Class B",
    "Symbol": "PARA",
    "Weight": "0.01%",
    "Price": 11.07,
    "Chg": -0.41,
    "% Chg": "(-3.57%)"
  },
  {
    "#": 493,
    "Company": "Davita Inc.",
    "Symbol": "DVA",
    "Weight": "0.01%",
    "Price": 149.49,
    "Chg": -4.24,
    "% Chg": "(-2.76%)"
  },
  {
    "#": 494,
    "Company": "Apa Corporation",
    "Symbol": "APA",
    "Weight": "0.01%",
    "Price": 15.18,
    "Chg": -2.56,
    "% Chg": "(-14.43%)"
  },
  {
    "#": 495,
    "Company": "Wynn Resorts Ltd",
    "Symbol": "WYNN",
    "Weight": "0.01%",
    "Price": 70.09,
    "Chg": -2.79,
    "% Chg": "(-3.83%)"
  },
  {
    "#": 496,
    "Company": "Fox Corporation Class B",
    "Symbol": "FOX",
    "Weight": "0.01%",
    "Price": 45.73,
    "Chg": -2.17,
    "% Chg": "(-4.53%)"
  },
  {
    "#": 497,
    "Company": "Mgm Resorts International",
    "Symbol": "MGM",
    "Weight": "0.01%",
    "Price": 26.86,
    "Chg": -1.04,
    "% Chg": "(-3.73%)"
  },
  {
    "#": 498,
    "Company": "Invesco Ltd",
    "Symbol": "IVZ",
    "Weight": "0.01%",
    "Price": 12.81,
    "Chg": -1.02,
    "% Chg": "(-7.38%)"
  },
  {
    "#": 499,
    "Company": "Brown-Forman Corporation Class B",
    "Symbol": "BF.B",
    "Weight": "0.01%",
    "Price": 32.02,
    "Chg": -0.89,
    "% Chg": "(-2.70%)"
  },
  {
    "#": 500,
    "Company": "Mohawk Industries, Inc.",
    "Symbol": "MHK",
    "Weight": "0.01%",
    "Price": 105.65,
    "Chg": -2.19,
    "% Chg": "(-2.03%)"
  },
  {
    "#": 501,
    "Company": "Franklin Resources, Inc.",
    "Symbol": "BEN",
    "Weight": "0.01%",
    "Price": 17.51,
    "Chg": -0.44,
    "% Chg": "(-2.45%)"
  },
  {
    "#": 502,
    "Company": "Caesars Entertainment, Inc.",
    "Symbol": "CZR",
    "Weight": "0.01%",
    "Price": 23.18,
    "Chg": -0.59,
    "% Chg": "(-2.48%)"
  },
  {
    "#": 503,
    "Company": "News Corporation Class B",
    "Symbol": "NWS",
    "Weight": "0.01%",
    "Price": 27.7,
    "Chg": -1.73,
    "% Chg": "(-5.88%)"
  }
]