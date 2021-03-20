-- edit profile
-- nm,db,g,nation,pid
update person
  set name = nm, dob = db, gender = g, nationality = nation
  where person_id = pid

-- add lang pref
-- pid,l
insert into langpreference
  select pid,id from language
  where name = l

-- search movie
-- s
select id from show
where show.name = s

-- rate a movie
-- uid,sid,r
if exists (select * from mru where mru.user_id = uid and mru.show_id=sid)
begin
  update rating
    set numeric_rating = r
    where id = (select rating_id from mru where mru.user_id = uid and mru.show_id=sid)
end
else
begin
  insert into rating(id,numeric_rating) select count(*),r from rating
  insert into mru select uid, sid, count(*) from rating
end

-- add to watchlist
-- uid,sid
if not exists (select * from watchlist where user_id=uid and show_id = sid)
begin
  insert into watchlist values(uid,sid)
end

-- add a review
-- uid,sid,r
update rating
  set review = r
  where id = (select rating_id from mru where mru.user_id = uid and mru.show_id=sid)

-- upvote a review
-- uid,sid
update rating
  set upvote = upvote + 1
  where id = (select rating_id from mru where mru.user_id = uid and mru.show_id=sid)

-- downvote a review
-- uid,sid
update rating
  set downvote = downvote + 1
  where id = (select rating_id from mru where mru.user_id = uid and mru.show_id=sid)

-- all reviews of a movie
-- sid
select review from rating,mru
where rating.id = mru.rating_id and mru.show_id = sid

-- top movies
-- t

select * from show
order by imdb_rating
limit t
