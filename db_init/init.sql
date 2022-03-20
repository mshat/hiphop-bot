CREATE DATABASE hiphop_bot;

CREATE ROLE program WITH PASSWORD 'test';
GRANT ALL PRIVILEGES ON DATABASE hiphop_bot TO program;
ALTER ROLE program WITH LOGIN;

--connect as program
\c hiphop_bot program

--table Gender
CREATE TABLE gender(
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) NOT NULL
);

INSERT INTO gender VALUES
    (0, 'male'),
    (1, 'female');

--table Theme
CREATE TABLE theme (
    id SERIAL PRIMARY KEY,
    name VARCHAR(15) NOT NULL
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
    id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL
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
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    year_of_birth INT NOT NULL,
    group_members_num INT NOT NULL,
    theme_id INT REFERENCES theme (id) NOT NULL,
    gender_id INT REFERENCES gender (id) NOT NULL,
    genre_id INT REFERENCES genre (id) NOT NULL
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
    id SERIAL PRIMARY KEY,
    first_artist_id INT REFERENCES artist (id) NOT NULL,
    second_artist_id INT REFERENCES artist (id) NOT NULL,
    proximity FLOAT NOT NULL
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


--table Genres_adjacency_table
CREATE TABLE genres_adjacency_table (
    id SERIAL PRIMARY KEY,
    parent_genre_node_id INT REFERENCES genre (id) NOT NULL,
    child_genre_node_id INT REFERENCES genre (id) NOT NULL
);

CREATE TEMP TABLE new_genres_adjacency_table (info json);
\copy new_genres_adjacency_table from 'docker-entrypoint-initdb.d/genres_adjacency_table.json'

insert into genres_adjacency_table (id, parent_genre_node_id, child_genre_node_id)
select p.*
from new_genres_adjacency_table l
  cross join lateral json_populate_recordset(null::genres_adjacency_table, info) as p
on conflict (id) do update
  set parent_genre_node_id = excluded.parent_genre_node_id,
  child_genre_node_id = excluded.child_genre_node_id;


--table streaming_service
CREATE TABLE streaming_service(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

CREATE TEMP TABLE new_streaming_service (info json);
\copy new_streaming_service from 'docker-entrypoint-initdb.d/streaming_services.json'

insert into streaming_service (id, name)
select p.*
from new_streaming_service l
  cross join lateral json_populate_recordset(null::streaming_service, info) as p
on conflict (id) do update
  set name = excluded.name;


--table streaming_service_link
CREATE TABLE streaming_service_link(
    id SERIAL PRIMARY KEY,
    artist_id INT REFERENCES artist (id) NOT NULL,
    streaming_service_id INT REFERENCES streaming_service (id) NOT NULL,
    link VARCHAR(150) NOT NULL
);

CREATE TEMP TABLE new_streaming_service_link (info json);
\copy new_streaming_service_link from 'docker-entrypoint-initdb.d/streaming_service_links.json'

insert into streaming_service_link (id, artist_id, streaming_service_id, link)
select p.*
from new_streaming_service_link l
  cross join lateral json_populate_recordset(null::streaming_service_link, info) as p
on conflict (id) do update
  set artist_id = excluded.artist_id,
  streaming_service_id = excluded.streaming_service_id,
  link = excluded.link;


--table tg_user
CREATE TABLE tg_user (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    username VARCHAR(32)
);

--table query_solving_state
CREATE TABLE query_solving_state (
    id SERIAL PRIMARY KEY,
    state VARCHAR(8) NOT NULL
);

INSERT INTO query_solving_state VALUES
    (0, 'solved'),
    (1, 'unsolved');

--table user_history
CREATE TABLE user_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES tg_user (id) NOT NULL,
    query_solving_state_id INT REFERENCES query_solving_state (id) NOT NULL,
    query VARCHAR(200),
    query_time timestamp NOT NULL,
    matched_handler VARCHAR(30)
);