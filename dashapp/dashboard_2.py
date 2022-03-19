from dash import dash, dcc, html, Input, Output
from app.models import User, Post, db
import plotly.express as px
import pandas as pd
from .layout import html_layout







def dashboard_2(server):
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_2/",
        external_stylesheets=[
            '/static/main.css',
        ]
    )

    app.index_string = html_layout



    app.layout = html.Div(children=[
        html.Div([
            "Range Selector: ",
            dcc.RadioItems([5, 10, 20, 30], 10, id='range-selection', inline=True, style={"padding":"5px"}),
            dcc.Graph(id='graph-with-selector', className="media content-section"),

        ])])


    @app.callback(
        Output('graph-with-selector', 'figure'),
        Input('range-selection', 'value'))
    def update_figure(range_selection):
        posts = db.session.query(Post, User).join(User)
        posts_df = pd.read_sql(posts.statement, posts.session.bind)
        posts_df.sort_values(by=['view_count'], ascending=True, inplace=True)
        posts_df = posts_df.tail(range_selection)

        fig = px.bar(
            posts_df,
            title="Most Viewed Posts",
            orientation='h',
            y="title",
            x='view_count',
            # text_auto=True,
            text="Username: " + posts_df["username"].astype(str) + "<br>View Count: " + posts_df["view_count"].astype(
                str),
            height=750,
            # color="username"
        )

        fig.update_layout(bargap=0.2)

        return fig



    return app.server

