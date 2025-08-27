# Movie-Management-API
Movie Management API Which can perform seamless CRUD Operations with SQLite Database for movie data.

# Details about Movie Management API:
# Tech Stack Used:
1) FastAPI : Provides lightweight, fast and relaible API Development & CRUD Operations, Here It has support for Swagger UI for seamless testing and using of API.
2) SQLite: Provides In-memory DB To create, store & Performing CRUD Operations on the data produced by FastAPI Movie Management API.
3) Pydantic : For robust type checking and data validation to ensure proper data is ingested to server to avoid unexpected runtime errors.
4) Pytest & HTTPX: For running tests.
5) Containerization : Dockerfile to run application in containers.

# Endpoints and their functionality:
1) GET /movies — List all movies stored in SQLITE DB.
2) GET /movies/{id} — Get movie by ID
3) POST /movies — Create a new movie, creating a new resource/movie on server and saving in SQLITE DB
4) PUT /movies/{id} — Update existing movie by movie id then lets to update title, genre, director, releaseYear, ratings of their respective movie ID
5) DELETE /movies/{id} — Delete movie by ID

# Run Command :
* To Run locally:
  
1\) clone the repo:
```bash
git clone https://github.com/abc08/Movie-Management-API
cd Movie-Management-API
```
  
2\) Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3\) Install dependencies
```bash
pip install -r requirements.txt
```


4\) Run the FastAPI application
```bash
uvicorn main:app --reload
```


# Run Command with Docker:

* To Run with Docker:

1\) Build the Docker image:
```bash
docker build -t movie-management-api .
```
2\) Run the Docker container:
```bash
docker run -d -p 8000:8000 movie-management-api
```
3\) Open the application in your browser:
```bash
http://localhost:8000
```

# Running Tests:
1) clone the repo and move current directory to cloned repo directory
```bash
cd Movie-Management-API
```
2) Ensure if you have already downloaded pytest in your venv, if it is not present then run this command:
```bash
pip install pytest
```
3) Now run this command on an new terminal inside your IDE to run all test cases:
```bash
pytest -v
```
