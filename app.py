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
    print("Current visit counts:", visit_counts)  # Debugging line
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
    print("Most visited essays:", most_visited)  # Debugging line
    return most_visited

@app.route('/')
def hello_priyanka():
    articles_by_year = get_articles_by_year()
    recent_essays = get_recent_essays()
    most_visited = get_most_visited_essays()
    return render_template('home.html', articles_by_year=articles_by_year, recent_essays=recent_essays, most_visited_essays=most_visited)

@app.route('/<path:path>/')
def post(path):
    page = pages.get_or_404(path)
    
    # Increment visit count
    visit_counts[path] = visit_counts.get(path, 0) + 1
    save_visit_counts(visit_counts)
    print(f"Incremented visit count for {path}: {visit_counts[path]}")  # Debugging line
    
    recent_essays = get_recent_essays()
    most_visited = get_most_visited_essays()
    return render_template('post.html', page=page, recent_essays=recent_essays, most_visited_essays=most_visited)

@app.context_processor
def inject_common_data():
    return dict(
        recent_essays=get_recent_essays(),
        most_visited_essays=get_most_visited_essays()
    )

if __name__ == '__main__':
    app.run(debug=True)
