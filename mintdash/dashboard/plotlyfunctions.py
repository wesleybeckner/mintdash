from dash import dash_table, html
from dash.dash_table.Format import Format, Scheme, Trim
import numpy as np
import plotly.express as px
import pandas as pd
import base64
import datetime
import io
import dash_bootstrap_components as dbc
import os

colors = {'background': '#FFFFFF',
              'text': '#111111'}
style = {'height': 320}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.MINTY]

plot_layouts = {
    "plot_bgcolor": colors['background'],
    "paper_bgcolor": colors['background'],
    "height": style['height'],
    "margin": dict(
            l=0,
            r=0,
            b=0,
            t=30,
            pad=4
       )}

# establish local data files
dir_name = 'data/'
# Get list of all files only in the given directory
f = filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) )
# Sort list of files based on last modification time in ascending order
f = sorted( f,
                        key = lambda x: os.path.getmtime(os.path.join(dir_name, x))
                        )
f = f[::-1]

DROPDOWN = dbc.DropdownMenu(
        label="Menu",
        children=[
            dbc.DropdownMenuItem("Example", href="/morestuff/", external_link=True),
        ],
    )

NAVBAR =   dbc.Navbar(      
    dbc.Row([
        
                dbc.Col(
                    
                    dbc.Col(html.A(html.Img(src='../static/linkedin.png', height="40px",
                    style={'background-color': 'transparent'}), href='https://www.linkedin.com/in/wesley-beckner-phd-b5631ab5/',
                    ),
                    
                ),
                    width=4),
                
            dbc.Col(
                dbc.Spinner(
                    [html.H2("MintDash",
                            style={'margin': '10px',
                                   'text-align': 'center',
                                   'color': colors['text'], },
                            id='header'),
                    html.Div(id='loaddummy')], type="grow", color="primary"),
                width=4, align="center"),

            dbc.Col(dbc.Row(
                html.A("Source Code", href="https://github.com/wesleybeckner/mintdash"),
                className="row",
                style={
                    'float': 'right',
                    'margin-right': '15px',
                },
            ),
                width=4),

            ],
            justify="between",
            align="center",
            className="twelve columns",
            ),
    )

def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0
    
    if (isinstance(df_column.dtype, pd.DatetimeTZDtype) or
       (df_column.dtype == '<M8[ns]')):
        
        return 'datetime'
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype) or
             (df_column.dtype == np.float64)):
        return 'numeric'
    else:
        return 'any'

def create_table(df, id='data', filter_action='native', export='xlsx',
                 fixed_header=True, height='260', scheme=Scheme.fixed,
                 trim=Trim.yes, dark_mode=False):
    if scheme and trim:
        table = dash_table.DataTable(
            id=id,
            data=df.to_dict('records'),
            columns=[
                {'name': i, 'id': i, 'type': table_type(df[i]),
                'format': Format(precision=3, scheme=scheme,
                    trim=trim)} for i in df.columns
            ])
    else:
        table = dash_table.DataTable(
            id=id,
            data=df.to_dict('records'),
            columns=[
                {'name': i, 'id': i, 'type': table_type(df[i]),
                'format': Format(precision=3)} for i in df.columns
            ])
    table.style_table={'overflowX': 'auto',
                        'height': f'{height}px', 'overflowY': 'auto',
                        "margin": dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=30,
                                        pad=4
                                    )
                        }
    table.style_cell={'minWidth': 95}
    if filter_action:
        table.filter_action = filter_action
    if export:
        table.export = export
    if fixed_header:
        table.fixed_rows={'headers': True}
    if dark_mode:
        table.style_data={
                'color': 'white',
                'backgroundColor': 'rgb(50, 50, 50)',}
        table.style_filter={
                'color': 'white',
                'backgroundColor': 'rgb(100, 100, 100)',}
        table.style_header={
                'color': 'white',
                'backgroundColor': 'rgb(30, 30, 30)',}
        table.style_table['backgroundColor'] = 'black'
    else:
        table.style_data={
                'color': 'black'}
        table.style_filter={
                'color': 'black'}
        table.style_header={
                'color': 'black'}
    
    return table

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = None
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            print("excel")
            df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print("whoops")
        print(e)
        return html.Div([
            html.P('There was an error processing this file.'),
            html.P('Stack trace:'),
            html.P(f'{e}')
        ], style={'padding': '10px'}), None, None, None, None
    if df is not None:
        # infer dates
        for col in df.columns:
            if df[col].dtype == np.object:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
        targets = list(df.columns[df.dtypes == np.float64].values)
        descriptors = df.columns[df.dtypes != np.float64].values
        dates = None
        if df.select_dtypes(include=['datetime64']).values.shape[1] != 0:
            dates = df.select_dtypes(include=['datetime64']).iloc[:,0].dt.year.unique()

    return html.Div([
        html.H5(filename, style={'margin': '10px'}),
        html.H6(datetime.datetime.fromtimestamp(date), style={'margin': '10px'}),
        create_table(df),
        ]), [{'label': i, 'value': i} for i in descriptors],\
        [{'label': i, 'value': i} for i in targets],\
        df.to_json(), dates

def box(df, y, x, color):
    fig = px.box(df, x, y, color, points='all')
    fig.update_layout(plot_layouts)
    fig.update_layout(showlegend=False)
    return fig

def line(df, y, x, color):
    fig = px.line(df, x, y, color=color)
    fig.update_layout(plot_layouts)
    fig.update_layout(showlegend=False)
    return fig

def bar(df):
    fig = px.bar(df)
    fig.update_layout(plot_layouts)
    fig.update_layout(showlegend=False)
    return fig

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

########################################################################
######################### APP SPECIFIC FUNCTIONS #######################
######################################################################## 

def make_df(df, year=[2021],bins=[20,150],
            x='Category', quantile=0.1, topcut=20,
            aggregate_by='average'):
    # load/prepare datafile
    
    df = df.loc[df['Date'].dt.year.isin(year)]
    df = df.set_index('Date')

    # choose x, bins
    if bins:
        if bins == 'Time Comparison':
            grabs = df.resample('M').count()
            most_recent = grabs.iloc[-int(grabs.shape[0]/2):].index
            previous = grabs.loc[~grabs.index.isin(most_recent)].index
            labels = [f'before {previous[-1].date()}', f'after {previous[-1].date()}']
            
            if x != 'Date':
                dff = df.groupby(x).resample('M')[['Amount']].mean()
            else:
                dff = df.resample('M')[['Amount']].sum()
            dff = dff.reset_index()
            dff.loc[dff.Date.isin(most_recent), 'Bin'] = labels[1]
            dff.loc[dff.Date.isin(previous), 'Bin'] = labels[0]
            
        else:
            labels = [f'less than {bins[0]}', f'between {bins[0]} and {bins[1]}', f'greater than {bins[1]}']
            if x != 'Date':
                dff = df.loc[(df.Amount < bins[0])].groupby(x).resample('M')[['Amount']].sum()
                dff.columns = [labels[0]]
                dff[labels[1]] = df.loc[(df.Amount >= bins[0]) &
                                        (df.Amount < bins[1])].groupby(x).resample('M')[['Amount']].sum()
                dff[labels[2]] = df.loc[(df.Amount > bins[1])].groupby(x).resample('M')[['Amount']].sum()
                dff = dff.reset_index()
                dff = dff.melt(id_vars=[x, 'Date'], value_name='Amount', var_name='Bin')
            else:
                dff = df.loc[(df.Amount < bins[0])].resample('M')[['Amount']].sum()
                dff.columns = [labels[0]]
                dff[labels[1]] = df.loc[(df.Amount >= bins[0]) &
                                        (df.Amount < bins[1])].resample('M')[['Amount']].sum()
                dff[labels[2]] = df.loc[(df.Amount > bins[1])].resample('M')[['Amount']].sum()
                dff = dff.reset_index()
                dff = dff.melt(id_vars=['Date'], value_name='Amount', var_name='Bin')
    else:
        
        if x != 'Date':
            dff = df.groupby(x).resample('M')[['Amount']].sum()
            dff = dff.reset_index()
        else:
            dff = df.resample('M')[['Amount']].sum()
            dff = dff.reset_index()
            
    if quantile:
        mymap1 = (dff.resample(on='Date', rule='M').sum()['Amount'] <= dff.resample(on='Date', rule='M').sum().quantile(quantile)[0]).to_dict()
        mymap2 = (dff.resample(on='Date', rule='M').sum()['Amount'] >= dff.resample(on='Date', rule='M').sum().quantile(1-quantile)[0]).to_dict()

        mymap = {}
        for key, val in mymap1.items():
            if val == True:
                mymap[key] = 'Bottom'
            elif mymap2[key] == True:
                mymap[key] = 'Top'
            else:
                mymap[key] = 'Middle'
        dff['Quantile'] = dff['Date'].map(mymap)

    # cut off small - value categories (x)
    if x != 'Date':
        dfftop = dff.groupby(x)[['Amount']].sum().sort_values('Amount', ascending=False)[:topcut]
        dfftop = dfftop.reset_index()
        dff1 = dff.loc[dff[x].isin(dfftop[x])]
        dff2 = dff.loc[~dff[x].isin(dfftop[x])]
        if bins and quantile:
            dffbot = pd.DataFrame(dff2.groupby(['Date', 'Bin', 'Quantile'])['Amount'].sum()).reset_index()
        elif quantile:
            dffbot = pd.DataFrame(dff2.groupby(['Date', 'Quantile'])['Amount'].sum()).reset_index()
        elif bins:
            dffbot = pd.DataFrame(dff2.groupby(['Date', 'Bin'])['Amount'].sum()).reset_index()
        else:
            dffbot = pd.DataFrame(dff2.groupby(['Date'])['Amount'].sum()).reset_index()
        dffbot[x] = 'Other'
        dff = pd.concat([dff1, dffbot])

    # collapse onto groupby
    if aggregate_by == 'average':
        if bins and quantile:
            dff = dff.groupby([x, 'Quantile', 'Bin'])[['Amount']].mean().reset_index()
        elif quantile:
            dff = dff.groupby([x, 'Quantile'])[['Amount']].mean().reset_index()
        elif bins:
            dff = dff.groupby([x, 'Bin'])[['Amount']].mean().reset_index()
        else:
            dff = dff.groupby([x])[['Amount']].mean().reset_index()
    else:
        if bins and quantile:
            dff = dff.groupby([x, 'Quantile', 'Bin'])[['Amount']].sum().reset_index()
        elif quantile:
            dff = dff.groupby([x, 'Quantile'])[['Amount']].sum().reset_index()
        elif bins:
            dff = dff.groupby([x, 'Bin'])[['Amount']].sum().reset_index()
        else:
            dff = dff.groupby([x])[['Amount']].sum().reset_index()

    # sort results, up to 3 sort categories
    if x != 'Date':
        sorter1 = dff.groupby(x)['Amount'].sum().sort_values(ascending=False).index
        sorterIndex1 = dict(zip(sorter1, range(len(sorter1))))
    if quantile:
        sorter2 = ['Top', 'Middle', 'Bottom']
        sorterIndex2 = dict(zip(sorter2, range(len(sorter2))))
    if bins:
        sorter3 = labels
        sorterIndex3 = dict(zip(sorter3, range(len(sorter3))))
        
    if bins and x != 'Date' and quantile:
        sorters = [sorterIndex1, sorterIndex2, sorterIndex3]
    elif bins and quantile:
        sorters = [sorterIndex2, sorterIndex3]
    elif quantile:
        sorters = [sorterIndex2]
    elif bins:
        sorters = [sorterIndex3]
        
    if x != 'Date':
        dff['sort1'] = dff[x].map(sorterIndex1)
    if quantile:
        dff['sort2'] = dff.Quantile.map(sorterIndex2)
    if bins:
        dff['sort3'] = dff.Bin.map(sorterIndex3)
        if x != 'Date' and quantile:
            dff = dff.sort_values(['sort1', 'sort2', 'sort3']).reset_index(drop=True)
            dff = dff.drop(['sort1', 'sort2', 'sort3'], axis=1)
        elif quantile:
            dff = dff.sort_values(['sort2', 'sort3']).reset_index(drop=True)
            dff = dff.drop(['sort2', 'sort3'], axis=1)
        elif x != 'Date':
            dff = dff.sort_values(['sort1', 'sort3']).reset_index(drop=True)
            dff = dff.drop(['sort1', 'sort3'], axis=1)
        else:
            dff = dff.sort_values(['sort3']).reset_index(drop=True)
            dff = dff.drop(['sort3'], axis=1)
    else:
        if x != 'Date' and quantile:
            dff = dff.sort_values(['sort1', 'sort2']).reset_index(drop=True)
            dff = dff.drop(['sort1', 'sort2'], axis=1)
            sorters = [sorterIndex1, sorterIndex2]
            labels = None
        elif quantile:
            dff = dff.sort_values(['sort2']).reset_index(drop=True)
            dff = dff.drop(['sort2'], axis=1)
            sorters = [sorterIndex2]
            labels = None
        elif x != 'Date':
            dff = dff.sort_values(['sort1']).reset_index(drop=True)
            dff = dff.drop(['sort1'], axis=1)
            sorters = [sorterIndex1]
            labels = None
        else:
            sorters = None
            labels = None
    return dff, sorters, labels

def make_figs(df, year, x, bins, quantile, topcut, duplicate_legends=True, showfig=True):
    dff, sorters, labels = make_df(df, year, bins, 'Date', quantile)
    if bins:
        corr = dff.pivot(index='Date', columns='Bin', values='Amount').corr()
    if bins:
        dff, sorters, labels = make_df(df, year, bins, 'Date', quantile)
        if bins == 'Time Comparison':
            cmap = {labels[0]: '#636EFA', labels[1]: '#EF553B'}
        else:
            cmap = {labels[0]: '#636EFA', labels[1]: '#EF553B', labels[2]: '#00CC96'}
        if quantile:
            fig1 = px.bar(dff, x='Date', y='Amount', color='Bin', barmode='stack', pattern_shape='Quantile',
                     pattern_shape_sequence=[".", "", "+"], color_discrete_map=cmap)
        else:
            fig1 = px.bar(dff, x='Date', y='Amount', color='Bin', barmode='stack', color_discrete_map=cmap)

    
    elif quantile:
        fig1 = px.bar(dff, x='Date', y='Amount', barmode='stack',
                      color = 'Quantile',
        #                   pattern_shape='Quantile',
        #                  pattern_shape_sequence=[".", "", "+"]
                     )
    else:
        fig1 = px.bar(dff, x='Date', y='Amount', barmode='stack')


    fig1.update_layout(yaxis={'title': 'Amount (Total)'},
                       height=300)
    
    if showfig:
        fig1.show()

    dff, sorters, labels = make_df(df, year, bins, x, quantile, topcut)

    if bins:
        if quantile:
            fig2 = px.bar(dff, x=x, y='Amount', color='Bin', barmode='stack', pattern_shape='Quantile',
                         pattern_shape_sequence=[".", "", "+"], color_discrete_map=cmap)
        else:
            fig2 = px.bar(dff, x=x, y='Amount', color='Bin', barmode='stack', color_discrete_map=cmap)
    elif quantile:
        fig2 = px.bar(dff, x=x, y='Amount', barmode='stack', 
                      color = 'Quantile',
    #                   pattern_shape='Quantile',
    #                  pattern_shape_sequence=[".", "", "+"]
                     )
    else:
        fig2 = px.bar(dff, x=x, y='Amount', barmode='stack'
    #                   pattern_shape='Quantile',
    #                  pattern_shape_sequence=[".", "", "+"]
                     )
    fig2.update_layout(yaxis={'title': 'Amount (Monthly Average)'},
                       height=300, 
                       showlegend=duplicate_legends)
    if showfig:
        fig2.show()

    ### FIGURE 3 ###
    if quantile:
        if bins:
            growth = round(((dff.loc[dff.Quantile == 'Top'].set_index(['Category', 'Bin'])[['Amount']] -\
            dff.loc[dff.Quantile == 'Bottom'].set_index(['Category', 'Bin'])[['Amount']]) /\
            dff.loc[dff.Quantile == 'Bottom'].set_index(['Category', 'Bin'])[['Amount']]).sort_values('Amount', ascending=False)*100,0)
        else:
            growth = round(((dff.loc[dff.Quantile == 'Top'].set_index(['Category'])[['Amount']] -\
            dff.loc[dff.Quantile == 'Bottom'].set_index(['Category'])[['Amount']]) /\
            dff.loc[dff.Quantile == 'Bottom'].set_index(['Category'])[['Amount']]).sort_values('Amount', ascending=False)*100,0)

        growth = growth[~growth.isin([np.nan, -np.inf, np.inf, -100]).any(1)]
        growth = growth.reset_index()

        if bins:
            maxy = max(growth.loc[growth['Amount'] > 0].groupby('Category')['Amount'].sum())*1.2
            try:
                miny = min(growth.loc[growth['Amount'] < 0].groupby('Category')['Amount'].sum())*8
            except:
                miny = 0
            fig3 = px.bar(growth, x='Category', y='Amount', color='Bin', color_discrete_map=cmap, text='Amount')
        else:
            maxy = max(growth.loc[growth['Amount'] > 0].groupby('Category')['Amount'].sum())*1.2
            try:
                miny = min(growth.loc[growth['Amount'] < 0].groupby('Category')['Amount'].sum())*8
            except:
                miny = 0
            fig3 = px.bar(growth, x='Category', y='Amount', text='Amount')

        fig3.update_layout(yaxis={'title': '% Bottom vs Top Quantile'}, 
                           showlegend=duplicate_legends)
        if showfig:
            fig3.show()
        
    elif bins == 'Time Comparison':
        growth = round(((dff.loc[dff.Bin == labels[1]].set_index(['Category'])[['Amount']] -\
        dff.loc[dff.Bin == labels[0]].set_index(['Category'])[['Amount']]) /\
        dff.loc[dff.Bin == labels[0]].set_index(['Category'])[['Amount']]).sort_values('Amount', ascending=False)*100,0)
        growth = growth[~growth.isin([np.nan, -np.inf, np.inf, -100]).any(1)]
        growth = growth.reset_index()
        maxy = max(growth.loc[growth['Amount'] > 0].groupby('Category')['Amount'].sum())*1.2
        miny = min(growth.loc[growth['Amount'] < 0].groupby('Category')['Amount'].sum())*8
        fig3 = px.bar(growth, x='Category', y='Amount', text='Amount')
        fig3.update_layout(yaxis={'title': f'% {labels[1]} vs {labels[0]}'}, 
            showlegend=duplicate_legends, yaxis_range=[miny, maxy])
        if showfig:
            fig3.show()
    elif bins:
        fig3 = px.imshow(corr)
        fig3.update_layout({'title': "Pearson's Correlations"})
        if showfig:
            fig3.show()
    else:
        dff, sorters, labels = make_df(df, year, None, 'Date', None)
        dff = dff.resample('Y', on='Date')[['Amount']].sum()
        dff = dff.reset_index()
        dff['Date'] = dff['Date'].dt.year
        fig3 = px.bar(dff, x='Date', y='Amount')
        fig3.update_layout(showlegend=False)
        fig3.update_xaxes(
                # dtick="Y1",
                ticklabelmode="instant",
                tickformat="%Y",
                type='category')
    fig1.update_layout(plot_layouts)
    fig2.update_layout(plot_layouts)
    if fig3:
        fig3.update_layout(plot_layouts)
    return fig1, fig2, fig3