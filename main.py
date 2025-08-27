from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
import sqlite3


app = FastAPI(title="Movie Management API")

# Pydantic base model for robust type checking and data validation
class Movie(BaseModel):         
    id: int = Field(description="The id of the movie")
    title: str =  Field(description="The title of the movie.")
    director: str = Field(description="The name of the director of the movie.")
    releaseYear: int = Field(description="The release year of the movie for example 2004.", ge=1800, le=2026)
    genre: str = Field(description="The genre of the movie for example Action, Comedy, Drama etc.")
    rating: int = Field(description="The rating of the movie on a scale of 1 to 10.", ge=1, le=10)  # 1 to 10 scale

# additional pydantic model for handle updates using put request where all fields are optional
class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    releaseYear: int | None = Field(None, gt=1800, lt=2100)
    genre: str | None = None
    rating: int | None = Field(None, ge=1, le=10)

#home route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Management API!"}

# route to create movie details on server and updating on sqlite database
@app.post("/movies/",status_code=201)
def create_movie(movie: Movie):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # creates table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        director TEXT NOT NULL,
        releaseYear INTEGER NOT NULL,
        genre TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 10)
    );
    """)

    try:
        cursor.execute(
            "INSERT INTO movies (id, title, director, releaseYear, genre, rating) VALUES (?, ?, ?, ?, ?, ?)",
            (movie.id, movie.title, movie.director, movie.releaseYear, movie.genre, movie.rating),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.close()
        return {"error": str(e)}

    conn.close()
    return {"message": "Movie added successfully", "movie_id": movie.id}


# route to extract all movie details from sqlite database
@app.get("/movies", status_code=200)
def get_all_movies():
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        rows = cursor.fetchall()
        conn.close()

        movies = []
        for row in rows:
           movies.append({
            "id": row[0],
            "title": row[1],
            "director": row[2],
            "releaseYear": row[3],
            "genre": row[4],
            "rating": row[5]
          })
           
        return movies
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# route to extact movie details by its id from sqlite database
@app.get("/movies/{movie_id}",status_code=200)
def get_movies(movie_id: int):
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
           movie = {
            "id": row[0],
            "title": row[1],
            "director": row[2],
            "releaseYear": row[3],
            "genre": row[4],
            "rating": row[5]
            }

        return movie
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))



# route to update movie details by its id in sqlite database
@app.put("/movies/{movie_id}", status_code=200)
def update_movie(movie: MovieUpdate, movie_id: int):
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE movies
        SET title = ?, director = ?, releaseYear = ?, genre = ?, rating = ?
        WHERE id = ?
        """, (movie.title, movie.director, movie.releaseYear, movie.genre, movie.rating, movie_id))

        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Movie not found")

        return {"message": "Movie updated successfully"}

    except sqlite3.Error as e:
        # Catches any SQLite errors (like IntegrityError, OperationalError, etc.)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        conn.close()

# route to delete movie details by its id from sqlite database
@app.delete("/movies/{movie_id}", status_code=200)
def delete_movie(movie_id: int):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Movie not found")  
    return {"message": "Movie deleted successfully"}