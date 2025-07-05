CREATE TABLE public.artists (
    id TEXT PRIMARY KEY,
    followers NUMERIC,
    genres TEXT,
    name TEXT,
    popularity INTEGER
);


----------------------------------------------------------------------

CREATE TABLE public.Tracks (
    id TEXT PRIMARY KEY,
    name TEXT,
    popularity INTEGER,
    duration_ms INTEGER,
    explicit BOOLEAN,
    artists TEXT,
    id_artists TEXT,
    release_date TEXT,
    danceability NUMERIC,
    energy NUMERIC,
    key INTEGER,
    loudness NUMERIC,
    mode INTEGER,
    speechiness NUMERIC,
    acousticness NUMERIC,
    instrumentalness NUMERIC,
    liveness NUMERIC,
    valence NUMERIC,
    tempo NUMERIC,
    time_signature INTEGER
);



	
	
	
	
	
	