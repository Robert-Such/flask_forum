from dash import dash, dcc, html, Input, Output
from app.models import User, Post, Comment, Upvote, Downvote
import plotly.express as px
import pandas as pd
from .layout import html_layout


def dashboard_1(server):
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_1/",
        external_stylesheets=['/static/main.css']
    )

    app.index_string = html_layout

    app.layout = html.Div(children=[
        html.Div([
            "Type Selector: ",
            dcc.RadioItems(['Users', 'Posts', 'Comments', 'Upvotes', 'Downvotes'], 'Posts', id='type-selection', inline=True, style={"padding": "5px"}),
            dcc.Graph(id='graph-with-selector', className="media content-section"),

        ])])

    @app.callback(
        Output('graph-with-selector', 'figure'),
        Input('type-selection', 'value'))
    def update_figure(type_selection):
        height = 700
        if type_selection == 'Users':
            users = User.query
            users_df = pd.read_sql(users.statement, users.session.bind)
            fig = px.histogram(
                users_df,
                title="Users Added Over Time",
                x="date_created",
                text_auto=True,
                height=height,
            )
            fig.update_layout(bargap=0.2)
            return fig

        if type_selection == 'Posts':
            posts = Post.query
            posts_df = pd.read_sql(posts.statement, posts.session.bind)
            fig = px.histogram(
                posts_df,
                title="Post Volume Over Time",
                x="date_posted",
                text_auto=True,
                height=height
            )
            fig.update_layout(bargap=0.2)
            return fig

        if type_selection == 'Comments':
            comments = Comment.query
            comments_df = pd.read_sql(comments.statement, comments.session.bind)
            fig = px.histogram(
                comments_df,
                title="Comment Volume Over Time",
                x="date_posted",
                text_auto=True,
                height=height,
            )
            fig.update_layout(bargap=0.2)
            return fig

        if type_selection == 'Upvotes':
            upvotes = Upvote.query
            upvotes_df = pd.read_sql(upvotes.statement, upvotes.session.bind)
            fig = px.histogram(
                upvotes_df,
                title="Upvote Volume Over Time",
                x="date_posted",
                text_auto=True,
                height=height,
            )
            fig.update_layout(bargap=0.2)
            fig.update_traces(marker=dict(color='#30b747'), textfont_color='#000000')
            return fig

        if type_selection == 'Downvotes':
            downvotes = Downvote.query
            downvotes_df = pd.read_sql(downvotes.statement, downvotes.session.bind)
            fig = px.histogram(
                downvotes_df,
                title="Downvote Volume Over Time",
                x="date_posted",
                text_auto=True,
                height=height,
            )
            fig.update_layout(bargap=0.2)
            fig.update_traces(marker=dict(color='red'), textfont_color='#000000')
            return fig

    return app.server

