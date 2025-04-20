import sys; sys.dont_write_bytecode=True
import pandas as pd


endpoint = lambda slug: f'http://proj-finance-backend.onrender.com/financial-raw/{slug}'


def get(slug='microsoft'):
    return pd.read_json(endpoint(slug))


sample_req = 'https://proj-finance-backend.onrender.com/financial-raw/microsoft'

sample_res = [
  {
    "Year": 2025,
    "Shares": 7430,
    "Capital": 2769000,
    "DYield": 0.81,
    "Revenue": 261800,
    "Income": 113610,
    "Asset": 512160,
    "Equity": 268470
  },
  {
    "Year": 2024,
    "Shares": 7430,
    "Capital": 3200000,
    "DYield": 0.73,
    "Revenue": 227580,
    "Income": 101210,
    "Asset": 411970,
    "Equity": 206220
  },
  {
    "Year": 2023,
    "Shares": 7450,
    "Capital": 2794000,
    "DYield": 0.74,
    "Revenue": 204090,
    "Income": 82580,
    "Asset": 364840,
    "Equity": 166540
  },
  {
    "Year": 2022,
    "Shares": 7500,
    "Capital": 1787000,
    "DYield": 1.06,
    "Revenue": 184900,
    "Income": 79680,
    "Asset": 333770,
    "Equity": 141980
  },
  {
    "Year": 2021,
    "Shares": 7550,
    "Capital": 2522000,
    "DYield": 0.68,
    "Revenue": 153280,
    "Income": 60720,
    "Asset": 301310,
    "Equity": 118300
  },
  {
    "Year": 2020,
    "Shares": 7620,
    "Capital": 1681000,
    "DYield": 0.94,
    "Revenue": 134240,
    "Income": 49850,
    "Asset": 286550,
    "Equity": 102330
  },
  {
    "Year": 2019,
    "Shares": 7690,
    "Capital": 1200000,
    "DYield": 1.2,
    "Revenue": 118450,
    "Income": 39920,
    "Asset": 258840,
    "Equity": 82710
  },
  {
    "Year": 2018,
    "Shares": 7710,
    "Capital": 780360,
    "DYield": 1.69,
    "Revenue": 99980,
    "Income": 29790,
    "Asset": 250310,
    "Equity": 87710
  },
  {
    "Year": 2017,
    "Shares": 7750,
    "Capital": 659900,
    "DYield": 1.86,
    "Revenue": 88890,
    "Income": 23230,
    "Asset": 193460,
    "Equity": 71990
  },
  {
    "Year": 2016,
    "Shares": 7960,
    "Capital": 483160,
    "DYield": 2.37,
    "Revenue": 88080,
    "Income": 16120,
    "Asset": 174470,
    "Equity": 80080
  },
  {
    "Year": 2015,
    "Shares": 8220,
    "Capital": 439670,
    "DYield": 2.33,
    "Revenue": 93450,
    "Income": 27280,
    "Asset": 172380,
    "Equity": 89780
  },
  {
    "Year": 2014,
    "Shares": 8320,
    "Capital": 381720,
    "DYield": 2.48,
    "Revenue": 83430,
    "Income": 28030,
    "Asset": 142430,
    "Equity": 78940
  },
  {
    "Year": 2013,
    "Shares": 8390,
    "Capital": 310500,
    "DYield": 2.59,
    "Revenue": 72930,
    "Income": 20020,
    "Asset": 121270,
    "Equity": 66360
  },
  {
    "Year": 2012,
    "Shares": 8400,
    "Capital": 223660,
    "DYield": 3.11,
    "Revenue": 72050,
    "Income": 27880,
    "Asset": 108700,
    "Equity": 57080
  },
  {
    "Year": 2011,
    "Shares": 8490,
    "Capital": 218380,
    "DYield": 2.62,
    "Revenue": 66690,
    "Income": 27090,
    "Asset": 86110,
    "Equity": 46170
  },
  {
    "Year": 2010,
    "Shares": 8850,
    "Capital": 234520,
    "DYield": 1.97,
    "Revenue": 58680,
    "Income": 21840,
    "Asset": 77880,
    "Equity": 39550
  },
  {
    "Year": 2009,
    "Shares": 8900,
    "Capital": 268550,
    "DYield": 1.71,
    "Revenue": 61980,
    "Income": 22400,
    "Asset": 72790,
    "Equity": 36280
  },
  {
    "Year": 2008,
    "Shares": 9360,
    "Capital": 172920,
    "DYield": 2.37,
    "Revenue": 57890,
    "Income": 24290,
    "Asset": 63170,
    "Equity": 31090
  },
  {
    "Year": 2007,
    "Shares": 9800,
    "Capital": 332110,
    "DYield": 1.15,
    "Revenue": 46050,
    "Income": 17410,
    "Asset": 69590,
    "Equity": 40100
  },
  {
    "Year": 2006,
    "Shares": 10560,
    "Capital": 291940,
    "DYield": 1.24,
    "Revenue": 41350,
    "Income": 17370,
    "Asset": 70810,
    "Equity": 48110
  },
  {
    "Year": 2005,
    "Shares": 10870,
    "Capital": 271540,
    "DYield": 1.22,
    "Revenue": 38470,
    "Income": 14920,
    "Asset": 94360,
    "Equity": 74820
  },
  {
    "Year": 2004,
    "Shares": 10810,
    "Capital": 290710,
    "DYield": 11.83,
    "Revenue": 34260,
    "Income": 12270,
    "Asset": 81730,
    "Equity": 64910
  },
  {
    "Year": 2003,
    "Shares": None,
    "Capital": 295290,
    "DYield": 0.88,
    "Revenue": 30780,
    "Income": 11910,
    "Asset": 67640,
    "Equity": 52180
  },
  {
    "Year": 2002,
    "Shares": None,
    "Capital": 276630,
    "DYield": 0,
    "Revenue": 26720,
    "Income": 9000,
    "Asset": 58830,
    "Equity": 47280
  },
  {
    "Year": 2001,
    "Shares": None,
    "Capital": 358050,
    "DYield": 0,
    "Revenue": 23770,
    "Income": 15030,
    "Asset": None,
    "Equity": None
  },
  {
    "Year": 2000,
    "Shares": None,
    "Capital": 230800,
    "DYield": 0,
    "Revenue": 22610,
    "Income": 13340,
    "Asset": None,
    "Equity": None
  },
  {
    "Year": 1999,
    "Shares": None,
    "Capital": 604410,
    "DYield": 0,
    "Revenue": 17150,
    "Income": 9690,
    "Asset": None,
    "Equity": None
  },
  {
    "Year": 1998,
    "Shares": None,
    "Capital": 348100,
    "DYield": 0,
    "Revenue": 13090,
    "Income": 6200,
    "Asset": None,
    "Equity": None
  },
  {
    "Year": 1997,
    "Shares": None,
    "Capital": 157360,
    "DYield": 0,
    "Revenue": 9430,
    "Income": 3800,
    "Asset": None,
    "Equity": None
  },
  {
    "Year": 1996,
    "Shares": None,
    "Capital": 99410,
    "DYield": 0,
    "Revenue": None,
    "Income": None,
    "Asset": None,
    "Equity": None
  }
]