# dash_exercise
A simple dashboard using Dash, Plotly, Pandas. 

## Dependencies -
The Assignment was solved using the following:
1.	Python 3.8 Interpreter (3.8.5)
2.	Dash 2.0.0
3.	Dash-table 5.0.0
4.	Flask 2.0.2
5.	Pandas 1.3.4
6.	Plotly 5.1.0

## Remarks -
The distinguish between numeric variables to categorical made on a personal logic basis, and then using the function ‘get_col_keys’ by a specific threshold.

All graphs were build using plotly-express, besides the charts with two categorical variables that was too complexed and was build using plotly graph objects.

When a user will enter the same variable to both X and Y dropdowns, Dash will issue a warning and return an empty graph, using dbc.Alert.

Style was made using ‘external_stylesheets’ and with the style attribute of the components.
It considered best practice to include all css style in a specific file, so I tried to match it.

The Dash App is working and there are 7 screenshots, with different styles to show that.


### See More examples at:
https://dash.gallery/Portal/

