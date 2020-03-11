from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_info = mongo.db.mars.find_one()
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scrape():
    mars_scrape = scrape_mars.scrape()
    mongo.db.mars.drop()
    mongo.db.mars.insert_one(mars_scrape)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
