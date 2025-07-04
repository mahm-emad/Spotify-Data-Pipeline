from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():

    # Initialize Spark Session with PostgreSQL JDBC driver
    spark = (
        SparkSession.builder.appName("ArtistTrackETL")
        .config("spark.jars", "/opt/spark/jars/postgresql-42.7.3.jar")  # Update with your JDBC driver path
        .getOrCreate()
    )

    # Source PostgreSQL connection (artists and tracks)
    source_jdbc_url = "jdbc:postgresql://172.17.0.1:5442/postgres" # Use container name and internal port
    source_properties = {
        "user": "postgres",
        "password": "postgres",
        "driver": "org.postgresql.Driver"
    }

    # Destination PostgreSQL connection (dw_db)
    dest_jdbc_url = "jdbc:postgresql://172.17.0.1:5433/dw_db"
    dest_properties = {
        "user": "dw_user",
        "password": "dw_pass",
        "driver": "org.postgresql.Driver"
    }

    # Extract: Read data from PostgreSQL tables
    artists_df = spark.read.jdbc(
        url=source_jdbc_url,
        table="artists",
        properties=source_properties
    )

    tracks_df = spark.read.jdbc(
        url=source_jdbc_url,
        table="tracks",
        properties=source_properties
    )

    # Tranform and Load into dim_artists
    dim_artists = (
        artists_df.select(
            F.col("id").alias("artist_id_bk"),
            F.col("name").alias("artist_name"),
            F.col("followers"),
            F.col("popularity")
        )
    )

    dim_artists.write.jdbc(
        url=dest_jdbc_url,
        table="dim_artists",
        mode="append",
        properties=dest_properties
    )

    # Tranform and Load into dim_tracks
    dim_tracks = (
        tracks_df
        .select(
            F.col("id").alias("track_id_bk"),
            F.col("name").alias("track_name"),
            F.col("duration_ms"),
            F.col("explicit").cast("boolean").alias("explicit")
        )
    )

    dim_tracks.write.jdbc(
        url=dest_jdbc_url,
        table="dim_tracks",
        mode="append",
        properties=dest_properties
    )

    # Transform: Making required tranformation in the artists table to load into dim_genres 
    genres=artists_df.withColumn(
        "genres_clean",
        F.regexp_replace(F.col("genres"), "[\\[\\]']", ""))\
    .withColumn(
        "genres_array",
        F.split(F.col("genres_clean"), ",\\s*")
    ).withColumn("genre", F.explode("genres_array")).select(F.col('genre').alias('genre_name'))

    genres_t = genres.distinct() # Unique values of genre will be loaded into dim_genres

    # Loading into dim_genres
    genres_t.write.jdbc(
        url=dest_jdbc_url,
        table="dim_genres",
        mode="append",
        properties=dest_properties
    )

    # After loading into dim_artists and dim_genres, We load into the bridge table dim_artist_genre
    dim_genres = spark.read.jdbc(url=dest_jdbc_url, table="dim_genres", properties=dest_properties)

    dim_artists = spark.read.jdbc(url=dest_jdbc_url, table="dim_artists", properties=dest_properties)

    artists_gen=artists_df.withColumn(
        "genres_clean",
        F.regexp_replace(F.col("genres"), "[\\[\\]']", ""))\
    .withColumn(
        "genres_array",
        F.split(F.col("genres_clean"), ",\\s*")
    ).withColumn("genre", F.explode("genres_array"))


    dim_artist_genre = dim_artists.join(artists_gen,dim_artists['artist_id_bk']==artists_gen['id'],'inner')\
                            .join(genres_t,artists_gen['genre']==genres_t['genre_name'],'inner')\
                            .join(dim_genres,genres_t['genre_name']==dim_genres['genre_name'])\
                            .select(F.col('artist_id_sk').alias('artist_id'),F.col('gid').alias('genre_id'))

    dim_artist_genre.write.jdbc(
        url=dest_jdbc_url,
        table="dim_artist_genre",
        mode="append",
        properties=dest_properties
    )

    # Fact table loading:

    # Extract necessary tables for lookup

    dim_artists = spark.read.jdbc(url=dest_jdbc_url, table="dim_artists", properties=dest_properties)

    dim_tracks = spark.read.jdbc(url=dest_jdbc_url, table="dim_tracks", properties=dest_properties)

    dim_date = spark.read.jdbc(url=dest_jdbc_url, table="dim_date", properties=dest_properties)

    # Transform: Making required tranformations for lookup and fact loading

    tracks_df = tracks_df.withColumn("release_date",F.to_date(F.col("release_date")))

    tracks_df = tracks_df.withColumn("id_artists",F.regexp_replace(F.col("id_artists"), "[\\[\\]']", ""))\
        .withColumn("id_artists",F.split(F.col("id_artists"), ",\\s*"))\
        .withColumn("id_artists", F.explode("id_artists"))

    # Loading into track_fact
    fact_t = artists_df.join(dim_artists,artists_df["id"] == dim_artists["artist_id_bk"],"inner")\
        .join(tracks_df,artists_df["id"] == tracks_df["id_artists"],"inner")\
        .join(dim_tracks,tracks_df["id"] == dim_tracks["track_id_bk"],"inner")\
        .join(dim_date,tracks_df["release_date"] == dim_date["release_date"],"inner")\
        .select(
                dim_date["date_sk"],
                dim_artists["artist_id_sk"],
                dim_tracks["track_id_sk"],
                dim_date["release_date"],
                tracks_df["popularity"].alias("track_popularity")
                )

    fact_t.write.jdbc(url=dest_jdbc_url,table="track_fact",properties=dest_properties,mode="append")

    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
