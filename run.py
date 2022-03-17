from datetime import datetime
from app import create_app
from app.models import Post, Comment, User, Upvote, Downvote
from flask_login import current_user
from app.users import defaultavatar

app = create_app()


@app.context_processor
def static_info():
    syspostcount = Post.query.count()
    syscommentcount = Comment.query.count()
    sysusercount = User.query.count()
    systopiccount = Post.query.with_entities(Post.topic).distinct().count()
    sysupvotecount = Upvote.query.count()
    sysdownvotecount = Downvote.query.count()
    now = datetime.utcnow()

    if current_user.is_authenticated:
        username = current_user.username
        useremail = current_user.email
        date_created = current_user.date_created
        usrpostcount = Post.query.filter_by(user_id=current_user.id).count()
        usrcommentcount = Comment.query.filter_by(user_id=current_user.id).count()
        usrupvotecount = Upvote.query.filter_by(user_id=current_user.id).count()
        usrdownvotecount = Downvote.query.filter_by(user_id=current_user.id).count()

        return dict(sysupvotecount=sysupvotecount, sysdownvotecount=sysdownvotecount, systopiccount=systopiccount, syspostcount=syspostcount, syscommentcount=syscommentcount,
                    sysusercount=sysusercount, usrpostcount=usrpostcount, usrcommentcount=usrcommentcount, usrupvotecount=usrupvotecount,
                    usrdownvotecount=usrdownvotecount, username=username, useremail=useremail, date_created=date_created, now=now)
    else:
        return dict(sysupvotecount=sysupvotecount, sysdownvotecount=sysdownvotecount, systopiccount=systopiccount, syspostcount=syspostcount, syscommentcount=syscommentcount, sysusercount=sysusercount, now=now)


@app.template_filter('associate')
def associate(comment_id):
    post_id = Comment.query.filter_by(id=comment_id).first().post_id
    return post_id

@app.template_filter('avatar')
def avatar(username):
    result = defaultavatar.get_svg_avatar(username)
    return result

@app.template_filter('humanize')
def humanize_ts(time=False):
    now = datetime.utcnow()
    if(time is None):
        return 'N/A'
    diff = now - time
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"

@app.template_filter('replycount')
def replycount_ts(post_id):
    post = Post.query.get_or_404(post_id)
    replycount = Comment.query.filter_by(post_id=post.id).count()
    return replycount

@app.template_filter('lastcomment')
def lastcomment_ts(post_id):
    post = Post.query.get_or_404(post_id)
    try:
        lastcomment = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).first().date_posted
    except Exception as e:
        lastcomment = None
    return lastcomment


if __name__ == '__main__':
    app.run(debug=True)
