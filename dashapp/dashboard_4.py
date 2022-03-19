from dash import dash, html, Input, Output, dcc
from .layout import html_layout
from app.models import db
from sqlalchemy_schemadisplay import create_schema_graph
import dash_interactive_graphviz




def dashboard_4(server):
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard_4/",
        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
        #external_stylesheets=['/static/main.css']
    )

    app.index_string = html_layout


    app.layout = html.Div(
        [
            html.Div(
                dash_interactive_graphviz.DashInteractiveGraphviz(id="output"),
                style=dict(flexGrow=1, position="relative"),
            ),
            html.Div(
                [
                    html.Label('Show Datatypes?'),
                    dcc.Dropdown(
                        id='datatype',
                        options=[
                            {'label': 'Yes', 'value': True},
                            {'label': 'No', 'value': False},
                        ],
                        value=True
                    ),
                    html.Label('Show Indexes?'),
                    dcc.Dropdown(
                        id='indexes',
                        options=[
                            {'label': 'Yes', 'value': True},
                            {'label': 'No', 'value': False},
                        ],
                        value=True
                    ),
                    html.Label('Show Datatypes?'),
                    dcc.Dropdown(
                        id='direction',
                        options=[
                            {'label': 'Left to Right', 'value': 'LR'},
                            {'label': 'Right to Left', 'value': 'RL'},
                            {'label': 'Top to Bottom', 'value': 'TB'},
                            {'label': 'Bottom to Top', 'value': 'BT'},
                        ],
                        value='LR'
                    ),

                    html.Label('Concentrate?'),
                    dcc.Dropdown(
                        id='concentrate',
                        options=[
                            {'label': 'Yes', 'value': True},
                            {'label': 'No', 'value': False},
                        ],
                        value=False
                    ),
                ],
                style=dict(display="flex", flexDirection="column"),
            ),
        ],
        style=dict(position="absolute", height="100%", width="100%", display="flex"),
    )

    @app.callback(
        Output('output', 'dot_source'),
        Input('datatype', 'value'),
        Input('indexes', 'value'),
        Input('direction', 'value'),
        Input('concentrate', 'value')
    )
    def update_figure(datatype, indexes, direction, concentrate):
        graph = create_schema_graph(metadata=db.metadata,
                                    show_datatypes=datatype,  # The image would get nasty big if we'd show the datatypes
                                    show_indexes=indexes,  # ditto for indexes
                                    rankdir=direction,  # From left to right (instead of top to bottom)
                                    concentrate=concentrate  # Don't try to join the relation lines together
                                    )
        dot_source = graph.to_string()
        return dot_source

    return app.server