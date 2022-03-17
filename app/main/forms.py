from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class AutoPopulateForm(FlaskForm):
    forum_start_date = DateField('Forum Start Date', validators=[DataRequired()])
    user_limit = IntegerField('User Limit', validators=[DataRequired()])
    post_limit = IntegerField('Post Limit', validators=[DataRequired()])
    comment_limit = IntegerField('Comment Limit', validators=[DataRequired()])
    upvote_limit = IntegerField('Upvote Limit', validators=[DataRequired()])
    downvote_limit = IntegerField('Downvote Limit', validators=[DataRequired()])
    submit = SubmitField('Auto Populate')


class ResetForm(FlaskForm):
    submit = SubmitField('Reset')