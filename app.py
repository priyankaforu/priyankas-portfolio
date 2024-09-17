from flask import Flask, render_template, jsonify
from collections import defaultdict

app = Flask(__name__)

ARTICLES = [
    {
        'id': 1,
        'title' : 'Transformation of UX design',
        'Genre' : 'Tech & Design',
        'year'  : 2024
    },
    {
        'id': 2,
        'title' : 'The stoic philosophy in leading adventurous life',
        'Genre' : 'Philosophy',
        'year'  : 2023
    },
    {
        'id': 3,
        'title' : 'Machine learning modules',
        'Genre' : 'ML and AI',
        'year'  : 2024
    }

]

@app.route('/')
def hello_priyanka():
    articles_by_year = defaultdict(list)
    for article in ARTICLES:
        articles_by_year[article['year']].append(article)
    sorted_years = sorted(articles_by_year.keys(), reverse=True)
    return render_template('home.html', articles_by_year=articles_by_year, years=sorted_years)
@app.route("/api/articles")
def list_articles():
    return jsonify(ARTICLES)

print(__name__)
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)