from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
unliked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2]or "N/A",
        "runtime":all_movies.iloc[0,3],
        "weighted_rating": all_movies.iloc[0,4]   
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()
    return jsonify({
        "data":movie_data,
        "status":'success'
    })
    
@app.route("/like",methods = ["GET"])
def liked_movie():
    global all_movies
    movie_data = assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0],inplace = True)
    all_movies = all_movies.reset_index(drop = True)
    
    return jsonify({
        #"data": liked_movies,
        "status":"success"
    })
    
@app.route("/dislike",methods = ["GET"])
def unliked_movie():
    global all_movies
    movie_data = assign_val()
    unliked_movies.append(movie_data)
    all_movies.drop([0],inplace = True)
    all_movies = all_movies.reset_index(drop = True)
    
    return jsonify({
        #"data": unliked_movies,
        "status":"success"
    })
        
@app.route("/did_not_watch",methods = ["GET"])
def did_not_watch_view():
    global all_movies
    movie_data = assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0],inplace = True)
    all_movies = all_movies.reset_index(drop = True)
    
    return jsonify({
        #"data": did_not_watch,
        "status":"success"
    })
    
@app.route("/popular_movies")    
def popular_movies():
    popular_movie_data = []
    for index,row in output.iterrows():
        _p = {
            "original_title": row['original_title'],
            "poster_link":row['poster_link'],
            "release_date":row['release_date'] or "N/A",
            "duration": row['runtime'],
            "rating": row['weighted_rating']/2
        }
        popular_movie_data.append(_p)
        return jsonify({
            "data":popular_movie_data,
            "status":"success"
        })
        
@app.route("/recommended_movies")
def recommended_movies():
    global liked_movies
    col_names=['original_title', 'poster_link', 'release_date', 'runtime', 'weighted_rating']
    all_recommended = pd.DataFrame(columns = col_names)
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie["original_title"])
        all_recommended = all_recommended.append(output)
    all_recommended.drop_duplicates(subset=["original_title"],inplace = True)
    
    recommended_movie_data = []
    for index,row in all_recommended.iterrows():
        _p = {
            "original_title": row['original_title'],
            "poster_link":row['poster_link'],
            "release_date":row['release_date'] or "N/A",
            "duration": row['runtime'],
            "rating": row['weighted_rating']/2
        }
        recommended_movie_data.append(_p)  
    return jsonify({
        "data": recommended_movie_data,
        "status":"success"
    })
        
               
if __name__ == "__main__":
  app.run()        
