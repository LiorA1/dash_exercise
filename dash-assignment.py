import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go


external_stylesheets = [dbc.themes.FLATLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # DARKLY  Cyborg  SLATE FLATLY  LUX

"""
Change the path below according to the location of the data file
"""
df = pd.read_csv(r"C:\pricing data.csv")

vals = list(df.columns)
numeric_vals = []  # ['Age', 'Car Age', 'Car Value', 'Car Weight', 'Margin Parameter', 'Premium']
categorical_vals = []  # ['Car Group', 'Tenure', 'Annual Miles', 'Fuel Type', 'Gender']


def get_col_keys(df_in: pd.DataFrame, threshold: int = 35) -> None:
    """
    Get all columns headers and distributes them to the numeric_vals and categorical_vals global lists,
    using a given threshold.
    :param threshold: the threshold which distinguish between numeric_vals and categorical_vals.
    :param df_in: The pandas.DataFrame
    :return: None
    """
    global vals
    global numeric_vals
    global categorical_vals

    for val in vals:
        if len(df_in[val].unique()) > threshold:
            numeric_vals.append(val)
        else:
            categorical_vals.append(val)


get_col_keys(df)


def create_grouped_df(df_in, group_column_name, target_column, aggregate_type):
    """
    Groups the data by the selected columns and aggregaion types.
    Returns a new df with the grouped data.
    """

    aggregate_type = "mean" if aggregate_type == "average" else aggregate_type

    #
    df_out = df_in[[group_column_name, target_column]]
    if target_column in categorical_vals:
        df_out['annotate'] = 1
        if target_column != group_column_name:
            if aggregate_type == "sum":
                df_out = df_out.groupby(by=[group_column_name, target_column], as_index=False)['annotate'].sum()
            else:
                df_out = df_out.groupby(by=[group_column_name, target_column], as_index=False)['annotate'].sum()
                y_stream = df_out[target_column].unique()
                df_out['annotate'] = df_out['annotate'] / len(y_stream)

        else:
            df_out = df_out.groupby(by=[group_column_name], as_index=False)
    else:
        df_out = df_out.groupby(by=[group_column_name], as_index=False)
        df_out = df_out.agg({target_column: aggregate_type})


    return df_out


@app.callback(
    Output("graph-figure", "figure"),
    Input("aggregate-dropdown", "value"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value"),
)
def update_graph_1(aggregate_type, x_axis: str, y_axis: str):
    """
    Returns the graph figure.
    The graph will include a bar plot in case the x-axis is a nominal variables, and a scatter plot in case it is numeric.
    """

    fig = {}

    if x_axis == y_axis:
        print("not a valid input")
        # use Alert
        return fig

    grouped_df = df if x_axis == y_axis else create_grouped_df(df, x_axis, y_axis, aggregate_type)

    #
    if x_axis in numeric_vals:
        # scatter graph
        fig = px.scatter(grouped_df, x=x_axis, y=y_axis)

    elif x_axis in categorical_vals:
        # bar chart

        if y_axis in categorical_vals:
            # need to build a complicated graph using go

            y_stream = df[y_axis].unique()
            y_list = list(y_stream)
            y_list.sort()

            # fig = px.sunburst(grouped_df, path=[x_axis, y_axis], values="ICounter")

            fig = go.Figure()

            for i in range(len(y_stream)):
                list_x = [s for s in grouped_df[grouped_df[y_axis] == y_list[i]][x_axis]]
                list_y = [s for s in grouped_df[grouped_df[y_axis] == y_list[i]]['annotate']]
                fig.add_trace(
                    go.Bar(x=list_x,
                           y=list_y,
                           name=str(y_list[i]))
                )

            # Add Labels and X-Y names
            fig.update_layout(barmode='stack')
            fig.update_xaxes(title_text=x_axis)
            fig.update_yaxes(title_text=y_axis)
        else:
            fig = px.bar(grouped_df, x=x_axis, y=y_axis, text=y_axis)
            fig.update_traces(texttemplate='%{text:.2s}')

    #
    return fig


same_axe_alert = dbc.Alert("You cant choose both axis to be the same field, please choose different values.",
                           color="danger",
                           dismissable=True)


@app.callback(
    Output("alert-div", "children"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value"),
)
def alert_user(x_axis: str, y_axis: str):
    res = dash.no_update
    if x_axis == y_axis:
        res = same_axe_alert
    return res


#
# Layout
boxplot_layout = (
    dbc.Container(
        [
            html.Div(
                id="header-div",
                children=[
                    html.H1("Segmented Portfolio Analysis",
                            style={
                                'margin': "8px",
                                'text-align': 'center'
                            }
                            ),
                ],

            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                # aggregate dropdown (sum, mean)
                                                                                id="aggregate-dropdown",
                                                                                options=[
                                                                                    {
                                                                                        "label": "Total",
                                                                                        "value": "sum",
                                                                                    },
                                                                                    {
                                                                                        "label": "Average",
                                                                                        "value": "average",
                                                                                    },
                                                                                ],
                                                                                value="sum",
                                                                                style={
                                                                                    'text-color': "black"
                                                                                }
                                                                            )
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                # dropdown with all columns
                                                                                id="y-axis-dropdown",
                                                                                options=[
                                                                                    {"label": str(val), "value": val}
                                                                                    for val in vals],
                                                                                multi=False,
                                                                                value=vals[0]  # "Margin Parameter"
                                                                            )
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            html.Label(
                                                                                "by",
                                                                                style={
                                                                                    'text-align': "center",
                                                                                    'margin': "auto"
                                                                                }

                                                                            )
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                # dropdown with all columns
                                                                                id="x-axis-dropdown",
                                                                                options=[
                                                                                    {"label": str(val), "value": val}
                                                                                    for val in vals],
                                                                                multi=False,
                                                                                value=vals[1]
                                                                                # "Car Group"  # "Car Age"
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                                style={
                                                                    'padding': "4px"
                                                                }

                                                            )
                                                        )
                                                    )
                                                ],
                                                style={
                                                    'margin': "4px 8px 4px 8px",
                                                },
                                            ),
                                            html.Div(id="alert-div", children=[]),
                                            html.Div(
                                                dcc.Graph(id="graph-figure"),
                                                style={
                                                    'padding': "8px",
                                                    'margin': "auto",
                                                    'width': "95%"
                                                }
                                            ),
                                        ]
                                    )
                                ],
                                inverse=True,
                            )
                        ]
                    )
                ])
        ],
        style={
            'margin': "auto",
        }

    ))

#
app.layout = boxplot_layout

if __name__ == "__main__":
    # http://127.0.0.1:8051/
    app.run_server(debug=True)
