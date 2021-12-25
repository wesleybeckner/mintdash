"""Routes for parent Flask app."""
from flask import request
from flask import current_app as app
from .api import freeze_df
import pandas as pd

@app.route('/freeze/', methods=["POST", "GET"])
def freeze():
    if request.method == "POST":
        url = request.get_json()
        df = pd.DataFrame(url)
        df['Date'] = pd.to_datetime(df['Date'])
        return freeze_df(df)
    elif request.method == "GET":
        return "API Running, send dataframe in JSON"