import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
import multiprocessing as mp
import joblib

def process_data(df, pivot_dates=True):
    """
    ### ASSUMPTIONS ###
    only 1 date column and 1 target (floating point) value column
    the rest are groupby columns
    ### NOTE ###
    Does not work when there are already datetime[62ns] columns //FIXED
    will only detect a single datetime column (the first one appearing left-side)
    """
    
    # infer dates
    date_col = None
    groupby = []
    target_col = None
    for col in df.columns:
        if (df[col].dtype == np.object):
            # will only detect a single datetime column (the first one appearing left-side)
            if date_col is None:
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_col = col

                except:
                    groupby.append(col)
            else:
                groupby.append(col)
        else:
            target_col = col

    # elsewhere in the app we may have converted to datetime already
    if date_col == None and (df.dtypes == 'datetime64[ns]').any():
        date_col = df.columns[df.dtypes == 'datetime64[ns]'][0]

    if pivot_dates:
        # reset index to prep for pivot
        if len(groupby) > 0:
            df = df.set_index(groupby)

        # expand out date for regression/model fitting
        # value will automatically be the target_col
        df = df.pivot(columns=date_col)

        # remove extraneous units label (result form th epivot)
        df.columns = df.columns.droplevel()
        df = df.reset_index()
    
    return df