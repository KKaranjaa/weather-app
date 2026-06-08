# 🌤️ Weather App

A Django weather application that displays real-time weather conditions, a live clock, and a recognisable landmark background image for any city in the world. It also auto-detects your current location and silently refreshes it every 5 minutes.

---

## Features

- 🔍 Search weather for any city (returns city + country)
- 🖼️ Landmark background image for the searched city (via Wikipedia)
- 🕐 Live ticking clocks — searched city time **and** your local time
- 📍 Auto-detects your location on first visit (permission asked once only)
- 🔄 Silent background location refresh every 5 minutes
- 📱 Fully responsive — mobile, tablet, laptop, and desktop

---

## Tech Stack

- **Backend:** Python 3, Django
- **APIs:** OpenWeatherMap, Wikipedia REST API
- **Frontend:** Vanilla HTML, CSS (glassmorphism), JavaScript

---

## Setup

### 1. Clone the repository

```bash
git clone <repository_url>
cd weatherproject
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

| Variable | Where to get it |
|---|---|
| `WEATHER_API_KEY` | [openweathermap.org/api](https://openweathermap.org/api) — free tier works |
| `GOOGLE_API_KEY` | [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview) (optional — used for fallback images) |
| `GOOGLE_SEARCH_ENGINE_ID` | Your Programmable Search Engine ID (optional) |

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## Environment Variables Reference

```
WEATHER_API_KEY=your_openweathermap_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## Project Structure

```
weatherproject/
├── weatherapp/
│   ├── templates/
│   │   └── index.html        # Main UI
│   ├── views.py              # Weather + image logic
│   ├── urls.py
│   └── admin.py
├── weatherproject/
│   ├── settings.py
│   └── urls.py
├── static/
│   └── style.css             # Responsive glassmorphism styles
├── .env.example              # Template for environment variables
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## License

MIT — feel free to use and modify.
