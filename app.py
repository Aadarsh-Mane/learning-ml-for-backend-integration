from flask import Flask, request, jsonify
import pickle
import requests

app = Flask(__name__)

# Load the movie data and similarity matrix
def download_pkl(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

# Dropbox URLs for direct download
movies_pkl_url = 'https://www.dropbox.com/scl/fi/dm5ade8da4urx3g0i7dzy/movies.pkl?rlkey=vzb5f2rqa29lj6tu0k9kzwhce&st=rqapoi8f&dl=1'
similarity_pkl_url = 'https://www.dropbox.com/scl/fi/l17gtqx2h5ljecorlav43/similarity.pkl?rlkey=4mdxvna4l667bdbgqets5gv6p&st=os7fdc21&dl=1'

# Download the files to the current directory
download_pkl(movies_pkl_url, 'movies.pkl')
download_pkl(similarity_pkl_url, 'similarity.pkl')

# Load the pickle files
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# movies = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names, recommended_movie_posters

# Define an API route to get recommendations
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    movie = data['movie']
    recommended_movie_names, recommended_movie_posters = recommend(movie)
    
    return jsonify({
        'movies': recommended_movie_names,
        'posters': recommended_movie_posters
    })

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == "__main__":
    from os import environ
    app.run(host='0.0.0.0', port=environ.get('PORT', 5000), debug=False)

