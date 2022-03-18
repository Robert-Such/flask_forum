from dash import dash, dcc, html
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

    ppu = px.treemap(posts_per_user,
                     title='Post Volume Per User',
                     path=[px.Constant("user Base"), posts_per_user.index],
                     values='username',
                     color='username'
                     )

    cpu = px.treemap(comments_per_user,
                     title='Comment Volume Per User',
                     path=[px.Constant("user Base"), comments_per_user.index],
                     values='username',
                     color='username'
                     )

    ppu.data[0].textinfo = 'label+text+value'
    cpu.data[0].textinfo = 'label+text+value'


    app.layout = html.Div(children=[
        # All elements from the top of the page
        html.Div([
            dcc.Graph(id='graph1', figure=ppu, className="media content-section"),
            dcc.Graph(id='graph2', figure=cpu, className="media content-section"),

        ])])



    return app.server