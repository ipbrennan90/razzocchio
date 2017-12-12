from flask import Flask, render_template, request
import requests
import pdb
import argparse
import sys
import config
from Robinhood import Robinhood

app = Flask(__name__, static_folder="../static/dist",
            template_folder="../static")

parser = argparse.ArgumentParser()

parser.add_argument('--env', help='Set environment you are working in')

args=parser.parse_args()

if args.env == 'dev':
    app.config.from_object('config.DevelopmentConfig')
elif args.env == 'prod':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.Config')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/stocks/<stock_symbol>")
def get_dem_stocks(stock_symbol):
    payload = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': stock_symbol,
        'interval': request.args.get('interval', '') or '1min',
        'outputsize': 'compact',
        'datatype': 'json',
        'apikey': app.config['ALPHA_V_KEY']
    }
    req = requests.get("https://www.alphavantage.co/query", params=payload)
    return req.text

@app.route("/robinhood/login")
def login():
    my_trader = Robinhood()
    logged_in = my_trader.login(username=app.config['ROBINHOOD_USER'], password=app.config['ROBINHOOD_PASS'])
    pdb.set_trace()
    
if __name__ == "__main__":
    app.run()
