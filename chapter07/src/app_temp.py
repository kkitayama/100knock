from flask import Flask, render_template, request
from itertools import islice
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
        for post in islice(mongo.sort("rating.count", -1), 10):
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

# ------------------

client = MongoClient('localhost', 27017)
db_artist = client.database_artist
collection_artist = db_artist.collection_artist

searcher = Artist_searcher()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def renew():
    query = request.form['query']
    select_type = request.form['select_type']
    searcher.set_info(query=query, select_type=select_type)
    df = searcher.get_df().set_index("name").to_html(classes='books')

    return render_template('index.html',
                            data_frame=df,
                            query=query,
                            select_type=select_type)

if __name__ == "__main__":
    app.debug=True
    app.run()