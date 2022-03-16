from flaskforum import bcrypt
from flaskforum.models import User, Post, Comment, Upvote, Downvote
import names, random, random_topic
from flaskforum import create_app, db
from quote import quote
import html5lib, requests, bs4
from tenacity import *
from faker import Faker
fake = Faker()




@retry
def get_topic():
        print('*** Getting Topic ***')
        title = random_topic.get_topic()
        if title is None:
                print('Title is None... Trying Again')
                raise TryAgain
        elif title is not None:
                print(title)
                words = list(map(str, title.split()))
                topic = random.choice(words)
                return topic, title
        else:
                print('Some Other Error... Trying Again')
                raise TryAgain


@retry
def get_quote():
        print('*** Getting Quote ***')
        topic, title = get_topic()
        new_quote = quote(topic, limit=1)
        if new_quote is None:
                print('New_Quote is None... Trying Again')
                raise TryAgain
        elif new_quote is not None:
                print(new_quote)
                return topic, title, new_quote
        else:
                print('Some Other Error... Trying Again')
                raise TryAgain


def new_users(forum_start_date, user_limit):
        for i in range(user_limit):
                print(f'SEEDING USER:{i}')
                full_name = names.get_full_name()
                print(full_name)
                email_name = full_name.replace(" ", ".")
                email = f'{email_name}@gmail.com'
                pswd = 'pswd'
                hashed_password = bcrypt.generate_password_hash(pswd).decode('utf-8')
                date = fake.date_time_between(start_date=forum_start_date, end_date='now')
                user = User(username=full_name, email=email, password=hashed_password, date_created=date)
                db.session.add(user)
                db.session.commit()


def new_posts(user_limit, post_limit):
        for i in range(post_limit):
                print(f'SEEDING POST:{i}')
                user = User.query.filter_by(id=random.randint(1, user_limit)).first()
                print(user)
                topic, title, new_quote = get_quote()
                for i in range(len(new_quote)):
                        content = (new_quote[i]['quote'])[:1000]
                view_count = random.randint(50, 500)
                date = fake.date_time_between(start_date=user.date_created, end_date='now')
                post = Post(topic=topic, title=title, content=content, author=user, view_count=view_count, date_posted=date)
                db.session.add(post)
                db.session.commit()


def new_comments(user_limit, post_limit, comment_limit):
        for i in range(comment_limit):
                print(f'SEEDING COMMENT:{i}')
                user = User.query.filter_by(id=random.randint(1, user_limit)).first()
                print(user)
                post = Post.query.filter_by(id=random.randint(1, post_limit)).first()
                post_id = post.id
                topic, title, new_quote = get_quote()
                for i in range(len(new_quote)):
                        content = (new_quote[i]['quote'])[:200]
                date = fake.date_time_between(start_date=post.date_posted, end_date='now')
                comment = Comment(content=content, author=user, post_id=post_id, date_posted=date)
                db.session.add(comment)
                db.session.commit()


def new_upvotes(user_limit, post_limit, comment_limit, upvote_limit):
        for i in range(upvote_limit):
                user = User.query.filter_by(id=random.randint(1, user_limit)).first()
                date = fake.date_time_between(start_date=user.date_created, end_date='now')
                print(user)
                if (i % 2) == 0:
                        print(f'SEEDING UPVOTE (POST):{i}')
                        post = Post.query.filter_by(id=random.randint(1, post_limit)).first()
                        post_id = post.id
                        upvote = Upvote(user_id=user.id, post_id=post_id, date_posted=date)
                        post.upvote_count += 1
                        db.session.add(upvote)
                        db.session.commit()
                else:
                        print(f'SEEDING UPVOTE (COMMENT):{i}')
                        comment = Comment.query.filter_by(id=random.randint(1, comment_limit)).first()
                        comment_id = comment.id
                        upvote = Upvote(user_id=user.id, comment_id=comment_id)
                        comment.upvote_count += 1
                        db.session.add(upvote)
                        db.session.commit()


def new_downvotes(user_limit, post_limit, comment_limit, downvote_limit):
        for i in range(downvote_limit):
                user = User.query.filter_by(id=random.randint(1, user_limit)).first()
                date = fake.date_time_between(start_date=user.date_created, end_date='now')
                print(user)
                if (i % 2) == 0:
                        print(f'SEEDING UPVOTE (POST):{i}')
                        post = Post.query.filter_by(id=random.randint(1, post_limit)).first()
                        post_id = post.id
                        downvote = Downvote(user_id=user.id, post_id=post_id, date_posted=date)
                        post.downvote_count += 1
                        db.session.add(downvote)
                        db.session.commit()
                else:
                        print(f'SEEDING UPVOTE (COMMENT):{i}')
                        comment = Comment.query.filter_by(id=random.randint(1, comment_limit)).first()
                        comment_id = comment.id
                        downvote = Downvote(user_id=user.id, comment_id=comment_id)
                        comment.downvote_count += 1
                        db.session.add(downvote)
                        db.session.commit()
