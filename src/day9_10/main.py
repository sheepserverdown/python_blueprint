import requests
import json
from flask import Flask, render_template, request, redirect

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine")


# 파싱으로 받아와야할것
# title, url, points, author, comments 갯수

# json parsing
def parse_news_json(text):
    data = json.loads(text)['hits']
    parsed_list = []
    for dic_data in data:
        title = dic_data['title']
        url = dic_data['url']
        points = dic_data['points']
        author = dic_data['author']
        comment_count = dic_data['num_comments']
        data_id = dic_data['objectID']
        data_list = {"id": data_id,
                     "title": title,
                     "url": url,
                     "points": points,
                     "author": author,
                     "comment_count": comment_count}
        parsed_list.append(data_list)
    return parsed_list


def parse_comment_json(text):
    data = json.loads(text)
    parsed_list = []

    children = data['children']
    children_list = []
    for dic_data in children:
        author = dic_data['author']
        text = dic_data['text']
        data_list = {
            "author": author,
            "text": text
        }
        children_list.append(data_list)
    parsed_list = {
        "title": data['title'],
        "points": data['points'],
        "author": data['author'],
        "url": data['url'],
        "children": children_list}
    return parsed_list


@app.route("/")
def home():
    sort = request.args.get('order_by')
    existingData = db.get(sort)
    if existingData:
        parse_data = existingData
    else:
        if sort == 'popular' or sort is None:
            sort = 'popular'
            target = requests.get(popular)
        else:  # 새로순 정렬
            sort = 'new'
            target = requests.get(new)
        parse_data = parse_news_json(target.text)
        db[sort] = parse_data
    return render_template("index.html",
                           sort=sort,
                           parse_data=parse_data
                           )


@app.route("/<id>")
def detail_content(id):
    target = requests.get(make_detail_url(id))
    parse_data = parse_comment_json(target.text)
    # print(parse_data['children'][1])
    # return redirect('/')
    return render_template("detail.html"
                           , parse_data=parse_data
                           )


app.run(host="0.0.0.0")