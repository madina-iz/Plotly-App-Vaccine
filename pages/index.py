# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            #### Vaccination is a key public health measure used to fight infectious diseases. It provides immunization for individuals, and enough immunization in a community can further reduce the spread of diseases through “herd immunity.”

            #### The National Center for Immunization and Respiratory Diseases, the National Center for Health Statistics, Centers for Disease Control and Prevention jointly conducted the National 2009 H1N1 Flu Survey.
            
            #### Based on that survey, we have built a machine learning algorithm to predict whether people got a seasonal flu vaccine using information they shared about their backgrounds, opinions, and health behaviors.            

            """
        ),
        dcc.Link(dbc.Button('Click Here to Get Predictions', color='primary'), href='/predictions')
    ],
    md=4,
)

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col(
    [
        html.Img(src='assets/feature_imp.png', className='img-fluid')
        #dcc.Graph(figure=fig),
    ]
)

layout = dbc.Row([column1, column2])