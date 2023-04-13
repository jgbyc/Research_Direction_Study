from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
from mysql_utils import MysqlDriver

app = Dash(__name__)

mysqlDriver = MysqlDriver()

tableResult = mysqlDriver.select('select * from faculty limit 50')
# print(pd.DataFrame(tableResult).to_dict('records'))
completeKeywordSet = mysqlDriver.select('select name from keyword')
# print(completeKeywordSet)

widget1 = html.Div([
    dcc.Dropdown(
        id='keyword selection',
        options=[row[0] for row in completeKeywordSet],
        value=['machine learning', 'simulation', 'neural networks'],
        multi=True,
    ),
    dcc.Graph(id='keyword count line chart'),
    dcc.RangeSlider(
        min=1900,
        max=2022,
        step=1,
        marks={i: '{}'.format(i) for i in range(1900, 2022, 10)},
        tooltip={"placement": "bottom", "always_visible": False},
        id='year slider',
        value=[1900, 2022],
        allowCross=False
    )
])

# Main layout
app.layout = html.Div([
    html.H1(children='This is the Main tittle'),
    dash_table.DataTable(data=pd.DataFrame(tableResult).to_dict('records'), page_size=6),
    widget1
])

# Callback section
@app.callback(
    Output('keyword count line chart', 'figure'),
    Input('keyword selection', 'value'),
    Input('year slider', 'value')
)
def updateKeywordCountLineChart(dropDownValue, rangeSliderValue):
    if not dropDownValue:
        fig = px.line(pd.DataFrame(data=[]))
        return fig
    queryResult = mysqlDriver.keywordCountByYear(dropDownValue, rangeSliderValue)
    # print(pd.DataFrame(data=queryResult, columns=['count', 'year', 'name']))
    fig = px.line(pd.DataFrame(data=queryResult, columns=['count', 'year', 'name']).astype({'year': 'int'}),
                  x='year', y='count', color='name')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)