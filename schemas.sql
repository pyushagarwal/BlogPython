PRAGMA foreign_keys = ON;

drop table if exists users;
create table users(
	uid integer primary key autoincrement,
	username text unique not null,
	password text not null
);

drop table if exists entries;
create table entries( 
	id integer primary key autoincrement,
	heading text not null,
	detail text not null,
	uid integer not null,
	likes integer default '0',
	Foreign Key(uid) references users(uid) 
	);


drop table if exists likes;
create table likes(
	uid integer not null,
	post_id integer not null,
	Foreign Key(uid) references users(uid), 
	Foreign Key(post_id) references entries(id),
	unique(uid,post_id)
	);
