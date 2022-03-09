

create table [user]
(
    id         integer primary key autoincrement ,
    username   varchar  not null unique,
    email      varchar not null unique,
    date_created datetime not null default current_timestamp,
    image_file varchar  not null,
    password   varchar  not null
);


create table [post]
(
    id          integer primary key autoincrement ,
    title       varchar not null,
    date_posted datetime not null default current_timestamp,
    content     varchar not null,
    user_id     integer not null references [user]
);

create table [comment]
(
    id          integer primary key,
    date_posted datetime not null default current_timestamp,
    content     varchar not null,
    user_id     integer not null references [user],
    post_id     integer not null references [post]
);

