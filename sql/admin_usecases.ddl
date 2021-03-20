-- add show
-- list
insert into show
  select count(*)+1,list from show

-- update avg_rating
-- r,sid
update show
  set avg_rating = r
  where id = sid

-- add ott
-- ott_name
insert into ott
  select count(*)+1,ott_name
  from ott

-- add director
-- dir_name,sid
insert into person(id,name)
  select count(*)+1,dir_name
  from person
insert into director
  select sid,count(*)
  from person

-- add actor
-- ac_name,sid
insert into person(id,name)
  select count(*)+1,ac_name
  from person
insert into actor
  select sid,count(*)
  from person

-- add genre
-- g
insert into genre
  select count(*)+1,g
  from genre

-- add language
-- l
insert into language
  select count(*)+1,l
  from language

-- add country
-- c
insert into country
  select count(*)+1,c
  from country
