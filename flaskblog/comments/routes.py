from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Comment, Post
from flaskblog.comments.forms import CommentForm

comments = Blueprint('comments', __name__)


@comments.route("/comment/<int:post_id>/new", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('create_comment.html', post=post, form=form, legend='Create Comment')


@comments.route("/comment/<int:post_id>/<int:comment_id>")
def comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return render_template('post.html', comment=comment)
