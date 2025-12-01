const preferencesInput = document.getElementById('preferences');
const getRecommendationsBtn = document.getElementById('getRecommendations');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');

let currentPage = 1;
let currentPreferences = '';
let hasMore = false;

// Genre chip click handlers
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const genre = chip.getAttribute('data-genre');
    preferencesInput.value = genre;
    searchMovies();
  });
});

// Search button click
getRecommendationsBtn.addEventListener('click', searchMovies);

// Enter key press
preferencesInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    searchMovies();
  }
});

function searchMovies() {
  const preferences = preferencesInput.value.trim();
  
  if (!preferences) {
    alert('Please enter a genre or movie preference');
    return;
  }
  
  currentPreferences = preferences;
  currentPage = 1;
  resultsDiv.innerHTML = '';
  
  fetchMovies();
}

async function fetchMovies() {
  loadingDiv.classList.remove('hidden');
  getRecommendationsBtn.disabled = true;
  
  try {
    const response = await fetch('http://localhost:3000/api/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        preferences: currentPreferences,
        page: currentPage
      }),
    });
    
    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    displayMovies(data.movies, currentPage === 1);
    hasMore = data.hasMore && currentPage < 3; // Limit to 3 pages (60 movies)
    
    if (hasMore) {
      showLoadMoreButton();
    } else {
      hideLoadMoreButton();
    }
  } catch (error) {
    if (currentPage === 1) {
      resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
  } finally {
    loadingDiv.classList.add('hidden');
    getRecommendationsBtn.disabled = false;
  }
}

function displayMovies(movies, clearFirst = false) {
  if (!movies || movies.length === 0) {
    if (clearFirst) {
      resultsDiv.innerHTML = '<div class="error">No movies found. Try a different genre or search term.</div>';
    }
    return;
  }
  
  const moviesHTML = movies.map(movie => `
    <div class="movie-card">
      ${movie.poster ? `<img src="${movie.poster}" alt="${movie.title}" class="movie-poster">` : '<div class="movie-poster" style="background: rgba(102, 126, 234, 0.1); display: flex; align-items: center; justify-content: center; font-size: 3rem;">🎬</div>'}
      <div class="movie-info">
        <h3>${movie.title}</h3>
        <div class="movie-meta">
          <span>📅 ${movie.year}</span>
          ${movie.rating !== 'N/A' ? `<span class="rating">⭐ ${movie.rating}</span>` : ''}
        </div>
        <div class="movie-overview">${movie.overview || 'No description available.'}</div>
      </div>
    </div>
  `).join('');
  
  if (clearFirst) {
    resultsDiv.innerHTML = moviesHTML;
  } else {
    // Remove load more button if exists
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) loadMoreBtn.remove();
    resultsDiv.innerHTML += moviesHTML;
  }
}

function showLoadMoreButton() {
  const existingBtn = document.getElementById('loadMoreBtn');
  if (existingBtn) return;
  
  const loadMoreBtn = document.createElement('button');
  loadMoreBtn.id = 'loadMoreBtn';
  loadMoreBtn.className = 'load-more-btn';
  loadMoreBtn.textContent = 'Load More Movies';
  loadMoreBtn.onclick = async () => {
    currentPage++;
    await fetchMovies();
  };
  
  resultsDiv.appendChild(loadMoreBtn);
}

function hideLoadMoreButton() {
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  if (loadMoreBtn) loadMoreBtn.remove();
}
