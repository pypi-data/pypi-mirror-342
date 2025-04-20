import sys; sys.dont_write_bytecode=True
import pandas as pd


endpoint = lambda pages: f'https://proj-finance-backend.onrender.com/financial-list?pages={pages}'


def get(pages=10):
    return pd.read_json(endpoint(pages))


sample_req = 'https://proj-finance-backend.onrender.com/financial-list?pages=1'

sample_res = [
  {
    "Country": "USA",
    "Ticker": "AAPL",
    "Name": "Apple",
    "Slug": "apple"
  },
  {
    "Country": "USA",
    "Ticker": "MSFT",
    "Name": "Microsoft",
    "Slug": "microsoft"
  },
  {
    "Country": "USA",
    "Ticker": "NVDA",
    "Name": "NVIDIA",
    "Slug": "nvidia"
  },
  {
    "Country": "USA",
    "Ticker": "AMZN",
    "Name": "Amazon",
    "Slug": "amazon"
  },
  {
    "Country": "USA",
    "Ticker": "GOOG",
    "Name": "Alphabet (Google)",
    "Slug": "alphabet-google"
  },
  {
    "Country": "S. Arabia",
    "Ticker": "2222.SR",
    "Name": "Saudi Aramco",
    "Slug": "saudi-aramco"
  },
  {
    "Country": "USA",
    "Ticker": "META",
    "Name": "Meta Platforms (Facebook)",
    "Slug": "meta-platforms"
  },
  {
    "Country": "USA",
    "Ticker": "BRK-B",
    "Name": "Berkshire Hathaway",
    "Slug": "berkshire-hathaway"
  },
  {
    "Country": "Taiwan",
    "Ticker": "TSM",
    "Name": "TSMC",
    "Slug": "tsmc"
  },
  {
    "Country": "USA",
    "Ticker": "TSLA",
    "Name": "Tesla",
    "Slug": "tesla"
  },
  {
    "Country": "USA",
    "Ticker": "AVGO",
    "Name": "Broadcom",
    "Slug": "broadcom"
  },
  {
    "Country": "USA",
    "Ticker": "LLY",
    "Name": "Eli Lilly",
    "Slug": "eli-lilly"
  },
  {
    "Country": "USA",
    "Ticker": "WMT",
    "Name": "Walmart",
    "Slug": "walmart"
  },
  {
    "Country": "USA",
    "Ticker": "JPM",
    "Name": "JPMorgan Chase",
    "Slug": "jp-morgan-chase"
  },
  {
    "Country": "USA",
    "Ticker": "V",
    "Name": "Visa",
    "Slug": "visa"
  },
  {
    "Country": "China",
    "Ticker": "TCEHY",
    "Name": "Tencent",
    "Slug": "tencent"
  },
  {
    "Country": "USA",
    "Ticker": "XOM",
    "Name": "Exxon Mobil",
    "Slug": "exxon-mobil"
  },
  {
    "Country": "USA",
    "Ticker": "MA",
    "Name": "Mastercard",
    "Slug": "mastercard"
  },
  {
    "Country": "USA",
    "Ticker": "UNH",
    "Name": "UnitedHealth",
    "Slug": "united-health"
  },
  {
    "Country": "USA",
    "Ticker": "COST",
    "Name": "Costco",
    "Slug": "costco"
  },
  {
    "Country": "USA",
    "Ticker": "JNJ",
    "Name": "Johnson & Johnson",
    "Slug": "johnson-and-johnson"
  },
  {
    "Country": "USA",
    "Ticker": "PG",
    "Name": "Procter & Gamble",
    "Slug": "procter-and-gamble"
  },
  {
    "Country": "USA",
    "Ticker": "NFLX",
    "Name": "Netflix",
    "Slug": "netflix"
  },
  {
    "Country": "USA",
    "Ticker": "ORCL",
    "Name": "Oracle",
    "Slug": "oracle"
  },
  {
    "Country": "USA",
    "Ticker": "ABBV",
    "Name": "AbbVie",
    "Slug": "abbvie"
  },
  {
    "Country": "USA",
    "Ticker": "HD",
    "Name": "Home Depot",
    "Slug": "home-depot"
  },
  {
    "Country": "China",
    "Ticker": "BABA",
    "Name": "Alibaba",
    "Slug": "alibaba"
  },
  {
    "Country": "USA",
    "Ticker": "BAC",
    "Name": "Bank of America",
    "Slug": "bank-of-america"
  },
  {
    "Country": "Germany",
    "Ticker": "SAP",
    "Name": "SAP",
    "Slug": "sap"
  },
  {
    "Country": "France",
    "Ticker": "MC.PA",
    "Name": "LVMH",
    "Slug": "lvmh"
  },
  {
    "Country": "USA",
    "Ticker": "KO",
    "Name": "Coca-Cola",
    "Slug": "coca-cola"
  },
  {
    "Country": "Denmark",
    "Ticker": "NVO",
    "Name": "Novo Nordisk",
    "Slug": "novo-nordisk"
  },
  {
    "Country": "USA",
    "Ticker": "TMUS",
    "Name": "T-Mobile US",
    "Slug": "t-mobile-us"
  },
  {
    "Country": "China",
    "Ticker": "1398.HK",
    "Name": "ICBC",
    "Slug": "icbc"
  },
  {
    "Country": "USA",
    "Ticker": "CVX",
    "Name": "Chevron",
    "Slug": "chevron"
  },
  {
    "Country": "France",
    "Ticker": "RMS.PA",
    "Name": "Hermès",
    "Slug": "hermes-international"
  },
  {
    "Country": "China",
    "Ticker": "600519.SS",
    "Name": "Kweichow Moutai",
    "Slug": "kweichow-moutai"
  },
  {
    "Country": "Netherlands",
    "Ticker": "ASML",
    "Name": "ASML",
    "Slug": "asml"
  },
  {
    "Country": "Switzerland",
    "Ticker": "ROG.SW",
    "Name": "Roche",
    "Slug": "roche"
  },
  {
    "Country": "Switzerland",
    "Ticker": "NESN.SW",
    "Name": "Nestlé",
    "Slug": "nestle"
  },
  {
    "Country": "S. Korea",
    "Ticker": "005930.KS",
    "Name": "Samsung",
    "Slug": "samsung"
  },
  {
    "Country": "USA",
    "Ticker": "CRM",
    "Name": "Salesforce",
    "Slug": "salesforce"
  },
  {
    "Country": "China",
    "Ticker": "601288.SS",
    "Name": "Agricultural Bank of China",
    "Slug": "agricultural-bank-of-china"
  },
  {
    "Country": "USA",
    "Ticker": "PM",
    "Name": "Philip Morris International",
    "Slug": "philip-morris"
  },
  {
    "Country": "USA",
    "Ticker": "CSCO",
    "Name": "Cisco",
    "Slug": "cisco"
  },
  {
    "Country": "China",
    "Ticker": "601939.SS",
    "Name": "China Construction Bank",
    "Slug": "china-construction-bank"
  },
  {
    "Country": "UAE",
    "Ticker": "IHC.AE",
    "Name": "International Holding Company",
    "Slug": "international-holding-company"
  },
  {
    "Country": "China",
    "Ticker": "0941.HK",
    "Name": "China Mobile",
    "Slug": "china-mobile"
  },
  {
    "Country": "USA",
    "Ticker": "WFC",
    "Name": "Wells Fargo",
    "Slug": "wells-fargo"
  },
  {
    "Country": "Japan",
    "Ticker": "TM",
    "Name": "Toyota",
    "Slug": "toyota"
  },
  {
    "Country": "USA",
    "Ticker": "ABT",
    "Name": "Abbott Laboratories",
    "Slug": "abbott-laboratories"
  },
  {
    "Country": "USA",
    "Ticker": "IBM",
    "Name": "IBM",
    "Slug": "ibm"
  },
  {
    "Country": "UK",
    "Ticker": "AZN",
    "Name": "AstraZeneca",
    "Slug": "astrazeneca"
  },
  {
    "Country": "USA",
    "Ticker": "MRK",
    "Name": "Merck",
    "Slug": "merck"
  },
  {
    "Country": "USA",
    "Ticker": "MCD",
    "Name": "McDonald",
    "Slug": "mcdonald"
  },
  {
    "Country": "UK",
    "Ticker": "LIN",
    "Name": "Linde",
    "Slug": "linde"
  },
  {
    "Country": "Switzerland",
    "Ticker": "NVS",
    "Name": "Novartis",
    "Slug": "novartis"
  },
  {
    "Country": "UK",
    "Ticker": "SHEL",
    "Name": "Shell",
    "Slug": "shell"
  },
  {
    "Country": "China",
    "Ticker": "601988.SS",
    "Name": "Bank of China",
    "Slug": "bank-of-china"
  },
  {
    "Country": "USA",
    "Ticker": "GE",
    "Name": "General Electric",
    "Slug": "general-electric"
  },
  {
    "Country": "USA",
    "Ticker": "PEP",
    "Name": "Pepsico",
    "Slug": "pepsico"
  },
  {
    "Country": "USA",
    "Ticker": "T",
    "Name": "AT&T",
    "Slug": "att"
  },
  {
    "Country": "UK",
    "Ticker": "HSBC",
    "Name": "HSBC",
    "Slug": "hsbc"
  },
  {
    "Country": "India",
    "Ticker": "RELIANCE.NS",
    "Name": "Reliance Industries",
    "Slug": "reliance-industries"
  },
  {
    "Country": "Netherlands",
    "Ticker": "PRX.AS",
    "Name": "Prosus",
    "Slug": "prosus"
  },
  {
    "Country": "France",
    "Ticker": "OR.PA",
    "Name": "L'Oréal",
    "Slug": "l-oreal"
  },
  {
    "Country": "USA",
    "Ticker": "PLTR",
    "Name": "Palantir",
    "Slug": "palantir"
  },
  {
    "Country": "Ireland",
    "Ticker": "ACN",
    "Name": "Accenture",
    "Slug": "accenture"
  },
  {
    "Country": "USA",
    "Ticker": "VZ",
    "Name": "Verizon",
    "Slug": "verizon"
  },
  {
    "Country": "China",
    "Ticker": "0857.HK",
    "Name": "PetroChina",
    "Slug": "petro-china"
  },
  {
    "Country": "USA",
    "Ticker": "AXP",
    "Name": "American Express",
    "Slug": "american-express"
  },
  {
    "Country": "USA",
    "Ticker": "MS",
    "Name": "Morgan Stanley",
    "Slug": "morgan-stanley"
  },
  {
    "Country": "USA",
    "Ticker": "TMO",
    "Name": "Thermo Fisher Scientific",
    "Slug": "thermo-fisher-scientific"
  },
  {
    "Country": "Germany",
    "Ticker": "DTE.DE",
    "Name": "Deutsche Telekom",
    "Slug": "deutsche-telekom"
  },
  {
    "Country": "Germany",
    "Ticker": "SIE.DE",
    "Name": "Siemens",
    "Slug": "siemens"
  },
  {
    "Country": "USA",
    "Ticker": "DIS",
    "Name": "Walt Disney",
    "Slug": "walt-disney"
  },
  {
    "Country": "USA",
    "Ticker": "ISRG",
    "Name": "Intuitive Surgical",
    "Slug": "intuitive-surgical"
  },
  {
    "Country": "USA",
    "Ticker": "RTX",
    "Name": "RTX",
    "Slug": "raytheon-technologies"
  },
  {
    "Country": "USA",
    "Ticker": "INTU",
    "Name": "Intuit",
    "Slug": "intuit"
  },
  {
    "Country": "USA",
    "Ticker": "BX",
    "Name": "Blackstone Group",
    "Slug": "blackstone-group"
  },
  {
    "Country": "India",
    "Ticker": "HDB",
    "Name": "HDFC Bank",
    "Slug": "hdfc-bank"
  },
  {
    "Country": "USA",
    "Ticker": "QCOM",
    "Name": "QUALCOMM",
    "Slug": "qualcomm"
  },
  {
    "Country": "USA",
    "Ticker": "GS",
    "Name": "Goldman Sachs",
    "Slug": "goldman-sachs"
  },
  {
    "Country": "Mexico",
    "Ticker": "FMX",
    "Name": "Fomento Económico Mexicano",
    "Slug": "fomento-economico-mexicano"
  },
  {
    "Country": "USA",
    "Ticker": "AMGN",
    "Name": "Amgen",
    "Slug": "amgen"
  },
  {
    "Country": "USA",
    "Ticker": "PGR",
    "Name": "Progressive",
    "Slug": "progressive"
  },
  {
    "Country": "USA",
    "Ticker": "AMD",
    "Name": "AMD",
    "Slug": "amd"
  },
  {
    "Country": "China",
    "Ticker": "PDD",
    "Name": "PDD Holdings (Pinduoduo)",
    "Slug": "pinduoduo"
  },
  {
    "Country": "USA",
    "Ticker": "NOW",
    "Name": "ServiceNow",
    "Slug": "servicenow"
  },
  {
    "Country": "USA",
    "Ticker": "ADBE",
    "Name": "Adobe",
    "Slug": "adobe"
  },
  {
    "Country": "USA",
    "Ticker": "TXN",
    "Name": "Texas Instruments",
    "Slug": "texas-instruments"
  },
  {
    "Country": "China",
    "Ticker": "XIACF",
    "Name": "Xiaomi",
    "Slug": "xiaomi"
  },
  {
    "Country": "China",
    "Ticker": "002594.SZ",
    "Name": "BYD",
    "Slug": "byd"
  },
  {
    "Country": "Canada",
    "Ticker": "RY",
    "Name": "Royal Bank Of Canada",
    "Slug": "royal-bank-of-canada"
  },
  {
    "Country": "Australia",
    "Ticker": "CBA.AX",
    "Name": "Commonwealth Bank",
    "Slug": "commonwealth-bank"
  },
  {
    "Country": "USA",
    "Ticker": "CAT",
    "Name": "Caterpillar",
    "Slug": "caterpillar"
  },
  {
    "Country": "Japan",
    "Ticker": "MUFG",
    "Name": "Mitsubishi UFJ Financial",
    "Slug": "mitsubishi-ufj-financial"
  },
  {
    "Country": "Spain",
    "Ticker": "IDEXY",
    "Name": "Inditex",
    "Slug": "inditex"
  },
  {
    "Country": "USA",
    "Ticker": "SPGI",
    "Name": "S&P Global",
    "Slug": "sp-global"
  },
  {
    "Country": "Japan",
    "Ticker": "SONY",
    "Name": "Sony",
    "Slug": "sony"
  }
]