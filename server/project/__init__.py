from flask import Flask, render_template, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import requests
import pdb
from Robinhood import Robinhood
import functools
import project.config as config

app = Flask(__name__, static_folder="../../static/dist",
            template_folder="../../static")


app.config.from_object('project.config.Config')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.models.user import User
from project.controllers import stocks



def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticte'] = 'Basic realm="Main"'

    return resp

def requires_authorization(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not session['logged_in']:
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/<path:text>', methods=['GET'])
def router(text=None):
    if text and 'api' in text:
        pass
    else:
        return render_template("index.html")


@app.route("/api/stocks/<stock_symbol>")
def get_dem_stocks(stock_symbol):
    return stocks.get(request, stock_symbol)


@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password'],
        robinhood_username=json_data['robinhood_username']
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route("/api/login", methods=['POST'])
def login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        my_trader = Robinhood()
        session['trader'] = my_trader.login(
            username=app.config['ROBINHOOD_USER'],
            password=app.config['ROBINHOOD_PASS']
        )
        pdb.set_trace()
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})


@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})


if __name__ == "__main__":
    app.run()
