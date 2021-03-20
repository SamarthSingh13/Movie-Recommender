DROP TABLE if exists mru;
DROP TABLE if exists rating;
DROP TABLE if exists watchlist;
DROP TABLE if exists langpreference;
DROP TABLE if exists userp;
DROP TABLE if exists director;
DROP TABLE if exists actor;
DROP TABLE if exists person;
DROP TABLE if exists origin_country;
DROP TABLE if exists country;
DROP TABLE if exists original_language;
DROP TABLE if exists language;
DROP TABLE if exists genre_of;
DROP TABLE if exists genre;
DROP TABLE if exists available;
DROP TABLE if exists ott;
DROP TABLE if exists show;

CREATE TABLE show (
  id int,
  title text,
  duration int,
  release_year int,
  avg_rating float,
  imdb_rating float,
  rotten_tomato text,
  is_movie int,
  PRIMARY KEY (id)
);

CREATE TABLE ott (
  id int,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE available (
  show_id int,
  ott_id int,
  PRIMARY KEY (show_id,ott_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(ott_id) references ott(id)
);

CREATE TABLE genre (
  id int,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE genre_of (
  show_id int,
  genre_id int,
  PRIMARY KEY (show_id,genre_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(genre_id) references genre(id)
);

CREATE TABLE language (
  id int,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE original_language (
  show_id int,
  language_id int,
  PRIMARY KEY (show_id,language_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(language_id) references language(id)
);

CREATE TABLE country (
  id int,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE origin_country (
  show_id int,
  country_id int,
  PRIMARY KEY (show_id,country_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(country_id) references country(id)
);

CREATE TABLE person (
  id int,
  name text,
  dob date,
  gender text,
  PRIMARY KEY (id)
);

CREATE TABLE actor (
  show_id int,
  person_id int,
  PRIMARY KEY (show_id,person_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(person_id) references person(id)
);

CREATE TABLE director (
  show_id int,
  person_id int,
  PRIMARY KEY (show_id,person_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(person_id) references person(id)
);

CREATE TABLE userp (
  person_id int,
  userpname text,
  email text,
  password text,
  nationality int,
  PRIMARY KEY (person_id),
  FOREIGN KEY(person_id) references person(id),
  FOREIGN KEY(nationality) references country(id)
);

CREATE TABLE langpreference (
  person_id int,
  language_id int,
  PRIMARY KEY (person_id,language_id),
  FOREIGN KEY(person_id) references person(id),
  FOREIGN KEY(language_id) references language(id)
);

CREATE TABLE watchlist (
  userp_id int,
  show_id int,
  PRIMARY KEY (userp_id,show_id),
  FOREIGN KEY(userp_id) references userp(person_id),
  FOREIGN KEY(show_id) references show(id)
);

CREATE TABLE rating (
  id int,
  numeric_rating float,
  review text,
  upvotes int,
  downvotes int,
  PRIMARY KEY (id)
);

CREATE TABLE mru (
  show_id int,
  userp_id int,
  rating_id int,
  PRIMARY KEY (show_id,userp_id),
  FOREIGN KEY(show_id) references show(id),
  FOREIGN KEY(userp_id) references userp(person_id),
  FOREIGN KEY(rating_id) references rating(id)
);
