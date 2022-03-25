CREATE DATABASE hiphop_bot
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.utf8'
    LC_CTYPE = 'ru_RU.utf8'
		TEMPLATE template0
    CONNECTION LIMIT = -1;

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

WITH new_genres (doc) AS
( VALUES (
'[{"id": 1, "name": "hiphop"}, {"id": 2, "name": "battlerap"}, {"id": 3, "name": "hiphopmusic"}, {"id": 4, "name": "freestyle"}, {"id": 5, "name": "regular"}, {"id": 6, "name": "newschool"}, {"id": 7, "name": "oldschool"}, {"id": 8, "name": "alternative"}, {"id": 9, "name": "electronichiphop"}, {"id": 10, "name": "hardcore"}, {"id": 11, "name": "popular"}, {"id": 12, "name": "emo"}, {"id": 13, "name": "raprock"}, {"id": 14, "name": "cloud"}, {"id": 15, "name": "club"}, {"id": 16, "name": "drill"}, {"id": 17, "name": "electronicvocal"}, {"id": 18, "name": "grime"}, {"id": 19, "name": "mumble"}, {"id": 20, "name": "phonk"}, {"id": 21, "name": "horrorcore"}, {"id": 22, "name": "rapcore"}, {"id": 23, "name": "underground"}, {"id": 24, "name": "hookah"}, {"id": 25, "name": "pop"}, {"id": 26, "name": "oldschoolhardcore"}, {"id": 27, "name": "russianrap"}, {"id": 28, "name": "gangsta"}, {"id": 29, "name": "workout"}, {"id": 30, "name": "classic"}, {"id": 31, "name": "soft"}]'::json))

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

WITH new_genres_adjacency_table (doc) AS
( VALUES (
'[{"id": 1, "parent_genre_node_id": 1, "child_genre_node_id": 2}, {"id": 2, "parent_genre_node_id": 1, "child_genre_node_id": 3}, {"id": 3, "parent_genre_node_id": 2, "child_genre_node_id": 4}, {"id": 4, "parent_genre_node_id": 2, "child_genre_node_id": 5}, {"id": 5, "parent_genre_node_id": 3, "child_genre_node_id": 6}, {"id": 6, "parent_genre_node_id": 3, "child_genre_node_id": 7}, {"id": 7, "parent_genre_node_id": 6, "child_genre_node_id": 8}, {"id": 8, "parent_genre_node_id": 6, "child_genre_node_id": 9}, {"id": 9, "parent_genre_node_id": 6, "child_genre_node_id": 10}, {"id": 10, "parent_genre_node_id": 6, "child_genre_node_id": 11}, {"id": 11, "parent_genre_node_id": 7, "child_genre_node_id": 26}, {"id": 12, "parent_genre_node_id": 7, "child_genre_node_id": 27}, {"id": 13, "parent_genre_node_id": 8, "child_genre_node_id": 12}, {"id": 14, "parent_genre_node_id": 8, "child_genre_node_id": 13}, {"id": 15, "parent_genre_node_id": 9, "child_genre_node_id": 14}, {"id": 16, "parent_genre_node_id": 9, "child_genre_node_id": 15}, {"id": 17, "parent_genre_node_id": 9, "child_genre_node_id": 16}, {"id": 18, "parent_genre_node_id": 9, "child_genre_node_id": 17}, {"id": 19, "parent_genre_node_id": 9, "child_genre_node_id": 18}, {"id": 20, "parent_genre_node_id": 9, "child_genre_node_id": 19}, {"id": 21, "parent_genre_node_id": 9, "child_genre_node_id": 20}, {"id": 22, "parent_genre_node_id": 10, "child_genre_node_id": 21}, {"id": 23, "parent_genre_node_id": 10, "child_genre_node_id": 22}, {"id": 24, "parent_genre_node_id": 10, "child_genre_node_id": 23}, {"id": 25, "parent_genre_node_id": 11, "child_genre_node_id": 24}, {"id": 26, "parent_genre_node_id": 11, "child_genre_node_id": 25}, {"id": 27, "parent_genre_node_id": 26, "child_genre_node_id": 28}, {"id": 28, "parent_genre_node_id": 26, "child_genre_node_id": 29}, {"id": 29, "parent_genre_node_id": 27, "child_genre_node_id": 30}, {"id": 30, "parent_genre_node_id": 27, "child_genre_node_id": 31}]'::json))

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

WITH new_streaming_service (doc) AS
( VALUES (
'[{"id": 1, "name": "spotify"}, {"id": 2, "name": "boom"}, {"id": 3, "name": "yandex music"}]'::json))

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
