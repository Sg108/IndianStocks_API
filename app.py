import gspread
from dotenv import load_dotenv
import json
import os
from google.oauth2.service_account import Credentials
import requests
import pandas as pd
import time
import difflib
from fastapi import FastAPI, HTTPException
from typing import List,Dict
import uvicorn
from fastapi.responses import HTMLResponse

load_dotenv()
app = FastAPI()

def find_closest_ticker(stock_name, stocks_dict):
    # Get the closest match from the stock names
    closest_matches = difflib.get_close_matches(stock_name, stocks_dict.keys(), n=1, cutoff=0.6)
    
    if closest_matches:
        # Return the ticker for the closest match
        #closest_match = closest_matches
        return stocks_dict[closest_matches[0]]
        #return stocks_dict[closest_match]
    else:
        return None

# Replace with your Financial Modeling Prep API Key
# api_key = 'oBAjwF53F4f0TGlBrkDtbwMlULiRp8pb'

# # ISIN you want to look up
#isin = 'INE216P01012'  # Example ISIN for Apple Inc.

# # Make the request to the FMP API

# url = f'https://financialmodelingprep.com/api/v3/search/isin?isin={isin}&apikey=oBAjwF53F4f0TGlBrkDtbwMlULiRp8pb'
# response = requests.get(url)

# # Parse the response
# data = response.json()
# print(data)
user_input='SBI CARDS & PAY SER LTD'
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
google_sheets_credentials = os.getenv('Google_Sheets_cred')
credentials_dict = json.loads(google_sheets_credentials)
#print(google_sheets_credentials)
client = gspread.service_account_from_dict(credentials_dict, scopes=scopes)
#client = gspread.authorize(creds)
sheet1 = client.open_by_key(os.getenv('Sheet_ID')).worksheet('Gfinance')
sheet2 = client.open_by_key(os.getenv('Sheet_ID')).worksheet('TickerSheet')
dict={}
ticker_data = sheet2.get_all_values()
for row in ticker_data:
    dict[row[2].upper()]=row[0]

#print(dict)


@app.get("/",response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>HTML Response</title>
        </head>
        <body>
            <h1>Stonks API</h1>
            <p>Here you can get historical stock price of any stock registered in NSE</p>
            <ul>handler - /api/get_stock_price/:type , where type can have either ISIN number or stock name</p>
            <li>with ISIN you need to give type = "ISIN" and in the body give "ISIN":[[isin number]],"start_date":[[start_date]] and "end_date":[[end_date]]</li>
            <li>with stock name you need to give type = "Stock_Name" and in the body give "Stock_Name":[[stock name]],"start_date":[[start_date]] and "end_date":[[end_date]]</li>
            </ul>
        </body>
    </html>
    """

@app.get("/api/get_stock_price/{type}")
async def get_stockPrice(type:str,body:Dict):
    if type == "ISIN":
        ticker=sheet2.find(body["ISIN"])
        if ticker:
            TICKER_SYMBOL=sheet2.cell(ticker.row,1).value
            formula= f'=GOOGLEFINANCE("NSE:{TICKER_SYMBOL}","price", "{body["start_date"]}", "{body["end_date"]}")'
            sheet1.update_cell(1,1,formula)
            time.sleep(1)
            data = sheet1.get_all_values()
            return {"ticker":TICKER_SYMBOL,"data":data}
        else:
            return {"error":"invalid isin number"}
    elif type == "Stock_Name":
        user_input=body["Stock_Name"]
        ticker = find_closest_ticker(user_input.upper(), dict)
        #print(dict)
        if ticker:
            formula= f'=GOOGLEFINANCE("NSE:{ticker}","price", "{body["start_date"]}", "{body["end_date"]}")'
            sheet1.update_cell(1,1,formula)
            time.sleep(1)
            data = sheet1.get_all_values()
        else:
            return {"error":"invalid stock name"}
        return {"ticker":ticker,"data":data}
    else:
        return {"error":"invalid type"}
            

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# ticker=sheet2.find(isin)
# TICKER_SYMBOL=sheet2.cell(ticker.row,1).value
# sheet1 = client.open_by_key('1H3SwCEnn1w8AKxLhrRoCd1ywAIn731bjZlOKtarxoz4').worksheet('Gfinance')
# formula= f'=GOOGLEFINANCE("NSE:{TICKER_SYMBOL}","price", DATE(2023,1,1), DATE(2024,12,31))'
# sheet1.update_cell(1,1,formula)
# time.sleep(1)
# data = sheet1.get_all_values()
# Example: Read the first row of data
# data = sheet.row_values(1)
# print(data)
# for row in data:
#     print(row)