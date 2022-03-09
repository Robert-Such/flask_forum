from flask import (render_template, url_for, flash,
                   redirect, abort, request, Blueprint)
from flask_login import current_user, login_required
from flaskforum import db
from flaskforum.models import Comment, Post
from flaskforum.comments.forms import CommentForm

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
def comment(comment_id, post_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    return render_template('comment.html', comment=comment, post=post)


@comments.route("/comment/<int:post_id>/<int:comment_id>/update", methods=['GET', 'POST'])
@login_required
def update_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('comments.comment', post_id=post.id, comment_id=comment.id))
    elif request.method == 'GET':
        form.content.data = comment.content
    return render_template('update_comment.html', title='Update Comment', form=form, legend='Update Comment',
                           post=post, comment=comment)


@comments.route("/comment/<int:post_id>/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id, post_id):
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    if comment.author != current_user:
        abort(403)
    print('deleting comment ID')
    print(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))

