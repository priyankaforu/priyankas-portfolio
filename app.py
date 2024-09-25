from flask import Flask, render_template, request
from flask_flatpages import FlatPages
from datetime import datetime
from collections import defaultdict
import json
import os

app = Flask(__name__)
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_ROOT'] = 'content'
pages = FlatPages(app)

# File to store visit counts
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

def get_articles_by_year():
    articles_by_year = defaultdict(list)
    for page in pages:
        if 'date' in page.meta:
            year = page.meta['date'].year
            articles_by_year[year].append({
                'title': page.meta.get('title', 'Untitled'),
                'genre': page.meta.get('genre', ''),
                'path': page.path
            })
    return dict(sorted(articles_by_year.items(), reverse=True))

def get_recent_essays(limit=5):
    sorted_pages = sorted(pages, key=lambda p: p.meta.get('date', datetime.min), reverse=True)
    return [{'title': page.meta.get('title', 'Untitled'), 'path': page.path} for page in sorted_pages[:limit]]

def get_most_visited_essays(limit=5):
    sorted_visits = sorted(visit_counts.items(), key=lambda x: x[1], reverse=True)
    most_visited = []
    for path, count in sorted_visits[:limit]:
        page = pages.get(path)
        if page:
            most_visited.append({
                'title': page.meta.get('title', 'Untitled'),
                'path': path,
                'visits': count
            })
    return most_visited

def get_available_months():
    available_months = set()
    for page in pages:
        if 'date' in page.meta:
            date = page.meta['date']
            available_months.add((date.year, date.month))
    return sorted(list(available_months), reverse=True)

@app.route('/')
def hello_priyanka():
    articles_by_year = get_articles_by_year()
    recent_essays = get_recent_essays()
    most_visited = get_most_visited_essays()
    available_months = get_available_months()
    return render_template('home.html', articles_by_year=articles_by_year, recent_essays=recent_essays, most_visited_essays=most_visited, available_months=available_months)

@app.route('/<int:year>/<int:month>/')
def month_archive(year, month):
    monthly_articles = []
    for page in pages:
        if 'date' in page.meta:
            date = page.meta['date']
            if date.year == year and date.month == month:
                monthly_articles.append({
                    'title': page.meta.get('title', 'Untitled'),
                    'genre': page.meta.get('genre', ''),
                    'date': date,
                    'path': page.path,
                    'html': page.html
                })
    return render_template('month_archive.html', year=year, month=month, articles=monthly_articles)

@app.route('/<path:path>/')
def post(path):
    page = pages.get_or_404(path)
    
    # Increment visit count
    visit_counts[path] = visit_counts.get(path, 0) + 1
    save_visit_counts(visit_counts)
    
    recent_essays = get_recent_essays()
    most_visited = get_most_visited_essays()
    return render_template('post.html', page=page, recent_essays=recent_essays, most_visited_essays=most_visited)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/electronics')
def electronics():
    return render_template('electronics.html')

@app.route('/book-reads')
def book_reads():
    return render_template('book_reads.html')

@app.route('/working-models')
def working_models():
    return render_template('working_models.html')

@app.context_processor
def inject_common_data():
    return dict(
        recent_essays=get_recent_essays(),
        most_visited_essays=get_most_visited_essays(),
        available_months=get_available_months()
    )

# Custom Jinja2 filter for month names
@app.template_filter('month_name')
def month_name_filter(month_number):
    return datetime(2000, month_number, 1).strftime('%B')

if __name__ == '__main__':
    app.run(debug=True)
