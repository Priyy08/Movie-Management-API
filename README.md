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
      ```
      git clone https://github.com/Priyy08/Movie-Management-API
  
      cd Movie-Management-API
  

   2\) Create and activate a virtual environment (optional but recommended):
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   3\) Install dependencies
   ```
   pip install -r requirements.txt
   ```
   4\) Run the FastAPI application
   ```
   uvicorn main:app --reload
   ```   
    
