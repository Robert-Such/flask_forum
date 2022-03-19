from dash import dash, dcc, html
from app.models import User, Post, Comment, Upvote, Downvote
import plotly.express as px
import pandas as pd
from .layout import html_layout

users = User.query
posts = Post.query
comments = Comment.query
upvotes = Upvote.query
downvotes = Downvote.query

users_df = pd.read_sql(users.statement, users.session.bind)
posts_df = pd.read_sql(posts.statement, posts.session.bind)
comments_df = pd.read_sql(comments.statement, comments.session.bind)
upvotes_df = pd.read_sql(upvotes.statement, upvotes.session.bind)
downvotes_df = pd.read_sql(downvotes.statement, downvotes.session.bind)


def dashboard_1(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_1/",
        external_stylesheets=['/static/main.css']
    )

    dash_app.index_string = html_layout

    user_volume = px.histogram(
        users_df,
        title="Users Added Over Time",
        x="date_created",
        text_auto=True,
        height=400,
    )

    post_volume = px.histogram(
        posts_df,
        title="Post Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400
    )

    comment_volume = px.histogram(
        comments_df,
        title="Comment Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400,
    )

    upvote_volume = px.histogram(
        upvotes_df,
        title="Upvote Volume Over Time",
        x="date_posted",
        text_auto=True,
        height=400,
    )

    downvote_volume = px.histogram(
        downvotes_df,
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
        html.Div([
            dcc.Graph(id='graph1', figure=user_volume, className="media content-section"),
            dcc.Graph(id='graph2', figure=post_volume, className="media content-section"),
            dcc.Graph(id='graph3', figure=comment_volume, className="media content-section"),
            dcc.Graph(id='graph4', figure=upvote_volume, className="media content-section"),
            dcc.Graph(id='graph5', figure=downvote_volume, className="media content-section"),

        ])])

    return dash_app.server

