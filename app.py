#
# Driver for Scraping Mars Web pages, saving scraped data to Mongodb database
#
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import mars_scrape

## Step 2 - MongoDB and Flask Application


app = Flask(__name__, static_url_path='/static') 


mongo = PyMongo(app)


@app.route('/')
def index():
	"""
		Read Data from Mongodb and then Render Screen with the data read
	"""
	mars = mongo.db.mars.find_one()
	return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
	"""
		Create Mars Mongodb, call scrape routine and then upsert scraped data to Mongodb
	"""
	mars = mongo.db.mars
	data = mars_scrape()
	# print(data['news_title'])
	# print(data['news_p'])
	# print(data['images_url'])
	# print(data['mars_weather'])
	# print(data['mars_html_table'])
	# print(data['mars_images'])
	mars.update(
        {},
        data,
        upsert=True
	
    )
	return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)



