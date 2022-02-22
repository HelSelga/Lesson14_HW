from flask import Flask
# from utils import

app = Flask(__name__)


@app.route('/movie/<title>')
def search_movie_by_title():
    pass


@app.route('/movie/<year>/to/<year>')
def search_movie_by_release_year():
    pass


@app.route('/rating/children')
def search_by_rating_g():
    pass


@app.route('/rating/family')
def search_by_rating_with_g():
    pass


@app.route('/rating/adult')
def search_by_rating_adult():
    pass


@app.route('/genre/<genre>')
def search_by_genre():
    pass


if __name__ == '__main__':
    app.run()
