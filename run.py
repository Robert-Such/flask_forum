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


if __name__ == '__main__':
    app.run(debug=True)
