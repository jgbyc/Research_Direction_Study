from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
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
# top keywords fig
queryResult = neo4jDriver.top_keywords()
keywordfig = px.histogram(queryResult, x="name", y="keyword_count", color = "name", labels={"keyword_count":"count"}, title="Top 10 Keywords",hover_name="name", hover_data=["name","keyword_count"])

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
    html.P(children='Please use this wideget to search and insert the faculty\'s information.'),

    dcc.Input(id="faculty name", type="text", placeholder="Input Name", debounce=True),
    dcc.Input(id="faculty position", type="text", placeholder="Input Postion", debounce=True),
    dcc.Input(id="faculty email", type="email", placeholder="Input Email", debounce=True),
    dcc.Input(id="faculty phone", type="text", placeholder="Input Phone", debounce=True),
    dcc.Input(id="faculty university name", type="text", placeholder="Input university name", debounce=True),

    dcc.Input(id="faculty research interest", type="text", placeholder="Input Research Interest"),
    dcc.Input(id="faculty photo_url", type="url", placeholder="Input Photo Url"),

    dash_table.DataTable(id='faculty table', page_size=6,
                         columns=[{'name': 'Name', 'id':'Name'}, {'name': 'Position', 'id':'Position'}, {'name': 'Email', 'id':'Email'},
                                  {'name': 'Phone', 'id':'Phone'}, {'name': 'University', 'id':'University'}]),
    html.Button(id='insert faculty button', n_clicks=0, children='Insert New Faculty'),
    html.Div(id='insert new faculty state')
])

publicationWidget = html.Div([
    html.H2(children='Publication\' Information'),
    html.P(children='Please use this wideget to search and insert the publication\'s information.'),

    dcc.Input(id="publication title", type="text", placeholder="Input Title", debounce=True),
    dcc.Input(id="publication venue", type="text", placeholder="Input Venue", debounce=True),
    dcc.Input(id="publication year", type="text", placeholder="Input Year", debounce=True),
    dcc.Input(id="publication num_citations", type="number", placeholder="Input Number of Citations", debounce=True),
    dash_table.DataTable(id='publication table', page_size=6),
    html.Button(id='delete publication button', n_clicks=0, children='Delete listed publications'),
    html.Div(id='delete publication state')
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

widget4 = html.Div([
    dcc.Graph(
        id='Top Keywords',
        figure=keywordfig
    )

])

# Main layout
app.layout = html.Div([
    html.H1(children='This is the Main tittle'),
    widget1,
    widget2,
    widget3,
    widget4,
    facultyWidget,
    publicationWidget
])

# widget1 line chart
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

# facultyWidget
@app.callback(
    Output('faculty table', 'data'),
    Output('faculty table', 'tooltip_data'),
    Input('faculty name', 'value'),
    Input('faculty position', 'value'),
    Input('faculty email', 'value'),
    Input('faculty phone', 'value'),
    Input('faculty university name', 'value')
)
def getFacultyInformation(queryName, queryPosition, queryEmail, queryPhone, queryUniversityName):
    queryResult = mysqlDriver.getFaculty(queryName, queryPosition, queryEmail, queryPhone, queryUniversityName)
    data = pd.DataFrame(data=queryResult, columns=['Name', 'Position', 'Research Interest', 'Email', 'Phone', 'Photo URL', 'University']).to_dict('records')
    tooltip_data = [{
            column: {
                'value': '**Photo:**\n\n![](' + row['Photo URL']
                + ')\n\n**Research Interest:** ' + str(row['Research Interest']),
                'type': 'markdown'
            } for column in row
        } for row in data]
    return data, tooltip_data

@app.callback(
    Output('insert new faculty state', 'children'),
    Input('insert faculty button', 'n_clicks'),
    State('faculty name', 'value'),
    State('faculty position', 'value'),
    State('faculty email', 'value'),
    State('faculty phone', 'value'),
    State('faculty university name', 'value'),
    State('faculty research interest', 'value'),
    State('faculty photo_url', 'value')
)
def updateFaculty(n_clicks, insertName, insertPosition, insertEmail, insertPhone, insertUniversityName, insertResearchInterest, insertPhotoURL):
    if (n_clicks == 0):
        return ''
    response = mysqlDriver.insertFaculty(insertName, insertPosition, insertEmail, insertPhone, insertUniversityName, insertResearchInterest, insertPhotoURL)
    return response

@app.callback(
    Output('publication table', 'data'),
    Input('publication title', 'value'),
    Input('publication venue', 'value'),
    Input('publication year', 'value'),
    Input('publication num_citations', 'value')
)
def getPublicationInformation(queryTitle, queryVenue, queryYear, queryNumOfCitations):
    queryResult = mysqlDriver.getPublication(queryTitle, queryVenue, queryYear, queryNumOfCitations)
    data = pd.DataFrame(data=queryResult, columns=['Title', 'Venue', 'Year', 'Number of Citations']).to_dict('records')
    return data

@app.callback(
    Output('delete publication state', 'children'),
    Input('delete publication button', 'n_clicks'),
    State('publication title', 'value'),
    State('publication venue', 'value'),
    State('publication year', 'value'),
    State('publication num_citations', 'value')
)
def updatePublication(n_clicks, title, venue, year, numOfCitations):
    if (n_clicks == 0):
        return ''
    response = mysqlDriver.deletePublication(title, venue, year, numOfCitations)
    return response

# widget2 scatter plot
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

# widget3 treemap
@app.callback(
    Output('Top University by Keyword', 'figure'),
    Input('keyword selection', 'value'),
)
def updateTop10UniveristyByKeyword(dropDownValue):
    if not dropDownValue:
        fig = px.line(pd.DataFrame(data=[]))
        return fig
    queryResult = neo4jDriver.top_university(dropDownValue)
    fig = px.treemap(queryResult, path=["University"], values='Publication_count',color='University', width=1000, height=700, hover_name="University", hover_data=["University","Publication_count"])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)