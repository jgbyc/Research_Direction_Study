from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
from mysql_utils import MysqlDriver
from mongodb_utils import mongodb_utils
from neo4j_utils import neo4j_utils

app = Dash(__name__)

mysqlDriver = MysqlDriver()
mongoDriver = mongodb_utils()
neo4jDriver = neo4j_utils()

# tableResult = mysqlDriver.select('select * from faculty limit 50')
# print(pd.DataFrame(tableResult).to_dict('records'))
completeKeywordSet = mysqlDriver.query('select name from keyword')
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

facultyWidget = html.Div([
    html.H2(children='Faculty\' Information'),
    html.P(children='Please use this wideget to search and update the faculty\'s information.'),

    dcc.Input(id="faculty name", type="text", placeholder="Input Name", debounce=True),
    dcc.Input(id="faculty position", type="text", placeholder="Input Postion", debounce=True),
    dcc.Input(id="faculty email", type="email", placeholder="Input Email", debounce=True),
    dcc.Input(id="faculty phone", type="text", placeholder="Input Phone", debounce=True),
    dcc.Input(id="faculty university name", type="text", placeholder="Input university name", debounce=True),

    dcc.Input(id="faculty research interest", type="text", placeholder="Input Research Interest"),
    dcc.Input(id="faculty photo_url", type="url", placeholder="Input Photo Url"),

    dash_table.DataTable(id='faculty table', page_size=6)
])

widget2 = html.Div([
    dcc.Graph(
        id='Top Publications by Keyword'
    )
])

widget3 = html.Div([
    dcc.Graph(
        id='Top University by Keyword'
    )
])

# Main layout
app.layout = html.Div([
    html.H1(children='This is the Main tittle'),
    widget1,
    widget2,
    widget3,
    facultyWidget
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
    queryResult = mysqlDriver.getKeywordCountByYear(dropDownValue, rangeSliderValue)
    # print(pd.DataFrame(data=queryResult, columns=['count', 'year', 'name']))
    fig = px.line(pd.DataFrame(data=queryResult, columns=['count', 'year', 'name']).astype({'year': 'int'}),
                  x='year', y='count', color='name')
    return fig

@app.callback(
    Output('faculty table', 'data'),
    Input('faculty name', 'value'),
    Input('faculty position', 'value'),
    Input('faculty email', 'value'),
    Input('faculty phone', 'value'),
    Input('faculty university name', 'value')
)
def getFacultyInformation(queryName, queryPosition, queryEmail, queryPhone, queryUniversityName):
    queryResult = mysqlDriver.getFaculty(queryName, queryPosition, queryEmail, queryPhone, queryUniversityName)
    data = pd.DataFrame(data=queryResult, columns=['Name', 'Position', 'Email', 'Phone', 'University']).to_dict('records')
    return data

@app.callback(
    Output('Top Publications by Keyword', 'figure'),
    Input('keyword selection', 'value'),
)
def updateTop25PublicationsByKeyword(dropDownValue):
    if not dropDownValue:
        fig = px.line(pd.DataFrame(data=[]))
        return fig
    queryResult = mongoDriver.top_pub(dropDownValue)
    fig = px.scatter(queryResult, x='year', y='numCitations', log_y = [1000,20000],color='title', hover_name='title', hover_data=['title', 'numCitations', 'year'])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)