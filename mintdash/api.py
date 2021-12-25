import pandas as pd
from datetime import datetime, date
import numpy as np
from .dashboard.plotlyfunctions import make_df

def freeze_df(df):
    df['Amount'] = df['Amount'].astype(float)
    categories = list(df.Category.unique())
    income = ['Income', 'Paycheck', 'Transfer', 'Federal Tax', 'Taxes', 'Rental Income', 'Interest Income']
    taxes = ['Federal Tax', 'Taxes']
    internal_acc = ['Credit Card Payment', 'Transfer', 'Financial']
    non_expense =  income + taxes + internal_acc
    expenses = [i for i in categories if i not in non_expense]
    df = df.loc[df['Category'].isin(expenses)]
    df = df.loc[df['Amount'] < 8000]


    ### MONTHLY DF ###
    dff, _, _ = make_df(df, x='Date', year=[2021], quantile=0.1, bins=None)
    monthly = dff.set_index("Date")
    monthly.columns = ['Decile', 'Amount']


    for quantile, label in zip([.25,.5], ['Quartile', 'Median']):
        dff, _, _ = make_df(df, x='Date', year=[2021], quantile=quantile, bins=None)
        dff = dff.set_index("Date")
        monthly[label] = dff['Quantile']

    monthly.index = monthly.index.month
    monthly = monthly.reset_index()
    monthly = monthly.sort_values('Date')
    monthly = monthly.reset_index(drop=True)
    monthly = monthly[['Date', 'Amount', 'Decile', 'Quartile', 'Median']]
    monthly['Amount'] = round(monthly['Amount'])
    monthly_spending = monthly.to_json()

    dff, _, _ = make_df(df, x='Date', year=[2021], quantile=None, bins=[20, 150])
    dff = round(dff)
    monthly = dff.groupby(['Date', 'Bin'], sort=False)['Amount'].sum().unstack('Bin').reset_index()
    monthly = monthly.set_index('Date')
    monthly.index = monthly.index.month
    monthly = monthly.reset_index()
    monthly = monthly.sort_values('Date')
    monthly = monthly.reset_index(drop=True)
    monthly_spending_threshold = monthly.to_json()

    dff, _, _ = make_df(df, x='Date', year=[2021], quantile=None, bins='Time Comparison')
    dff = round(dff)
    monthly = dff.groupby(['Date', 'Bin'], sort=False)['Amount'].sum().unstack('Bin').reset_index()
    monthly = monthly.set_index('Date')
    monthly.index = monthly.index.month
    monthly = monthly.reset_index()
    monthly = monthly.sort_values('Date')
    monthly = monthly.reset_index(drop=True)
    monthly_spending_time = monthly.to_json()

    ### CATEGORY DF ###
    dff, _, _ = make_df(df, x='Category', year=[2021], quantile=0.1, bins=None)
    dff = round(dff)
    dff = dff.groupby(['Category', 'Quantile'], sort=False)['Amount'].sum().unstack('Quantile').reset_index()
    category_spending_10 = dff.to_json()

    dff, _, _ = make_df(df, x='Category', year=[2021], quantile=0.25, bins=None)
    dff = round(dff)
    dff = dff.groupby(['Category', 'Quantile'], sort=False)['Amount'].sum().unstack('Quantile').reset_index()
    category_spending_25 = dff.to_json()

    dff, _, _ = make_df(df, x='Category', year=[2021], quantile=0.5, bins=None)
    dff = round(dff)
    dff = dff.groupby(['Category', 'Quantile'], sort=False)['Amount'].sum().unstack('Quantile').reset_index()
    category_spending_50 = dff.to_json()

    dff, _, _ = make_df(df, x='Category', year=[2021], quantile=None, bins=None)
    dff = round(dff)
    category_spending_none = dff.to_json()

    dff, _, _ = make_df(df, x='Category', year=[2021], quantile=None, bins=[20, 150])
    dff = round(dff)
    dff = dff.groupby(['Category', 'Bin'], sort=False)['Amount'].sum().unstack('Bin').reset_index()
    category_spending_threshold = dff.to_json()

    dff, _, _ = make_df(df, x='Category', year=[2021], quantile=None, bins='Time Comparison')
    dff = round(dff)
    dff = dff.groupby(['Category', 'Bin'], sort=False)['Amount'].sum().unstack('Bin').reset_index()
    category_spending_time = dff.to_json()
    tables = [monthly_spending, monthly_spending_threshold, monthly_spending_time, category_spending_none,\
           category_spending_10, category_spending_25, category_spending_50, category_spending_threshold,\
           category_spending_time]
    # return [f"{i}: {j}" for i,j in zip(range(len(tables)), tables)]
    return {"0": tables[0],
            "1": tables[1],
            "2": tables[2],
            "3": tables[3],
            "4": tables[4],
            "5": tables[5],
            "6": tables[6],
            "7": tables[7],
            "8": tables[8]}