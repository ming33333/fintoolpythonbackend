from flask import Blueprint, request
from dotenv import load_dotenv
import app.helpers as h
import pandas as pd
# API from https://theautomatic.net/yahoo_fin-documentation/#tickers_nasdaq

main = Blueprint('main', __name__)

@main.route('/search', methods=['GET'])
def search():
    data = request.args
    if 'company' not in data:
        return {'error': 'Request must contain a company param'}, 400
    company = data['company']

    if not hasattr(search, 'cached_results'): #Set a cache for only NASDAQ company data, if it doesn't exist
        print('Caching search results')
        search.cached_results = yf.tickers_nasdaq(include_company_data = True) 
    search_results = h.search_company(company, search.cached_results) #Search for company in cache data
    return {'matches': search_results} if search_results else {'matches': 'Nothing to see here'}
@main.route('/financeratios', methods=['GET'])
def financeratios():
    data = request.args
    if 'symbol' not in data:
        return {'error': 'Request must contain a symbol param'}, 400
    symbol = data['symbol']
    ratios = h.company_ratios(symbol)
    return {'status': 'success', 'data': ratios}, 200

@main.route('/test', methods=['GET'])
def test():
    return {'status': 'success',}, 200
    #return yf.get_company_info("aapl")

