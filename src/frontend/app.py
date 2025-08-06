from flask import Flask, render_template, request
from backend.main import Search  # adjust import as needed

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        searcher = Search(query)
        raw_results = searcher.search()  # You may need to adapt this to return a list
        # Format raw_results into dicts for the template
        for mcp, word, score in raw_results:
            results.append({
                'title': word,
                'url': f'/details/{mcp}',  # or actual URL if available
                'description': f'TFIDF Score: {score}'
            })
    return render_template('search_results.html', results=results, query=query)

if __name__ == '__main__':
    app.run()