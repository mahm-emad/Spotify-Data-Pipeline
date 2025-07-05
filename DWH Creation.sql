

-- Create the dim_date table
CREATE TABLE public.dim_date (
    date_sk SERIAL PRIMARY KEY,
    release_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL
);

-- Populate the dim_date table with data from 1991-01-01 to 2020-12-31
INSERT INTO public.dim_date (release_date, year, month, day)
SELECT
    d::DATE AS release_date,
    EXTRACT(YEAR FROM d)::INT AS year,
    EXTRACT(MONTH FROM d)::INT AS month,
    EXTRACT(DAY FROM d)::INT AS day
FROM
    generate_series('1920-01-01'::DATE, '2021-12-31'::DATE, '1 day') AS d;

----------------------------------------------------------------------------------------------

-- Dim_Artists Dimension Table
CREATE TABLE public.dim_artists (
    artist_id_sk SERIAL PRIMARY KEY,
    artist_id_bk TEXT NOT NULL,
    artist_name TEXT,
    followers NUMERIC,
    popularity INTEGER
);

-----------------------------------------------------------------------------------------------

-- Dim_Tracks Dimension Table
CREATE TABLE public.dim_tracks (
    track_id_sk SERIAL PRIMARY KEY,
    track_id_bk TEXT NOT NULL,
    track_name TEXT,
    duration_ms INTEGER,
    explicit BOOLEAN
);

-----------------------------------------------------------------------------------------------

-- Track_Fact Fact Table
CREATE TABLE public.track_fact (
    date_sk INTEGER NOT NULL REFERENCES public.dim_date(date_sk),
    track_id_sk INTEGER NOT NULL REFERENCES public.dim_tracks(track_id_sk),
    artist_id_sk INTEGER NOT NULL REFERENCES public.dim_artists(artist_id_sk),
    release_date DATE,
    track_popularity INTEGER,
    snapshot_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (date_sk, track_id_sk, artist_id_sk)
);

-----------------------------------------------------------------------------------------------

CREATE TABLE dim_genres (
	gid SERIAL primary key,
	genre_name text
	
	);
	
------------------------------------------------------------------------------------------------

CREATE TABLE dim_artist_genre (
	artist_id int references public.dim_artists(artist_id_sk),
	genre_id  int references public.dim_genres(gid),
	primary key (artist_id, genre_id)
	);





