import sys; sys.dont_write_bytecode=True
import warnings
import pandas as pd

warnings.filterwarnings('ignore')


endpoint = lambda: f'https://proj-finance-backend.onrender.com/index-us-nasdaq100'


def get(): 
    return pd.read_json(endpoint())


sample_req = 'https://proj-finance-backend.onrender.com/index-us-nasdaq100'

sample_res = [
  {
    "#": 1,
    "Company": "Apple Inc",
    "Symbol": "AAPL",
    "Portfolio%": "8.83%",
    "Price": 188.38,
    "Chg": -14.81,
    "% Chg": "(-7.29%)",
    "Unnamed: 7": None
  },
  {
    "#": 2,
    "Company": "Microsoft Corp",
    "Symbol": "MSFT",
    "Portfolio%": "8.35%",
    "Price": 359.84,
    "Chg": -13.27,
    "% Chg": "(-3.56%)",
    "Unnamed: 7": None
  },
  {
    "#": 3,
    "Company": "NVIDIA Corp",
    "Symbol": "NVDA",
    "Portfolio%": "7.18%",
    "Price": 94.31,
    "Chg": -7.49,
    "% Chg": "(-7.36%)",
    "Unnamed: 7": None
  },
  {
    "#": 4,
    "Company": "Amazon.com Inc",
    "Symbol": "AMZN",
    "Portfolio%": "5.66%",
    "Price": 171,
    "Chg": -7.41,
    "% Chg": "(-4.15%)",
    "Unnamed: 7": None
  },
  {
    "#": 5,
    "Company": "Broadcom Inc",
    "Symbol": "AVGO",
    "Portfolio%": "3.54%",
    "Price": 146.29,
    "Chg": -7.72,
    "% Chg": "(-5.01%)",
    "Unnamed: 7": None
  },
  {
    "#": 6,
    "Company": "Meta Platforms Inc",
    "Symbol": "META",
    "Portfolio%": "3.45%",
    "Price": 504.73,
    "Chg": -26.89,
    "% Chg": "(-5.06%)",
    "Unnamed: 7": None
  },
  {
    "#": 7,
    "Company": "Costco Wholesale Corp",
    "Symbol": "COST",
    "Portfolio%": "3.12%",
    "Price": 916.48,
    "Chg": -50.6,
    "% Chg": "(-5.23%)",
    "Unnamed: 7": None
  },
  {
    "#": 8,
    "Company": "Netflix Inc",
    "Symbol": "NFLX",
    "Portfolio%": "2.81%",
    "Price": 855.86,
    "Chg": -61.19,
    "% Chg": "(-6.67%)",
    "Unnamed: 7": None
  },
  {
    "#": 9,
    "Company": "Tesla Inc",
    "Symbol": "TSLA",
    "Portfolio%": "2.72%",
    "Price": 239.43,
    "Chg": -27.85,
    "% Chg": "(-10.42%)",
    "Unnamed: 7": None
  },
  {
    "#": 10,
    "Company": "Alphabet Inc",
    "Symbol": "GOOGL",
    "Portfolio%": "2.65%",
    "Price": 145.6,
    "Chg": -5.12,
    "% Chg": "(-3.40%)",
    "Unnamed: 7": None
  },
  {
    "#": 11,
    "Company": "Alphabet Inc",
    "Symbol": "GOOG",
    "Portfolio%": "2.54%",
    "Price": 147.74,
    "Chg": -4.89,
    "% Chg": "(-3.20%)",
    "Unnamed: 7": None
  },
  {
    "#": 12,
    "Company": "T-Mobile US Inc",
    "Symbol": "TMUS",
    "Portfolio%": "2.18%",
    "Price": 248.11,
    "Chg": -19.78,
    "% Chg": "(-7.38%)",
    "Unnamed: 7": None
  },
  {
    "#": 13,
    "Company": "Cisco Systems Inc",
    "Symbol": "CSCO",
    "Portfolio%": "1.67%",
    "Price": 54.54,
    "Chg": -2.77,
    "% Chg": "(-4.83%)",
    "Unnamed: 7": None
  },
  {
    "#": 14,
    "Company": "Linde PLC",
    "Symbol": "LIN",
    "Portfolio%": "1.59%",
    "Price": 437.96,
    "Chg": -29.26,
    "% Chg": "(-6.26%)",
    "Unnamed: 7": None
  },
  {
    "#": 15,
    "Company": "PepsiCo Inc",
    "Symbol": "PEP",
    "Portfolio%": "1.54%",
    "Price": 146.61,
    "Chg": -4.76,
    "% Chg": "(-3.14%)",
    "Unnamed: 7": None
  },
  {
    "#": 16,
    "Company": "Palantir Technologies Inc",
    "Symbol": "PLTR",
    "Portfolio%": "1.28%",
    "Price": 74.01,
    "Chg": -9.59,
    "% Chg": "(-11.47%)",
    "Unnamed: 7": None
  },
  {
    "#": 17,
    "Company": "Intuitive Surgical Inc",
    "Symbol": "ISRG",
    "Portfolio%": "1.24%",
    "Price": 451.58,
    "Chg": -43.03,
    "% Chg": "(-8.70%)",
    "Unnamed: 7": None
  },
  {
    "#": 18,
    "Company": "Amgen Inc",
    "Symbol": "AMGN",
    "Portfolio%": "1.21%",
    "Price": 294.39,
    "Chg": -15.46,
    "% Chg": "(-4.99%)",
    "Unnamed: 7": None
  },
  {
    "#": 19,
    "Company": "Intuit Inc",
    "Symbol": "INTU",
    "Portfolio%": "1.21%",
    "Price": 561.53,
    "Chg": -37,
    "% Chg": "(-6.18%)",
    "Unnamed: 7": None
  },
  {
    "#": 20,
    "Company": "Adobe Inc",
    "Symbol": "ADBE",
    "Portfolio%": "1.17%",
    "Price": 349.07,
    "Chg": -18.18,
    "% Chg": "(-4.95%)",
    "Unnamed: 7": None
  },
  {
    "#": 21,
    "Company": "QUALCOMM Inc",
    "Symbol": "QCOM",
    "Portfolio%": "1.08%",
    "Price": 127.46,
    "Chg": -11.96,
    "% Chg": "(-8.58%)",
    "Unnamed: 7": None
  },
  {
    "#": 22,
    "Company": "Booking Holdings Inc",
    "Symbol": "BKNG",
    "Portfolio%": "1.08%",
    "Price": 4284.02,
    "Chg": -166.51,
    "% Chg": "(-3.74%)",
    "Unnamed: 7": None
  },
  {
    "#": 23,
    "Company": "Advanced Micro Devices Inc",
    "Symbol": "AMD",
    "Portfolio%": "1.07%",
    "Price": 85.76,
    "Chg": -8.04,
    "% Chg": "(-8.57%)",
    "Unnamed: 7": None
  },
  {
    "#": 24,
    "Company": "Texas Instruments Inc",
    "Symbol": "TXN",
    "Portfolio%": "1.06%",
    "Price": 151.39,
    "Chg": -12.81,
    "% Chg": "(-7.80%)",
    "Unnamed: 7": None
  },
  {
    "#": 25,
    "Company": "Gilead Sciences Inc",
    "Symbol": "GILD",
    "Portfolio%": "1.03%",
    "Price": 107.25,
    "Chg": -5.14,
    "% Chg": "(-4.57%)",
    "Unnamed: 7": None
  },
  {
    "#": 26,
    "Company": "Comcast Corp",
    "Symbol": "CMCSA",
    "Portfolio%": "0.97%",
    "Price": 33.38,
    "Chg": -2.34,
    "% Chg": "(-6.55%)",
    "Unnamed: 7": None
  },
  {
    "#": 27,
    "Company": "Honeywell International Inc",
    "Symbol": "HON",
    "Portfolio%": "0.95%",
    "Price": 190.99,
    "Chg": -15.69,
    "% Chg": "(-7.59%)",
    "Unnamed: 7": None
  },
  {
    "#": 28,
    "Company": "Vertex Pharmaceuticals Inc",
    "Symbol": "VRTX",
    "Portfolio%": "0.94%",
    "Price": 474.62,
    "Chg": -9.39,
    "% Chg": "(-1.94%)",
    "Unnamed: 7": None
  },
  {
    "#": 29,
    "Company": "Automatic Data Processing Inc",
    "Symbol": "ADP",
    "Portfolio%": "0.89%",
    "Price": 286.13,
    "Chg": -19.26,
    "% Chg": "(-6.31%)",
    "Unnamed: 7": None
  },
  {
    "#": 30,
    "Company": "Applied Materials Inc",
    "Symbol": "AMAT",
    "Portfolio%": "0.79%",
    "Price": 126.95,
    "Chg": -8.56,
    "% Chg": "(-6.32%)",
    "Unnamed: 7": None
  },
  {
    "#": 31,
    "Company": "Palo Alto Networks Inc",
    "Symbol": "PANW",
    "Portfolio%": "0.78%",
    "Price": 153.57,
    "Chg": -11.6,
    "% Chg": "(-7.02%)",
    "Unnamed: 7": None
  },
  {
    "#": 32,
    "Company": "MercadoLibre Inc",
    "Symbol": "MELI",
    "Portfolio%": "0.72%",
    "Price": 1841.29,
    "Chg": -104.26,
    "% Chg": "(-5.36%)",
    "Unnamed: 7": None
  },
  {
    "#": 33,
    "Company": "Starbucks Corp",
    "Symbol": "SBUX",
    "Portfolio%": "0.72%",
    "Price": 82.1,
    "Chg": -6.16,
    "% Chg": "(-6.98%)",
    "Unnamed: 7": None
  },
  {
    "#": 34,
    "Company": "Intel Corp",
    "Symbol": "INTC",
    "Portfolio%": "0.66%",
    "Price": 19.85,
    "Chg": -2.58,
    "% Chg": "(-11.50%)",
    "Unnamed: 7": None
  },
  {
    "#": 35,
    "Company": "Mondelez International Inc",
    "Symbol": "MDLZ",
    "Portfolio%": "0.66%",
    "Price": 66.31,
    "Chg": -1.59,
    "% Chg": "(-2.34%)",
    "Unnamed: 7": None
  },
  {
    "#": 36,
    "Company": "Analog Devices Inc",
    "Symbol": "ADI",
    "Portfolio%": "0.63%",
    "Price": 164.6,
    "Chg": -16.28,
    "% Chg": "(-9.00%)",
    "Unnamed: 7": None
  },
  {
    "#": 37,
    "Company": "O'Reilly Automotive Inc",
    "Symbol": "ORLY",
    "Portfolio%": "0.61%",
    "Price": 1389.87,
    "Chg": -52.02,
    "% Chg": "(-3.61%)",
    "Unnamed: 7": None
  },
  {
    "#": 38,
    "Company": "Cintas Corp",
    "Symbol": "CTAS",
    "Portfolio%": "0.59%",
    "Price": 190.33,
    "Chg": -14.52,
    "% Chg": "(-7.09%)",
    "Unnamed: 7": None
  },
  {
    "#": 39,
    "Company": "KLA Corp",
    "Symbol": "KLAC",
    "Portfolio%": "0.59%",
    "Price": 576.53,
    "Chg": -44.29,
    "% Chg": "(-7.13%)",
    "Unnamed: 7": None
  },
  {
    "#": 40,
    "Company": "Lam Research Corp",
    "Symbol": "LRCX",
    "Portfolio%": "0.58%",
    "Price": 59.09,
    "Chg": -6.13,
    "% Chg": "(-9.40%)",
    "Unnamed: 7": None
  },
  {
    "#": 41,
    "Company": "Crowdstrike Holdings Inc",
    "Symbol": "CRWD",
    "Portfolio%": "0.58%",
    "Price": 321.63,
    "Chg": -25.76,
    "% Chg": "(-7.42%)",
    "Unnamed: 7": None
  },
  {
    "#": 42,
    "Company": "Micron Technology Inc",
    "Symbol": "MU",
    "Portfolio%": "0.55%",
    "Price": 64.72,
    "Chg": -9.62,
    "% Chg": "(-12.94%)",
    "Unnamed: 7": None
  },
  {
    "#": 43,
    "Company": "MicroStrategy Inc",
    "Symbol": "MSTR",
    "Portfolio%": "0.54%",
    "Price": 293.61,
    "Chg": 11.33,
    "% Chg": "(4.01%)",
    "Unnamed: 7": None
  },
  {
    "#": 44,
    "Company": "PDD Holdings Inc ADR",
    "Symbol": "PDD",
    "Portfolio%": "0.54%",
    "Price": 104.21,
    "Chg": -9.46,
    "% Chg": "(-8.32%)",
    "Unnamed: 7": None
  },
  {
    "#": 45,
    "Company": "AppLovin Corp",
    "Symbol": "APP",
    "Portfolio%": "0.52%",
    "Price": 219.37,
    "Chg": -42.61,
    "% Chg": "(-16.26%)",
    "Unnamed: 7": None
  },
  {
    "#": 46,
    "Company": "Fortinet Inc",
    "Symbol": "FTNT",
    "Portfolio%": "0.50%",
    "Price": 84.71,
    "Chg": -4.73,
    "% Chg": "(-5.29%)",
    "Unnamed: 7": None
  },
  {
    "#": 47,
    "Company": "DoorDash Inc",
    "Symbol": "DASH",
    "Portfolio%": "0.49%",
    "Price": 163.16,
    "Chg": -10.83,
    "% Chg": "(-6.22%)",
    "Unnamed: 7": None
  },
  {
    "#": 48,
    "Company": "Cadence Design Systems Inc",
    "Symbol": "CDNS",
    "Portfolio%": "0.49%",
    "Price": 232.88,
    "Chg": -16.03,
    "% Chg": "(-6.44%)",
    "Unnamed: 7": None
  },
  {
    "#": 49,
    "Company": "Regeneron Pharmaceuticals Inc",
    "Symbol": "REGN",
    "Portfolio%": "0.47%",
    "Price": 573.45,
    "Chg": -37.19,
    "% Chg": "(-6.09%)",
    "Unnamed: 7": None
  },
  {
    "#": 50,
    "Company": "Synopsys Inc",
    "Symbol": "SNPS",
    "Portfolio%": "0.46%",
    "Price": 388.13,
    "Chg": -29.63,
    "% Chg": "(-7.09%)",
    "Unnamed: 7": None
  },
  {
    "#": 51,
    "Company": "Marriott International Inc/MD",
    "Symbol": "MAR",
    "Portfolio%": "0.45%",
    "Price": 214.58,
    "Chg": -10.04,
    "% Chg": "(-4.47%)",
    "Unnamed: 7": None
  },
  {
    "#": 52,
    "Company": "Roper Technologies Inc",
    "Symbol": "ROP",
    "Portfolio%": "0.45%",
    "Price": 541.8,
    "Chg": -37.9,
    "% Chg": "(-6.54%)",
    "Unnamed: 7": None
  },
  {
    "#": 53,
    "Company": "PayPal Holdings Inc",
    "Symbol": "PYPL",
    "Portfolio%": "0.44%",
    "Price": 58.37,
    "Chg": -3.34,
    "% Chg": "(-5.41%)",
    "Unnamed: 7": None
  },
  {
    "#": 54,
    "Company": "American Electric Power Co Inc",
    "Symbol": "AEP",
    "Portfolio%": "0.43%",
    "Price": 104.48,
    "Chg": -4.63,
    "% Chg": "(-4.24%)",
    "Unnamed: 7": None
  },
  {
    "#": 55,
    "Company": "Monster Beverage Corp",
    "Symbol": "MNST",
    "Portfolio%": "0.43%",
    "Price": 57.08,
    "Chg": -2.57,
    "% Chg": "(-4.31%)",
    "Unnamed: 7": None
  },
  {
    "#": 56,
    "Company": "ASML Holding NV",
    "Symbol": "ASML",
    "Portfolio%": "0.42%",
    "Price": 605.55,
    "Chg": -17.67,
    "% Chg": "(-2.84%)",
    "Unnamed: 7": None
  },
  {
    "#": 57,
    "Company": "Constellation Energy Corp",
    "Symbol": "CEG",
    "Portfolio%": "0.41%",
    "Price": 170.96,
    "Chg": -19.28,
    "% Chg": "(-10.13%)",
    "Unnamed: 7": None
  },
  {
    "#": 58,
    "Company": "Autodesk Inc",
    "Symbol": "ADSK",
    "Portfolio%": "0.41%",
    "Price": 245.51,
    "Chg": -11.64,
    "% Chg": "(-4.53%)",
    "Unnamed: 7": None
  },
  {
    "#": 59,
    "Company": "Copart Inc",
    "Symbol": "CPRT",
    "Portfolio%": "0.40%",
    "Price": 54.51,
    "Chg": -2.13,
    "% Chg": "(-3.76%)",
    "Unnamed: 7": None
  },
  {
    "#": 60,
    "Company": "Paychex Inc",
    "Symbol": "PAYX",
    "Portfolio%": "0.40%",
    "Price": 143.32,
    "Chg": -10.21,
    "% Chg": "(-6.65%)",
    "Unnamed: 7": None
  },
  {
    "#": 61,
    "Company": "CSX Corp",
    "Symbol": "CSX",
    "Portfolio%": "0.40%",
    "Price": 27.21,
    "Chg": -0.78,
    "% Chg": "(-2.79%)",
    "Unnamed: 7": None
  },
  {
    "#": 62,
    "Company": "Charter Communications Inc",
    "Symbol": "CHTR",
    "Portfolio%": "0.37%",
    "Price": 338.29,
    "Chg": -30.11,
    "% Chg": "(-8.17%)",
    "Unnamed: 7": None
  },
  {
    "#": 63,
    "Company": "PACCAR Inc",
    "Symbol": "PCAR",
    "Portfolio%": "0.37%",
    "Price": 90.88,
    "Chg": -1.48,
    "% Chg": "(-1.60%)",
    "Unnamed: 7": None
  },
  {
    "#": 64,
    "Company": "Workday Inc",
    "Symbol": "WDAY",
    "Portfolio%": "0.36%",
    "Price": 217.14,
    "Chg": -11.19,
    "% Chg": "(-4.90%)",
    "Unnamed: 7": None
  },
  {
    "#": 65,
    "Company": "Airbnb Inc",
    "Symbol": "ABNB",
    "Portfolio%": "0.35%",
    "Price": 106.66,
    "Chg": -7.31,
    "% Chg": "(-6.41%)",
    "Unnamed: 7": None
  },
  {
    "#": 66,
    "Company": "Keurig Dr Pepper Inc",
    "Symbol": "KDP",
    "Portfolio%": "0.35%",
    "Price": 33.81,
    "Chg": -1.82,
    "% Chg": "(-5.11%)",
    "Unnamed: 7": None
  },
  {
    "#": 67,
    "Company": "Exelon Corp",
    "Symbol": "EXC",
    "Portfolio%": "0.35%",
    "Price": 45.35,
    "Chg": -1.88,
    "% Chg": "(-3.98%)",
    "Unnamed: 7": None
  },
  {
    "#": 68,
    "Company": "Ross Stores Inc",
    "Symbol": "ROST",
    "Portfolio%": "0.33%",
    "Price": 130.31,
    "Chg": -0.9,
    "% Chg": "(-0.69%)",
    "Unnamed: 7": None
  },
  {
    "#": 69,
    "Company": "Marvell Technology Inc",
    "Symbol": "MRVL",
    "Portfolio%": "0.33%",
    "Price": 49.43,
    "Chg": -6.21,
    "% Chg": "(-11.16%)",
    "Unnamed: 7": None
  },
  {
    "#": 70,
    "Company": "Fastenal Co",
    "Symbol": "FAST",
    "Portfolio%": "0.33%",
    "Price": 74.42,
    "Chg": -3.59,
    "% Chg": "(-4.60%)",
    "Unnamed: 7": None
  },
  {
    "#": 71,
    "Company": "NXP Semiconductors NV",
    "Symbol": "NXPI",
    "Portfolio%": "0.31%",
    "Price": 160.81,
    "Chg": -11.07,
    "% Chg": "(-6.44%)",
    "Unnamed: 7": None
  },
  {
    "#": 72,
    "Company": "Verisk Analytics Inc",
    "Symbol": "VRSK",
    "Portfolio%": "0.31%",
    "Price": 284.99,
    "Chg": -20.1,
    "% Chg": "(-6.59%)",
    "Unnamed: 7": None
  },
  {
    "#": 73,
    "Company": "AstraZeneca PLC ADR",
    "Symbol": "AZN",
    "Portfolio%": "0.31%",
    "Price": 68.46,
    "Chg": -5.46,
    "% Chg": "(-7.39%)",
    "Unnamed: 7": None
  },
  {
    "#": 74,
    "Company": "Xcel Energy Inc",
    "Symbol": "XEL",
    "Portfolio%": "0.30%",
    "Price": 67.89,
    "Chg": -4.25,
    "% Chg": "(-5.89%)",
    "Unnamed: 7": None
  },
  {
    "#": 75,
    "Company": "Coca-Cola Europacific Partners PLC",
    "Symbol": "CCEP",
    "Portfolio%": "0.30%",
    "Price": 83.93,
    "Chg": -5.89,
    "% Chg": "(-6.56%)",
    "Unnamed: 7": None
  },
  {
    "#": 76,
    "Company": "Axon Enterprise Inc",
    "Symbol": "AXON",
    "Portfolio%": "0.29%",
    "Price": 497.13,
    "Chg": -42.56,
    "% Chg": "(-7.89%)",
    "Unnamed: 7": None
  },
  {
    "#": 77,
    "Company": "Diamondback Energy Inc",
    "Symbol": "FANG",
    "Portfolio%": "0.27%",
    "Price": 123.37,
    "Chg": -17.91,
    "% Chg": "(-12.68%)",
    "Unnamed: 7": None
  },
  {
    "#": 78,
    "Company": "Kraft Heinz Co/The",
    "Symbol": "KHC",
    "Portfolio%": "0.27%",
    "Price": 29.68,
    "Chg": -1.13,
    "% Chg": "(-3.67%)",
    "Unnamed: 7": None
  },
  {
    "#": 79,
    "Company": "Electronic Arts Inc",
    "Symbol": "EA",
    "Portfolio%": "0.27%",
    "Price": 135.34,
    "Chg": -9.51,
    "% Chg": "(-6.57%)",
    "Unnamed: 7": None
  },
  {
    "#": 80,
    "Company": "Baker Hughes Co",
    "Symbol": "BKR",
    "Portfolio%": "0.27%",
    "Price": 35.41,
    "Chg": -5.45,
    "% Chg": "(-13.34%)",
    "Unnamed: 7": None
  },
  {
    "#": 81,
    "Company": "Take-Two Interactive Software Inc",
    "Symbol": "TTWO",
    "Portfolio%": "0.26%",
    "Price": 194.58,
    "Chg": -14.35,
    "% Chg": "(-6.87%)",
    "Unnamed: 7": None
  },
  {
    "#": 82,
    "Company": "Cognizant Technology Solutions Corp",
    "Symbol": "CTSH",
    "Portfolio%": "0.26%",
    "Price": 68.74,
    "Chg": -4.53,
    "% Chg": "(-6.18%)",
    "Unnamed: 7": None
  },
  {
    "#": 83,
    "Company": "Old Dominion Freight Line Inc",
    "Symbol": "ODFL",
    "Portfolio%": "0.25%",
    "Price": 152.06,
    "Chg": -3.69,
    "% Chg": "(-2.37%)",
    "Unnamed: 7": None
  },
  {
    "#": 84,
    "Company": "IDEXX Laboratories Inc",
    "Symbol": "IDXX",
    "Portfolio%": "0.25%",
    "Price": 393.73,
    "Chg": -17.03,
    "% Chg": "(-4.15%)",
    "Unnamed: 7": None
  },
  {
    "#": 85,
    "Company": "Atlassian Corp",
    "Symbol": "TEAM",
    "Portfolio%": "0.24%",
    "Price": 187.67,
    "Chg": -10.68,
    "% Chg": "(-5.38%)",
    "Unnamed: 7": None
  },
  {
    "#": 86,
    "Company": "Lululemon Athletica Inc",
    "Symbol": "LULU",
    "Portfolio%": "0.23%",
    "Price": 263.7,
    "Chg": 8.05,
    "% Chg": "(3.15%)",
    "Unnamed: 7": None
  },
  {
    "#": 87,
    "Company": "CoStar Group Inc",
    "Symbol": "CSGP",
    "Portfolio%": "0.23%",
    "Price": 72.62,
    "Chg": -3.73,
    "% Chg": "(-4.89%)",
    "Unnamed: 7": None
  },
  {
    "#": 88,
    "Company": "Datadog Inc",
    "Symbol": "DDOG",
    "Portfolio%": "0.21%",
    "Price": 87.93,
    "Chg": -6.54,
    "% Chg": "(-6.92%)",
    "Unnamed: 7": None
  },
  {
    "#": 89,
    "Company": "GE HealthCare Technologies Inc",
    "Symbol": "GEHC",
    "Portfolio%": "0.21%",
    "Price": 60.51,
    "Chg": -11.49,
    "% Chg": "(-15.96%)",
    "Unnamed: 7": None
  },
  {
    "#": 90,
    "Company": "Zscaler Inc",
    "Symbol": "ZS",
    "Portfolio%": "0.21%",
    "Price": 174.67,
    "Chg": -17.54,
    "% Chg": "(-9.13%)",
    "Unnamed: 7": None
  },
  {
    "#": 91,
    "Company": "ANSYS Inc",
    "Symbol": "ANSS",
    "Portfolio%": "0.19%",
    "Price": 286.85,
    "Chg": -23.6,
    "% Chg": "(-7.60%)",
    "Unnamed: 7": None
  },
  {
    "#": 92,
    "Company": "Dexcom Inc",
    "Symbol": "DXCM",
    "Portfolio%": "0.18%",
    "Price": 59.83,
    "Chg": -1.97,
    "% Chg": "(-3.19%)",
    "Unnamed: 7": None
  },
  {
    "#": 93,
    "Company": "Trade Desk Inc/The",
    "Symbol": "TTD",
    "Portfolio%": "0.16%",
    "Price": 46.24,
    "Chg": -2.84,
    "% Chg": "(-5.79%)",
    "Unnamed: 7": None
  },
  {
    "#": 94,
    "Company": "Warner Bros Discovery Inc",
    "Symbol": "WBD",
    "Portfolio%": "0.15%",
    "Price": 8.07,
    "Chg": -1.09,
    "% Chg": "(-11.90%)",
    "Unnamed: 7": None
  },
  {
    "#": 95,
    "Company": "Microchip Technology Inc",
    "Symbol": "MCHP",
    "Portfolio%": "0.15%",
    "Price": 36.22,
    "Chg": -4.49,
    "% Chg": "(-11.03%)",
    "Unnamed: 7": None
  },
  {
    "#": 96,
    "Company": "CDW Corp/DE",
    "Symbol": "CDW",
    "Portfolio%": "0.15%",
    "Price": 144.49,
    "Chg": -7.08,
    "% Chg": "(-4.67%)",
    "Unnamed: 7": None
  },
  {
    "#": 97,
    "Company": "Biogen Inc",
    "Symbol": "BIIB",
    "Portfolio%": "0.14%",
    "Price": 122.98,
    "Chg": -7.73,
    "% Chg": "(-5.91%)",
    "Unnamed: 7": None
  },
  {
    "#": 98,
    "Company": "GLOBALFOUNDRIES Inc",
    "Symbol": "GFS",
    "Portfolio%": "0.13%",
    "Price": 31.54,
    "Chg": -2.83,
    "% Chg": "(-8.23%)",
    "Unnamed: 7": None
  },
  {
    "#": 99,
    "Company": "ON Semiconductor Corp",
    "Symbol": "ON",
    "Portfolio%": "0.11%",
    "Price": 33.7,
    "Chg": -1.86,
    "% Chg": "(-5.23%)",
    "Unnamed: 7": None
  },
  {
    "#": 100,
    "Company": "MongoDB Inc",
    "Symbol": "MDB",
    "Portfolio%": "0.09%",
    "Price": 154.39,
    "Chg": -8.95,
    "% Chg": "(-5.48%)",
    "Unnamed: 7": None
  },
  {
    "#": 101,
    "Company": "ARM Holdings PLC ADR",
    "Symbol": "ARM",
    "Portfolio%": "0.09%",
    "Price": 87.71,
    "Chg": -10.01,
    "% Chg": "(-10.24%)",
    "Unnamed: 7": None
  }
]