from flask import render_template, request, Blueprint, flash
from flaskforum.models import Post, db
from flaskforum.main.forms import AutoPopulateForm, ResetForm
from flaskforum.main.utils import new_users, new_posts, new_comments, new_upvotes, new_downvotes

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/auto_populate_db", methods=['GET', 'POST'])
def auto_populate_db():
     form = AutoPopulateForm()
     if request.method == 'POST':
         forum_start_date = form.forum_start_date.data
         user_limit = form.user_limit.data
         post_limit = form.post_limit.data
         comment_limit = form.comment_limit.data
         upvote_limit = form.upvote_limit.data
         downvote_limit = form.downvote_limit.data
         db.drop_all()
         print('******  All Tables Dropped!  ******')
         db.create_all()
         print('****** New Tables Created!  ******')
         new_users(forum_start_date, user_limit)
         new_posts(user_limit, post_limit)
         new_comments(user_limit, post_limit, comment_limit)
         new_upvotes(user_limit, post_limit, comment_limit, upvote_limit)
         new_downvotes(user_limit, post_limit, comment_limit, downvote_limit)
         flash('Database has been auto populated!', 'success')
     return render_template('auto_populate_db.html', title='Auto Populate', form=form)


@main.route("/reset_db", methods=['GET', 'POST'])
def reset_db():
    form = ResetForm()
    if request.method == 'POST':
        db.drop_all()
        print('******  All Tables Dropped!  ******')
        db.create_all()
        print('****** New Tables Created!  ******')
        flash('Database has been cleared!', 'success')
    return render_template('reset_db.html', title='Reset', form=form)


# @users.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     return render_template('account.html', title='Account', form=form)


