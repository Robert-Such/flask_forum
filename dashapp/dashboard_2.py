from dash import dash, dcc, html, dash_table
from app.models import User, Post, db
import plotly.express as px
import pandas as pd
from .layout import html_layout



posts = db.session.query(Post, User).join(User)
posts_df = pd.read_sql(posts.statement, posts.session.bind)
posts_df.sort_values(by=['view_count'], ascending=True, inplace=True)
posts_df = posts_df.tail(10)


def dashboard_2(server):
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_2/",
        external_stylesheets=[
            '/static/main.css',
        ]
    )

    app.index_string = html_layout

    fig = px.bar(
        posts_df,
        title="Top Ten Most Viewed Posts",
        orientation='h',
        y="title",
        x='view_count',
        #text_auto=True,
        text="Username: " + posts_df["username"].astype(str) + "<br>View Count: " + posts_df["view_count"].astype(str),
        height=800,
        #color="username"
    )

    fig.update_layout(bargap=0.2)

    app.layout = html.Div(children=[
        # All elements from the top of the page
        html.Div([
            dcc.Graph(id='graph1', figure=fig, className="media content-section"),


        ])])



    return app.server

