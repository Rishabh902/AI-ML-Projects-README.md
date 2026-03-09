from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle , os
app = FastAPI()
templates = Jinja2Templates(directory="templates")


movies = pickle.load(open("model/movies.pkl","rb"))
similarity = pickle.load(open("model/similarity.pkl","rb"))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# recommendation API
@app.post("/recommend")
async def get_recommendation(data: dict):

    movie = data["movie"]

    try:
        rec_movies = recommend(movie)

        return {
            "recommendations": rec_movies
        }

    except:
        return {
            "recommendations": [],
            "message": "Movie not found"
        }