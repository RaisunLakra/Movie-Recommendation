import streamlit as st
import pickle
import requests

def load_key(file_path='.env'):
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                if line.startswith('TMDB_API_KEY'):
                    return line.split('=')[1].strip()
            return None
    except FileNotFoundError:
        print("The .env file was not found. Please make sure you have it in the correct location.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the key: {str(e)}")
        return None

TMDB_API_KEY = load_key('../.env')
if TMDB_API_KEY is None:
    print("Key not found. Please make sure you have the key in the correct location.")
    print("Enter key like this: TMDB_API_KEY=\{your_api_key\}")

# Function to fetch posters using the movie API
def fetch_posters(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US').json()
    if 'poster_path' in response and response['poster_path'] is not None:
        poster_path = response['poster_path']
        url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'
        return url + poster_path
    else:
        return "https://via.placeholder.com/600x900?text=No+Image+Available"

# Function to recommend movies
def recommend(selected_movie_name):
    index = movies_list[movies_list['title'] == selected_movie_name].index[0]
    similarity_score = list(enumerate(similarity_matrix[index]))
    sorted_scores = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    top_10_recommendation = [i[0] for i in sorted_scores[1:11]]
    recommended_movies_posters = []
    for movie_index in top_10_recommendation:
        movie_id = movies_list.iloc[movie_index]['id']
        poster_url = fetch_posters(movie_id)
        recommended_movies_posters.append(poster_url)
    recommended_movies = movies_list['title'].iloc[top_10_recommendation].tolist()
    return recommended_movies, recommended_movies_posters

def show_trending_movies():
    st.write('Top trending movies list\n')
    st.write(trending_movies_list)

# Load data
trending_movies_list = pickle.load(open('processed_data/trending_movies.pkl', 'rb'))
movies_list = pickle.load(open('processed_data/movies.pkl', 'rb'))
similarity_matrix = pickle.load(open('processed_data/similarity_matrix.pkl', 'rb'))
movies_titles = movies_list['title'].values

# Streamlit UI
st.title('🎥 Movies Recommendation System')

selected_movie_name = st.selectbox(
    "Please select a movie to recommend: ",
    movies_titles,
    index=None,
    placeholder="Start typing a movie name..."
)

# Recommend button
if selected_movie_name and st.button('🎬 Recommend'):
    count = 1
    movie_names, posters = recommend(selected_movie_name)
    
    # Start scrollable container
    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
    
    # Populate container with movie cards
    for movie, poster in zip(movie_names, posters):
        st.markdown(f"""
        <div class="movie-card">
            <img src="{poster}" alt="{movie}">
            <div class="movie-title">{count}. {movie}</div>
        </div>
        """, unsafe_allow_html=True)
        count += 1
    
    # Close scrollable container
    st.markdown('</div>', unsafe_allow_html=True)
       
    # Add styling for a sleek horizontal scrollable container
    st.markdown("""
    <style>
        .scroll-container {
            display: flex;
            overflow-x: auto;
            padding: 20px 10px;
            gap: 20px;
            scroll-behavior: smooth; /* Enables smooth scrolling */
            max-width: 100%;
        }
        .scroll-container::-webkit-scrollbar {
            height: 8px;
        }
        .scroll-container::-webkit-scrollbar-thumb {
            background-color: #888; /* Scrollbar color */
            border-radius: 10px;
        }
        .scroll-container::-webkit-scrollbar-thumb:hover {
            background-color: #555; /* Scrollbar hover effect */
        }
        .movie-card {
            flex: 0 0 auto; /* Prevent shrinking */
            text-align: center;
            width: 180px;
            padding: 10px;
            border-radius: 10px;
            background: #f4f4f4;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s;
        }
        .movie-card:hover {
            transform: scale(1.05); /* Subtle zoom effect */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        .movie-card img {
            width: 150px;
            height: 225px;
            border-radius: 8px;
        }
        .movie-title {
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            color: black;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    show_trending_movies()

if __name__ == '__main__':
    st.write("🎉 Your movie recommendation app is ready!")