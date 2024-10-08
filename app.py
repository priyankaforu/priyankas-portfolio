from flask import Flask, render_template, request, send_from_directory
from flask_flatpages import FlatPages
from flask_caching import Cache
from datetime import datetime
from collections import defaultdict
import json
import os

app = Flask(__name__)

# Configuration
app.config.update(
    FLATPAGES_EXTENSION='.md',
    FLATPAGES_ROOT='content',
    CACHE_TYPE='SimpleCache',
    CACHE_DEFAULT_TIMEOUT=300
)

# Initialize extensions
cache = Cache(app)
pages = FlatPages(app)

# Constants
VISIT_COUNT_FILE = 'visit_counts.json'

def load_visit_counts():
    if os.path.exists(VISIT_COUNT_FILE):
        with open(VISIT_COUNT_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_visit_counts(counts):
    with open(VISIT_COUNT_FILE, 'w') as f:
        json.dump(counts, f)

visit_counts = load_visit_counts()

def get_page_data(page):
    """Helper function to extract consistent page data"""
    return {
        'title': page.meta.get('title', 'Untitled'),
        'genre': page.meta.get('genre', ''),
        'path': page.path,
        'date': page.meta.get('date'),
        'type': page.meta.get('type'),
        'category': page.meta.get('category')
    }

@cache.memoize(timeout=3600)
def get_articles_by_year():
    articles_by_year = defaultdict(list)
    for page in pages:
        if 'date' in page.meta:
            year = page.meta['date'].year
            articles_by_year[year].append(get_page_data(page))
    return dict(sorted(articles_by_year.items(), reverse=True))

@cache.memoize(timeout=300)
def get_recent_essays(limit=5):
    sorted_pages = sorted(
        [p for p in pages if p.meta.get('type') != 'video'],
        key=lambda p: p.meta.get('date', datetime.min),
        reverse=True
    )
    return [get_page_data(page) for page in sorted_pages[:limit]]

@cache.memoize(timeout=300)
def get_most_visited_essays(limit=5):
    sorted_visits = sorted(visit_counts.items(), key=lambda x: x[1], reverse=True)
    most_visited = []
    for path, count in sorted_visits:
        page = pages.get(path)
        if page and page.meta.get('type') != 'video':
            data = get_page_data(page)
            data['visits'] = count
            most_visited.append(data)
            if len(most_visited) == limit:
                break
    return most_visited

@cache.memoize(timeout=3600)
def get_available_months():
    available_months = set()
    for page in pages:
        if 'date' in page.meta:
            date = page.meta['date']
            available_months.add((date.year, date.month))
    return sorted(list(available_months), reverse=True)

@app.route('/')
def hello_priyanka():
    return render_template('home.html',
        articles_by_year=get_articles_by_year(),
        recent_essays=get_recent_essays(),
        most_visited_essays=get_most_visited_essays(),
        available_months=get_available_months()
    )

@app.route('/<int:year>/<int:month>/')
@cache.memoize(timeout=3600)
def month_archive(year, month):
    monthly_articles = []
    for page in pages:
        if 'date' in page.meta:
            date = page.meta['date']
            if date.year == year and date.month == month:
                article_data = get_page_data(page)
                article_data['html'] = page.html
                monthly_articles.append(article_data)
    return render_template('month_archive.html',
        year=year,
        month=month,
        articles=monthly_articles
    )

@app.route('/<path:path>/')
def post(path):
    page = pages.get_or_404(path)
    
    visit_counts[path] = visit_counts.get(path, 0) + 1
    save_visit_counts(visit_counts)
    cache.delete_memoized(get_most_visited_essays)
    
    return render_template('post.html',
        page=page,
        recent_essays=get_recent_essays(),
        most_visited_essays=get_most_visited_essays()
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/electronics')
@app.route('/electronics/<category>')
@cache.memoize(timeout=300)
def electronics(category=None):
    electronics_pages = [page for page in pages if page.meta.get('genre') == 'electronics']
    
    if category and category != 'all':
        electronics_pages = [page for page in electronics_pages if page.meta.get('category') == category]
    
    articles = [page for page in electronics_pages if page.meta.get('type') != 'video']
    videos = [page for page in electronics_pages if page.meta.get('type') == 'video']
    
    sorted_articles = sorted(articles, key=lambda p: p.meta.get('date', datetime.min), reverse=True)
    sorted_videos = sorted(videos, key=lambda p: p.meta.get('date', datetime.min), reverse=True)
    
    return render_template('electronics.html',
        articles=sorted_articles,
        videos=sorted_videos,
        category=category
    )

@app.route('/book-reads')
@app.route('/book-reads/<category>')
@cache.memoize(timeout=300)
def book_reads(category=None):
    book_pages = [page for page in pages if page.meta.get('type') == 'book']
    
    if category and category != 'all':
        book_pages = [page for page in book_pages if page.meta.get('category') == category]
    
    sorted_books = sorted(book_pages, key=lambda p: p.meta.get('date', datetime.min), reverse=True)
    book_data = [{
        'title': page.meta.get('title', 'Untitled'),
        'path': page.path,
        'date': page.meta.get('date'),
        'genre': page.meta.get('genre', 'Uncategorized'),
        'html': page.html
    } for page in sorted_books]
    
    return render_template('book_reads.html',
        books=book_data,
        category=category
    )

@app.route('/working-models')
@app.route('/working-models/<category>')
@cache.memoize(timeout=300)
def working_models(category=None):
    working_models_pages = [page for page in pages if page.meta.get('genre') == 'working-models']
    
    if category and category != 'all':
        working_models_pages = [page for page in working_models_pages if page.meta.get('category') == category]
    
    articles = [page for page in working_models_pages if page.meta.get('type') != 'video']
    videos = [page for page in working_models_pages if page.meta.get('type') == 'video']
    
    sorted_articles = sorted(articles, key=lambda p: p.meta.get('date', datetime.min), reverse=True)
    sorted_videos = sorted(videos, key=lambda p: p.meta.get('date', datetime.min), reverse=True)
    
    return render_template('working_models.html',
        articles=sorted_articles,
        videos=sorted_videos,
        category=category
    )

@app.context_processor
def inject_common_data():
    """Inject common data into all templates"""
    return {
        'recent_essays': get_recent_essays(),
        'most_visited_essays': get_most_visited_essays(),
        'available_months': get_available_months()
    }

@app.template_filter('month_name')
def month_name_filter(month_number):
    return datetime(2000, month_number, 1).strftime('%B')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
