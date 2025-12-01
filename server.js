require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('.'));

const TMDB_API_KEY = process.env.TMDB_API_KEY;
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';

// Genre mapping for TMDB
const genreMap = {
  action: 28,
  adventure: 12,
  animation: 16,
  comedy: 35,
  crime: 80,
  documentary: 99,
  drama: 18,
  family: 10751,
  fantasy: 14,
  history: 36,
  horror: 27,
  music: 10402,
  mystery: 9648,
  romance: 10749,
  love: 10749,
  scifi: 878,
  'sci-fi': 878,
  thriller: 53,
  war: 10752,
  western: 37
};

app.post('/api/recommend', async (req, res) => {
  try {
    const { preferences, page = 1 } = req.body;
    
    console.log('Received preferences:', preferences, 'Page:', page);
    
    // Convert preference to genre ID
    const genreKey = preferences.toLowerCase().trim();
    const genreId = genreMap[genreKey];
    
    let url;
    if (genreId) {
      // Use discover endpoint with genre filter - fetch multiple pages
      url = `${TMDB_BASE_URL}/discover/movie?api_key=${TMDB_API_KEY}&with_genres=${genreId}&sort_by=popularity.desc&vote_count.gte=100&page=${page}`;
    } else {
      // Fallback to search if not a recognized genre
      url = `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(preferences)}&page=${page}`;
    }
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.results && data.results.length > 0) {
      const movies = data.results.map(movie => ({
        title: movie.title,
        year: movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A',
        rating: movie.vote_average ? movie.vote_average.toFixed(1) : 'N/A',
        overview: movie.overview,
        poster: movie.poster_path ? `${TMDB_IMAGE_BASE}${movie.poster_path}` : null
      }));
      
      res.json({ 
        movies,
        currentPage: page,
        totalPages: data.total_pages,
        hasMore: page < data.total_pages
      });
    } else {
      res.json({ movies: [], currentPage: page, totalPages: 0, hasMore: false });
    }
  } catch (error) {
    console.error('Detailed error:', error.message);
    console.error('Full error:', error);
    res.status(500).json({ error: error.message || 'Failed to get recommendations' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
