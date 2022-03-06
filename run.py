from datetime import datetime
from flaskblog import create_app
from flaskblog.models import Post, Comment, User
from flask_login import current_user

app = create_app()


@app.context_processor
def static_info():
    syspostcount = Post.query.count()
    syscommentcount = Comment.query.count()
    sysusercount = User.query.count()

    if current_user.is_authenticated:
        username = current_user.username
        useremail = current_user.email
        date_created = current_user.date_created.date()
        usrpostcount = Post.query.filter_by(user_id=current_user.id).count()
        usrcommentcount = Comment.query.filter_by(user_id=current_user.id).count()

        return dict(syspostcount=syspostcount, syscommentcount=syscommentcount, sysusercount=sysusercount,
                    usrpostcount=usrpostcount, usrcommentcount=usrcommentcount, username=username,
                    useremail=useremail, date_created=date_created)
    else:
        return dict(syspostcount=syspostcount, syscommentcount=syscommentcount, sysusercount=sysusercount)


@app.template_filter('humanize')
def humanize_ts(time=False):
    now = datetime.utcnow()
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


if __name__ == '__main__':
    app.run(debug=True)
