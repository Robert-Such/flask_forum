from dash import dash, dcc, html, dash_table
from app.models import User, Post, db
import plotly.express as px
import pandas as pd
from .layout import html_layout



posts = db.session.query(Post, User).join(User)
posts_df = pd.read_sql(posts.statement, posts.session.bind)

def dashboard_2(server):
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_2/",
        external_stylesheets=[
            '/static/main.css',
        ]
    )

    app.index_string = html_layout

    post_volume = px.histogram(
        posts_df,
        title="Post Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400,
        color="username"
    )

    post_volume.update_layout(bargap=0.2)

    app.layout = html.Div(children=[
        # All elements from the top of the page
        html.Div([
            dcc.Graph(id='graph1', figure=post_volume, className="media content-section"),


        ])])



    return app.server

