from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
from mysql_utils import MysqlDriver

app = Dash(__name__)

mysqlDriver = MysqlDriver()

tableResult = mysqlDriver.select('select * from faculty limit 50')
completeKeywordSet = mysqlDriver.select('select name from keyword')
widget1 = html.Div([
    dcc.Dropdown(
        options=[row['name'] for row in completeKeywordSet],
        multi=True,
    )
])

# Main layout
app.layout = html.Div([
    html.H1(children='This is the Main tittle'),
    dash_table.DataTable(data=tableResult, page_size=6),
    widget1
])

if __name__ == '__main__':
    app.run_server(debug=True)