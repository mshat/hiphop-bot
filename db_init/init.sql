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
    (1, 'male'),
    (2, 'female');

--table Theme
CREATE TABLE theme (
    id SERIAL PRIMARY KEY,
    name VARCHAR(15) NOT NULL
);

INSERT INTO theme VALUES
    (1, 'hard-gangsta'),
    (2, 'workout'),
    (3, 'soft-gangsta'),
    (4, 'feelings'),
    (5, 'fun'),
    (6, 'art'),
    (7, 'conscious');

--table Genre
CREATE TABLE genre(
    id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL
);

CREATE TEMP TABLE new_genres (doc json);
\copy new_genres from 'docker-entrypoint-initdb.d/genres.json'

insert into genre (name)
select p.name
from new_genres l
  cross join lateral json_populate_recordset(null::genre, doc) as p
on conflict (id) do update
  set name = excluded.name;

--table Artist
CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    year_of_birth INT NOT NULL,
    group_members_num INT NOT NULL,
    gender_id INT REFERENCES gender (id) NOT NULL
);

-- table artists_themes
CREATE TABLE artists_themes(
    id SERIAL PRIMARY KEY,
    artist_id INT REFERENCES artist (id) NOT NULL,
    theme_id INT REFERENCES theme (id) NOT NULL
)

-- table artists_genres
CREATE TABLE artists_genres(
    id SERIAL PRIMARY KEY,
    artist_id INT REFERENCES artist (id) NOT NULL,
    genre_id INT REFERENCES genre (id) NOT NULL
)

--table Artist_pairs_proximity
CREATE TABLE artist_pairs_proximity (
    id SERIAL PRIMARY KEY,
    first_artist_id INT REFERENCES artist (id) NOT NULL,
    second_artist_id INT REFERENCES artist (id) NOT NULL,
    proximity FLOAT NOT NULL,
    proximities FLOAT[] NOT NULL
);


--table Genres_adjacency_table
CREATE TABLE genres_adjacency_table (
    id SERIAL PRIMARY KEY,
    parent_genre_node_id INT REFERENCES genre (id) NOT NULL,
    child_genre_node_id INT REFERENCES genre (id) NOT NULL
);

CREATE TEMP TABLE new_genres_adjacency_table (doc json);
\copy new_genres_adjacency_table from 'docker-entrypoint-initdb.d/genres_adjacency_table.json'

insert into genres_adjacency_table (parent_genre_node_id, child_genre_node_id)
select p.parent_genre_node_id, p.child_genre_node_id
from new_genres_adjacency_table l
  cross join lateral json_populate_recordset(null::genres_adjacency_table, doc) as p
on conflict (id) do update
  set parent_genre_node_id = excluded.parent_genre_node_id,
  child_genre_node_id = excluded.child_genre_node_id;


--table streaming_service
CREATE TABLE streaming_service(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

CREATE TEMP TABLE new_streaming_service (doc json);
\copy new_streaming_service from 'docker-entrypoint-initdb.d/streaming_services.json'

insert into streaming_service (name)
select p.name
from new_streaming_service l
  cross join lateral json_populate_recordset(null::streaming_service, doc) as p
on conflict (id) do update
  set name = excluded.name;

--table streaming_service_link
CREATE TABLE streaming_service_link(
    id SERIAL PRIMARY KEY,
    artist_id INT REFERENCES artist (id) NOT NULL,
    streaming_service_id INT REFERENCES streaming_service (id) NOT NULL,
    link VARCHAR(150) NOT NULL
);

--table artists_names_aliases
CREATE TABLE artists_names_aliases (
    id SERIAL PRIMARY KEY,
    artist_id INT REFERENCES artist (id) NOT NULL UNIQUE,
    aliases VARCHAR(100)[] NOT NULL
);

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
    (1, 'solved'),
    (2, 'unsolved');

--table user_history
CREATE TABLE user_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES tg_user (id) NOT NULL,
    query_solving_state_id INT REFERENCES query_solving_state (id) NOT NULL,
    query VARCHAR(200),
    query_time timestamp NOT NULL,
    matched_handler VARCHAR(30)
);
