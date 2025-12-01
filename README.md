# CineMatch - Movie Recommender App

A professional movie recommendation app powered by The Movie Database (TMDB) API.

## Features

- 🎬 Browse thousands of movies by genre
- 🔍 Search movies by keyword
- ⭐ View ratings and detailed information
- 🖼️ High-quality movie posters
- 📱 Responsive design for all devices
- ⚡ Fast and intuitive interface

## Setup

1. Install dependencies:
```bash
npm install
```

2. Get your TMDB API key from [The Movie Database](https://www.themoviedb.org/settings/api)

3. Create a `.env` file:
```bash
copy .env.example .env
```

4. Add your API key to `.env`:
```
TMDB_API_KEY=your_actual_api_key_here
```

5. Start the server:
```bash
npm start
```

6. Open your browser to `http://localhost:3000`

## Usage

Simply type a genre (action, comedy, horror, romance, scifi) or search for specific movies. Browse up to 60 movies per search with the "Load More" feature!

## Supported Genres

Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Mystery, Romance, Sci-Fi, Thriller, War, Western
