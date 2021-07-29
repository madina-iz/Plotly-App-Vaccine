# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from joblib import load
app_pipe = load('assets/model8.joblib')
import pandas as pd
import dash_table
from collections import OrderedDict
# Imports from this application
import app
from app import app
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from category_encoders import OneHotEncoder, OrdinalEncoder
import datetime as dt


# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
          

                        
            # Select from dropdown options:

            """
        ),
        dcc.Markdown('#### Opinion about Vaccine Effectiveness (on a scale from 1 to 5):'), 
        dcc.Dropdown(
            id='opinion_seas_vacc_effective', 
            options = [
            {'label': 1., 'value': 1.},
            {'label': 2., 'value': 2.},
            {'label': 3., 'value': 3.},
            {'label': 4., 'value': 4.},
            {'label': 5., 'value': 5.}                             
            ],  
            className='mb-5',
            clearable=False,
            value=1. 
        ),
        dcc.Markdown('#### Opinion about Flu Infection Risk (on a scale from 1 to 5):'), 
        dcc.Dropdown(
            id='opinion_seas_risk', 
            options = [
            {'label': 1., 'value': 1.},
            {'label': 2., 'value': 2.},
            {'label': 3., 'value': 3.},
            {'label': 4., 'value': 4.},
            {'label': 5., 'value': 5.}                             
            ],  
            className='mb-5',
            clearable=False,
            value=1. 
        ),
        dcc.Markdown('#### Doctor Recommended?'), 
        dcc.Dropdown(
            id='doctor_recc_seasonal', 
            options = [
            {'label': 'No', 'value': 0.},
            {'label': 'Yes', 'value': 1.},                                    
            ],  
            className='mb-5',
            clearable=False,
            value=0. 
        ),
        dcc.Markdown('#### Age Group:'), 
        dcc.Dropdown(
            id='age_group', 
            options = [
            {'label': '18 - 34 Years', 'value': '18 - 34 Years'},
            {'label': '35 - 44 Years', 'value': '35 - 44 Years'},
            {'label': '45 - 54 Years', 'value': '45 - 54 Years'},
            {'label': '55 - 64 Years', 'value': '55 - 64 Years'},
            {'label': '65+ Years', 'value': '65+ Years'}                                           
            ],  
            className='mb-5',
            clearable=False,
            value='18 - 34 Years' 
        ),
        dcc.Markdown('#### Opinion about Getting Sick from Vaccine (on a scale from 1 to 5):'), 
        dcc.Dropdown(
            id='opinion_seas_sick_from_vacc', 
            options = [
            {'label': 1., 'value': 1.},
            {'label': 2., 'value': 2.},
            {'label': 3., 'value': 3.},
            {'label': 4., 'value': 4.},
            {'label': 5., 'value': 5.}                             
            ],  
            className='mb-5',
            clearable=False,
            value=1. 
        ),
        dcc.Markdown('#### Health Worker?'), 
        dcc.Dropdown(
            id='health_worker', 
            options = [
            {'label': 'No', 'value': 0.},
            {'label': 'Yes', 'value': 1.},                                    
            ],  
            className='mb-5',
            clearable=False,
            value=0. 
        ),
        dcc.Markdown('#### Have Health Insurance?'), 
        dcc.Dropdown(
            id='health_insurance', 
            options = [
            {'label': 'No', 'value': 0.},
            {'label': 'Yes', 'value': 1.},                                    
            ],  
            className='mb-5',
            clearable=False,
            value=0. 
        ),
        dcc.Markdown('#### Level of Education:'), 
        dcc.Dropdown(
            id='education', 
            options = [
            {'label': '< 12 Years', 'value': '< 12 Years'},
            {'label': '12 Years', 'value': '12 Years'},
            {'label': 'Some College', 'value': 'Some College'},
            {'label': 'College Graduate', 'value': 'College Graduate'},                                                 
            ],  
            className='mb-5',
            clearable=False,
            value='< 12 Years'
        ),
        
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            # Prediction

            ### Predict whether a person got vaccinated based on selections:

            """
        ),
        html.Div(id='prediction-content', className='lead', style={'font-style': 'italic', 'color': 'orange'})        
    ],
    md=4,
)

@app.callback(
    dash.dependencies.Output('prediction-content', 'children'),
    [dash.dependencies.Input('opinion_seas_vacc_effective', 'value'),
    dash.dependencies.Input('opinion_seas_risk', 'value'),
    dash.dependencies.Input('doctor_recc_seasonal', 'value'),
    dash.dependencies.Input('age_group', 'value'),
    dash.dependencies.Input('opinion_seas_sick_from_vacc', 'value'), 
    dash.dependencies.Input('health_worker', 'value'),
    dash.dependencies.Input('health_insurance', 'value'),
    dash.dependencies.Input('education', 'value')])

def predict(opinion_seas_vacc_effective, opinion_seas_risk, doctor_recc_seasonal, age_group,
            opinion_seas_sick_from_vacc, health_worker, health_insurance, education):
    df = pd.DataFrame(
        columns=['opinion_seas_vacc_effective','opinion_seas_risk','doctor_recc_seasonal','age_group',
                 'opinion_seas_sick_from_vacc', 'health_worker', 'health_insurance', 'education'],
        data=[[opinion_seas_vacc_effective, opinion_seas_risk, doctor_recc_seasonal, age_group,
               opinion_seas_sick_from_vacc, health_worker, health_insurance, education]]
    )
    
    y_pred = app_pipe.predict(df)[0]
    #print(y_pred)
    if y_pred == 0:
        return "NO - THE PERSON DID NOT GET VACCINATED"
    else:
        return "YES - THE PERSON GOT VACCINATED"
    #return f'{y_pred:.2f}'


layout = dbc.Row([column1, column2])