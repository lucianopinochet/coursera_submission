# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
df_new = spacex_df[['Flight Number','Launch Site','class','Payload Mass (kg)','Booster Version','Booster Version Category',]]
# Create a dash application
app = dash.Dash(__name__)
options=[{'label': 'All Sites', 'value': 'ALL'},]
for value in spacex_df['Launch Site'].unique():
    options.append({'label':value, 'value':value})
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=options, value='ALL', placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000, step=1000,
                                    marks={i: str(i) for i in range(0, 10001, 1000)},
                                    value=[0,10000]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
)
def get_pie_chart(entered_site):
    data = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', names='Launch Site', title='Launch Site Success Rate')
    else:
        data = data[data['Launch Site'] == entered_site]
        data = data['class'].value_counts()
        data = pd.DataFrame(data) 
        fig = px.pie(data, values='count',names=['Failure', 'Success'], title='Launch Site Success for %s' % entered_site)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='payload-slider', component_property='value'), Input(component_id='site-dropdown', component_property='value')],
)
def get_line_chart(payload_range, entered_site):
    data = spacex_df
    if entered_site == 'ALL':
        data = data[(payload_range[0] <= data['Payload Mass (kg)']) & (payload_range[1] >= data['Payload Mass (kg)'])] 
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success Correlation with Payload')
    else:
        data = data[data['Launch Site'] == entered_site]
        data = data[(payload_range[0] <= data['Payload Mass (kg)']) & (payload_range[1] >= data['Payload Mass (kg)'])]  
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success Correlation with Payload')
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(port=8052)
