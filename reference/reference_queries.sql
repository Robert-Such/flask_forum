-- Getting schema information from DB (if using Sqlite):
select name, sql
from sqlite_master
where type='table'
order by name;

-- Getting schema information from DB (if using MS-SQL):
select *
from information_schema.columns
order by table_name, ordinal_position;

-- Top Users According to Post Volume
select username, count(username) as Posts_Per_User
from post join user on post.user_id = user.id
group by username
order by count(username) desc
limit 15;

-- Top Users According to Comment Volume
select username, count(username) as Comments_Per_User
from comment join user on comment.user_id = user.id
group by username
order by count(username) desc
limit 15;

-- Top Posts According to View Count
select username, view_count, post.id as Post_ID, title as Post_Title
from post join user on post.user_id = user.id
order by view_count desc
limit 15;

-- histogram of users created per week:
select strftime('Year: %Y, Week: %W', date_created) as bin, count(*) as Count
from user
group by bin
order by bin;

-- histogram of users created per month:
select strftime('Year: %Y, Month: %m', date_created) as bin, count(*) as Count
from user
group by bin
order by bin



