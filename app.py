from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from mysql_utils import MysqlDriver
from mongodb_utils import mongodb_utils
from neo4j_utils import neo4j_utils
import textwrap
app = Dash(__name__)

mysqlDriver = MysqlDriver()
mongoDriver = mongodb_utils()
neo4jDriver = neo4j_utils()

completeKeywordSet = mysqlDriver.query('select name from keyword')
queryResult = neo4jDriver.top_keywords()
keywordfig = px.bar(
    queryResult, 
    x="name", 
    y="keyword_count", 
    labels={"keyword_count":"count"}, 
    color="keyword_count", 
    color_continuous_scale="geyser", 
    title="Top 10 Keywords", 
    hover_name="name", 
    hover_data=["name","keyword_count"]
    )

keywordDropdown = dcc.Dropdown(
    id='keyword selection',
    options=[row[0] for row in completeKeywordSet],
    value=['machine learning', 'simulation', 'neural networks'],
    multi=True,
)

keywordCountWidget = html.Div(
    [
        html.H3(children='Keyword Count Trend', style={'textAlign': 'center'}),
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
    ],
    style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}
)

facultyWidget = html.Div([
    html.H3(children='Faculty\' Information', style={'textAlign': 'center'}),
    html.P(children='Please use this wideget to search and insert the faculty\'s information.'),

    dcc.Input(id="faculty name", type="text", placeholder="Input Name", debounce=True),
    dcc.Input(id="faculty position", type="text", placeholder="Input Postion", debounce=True),
    dcc.Input(id="faculty email", type="email", placeholder="Input Email", debounce=True),
    dcc.Input(id="faculty phone", type="text", placeholder="Input Phone", debounce=True),
    dcc.Input(id="faculty university name", type="text", placeholder="Input university name", debounce=True),

    dcc.Input(id="faculty research interest", type="text", placeholder="Input Research Interest"),
    dcc.Input(id="faculty photo_url", type="url", placeholder="Input Photo Url"),

    dash_table.DataTable(
        id='faculty table', page_size=6,
        columns=[{'name': '', 'id': 'index'}, {'name': 'Name', 'id': 'Name'}, {'name': 'Position', 'id': 'Position'}, {'name': 'Email', 'id': 'Email'},
                 {'name': 'Phone', 'id': 'Phone'}, {'name': 'University', 'id': 'University'}],
        style_cell={'textAlign': 'left'},
        style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'whiteSpace': 'normal',
        'height': 'auto'
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        }
        ),
    html.Button(id='insert faculty button', n_clicks=0, children='Insert New Faculty'),
    html.Div(id='insert new faculty state')
])

publicationWidget = html.Div([
    html.H3(children='Publication\' Information', style={'textAlign': 'center'}),
    html.P(children='Please use this wideget to search and insert the publication\'s information.'),

    dcc.Input(id="publication title", type="text", placeholder="Input Title", debounce=True),
    dcc.Input(id="publication venue", type="text", placeholder="Input Venue", debounce=True),
    dcc.Input(id="publication year", type="text", placeholder="Input Year", debounce=True),
    dcc.Input(id="publication num_citations", type="number", placeholder="Input Number of Citations", debounce=True),
    dash_table.DataTable(
        id='publication table',
        columns=[{'name': '', 'id': 'index'}, {'name': 'Title', 'id': 'Title'}, {'name': 'Venue', 'id': 'Venue'}, {'name': 'Number of Citations', 'id': 'Number of Citations'}],
        page_size=6,
        style_cell={'textAlign': 'left'},
        style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'whiteSpace': 'normal',
        'height': 'auto'
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        }       
    ),
    html.Button(id='delete publication button', n_clicks=0, children='Delete listed publications'),
    html.Div(id='delete publication state')
])

topPublicationWidget = html.Div(
    [
        html.H3(children='Top Publication per Keyword', style={'textAlign': 'center'}),
        dcc.Graph(
            id='Top Publications by Keyword'
        )
    ],
    style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}
)

topUniversityWidget = html.Div(
    [
        html.H3(children='Top University per Keyword', style={'textAlign': 'center'}),
        dcc.Graph(
            id='Top University by Keyword'
        )
    ],
    style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}
)

topTenKeywordsWidget = html.Div(
    [
        html.H3(children='Top Ten Keywords', style={'textAlign': 'center'}),
        dcc.Graph(
            id='Top Keywords',
            figure=keywordfig
        )
    ],
    style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}
)

keywordGroup = html.Div([
    html.P(children='Please the dropdown list to select interested keywords'),
    keywordDropdown,
    # html.Hr(style={'border': '1px solid'}),
    keywordCountWidget,
    topPublicationWidget,
    # html.Hr(style={'border': '1px solid'}),
    topUniversityWidget,
    topTenKeywordsWidget
])
# textwrap function
def customwrap(s,width=30):
    return "<br>".join(textwrap.wrap(s, width=width))

# Main layout
app.layout = html.Div(
    [
        html.H1(children='Research Interest Study', style={'textAlign': 'center'}),
        keywordGroup,
        facultyWidget,
        publicationWidget
    ],
    id='mainDiv',
    style={'margin': 'auto', 'width': '85%', 'fontFamily': 'Arial, Helvetica, sans-serif'}
)

# Callback section
# keywordCountWidget
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
    data = pd.DataFrame(data=queryResult, columns=['Name', 'Position', 'Research Interest', 'Email', 'Phone', 'Photo URL', 'University']).reset_index().to_dict('records')
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

# Publication Widget
@app.callback(
    Output('publication table', 'data'),
    Input('publication title', 'value'),
    Input('publication venue', 'value'),
    Input('publication year', 'value'),
    Input('publication num_citations', 'value')
)
def getPublicationInformation(queryTitle, queryVenue, queryYear, queryNumOfCitations):
    queryResult = mysqlDriver.getPublication(queryTitle, queryVenue, queryYear, queryNumOfCitations)
    data = pd.DataFrame(data=queryResult, columns=['Title', 'Venue', 'Year', 'Number of Citations']).reset_index().to_dict('records')
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

# Top publication widget scatter plot
@app.callback(
    Output('Top Publications by Keyword', 'figure'),
    Input('keyword selection', 'value'),
    Input('year slider', 'value')
)
def updateTop15PublicationsByKeyword(dropDownValue, rangeSliderValue):
    if not dropDownValue:
        fig = px.line(pd.DataFrame(data=[]))
        return fig
    year_start, year_end = rangeSliderValue
    years = [x for x in range(int(year_start), int(year_end)+1)]
    queryResult = mongoDriver.top_pub(dropDownValue, years)
    if len(queryResult) > 0:
        fig = px.scatter(
            queryResult,
            x='year', 
            y='numCitations', 
            size="numCitations",
            log_y = [1000,20000],
            color=queryResult['title'].map(customwrap), 
            hover_name='title', 
            hover_data=['title', 'numCitations', 'year']#, 
            # width=1000, 
            # height=500
            )
    else:
        fig = px.line(pd.DataFrame(data=[]))
    return fig

# Top university widget treemap
@app.callback(
    Output('Top University by Keyword', 'figure'),
    Input('keyword selection', 'value'),
)
def updateUniveristyFacultyByKeyword(dropDownValue):
    if not dropDownValue:
        fig = px.line(pd.DataFrame(data=[]))
        return fig
    queryResult = neo4jDriver.top_faculty(dropDownValue)
    fig = px.treemap(
        queryResult, 
        path=[px.Constant('University'),'University','Faculty_name'], 
        values='Publication_count', 
        color = 'Publication_count', 
        color_continuous_scale='geyser'#, 
        # width=1000, 
        # height=700
        )# hover_name='University', hover_data=['Publication_count'])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)