import pandas as pd
import plotly_express as px
import dash
from dash import (
    dcc,
    html,
)
from dash.dependencies import (
    Input,
    Output,
)
import dash_bootstrap_components as dbc

df_raw = pd.read_csv(
    'https://raw.githubusercontent.com/GiselleVicatos/Sunderland_CETM25/main/country%20vaccinations.csv'
)

# CLEAN DATA

# Select only relevant columns

cols = [
    'country',
    'iso_code',
    'date',
    'people_fully_vaccinated',
]
df = df_raw[cols]

# Replace null values with value in previous row, but grouped by country
df['people_fully_vaccinated'] = df.groupby(['country'])['people_fully_vaccinated'].ffill()

# Select specific dates in the month over a 3 month period
df_final = df.loc[
    df['date'].isin(
        [
            '2021-01-15',
            '2021-02-01',
            '2021-02-15',
            '2021-03-01',
            '2021-03-15',
            '2021-04-01',
            '2021-04-15',
        ]
    )
]

# Need to pivot dataframe so that each date is a column reading
df_pivot = df_final.pivot(
    index=['iso_code', 'country'],
    columns='date',
    values='people_fully_vaccinated',
)
df_pivot.reset_index(level=0, inplace=True)
df_pivot.reset_index(level=0, inplace=True)
df_pivot = df_pivot.rename_axis(None, axis=1)

Africa = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Cameroon', 'Cape Verde', 'Central African Republic',
    'Chad', 'Comoros', 'Congo', "Cote d'Ivoire", 'Democratic Republic of the Congo', 'Djibouti', 'Egypt',
    'Equatorial Guinea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya',
    'Lesotho', 'Libya', 'Liberia', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique',
    'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Saint Helena', 'Sao Tome and Principe', 'Senegal', 'Seychelles',
    'Sierra Leone', 'Somalia', 'South Africa', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
]

Europe = [
    'Andorra', 'Albania', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria',
    'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Faeroe Islands', 'Finland', 'France', 'Georgia', 'Germany',
    'Gibraltar', 'Greece', 'Guernsey', 'Hungary', 'Iceland', 'Ireland', 'Isle of Man', 'Italy', 'Jersey', 'Kosovo',
    'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
    'North Macedonia', 'Northern Cyprus', 'Norway', 'Poland', 'Portugal', 'Romania', 'San Marino', 'Serbia', 'Slovakia',
    'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom',
]

# Dataframe with only African countries
df_africa = df_pivot[df_pivot['country'].isin(Africa)]

# Dataframe with only European countries
df_europe = df_pivot[df_pivot['country'].isin(Europe)]

# LINE GRAPH

# Line graph needs a sum of vaccinations for selected time periods
# Create new dataframe containing summations
date_data = {
    'Date': [
        '2021-01-15',
        '2021-02-01',
        '2021-02-15',
        '2021-03-01',
        '2021-03-15',
        '2021-04-01',
        '2021-04-15',
        '2021-01-15',
        '2021-02-01',
        '2021-02-15',
        '2021-03-01',
        '2021-03-15',
        '2021-04-01',
        '2021-04-15',
    ],
    'Continent': [
        'Africa', 'Africa', 'Africa', 'Africa', 'Africa', 'Africa', 'Africa', 'Europe', 'Europe', 'Europe', 'Europe',
        'Europe', 'Europe', 'Europe'
    ],
    'Fully_Vaccinated_Number': [
        df_africa['2021-01-15'].sum(), df_africa['2021-02-01'].sum(),
        df_africa['2021-02-15'].sum(), df_africa['2021-03-01'].sum(),
        df_africa['2021-03-15'].sum(), df_africa['2021-04-01'].sum(),
        df_africa['2021-04-15'].sum(),
        df_europe['2021-01-15'].sum(), df_europe['2021-02-01'].sum(),
        df_europe['2021-02-15'].sum(), df_europe['2021-03-01'].sum(),
        df_europe['2021-03-15'].sum(), df_europe['2021-04-01'].sum(),
        df_europe['2021-04-15'].sum(),
    ]
}

df_total_vacs = pd.DataFrame(date_data)

# Create line graph
figure_line = px.line(
    df_total_vacs,
    x='Date',
    y='Fully_Vaccinated_Number',
    color='Continent',
    markers=False,
    range_x=['2021-01-15', '2021-04-15'],
    color_discrete_map={
        'Africa': 'red',
        'Europe': 'blue'
    },
)

figure_line.update_xaxes(
    title_text='Date',
    title_font={'size': 18},
    showgrid=False,
)

figure_line.update_yaxes(
    title_text='Number of fully vaccinated people',
    title_font={'size': 18},
    showgrid=False,
)

figure_line.update_layout(
    title={
        'text': 'Total Number of Covid-19 Fully Vaccinated People in Europe Compared to Africa',
        'y': 1,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    font_family='Calibri',
    title_font_size=21,
    margin={'r': 150, 't': 50, 'l': 150, 'b': 50},
)

# CHOROPLETH MAP

# map only needs African and European countries, so a list is created to identify these countries
Africa_Europe = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Cameroon', 'Cape Verde', 'Central African Republic',
    'Chad', 'Comoros', 'Congo', "Cote d'Ivoire", 'Democratic Republic of the Congo', 'Djibouti', 'Egypt',
    'Equatorial Guinea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya',
    'Lesotho', 'Libya', 'Liberia', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique',
    'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Saint Helena', 'Sao Tome and Principe', 'Senegal', 'Seychelles',
    'Sierra Leone', 'Somalia', 'South Africa', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe', 'Andorra',
    'Albania', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czechia', 'Denmark', 'Estonia', 'Faeroe Islands', 'Finland', 'France', 'Georgia', 'Germany', 'Gibraltar', 'Greece',
    'Guernsey', 'Hungary', 'Iceland', 'Ireland', 'Isle of Man', 'Italy', 'Jersey', 'Kosovo', 'Latvia', 'Liechtenstein',
    'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia',
    'Northern Cyprus', 'Norway', 'Poland', 'Portugal', 'Romania', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia',
    'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom',
]

# Update dataframe with country list
df_final = df_final.loc[df_final['country'].isin(Africa_Europe)]

# Update date format
df_choropleth = df_final
df_choropleth['date'] = pd.to_datetime(df_choropleth['date'], format='%Y-%m-%d')
df_choropleth['date'] = df_choropleth['date'].dt.strftime('%d %b %Y')

# Create choropleth map
fig = px.choropleth(
    df_final,
    locations='iso_code',
    color='people_fully_vaccinated',
    hover_name='country',
    scope='world',
    color_continuous_scale='bluered',
    range_color=[0, 9000000],
    animation_frame='date',
)

fig.update_xaxes(
    domain=[0, 0.5],
    tickformat='%d %b %Y',
)

fig.update_layout(
    title={
        'text': 'Number of Fully Vaccinated People per Country',
        'y': 1,
        'x': 0.4,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    font_family='Calibri',
    title_font_size=21,
    coloraxis_colorbar=dict(title='Fully Vaccinated Numbers'),
    margin={'r': 600, 't': 50, 'l': 100, 'b': 0},
    height=700,
    width=1800,
    transition={'duration': 3000},
)

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000

fig.update_geos(projection_scale=1,
                resolution=110,
                )

# DASHBOARD

# List of annotations used in RadioItems
annotations = [
    'The purpose of the dashboard is to focus on two continents, Europe and Africa, and to show the discrepency '
    'between how many people were able to become fully vaccinated in Europe compared to how many people were able to '
    'become fully vaccinated in Africa over a three month period. The timeframe was chosen at a point when people were '
    'first becoming fully vaccinated to emphasise the discrepency in availability.',
    'The line chart shows that the rate of the total number of fully vaccinated people in Europe increases '
    'exponentially, while in Africa the increase is low and forms a plateau at the end of the three month period.',
    'The map chart highlights the growing number of fully vaccinated people in each country on the two continents. '
    'It also emphasises the discrepency in the availability of vaccines in individual European countries compared to '
    'African countries since the majority of European countries have fully vaccinated people at the end of the three '
    'month period, while Africa only has eight countries with fully vaccinated people at the end of the three '
    'month period.',
    'French Guiana is a country in South America and is an overseas region of France. In the map chart French Guiana '
    'has been mistaken as France despite France and French Guiana having separate ISO codes. This is an issue that is '
    'out of our hands, so please ignore it.',
]

# List of footnotes used in RadioItems
footnote = [
    '',
    ''' ###### The data was obtained from Kaggle, but was collected, merged and uploaded from the Our World in Data github repository. Vaccination data from each country was merged with the locations data.
    Sahni, S. (2021) *COVID-19 World Vaccination Progress. Total Vaccination for COVID-19 in the World from Our World 
    in Data.* Available at: https://www.kaggle.com/sagarsahni3/covid19-world-vaccination-progress 
    (Accessed: 17 November 2021).''',
]

# Create dashboard
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout
app.layout = dbc.Container(
    [
        # Heading row
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        'Comparing the Availability of Covid-19 Vaccinations in Europe and Africa',
                        className='text-center mb-4',
                    ),
                    width=12,
                    style={
                        'margin-top': '30px',
                        'font-family': 'Calibri',
                    },
                ),
            ],
        ),

        # Row containing RadioItems with overview, explanations, pitfalls options
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.RadioItems(
                            id='my-radio',
                            style={'padding': '10px'},
                            labelStyle={
                                'padding': '10px',
                                'font-family': 'Calibri',
                            },
                            labelClassName='font-weight-bold',
                            value=annotations[0],
                            options=[
                                {'label': 'Overview', 'value': annotations[0]},
                                {'label': 'Line Chart Explanation', 'value': annotations[1]},
                                {'label': 'Map Chart Explanation', 'value': annotations[2]},
                                {'label': 'Pitfalls', 'value': annotations[3]},
                            ],
                        ),
                    ],
                    className='text-center mb-4',
                ),
            ],
        ),

        # Row that contains the markdown that will contain overview, explanations, pitfalls
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(id='my-markdown')
                    ],
                    width={
                        'size': 10,
                        'offset': 1
                    },
                    className='font-weight-light text-justify mb-4',
                    style={'font-family': 'Calibri'},
                ),
            ],
        ),

        # Row that contains the line graph, dropdown column and cards
        dbc.Row(
            [
                # Column that contains the line graph
                dbc.Col(
                    [
                        dcc.Graph(
                            id='line_graph',
                            figure=figure_line,
                            style={'margin-bottom': '5em'}
                        ),
                    ],
                    width={
                        'size': 9,
                        'offset': 0,
                    },
                    style={
                        'margin-top': '30px',
                        'margin-left': '30px',
                    },

                ),
                # Column that contains the dropdown and cards
                dbc.Col(
                    [
                        # Row that contains the dropdown
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P(
                                            'Filter by Month:',
                                            style={
                                                'font-size': '18px',
                                                'font-family': 'Calibri',
                                                'margin-left': '30px',
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id='my-dropdown',
                                            value='2021-04-15',
                                            style={
                                                'width': '200px',
                                                'margin': 'auto',
                                            },
                                            options=[
                                                {'label': 'First Month', 'value': '2021-02-15'},
                                                {'label': 'Second Month', 'value': '2021-03-15'},
                                                {'label': 'Third Month', 'value': '2021-04-15'},
                                            ],
                                        ),
                                    ],
                                    style={
                                        'padding': '0px',
                                        'margin-top': '50px',
                                        'margin-bottom': '70px'
                                    },
                                ),
                            ],
                        ),

                        # Row that contains Card 1
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                html.H1(
                                                    id='tag1',
                                                    className='card-title ',
                                                    style={
                                                        'font-size': '20px',
                                                        'font-family': 'Calibri',
                                                    },
                                                ),
                                                html.P(
                                                    'Fully vaccinated numbers in Africa',
                                                    className='card-text ',
                                                    style={
                                                        'font-size': '13px',
                                                        'font-family': 'Calibri',
                                                    },
                                                ),
                                            ],
                                            style={
                                                'padding': '7px',
                                                'width': '205px',
                                                'font-family': 'Calibri',
                                                'font-size': '60px'
                                            },
                                            className='text-center mb-4 border-danger',
                                        ),
                                    ],
                                    style={
                                        'margin-top': '40px',
                                        'margin-bottom': '0px',
                                        'margin-left': '10px',
                                    },
                                ),
                            ],
                        ),

                        # Row that contains Card 2
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                html.H1(
                                                    id='tag2',
                                                    className='card-title ',
                                                    style={
                                                        'font-size': '20px',
                                                        'font-family': 'Calibri'
                                                    },
                                                ),
                                                html.P(
                                                    'Fully vaccinated numbers in Europe',
                                                    className='card-text ',
                                                    style={
                                                        'font-size': '13px',
                                                        'font-family': 'Calibri'
                                                    },
                                                ),
                                            ],
                                            body=True,
                                            color='white',
                                            style={
                                                'padding': '7px',
                                                'width': '205px',
                                                'font-family': 'Calibri',
                                                'font-size': '60px'
                                            },
                                            className='text-center mb-4 border-primary'
                                        ),
                                    ],
                                    style={
                                        'margin-left': '10px',
                                    },
                                ),
                            ],
                        ),
                    ],
                    width={
                        'size': 2,
                        'offset': 0
                    },
                ),
            ],
        ),

        # Row that contains the choropleth map
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='map',
                            figure=fig,
                        ),
                    ],
                    width={
                        'size': 5,
                        'offset': 0,
                    },
                    style={'margin-bottom': '30px'},
                ),
            ],
        ),

        # Row that contains RadioItems with data source options
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6(
                            'Data Source:',
                            className='text-left',
                        ),
                        dcc.RadioItems(
                            id='my-radioitem2',
                            style={
                                'padding': '2px',
                                'font-size': '15px',
                                'font-family': 'Calibri'
                            },
                            labelStyle={
                                'font-family': 'Calibri',
                                'display': 'flex'
                            },
                            labelClassName='font-weight-bold',
                            value=footnote[0],
                            options=[
                                {'label': 'Hide', 'value': footnote[0]},
                                {'label': 'Show', 'value': footnote[1]},
                            ],
                        ),
                    ],
                    width={'offset': 1},
                    style={'margin-bottom': '20px'},
                ),
            ],
        ),

        # Row that contains the markdown with the data source
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(id='my-footnote')
                    ],
                    width={
                        'size': 10,
                        'offset': 1,
                    },
                    className='font-weight-light text-justify',
                    style={'font-family': 'Calibri'},
                ),
            ],
        ),
    ],
    fluid=True,
)


# CALLBACKS

# Overview, explanations and pitfalls
@app.callback(
    Output('my-markdown', 'children'),
    Input('my-radio', 'value'),
)
def update_output(value):
    return '{}'.format(value)


# Data source
@app.callback(
    Output('my-footnote', 'children'),
    Input('my-radioitem2', 'value'),
)
def update_footnote(value):
    return '{}'.format(value)


# Line graph
@app.callback(
    Output('line_graph', 'figure'),
    Input('my-dropdown', 'value'),
)
def update_graph(toggle_value):
    print(type(toggle_value))
    dff = pd.DataFrame(date_data)
    fig = px.line(
        dff,
        x='Date',
        y='Fully_Vaccinated_Number',
        color='Continent',
        range_x=['2021-01-15', toggle_value],
        color_discrete_map={
            'Africa': 'red',
            'Europe': 'blue',
        },
    )
    fig.update_xaxes(
        title_text='Date',
        title_font={'size': 18},
        showgrid=False,
        tickformat='%d %b %Y'
    )
    fig.update_yaxes(
        title_text='Number of fully vaccinated people',
        title_font={'size': 18},
        showgrid=False,
    )
    fig.update_layout(
        title={
            'text': 'Total Number of Covid-19 Fully Vaccinated People in Europe Compared to Africa',
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        font_family='Calibri',
        title_font_size=21,
        margin={
            'r': 100,
            't': 50,
            'l': 100,
            'b': 50,
        },
    )
    return fig


# Card 1
@app.callback(
    Output('tag1', 'children'),
    Input('my-dropdown', 'value'),
)
def update_tag1(range_chosen):
    sum = df_africa[range_chosen].sum()
    my_sum = '{:,.0f}'.format(sum)
    return '{}'.format(my_sum)


# Card 2
@app.callback(
    Output('tag2', 'children'),
    Input('my-dropdown', 'value'),
)
def update_tag1(range_chosen):
    sum = (df_europe[range_chosen].sum())
    my_sum = '{:,.0f}'.format(sum)
    return '{}'.format(my_sum)


if __name__ == '__main__':
    app.run_server()
