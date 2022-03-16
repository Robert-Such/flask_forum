from flask import render_template, Blueprint


visualizations = Blueprint('visualizations', __name__)


@visualizations.route("/viz/posts")
def viz():
    return render_template("viz.html")