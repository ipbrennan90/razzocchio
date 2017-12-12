from flask import Flask, render_template
import requests
import pdb
import argparse
import sys
import config

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

print app.config

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/stocks")
def get_dem_stocks():
    req = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=VGZ&interval=1min&outputsize=compact&datatype=json&apikey=https://www.alphavantage.co/query")                     

if __name__ == "__main__":
    app.run()
