import pytest
from fastapi.testclient import TestClient
from main import app, Movie

client = TestClient(app)


#unit Tests (Pydantic validation) 
def test_movie_model_validation():
    # valid movie
    movie = Movie(
        id=1,
        title="Inception",
        director="Christopher Nolan",
        releaseYear=2010,
        genre="Sci-Fi",
        rating=9
    )
    assert movie.title == "Inception"
    assert movie.rating == 9

    # invalid rating (should raise ValidationError)
    with pytest.raises(Exception):
        Movie(
            id=2,
            title="Bad Movie",
            director="Someone",
            releaseYear=2000,
            genre="Drama",
            rating=15
        )


# Integration Tests (API)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Movie Management API!"}


def test_create_movie():
    movie_data = {
        "id": 101,
        "title": "The Matrix",
        "director": "Wachowski Sisters",
        "releaseYear": 1999,
        "genre": "Sci-Fi",
        "rating": 10
    }
    response = client.post("/movies/", json=movie_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Movie added successfully"
    assert response.json()["movie_id"] == 101


def test_get_movie_by_id():
    response = client.get("/movies/101")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 101
    assert data["title"] == "The Matrix"


def test_get_all_movies():
    response = client.get("/movies")  
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    assert any(m["id"] == 101 for m in movies)


def test_update_movie():
    update_data = {
        "title": "The Matrix Reloaded",
        "director": "Wachowski Sisters",
        "releaseYear": 2003,
        "genre": "Sci-Fi",
        "rating": 8
    }
    response = client.put("/movies/101", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Movie updated successfully"

    # verify update
    get_response = client.get("/movies/101")
    data = get_response.json()
    assert data["title"] == "The Matrix Reloaded"
    assert data["releaseYear"] == 2003


def test_delete_movie():
    response = client.delete("/movies/101")
    assert response.status_code == 200
    assert response.json()["message"] == "Movie deleted successfully"

    # verify movie is gone
    get_response = client.get("/movies/101")
    assert get_response.status_code == 200 or get_response.status_code == 404
    if get_response.status_code == 200:
        # If somehow still there
        assert get_response.json().get("id") != 101
    else:
        # FastAPI raises HTTPException with detail
        assert "detail" in get_response.json() or "error" in get_response.json()
