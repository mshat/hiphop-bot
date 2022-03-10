CREATE DATABASE hiphop_bot;

CREATE ROLE program WITH PASSWORD 'test';
GRANT ALL PRIVILEGES ON DATABASE hiphop_bot TO program;
ALTER ROLE program WITH LOGIN;

--connect as program
\c hiphop_bot program

--table Gender
CREATE TABLE gender(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(10)
);

INSERT INTO gender VALUES
    (0, 'male'),
    (1, 'female');

--table Theme
CREATE TABLE theme (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(15)
);

INSERT INTO theme VALUES
    (0, 'hard-gangsta'),
    (1, 'workout'),
    (2, 'soft-gangsta'),
    (3, 'feelings'),
    (4, 'fun'),
    (5, 'art'),
    (6, 'conscious');

--table Genre
CREATE TABLE genre(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(25)
);

CREATE TEMP TABLE new_genres (info json);
\copy new_genres from 'docker-entrypoint-initdb.d/genres.json'

insert into genre (id, name)
select p.*
from new_genres l
  cross join lateral json_populate_recordset(null::genre, info) as p
on conflict (id) do update
  set name = excluded.name;

--table Artist
CREATE TABLE artist (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    year_of_birth INT NOT NULL,
    group_members_num INT NOT NULL,
    theme_id INT REFERENCES theme (id),
    gender_id INT REFERENCES gender (id),
    genre_id INT REFERENCES genre (id)
);

CREATE TEMP TABLE new_artists (info json);
\copy new_artists from 'docker-entrypoint-initdb.d/artists.json'

insert into artist (id, name, year_of_birth, group_members_num, theme_id, gender_id, genre_id)
select p.*
from new_artists l
  cross join lateral json_populate_recordset(null::artist, info) as p
on conflict (id) do update
  set name = excluded.name,
  year_of_birth = excluded.year_of_birth,
  theme_id = excluded.theme_id,
  gender_id = excluded.gender_id,
  genre_id = excluded.genre_id;

--table Artist_pairs_proximity
CREATE TABLE artist_pairs_proximity (
    id INT NOT NULL PRIMARY KEY,
    first_artist_id INT REFERENCES artist (id),
    second_artist_id INT REFERENCES artist (id),
    proximity FLOAT
);

CREATE TEMP TABLE new_pairs_proximity (info json);
\copy new_pairs_proximity from 'docker-entrypoint-initdb.d/artist_pairs_proximity.json'

insert into artist_pairs_proximity (id, first_artist_id, second_artist_id, proximity)
select p.*
from new_pairs_proximity l
  cross join lateral json_populate_recordset(null::artist_pairs_proximity, info) as p
on conflict (id) do update
  set first_artist_id = excluded.first_artist_id,
  second_artist_id = excluded.second_artist_id,
  proximity = excluded.proximity;

select * from artist_pairs_proximity;