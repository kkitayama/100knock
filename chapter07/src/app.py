from flask import Flask, render_template, request
from pymongo import MongoClient
import pymongo
import pandas as pd

class Artist_searcher:
    def __init__(self):
        self.query = None
        self.select_type = None

    def set_info(self, query=None, select_type=None):
        self.query = query
        self.select_type = select_type

    def get_pymongo(self):
        if self.select_type == "name":
            return collection_artist.find({"name":self.query})

        if self.select_type == "alias":
            return collection_artist.find({"aliases.name":self.query})

        if self.select_type == "area":
            return collection_artist.find({"area":self.query})

        if self.select_type == "tag":
            return collection_artist.find({"tags.value":self.query})

    def sort_pymongo_rating(self, mongo):
        for post in mongo.sort("rating.count", -1).limit(10):
            yield post

    def get_info(self, post):
        name = post["name"]
        alias = post.get("aliases")
        area = post.get("area")
        work_type = post.get("type")
        begin = post.get("begin")

        if alias:
            alias = ', '.join(dic["name"] for dic in alias)

        if begin:
            year = begin.get("year")
            month = begin.get("month")
            date = begin.get("date")
            begin = '/'.join(str(num) for num in [year, month, date] if num)

        return (name, alias, area, work_type, begin)

    def get_iter_search(self):
        if self.query and self.select_type:
            mongo = self.get_pymongo()
            for post in self.sort_pymongo_rating(mongo):
                yield self.get_info(post)

    def get_df(self):
        df = pd.DataFrame((i for i in searcher.get_iter_search()),
                          columns=['name','alias','area','type','begin'])
        return df



app = Flask(__name__)

client = MongoClient('localhost', 27017)
db_artist = client.database_artist
collection_artist = db_artist.collection_artist

searcher = Artist_searcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def search():
    select_type = request.form['select_type']
    query = request.form['query']
    searcher.set_info(query=query, select_type=select_type)
    df = searcher.get_df().to_html(classes='books')

    return render_template('index.html',
                            select_type=select_type,
                            query=query,
                            data_frame=df)

if __name__ == "__main__":
    app.debug=True
    app.run()