from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_books():
    search_query = request.args.get('search')
    return render_template('allbooks.html', search_query=search_query)
