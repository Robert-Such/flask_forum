from dash import dash, dcc, html, Input, Output
from app.models import User, Post, Comment, db
import plotly.express as px
import pandas as pd
from .layout import html_layout


post = db.session.query(Post, User).join(User)
posts = pd.read_sql(post.statement, post.session.bind)
posts_per_user = posts['username'].value_counts()

comment = db.session.query(Comment, User).join(User)
comments = pd.read_sql(comment.statement, comment.session.bind)
comments_per_user = comments['username'].value_counts()


def dashboard_3(server):
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_3/",
        external_stylesheets=[
            '/static/main.css',
        ]
    )

    app.index_string = html_layout


    app.layout = html.Div(children=[
        html.Div([
            "Type Selector: ",
            dcc.RadioItems(['Posts', 'Comments'], 'Posts', id='type-selection', inline=True, style={"padding": "5px"}),
            dcc.Graph(id='graph-with-selector', className="media content-section"),

        ])])

    @app.callback(
        Output('graph-with-selector', 'figure'),
        Input('type-selection', 'value'))
    def update_figure(type_selection):
        if type_selection == 'Posts':
            post = db.session.query(Post, User).join(User)
            posts = pd.read_sql(post.statement, post.session.bind)
            posts_per_user = posts['username'].value_counts()
            fig = px.treemap(posts_per_user,
                             title='Post Volume Per User',
                             path=[px.Constant("user Base"), posts_per_user.index],
                             values='username',
                             color='username',
                             height=750
                             )
            fig.data[0].textinfo = 'label+text+value'
            return fig
        else:
            comment = db.session.query(Comment, User).join(User)
            comments = pd.read_sql(comment.statement, comment.session.bind)
            comments_per_user = comments['username'].value_counts()
            fig = px.treemap(comments_per_user,
                             title='Comment Volume Per User',
                             path=[px.Constant("user Base"), comments_per_user.index],
                             values='username',
                             color='username',
                             height=750
                             )
            fig.data[0].textinfo = 'label+text+value'
            return fig


    return app.server