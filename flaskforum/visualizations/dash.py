import dash
from dash import dcc
from dash import html
import plotly.express as px
from flaskforum.models import Post
from sqlalchemy import func, Date
from os import environ
from sqlalchemy import create_engine
import pandas as pd
from .layout import html_layout


db_uri = environ.get('SLF_SQLALCHEMY_DATABASE_URI')
engine = create_engine(db_uri)


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/viz/posts/"
    )

    dash_app.index_string = html_layout


    #Posts = pd.read_sql('select * from [user] join post on [user].id = post.user_id', con=engine)
    #Comments = pd.read_sql('select * from [user] join comment on [user].id = comment.user_id', con=engine)


    Users = pd.read_sql('user', con=engine)
    Posts = pd.read_sql('post', con=engine)
    Comments = pd.read_sql('comment', con=engine)
    Upvotes = pd.read_sql('upvote', con=engine)
    Downvotes = pd.read_sql('downvote', con=engine)


    user_volume = px.histogram(
        Users,
        title="Users Added Over Time",
        x="date_created",
        text_auto=True,
        height=400,
    )

    post_volume = px.histogram(
        Posts,
        title="Post Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400
    )

    comment_volume = px.histogram(
        Comments,
        title="Comment Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400,
    )

    upvote_volume = px.histogram(
        Upvotes,
        title="Upvote Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400,
    )

    downvote_volume = px.histogram(
        Downvotes,
        title="Downvote Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400,
    )


    user_volume.update_layout(bargap=0.2)
    post_volume.update_layout(bargap=0.2)
    comment_volume.update_layout(bargap=0.2)
    upvote_volume.update_layout(bargap=0.2)
    downvote_volume.update_layout(bargap=0.2)

    upvote_volume.update_traces(marker=dict(color='#30b747'), textfont_color='#000000')
    downvote_volume.update_traces(marker=dict(color='red'), textfont_color='#000000')


    dash_app.layout = html.Div(children=[
        # All elements from the top of the page
        html.Div([
            dcc.Graph(id='graph1', figure=user_volume),
            dcc.Graph(id='graph2', figure=post_volume),
            dcc.Graph(id='graph3', figure=comment_volume),
            dcc.Graph(id='graph4', figure=upvote_volume),
            dcc.Graph(id='graph5', figure=downvote_volume),

        ])])






    return dash_app.server

