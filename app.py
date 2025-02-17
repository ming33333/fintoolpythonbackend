from flask import Flask, request
import yahoo_fin.stock_info as yf
from dotenv import load_dotenv
import os
import json
import pandas as pd
# API from https://theautomatic.net/yahoo_fin-documentation/#tickers_nasdaq

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

def search_company(company, company_df):
    results = []
    for idx, row in company_df.iterrows():
        if pd.isna(row['Security Name']) or pd.isna(row['Symbol']):
            continue
        if company.lower() in row['Security Name'].lower() or company.lower() in row['Symbol'].lower():
            results.append({
                "id": idx,
                "name": row['Security Name'],
                "symbol": row['Symbol']
            })
    return results


@app.route('/search', methods=['GET'])
def search():
    data = request.args
    if 'company' not in data:
        return {'error': 'Request must contain a company param'}, 400
    company = data['company']

    if not hasattr(search, 'cached_results'): #Set a cache for only NASDAQ company data, if it doesn't exist
        print('Caching search results')
        search.cached_results = yf.tickers_nasdaq(include_company_data = True) 
    search_results = search_company(company, search.cached_results) #Search for company in cache data
    return {'matches': search_results} if search_results else {'matches': 'Nothing to see here'}
@app.route('/financeratios', methods=['GET'])
def financeratios():
    data = request.args
    if 'symbol' not in data:
        return {'error': 'Request must contain a symbol param'}, 400
    symbol = data['symbol']

    return {''}

@app.route('/test', methods=['GET'])
def test():
    print(yf.get_cash_flow('nflx'))
    return {'status': 'success', 'data': str(yf.get_cash_flow('nflx'))}, 200
    #return yf.get_company_info("aapl")

if __name__ == '__main__':
    if os.getenv('env') == 'dev': #Tried to set FLASK_ENV=development in .env file, but it didn't work but feature not working
        print('Setting FLASK_ENV to development')
        os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port=8080)