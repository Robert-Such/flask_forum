from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskforum import db
from flaskforum.models import Post, Comment, Upvote, Downvote
from flaskforum.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(topic=form.topic.data, title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    page = request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).paginate(page=page, per_page=5)

    if not post.view_count:
        post.view_count = 1
        db.session.commit()
    else:
        post.view_count += 1
        db.session.commit()
    return render_template('post.html', title=post.title, post=post, comments=comments)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.topic = form.topic.data
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.topic.data = post.topic
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html', title='Update Post', form=form, legend='Update Post', post=post)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/upvote", methods=['GET'])
@login_required
def upvote(post_id):
    post = Post.query.get_or_404(post_id)
    upvote = Upvote.query.filter_by(post_id=post_id).first()
    if not post:
        flash('Post does not exist.', category='error')
    elif upvote:
        post.upvote_count -= 1
        db.session.delete(upvote)
        db.session.commit()
    else:
        upvote = Upvote(user_id=current_user.id, post_id=post_id)
        post.upvote_count += 1
        db.session.add(upvote)
        db.session.commit()
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/downvote", methods=['GET'])
@login_required
def downvote(post_id):
    post = Post.query.get_or_404(post_id)
    downvote = Downvote.query.filter_by(post_id=post_id).first()
    if not post:
        flash('Post does not exist.', category='error')
    elif downvote:
        post.downvote_count -= 1
        db.session.delete(downvote)
        db.session.commit()
    else:
        downvote = Downvote(user_id=current_user.id, post_id=post_id)
        post.downvote_count += 1
        db.session.add(downvote)
        db.session.commit()
    return redirect(url_for('main.home'))

