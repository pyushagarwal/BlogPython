PRAGMA foreign_keys = ON;
drop table if exists likes;
create table likes(
	uid integer not null,
	post_id integer not null,
	Foreign Key(uid) references users(uid), 
	Foreign Key(post_id) references entries(id),
	unique(uid,post_id)
	);
insert into likes values(1,5);
insert into likes values(2,4);
select * from likes;
select *,count(*) as 'likes' from entries  join likes on entries.id = likes.post_id  group by entries.id;
select entries.id,heading,detail,users.username,likes,count(*) as 'likes' from entries left join likes on entries.id = likes.post_id  inner join users on users.uid = entries.uid  group by entries.id order by entries.id desc;
alter table entries add column likes integer default '0';
update entries set likes = (select * from entries inner join likes group by entries.id)
delete 