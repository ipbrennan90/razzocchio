from flask import Flask, render_template
import requests
import pdb

app = Flask(__name__, static_folder="../static/dist",
            template_folder="../static")

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
