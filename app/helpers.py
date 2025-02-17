
import pandas as pd
import yahoo_fin.stock_info as yf


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

def company_ratios(symbol):
       # df = yf.get_stats(symbol)['quarterly_results'] #TODO fix so can use later
        quarter = '4Q2024'
        start_date = '2024-12-31'
        end_date = '2025-01-01'

        df = yf.get_earnings(symbol)['quarterly_results']
        diluted_eps = df.at[df[df['date']== quarter].index.tolist()[0],'actual'] #TODO assuming only 1 quarter

        close_price = yf.get_data(symbol,start_date = start_date, end_date = end_date).at[start_date,"close"] #TODO assuming this day has a price
        
        pe_ratio = close_price/diluted_eps

        #total_debt = yf.get_financials(symbol,yearly= False,quarterly = True)#TODO does not grab all the data
        total_debt =yf.get_balance_sheet(symbol, yearly = False)
        print('total_debt',total_debt)
        return {"PE Ratio": 5,
                "Debt to Equity": 5,
                "ROE": 5,
                "OM": 5,
                "CR": 5,
                }