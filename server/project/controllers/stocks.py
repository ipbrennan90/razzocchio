# controller for querying alpha vantage api
import requests
from project import app
import pdb


alpha_v_base = 'https://www.alphavantage.co/query'

def get(request, stock_symbol):
    payload = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': stock_symbol,
        'interval': request.args.get('interval', '') or '1min',
        'outputsize': 'compact',
        'datatype': 'json',
        'apikey': app.config['ALPHA_V_KEY']
    }
    req = requests.get(alpha_v_base, params=payload)
    return req.text
