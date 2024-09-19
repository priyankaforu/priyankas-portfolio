from flask import Flask, render_template, request
from flask_flatpages import FlatPages
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_ROOT'] = 'content'
pages = FlatPages(app)

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

@app.route('/')
def hello_priyanka():
    articles_by_year = get_articles_by_year()
    return render_template('home.html', articles_by_year=articles_by_year)

@app.route('/<path:path>/')
def post(path):
    page = pages.get_or_404(path)
    return render_template('post.html', page=page)

if __name__ == '__main__':
    app.run(debug=True)
