import json
import pprint
import sqlite3


def sql_for_title(sql):
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = []
        for item in con.execute(sql).fetchall():
            result.append(dict(item))

        return result


def search_actors(name1, name2):
    sql = ("SELECT `cast` "
           "FROM netflix ")
    list_of_actors = []
    result = sql_for_title(sql)

    for name in result:
        if name1 in name.get('cast') and name2 in name.get('cast'):
            list_of_actors.append(name.get('cast'))

    if len(list_of_actors) >= 2:
        print(list_of_actors)


def search(type, date, genre):
    sql = (f"""
    SELECT * 
    FROM netflix 
    WHERE type= '{type}' AND release_year= {date} AND listed_in LIKE '%{genre}%' 
    """)

    result = []
    for item in sql_for_title(sql):
        s = {
            "title": item.get("title"),
            "description": item.get("description")
        }
        result.append(s)

    response = json.dumps(result)
    pprint.pprint(response)


if __name__ == '__main__':
    # search_actors('Rose McIver', 'Ben Lamb')
    search(type='TV Show', date=2015, genre='Drama')
