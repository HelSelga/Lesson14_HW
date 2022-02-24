import json

from flask import Flask
import sqlite3

app = Flask(__name__)


def sql_for_title(sql):
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = []
        for item in con.execute(sql).fetchall():
            s = dict(item)
            result.append(s)

        return result


@app.route('/movie/<title>')
def search_movie_by_title(title: str):
    sql = f"""SELECT *
              FROM netflix n
              WHERE n.title = {title}
              AND n.date_added = (SELECT MAX(date_added) FROM netflix n WHERE n.title = {title}) """
    result = []
    for item in sql_for_title(sql):
        s = {
            "title": item.get("title"),
            "country": item.get("country"),
            "release_year": item.get("release_year"),
            "genre": item.get("listed_in"),
            "description": item.get("description")
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


@app.route('/movie/<year1>/to/<year2>')
def search_movie_by_release_year(year1: str, year2: str):
    sql = f"""SELECT *
              FROM netflix n
              WHERE n.release_year BETWEEN {year1} AND {year2}
              LIMIT 100 """

    result = []
    for item in sql_for_title(sql):
        s = {
            "title": item.get("title"),
            "release_year": item.get("release_year")
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


@app.route('/rating/<value>')
def search_by_rating(value: str):
    sql = """SELECT *
             FROM netflix n """
    if value == 'children':
        sql += """WHERE  n.rating = 'G' """
    elif value == 'family':
        sql += """WHERE  n.rating LIKE '%G' """
    elif value == 'adult':
        sql += """WHERE  n.rating = 'R' OR n.rating = 'NC-17' """
    else:
        return app.response_class(response=json.dumps({}),
                                  status=204,
                                  mimetype="application/json")

    result = []
    for item in sql_for_title(sql):
        s = {
            "title": item.get("title"),
            "release_year": item.get("release_year"),
            "description": item.get("description")
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")



@app.route('/genre/<genre>')
def search_by_genre(genre: str):
    sql = f"""SELECT *
              FROM netflix n
              WHERE n.listed_in LIKE '%{genre}%'
              ORDER BY n.date_added DESC 
              LIMIT 10 """

    result = []
    for item in sql_for_title(sql):
        s = {
            "title": item.get("title"),
            "description": item.get("description")
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


if __name__ == '__main__':
    app.run()
