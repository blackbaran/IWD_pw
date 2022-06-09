import dash
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from dash.dependencies import Input, Output

# tutorial:
# https://www.statworx.com/en/content-hub/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/


# Load data
df = pd.read_csv("data/stockdata2.csv", index_col=0, parse_dates=True)
df.index = pd.to_datetime(df["Date"])


# functions
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({"label": i, "value": i})

    return dict_list


# Initialise the app
app = dash.Dash(__name__)


@app.callback(Output("timeseries", "figure"), [Input("stockselector", "value")])
def value(selected_dropdown_value):
    """
    Draw traces of the feature 'value' based one the currently selected stocks
    """
    trace = []
    df_sub = df

    for stock in selected_dropdown_value:
        trace.append(
            go.Scatter(
                x=df_sub[df_sub["stock"] == stock].index,
                y=df_sub[df_sub["stock"] == stock]["value"],
                mode="lines",
                opacity=0.7,
                name=stock,
                textposition="bottom center",
            )
        )

    traces = [trace]
    data = [val for sublist in traces for val in sublist]

    figure = {
        "data": data,
        "layout": go.Layout(
            colorway=["#5E0DAC", "#FF4F00", "#375CB1", "#FF7400", "#FFF400", "#FF0056"],
            template="plotly_dark",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            margin={"b": 15},
            hovermode="x",
            autosize=True,
            title={
                "text": "Stock Prices",
                "font": {"color": "white", "size": 40},
                "x": 0.5,
            },
            xaxis={"range": [df_sub.index.min(), df_sub.index.max()]},
        ),
    }

    return figure


@app.callback(Output("change", "figure"), [Input("stockselector", "value")])
def update_change(selected_dropdown_value):
    """Draw traces of the feature 'change' based one the currently selected stocks"""
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(
            go.Scatter(
                x=df_sub[df_sub["stock"] == stock].index,
                y=df_sub[df_sub["stock"] == stock]["change"],
                mode="lines",
                opacity=0.7,
                name=stock,
                textposition="bottom center",
            )
        )
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {
        "data": data,
        "layout": go.Layout(
            colorway=["#5E0DAC", "#FF4F00", "#375CB1", "#FF7400", "#FFF400", "#FF0056"],
            template="plotly_dark",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            margin={"t": 50},
            height=250,
            hovermode="x",
            autosize=True,
            title={"text": "Daily Change", "font": {"color": "white"}, "x": 0.5},
            xaxis={
                "showticklabels": False,
                "range": [df_sub.index.min(), df_sub.index.max()],
            },
        ),
    }

    return figure


# Define the app
app.layout = html.Div(
    children=[
        html.Div(
            className="row",  # Define the row element
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("Dash - STOCK PRICES"),
                        html.P("""Visualising time series with Plotly - Dash"""),
                        html.P("""Pick one or more stocks from the dropdown below."""),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="stockselector",
                                    options=get_options(df["stock"].unique()),
                                    multi=True,
                                    value=[df["stock"].sort_values()[0]],
                                    style={"backgroundColor": "#1E1E1E"},
                                    className="stockselector",
                                )
                            ],
                            style={"color": "#1E1E1E"},
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id="timeseries",
                            config={"displayModeBar": False},
                            animate=True,
                        ),
                        dcc.Graph(id="change", config={"displayModeBar": False}),
                    ],
                ),
            ],
        )
    ]
)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
