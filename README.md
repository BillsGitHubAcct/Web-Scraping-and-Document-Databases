
### Mission to Mars
 
1. A Jupyter Notebook script that scrapes Mars data  (mission_to_mars.ipynb) 

2. A Python version of the Jupyter Notebook written as a function  (scrape_mars.py) 	

3. A Flask Python Mongodb (app.py) script that: 

	* calls the above scrape function to retrieve the scraped Mars data
	* inserts the scraped data into a mongodb app's mars collection
	* reads the scraped data from mongodb
	* passes scraped data to index.html (in templates folder)
	* and renders the web


# mission_to_mars.ipynb


```python
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser
executable_path = {'executable_path': 'chromedriver.exe'}

```

### NASA Mars News
* Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.


```python
# Usea splinter here since the web page has to be fully rendered (js executed) before we are able to get
# the latest title and paragraph 
with  Browser('chrome', **executable_path, headless=True) as browser:
    url = 'https://mars.nasa.gov/news/'
    # open web page
    browser.visit(url)
    # scrape web page using beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # find latest title and paragraph
    news_title = soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').text

print('News title --> ' + news_title)
print('News paragraph --> \n' + news_p)
```

    News title --> NASA Engineers Dream Big with Small Spacecraft
    News paragraph --> 
    The first CubeSat mission to deep space will launch in May.
    

### JPL Mars Space Images - Featured Image

* Visit the url for JPL's Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

* Make sure to find the image url to the full size `.jpg` image.

* Make sure to save a complete url string for this image.


```python
with  Browser('chrome', **executable_path, headless=True) as browser:
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # open web page
    browser.visit(jpl_url)
    # scrape web page using beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Get url for image jpg
    jpl_url = soup.find('div', class_= 'jpl_logo').a['href']
    url_last = soup.find('div', class_='default floating_text_area ms-layer').footer.a['data-fancybox-href']
    image_url = jpl_url[:-1] + url_last 
print('image url --> ' + image_url)
```

    image url --> //www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA14884_ip.jpg
    

### Mars Weather

* Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.


```python
# Scrape Weather from Twitter Page using Soup
twitter_url = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(twitter_url)
soup = BeautifulSoup(response.text, 'html.parser')
mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print('mars_weather = ' + mars_weather)
```

    mars_weather = Sol 2026 (April 18, 2018), Sunny, high -6C/21F, low -73C/-99F, pressure at 7.19 hPa, daylight 05:26-17:21
    

### Mars Facts

* Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* Use Pandas to convert the data to a HTML table string.



```python
url = 'http://space-facts.com/mars/'
# Use pandas to read all tables from the web page into an array of dataframes
df = pd.read_html(url)
df[0].columns = ['description','value']
# Assign a dataframe with an html table
mars_html_table = df[0].to_html(index=False)
mars_html_table
```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th>description</th>\n      <th>value</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>Equatorial Diameter:</td>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <td>Polar Diameter:</td>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <td>Mass:</td>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <td>Moons:</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <td>Orbit Distance:</td>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <td>Orbit Period:</td>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <td>Surface Temperature:</td>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <td>First Record:</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <td>Recorded By:</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'




```python
### Mars Hemisperes
```


```python
executable_path = {'executable_path': 'chromedriver.exe'}

from splinter import Browser
from bs4 import BeautifulSoup
import requests
```


```python
with  Browser('chrome', **executable_path, headless=False) as browser:
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # open web page
    browser.visit(astro_url)
    # scrape web page using beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='item')
    mars_images = []
    # Read through items to get images from second page
    for first_page in results:
        # Get image title from first page
        title_text = first_page.h3.text
        # Click on title's link on first page and go to second page
        browser.click_link_by_partial_text(first_page.h3.text)
        # Wait for second page processing
        time.sleep(2)
        # Get second page's url
        page2_url = browser.url
        # Visit second page so parsing can begin
        browser.visit(page2_url)
        # Get second page's html for parsing
        html2 = browser.html
        # Begin parse of second page using beautifulsoup
        soup2 = BeautifulSoup(html2, 'html.parser')
        # Get Sample image's url on second page
        img_url = soup2.find('a',href=True, text='Sample')['href']
        # Save title and image url to list of dicts
        mars_images.append({"title" : title_text,"img_url" : img_url})
        # Go back to first page
        browser.back()
    print(mars_images)                              
```

# scrape_mars.py


```python


def mars_scrape():
	"""
		From Mars related sites scrape content for eventual 
		insert into mongodb and display on web page
	"""
	import pandas as pd
	import requests
	import time
	from bs4 import BeautifulSoup
	from splinter import Browser
	executable_path = {'executable_path': 'chromedriver.exe'}
	return_list = []
	# ### NASA Mars News
	with  Browser('chrome', **executable_path, headless=True) as browser:
		url = 'https://mars.nasa.gov/news/'
		# open web page
		browser.visit(url)
		# scrape web page using beautiful soup
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')
		# find latest title and paragraph
		news_title = soup.find('div', class_='content_title').a.text
		return_list.append(news_title)
		time.sleep(3)
		news_p = soup.find('div', class_='article_teaser_body').text
		return_list.append(news_p)
		time.sleep(3)
		
	print('News title --> ' + news_title)
	print('News paragraph --> \n' + news_p)

	# ### JPL Mars Space Images - Featured Image
	with  Browser('chrome', **executable_path, headless=True) as browser:
		jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
		# open web page
		browser.visit(jpl_url)
		# scrape web page using beautiful soup
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')
		# Get url for image jpg
		jpl_url = soup.find('div', class_= 'jpl_logo').a['href']
		url_last = soup.find('div', class_='default floating_text_area ms-layer').footer.a['data-fancybox-href']
		image_url = jpl_url[:-1] + url_last
		return_list.append(image_url)
	print('image url --> ' + image_url)
	

	# ### Mars Weather

	twitter_url = 'https://twitter.com/marswxreport?lang=en'
	response = requests.get(twitter_url)
	soup = BeautifulSoup(response.text, 'html.parser')
	mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
	print('mars_weather = ' + mars_weather)
	return_list.append([mars_weather])
	# ### Mars Facts

	url = 'http://space-facts.com/mars/'
	# Use pandas to read all tables from the web page into an array of dataframes
	df = pd.read_html(url)
	df[0].columns = ['description','value']
	# Assign a dataframe with an html table
	mars_html_table = df[0].to_html(index=False)
	print(mars_html_table)
	return_list.append(mars_html_table)
	# ### Mars Hemisperes

	with  Browser('chrome', **executable_path, headless=True) as browser:
		astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
		# open web page
		browser.visit(astro_url)
		# scrape web page using beautiful soup
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')
		results = soup.find_all('div', class_='item')
		mars_images = []
		# Read through items to get images from second page
		count = 1
		for first_page in results:
			# Get image title from first page
			title_text = first_page.h3.text
			# Click on title's link on first page and go to second page
			browser.click_link_by_partial_text(first_page.h3.text)
			# Wait for second page processing
			time.sleep(2)
			# Get second page's url
			page2_url = browser.url
			# Visit second page so parsing can begin
			browser.visit(page2_url)
			# Get second page's html for parsing
			html2 = browser.html
			# Begin parse of second page using beautifulsoup
			soup2 = BeautifulSoup(html2, 'html.parser')
			# Get Sample image's url on second page
			img_url = soup2.find('a',href=True, text='Sample')['href']
			# Save title and image url to list of dicts
			title_desc = "title" + str(count)
			img_desc = "img_url" + str(count)			
			mars_images.append({"title" : title_text,"img_url" : img_url})
			# Go back to first page
			browser.back()
		return_list.append(mars_images)
	# print('mars_images = ')
	# print(mars_images[0])
	# print(mars_images[1])
	# print(mars_images[2])
	# print(mars_images[3])
	title_text1 = mars_images[0]["title"]
	title_text2 = mars_images[1]["title"]
	title_text3 = mars_images[2]["title"]
	title_text4 = mars_images[3]["title"]
	image_url1 = mars_images[0]["img_url"]
	image_url2 = mars_images[1]["img_url"]
	image_url3 = mars_images[2]["img_url"]
	image_url4 = mars_images[3]["img_url"]
	return {"news_title": news_title, 
			"news_p": news_p, 
			"images_url": image_url,
			"mars_weather": mars_weather,
			"mars_html_table": mars_html_table,
			"title1": title_text1,
			"img_url1": image_url1,
			"title2": title_text2,
			"img_url2": image_url2,
			"title3": title_text3,
			"img_url3": image_url3,
			"title4": title_text4,
			"img_url4": image_url4		
			} 
```

# app.py


```python
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
```

# index.html


```python
<!DOCTYPE html>
<html lang="en">

<head>
  <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Mars</title>
  <!-- <link rel="stylesheet" type="text/css" href= "{{ url_for('static',filename='reset.css')}}"> -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='style.css')}}">
  
</head>

<body>
  <div class="container">
    <div class="jumbotron text-center">
      <h1>Mission to Mars</h1>
      <p><a class="btn btn-primary btn-lg" href="/scrape" role="button">Scrape New Data</a></p>
    </div>
      
    <!-- mars data -->
    <div class="row">
      <div class="col-md-12">
        <h2>Latest Mars News</h2>
		<h3>{{ mars.news_title }}</h3>
		<p>{{mars.news_p}}</p>
      </div>
    </div>
		
	<div class="row">
      <div class="col-md-6">
        <h2>Featured Mars Image</h2>
		<img class ="img-responsive" src= "{{ mars.images_url}}"/>
      </div>
	  <div class=" col-md-6 container ">
		<div class="panel panel-default">
			<div class="panel-body"><h3>Current Weather on Mars</h3>
									<p>{{mars.mars_weather}}</p>
			</div>
		</div>
	  </div>
      <div class="col-md-6">
        <h3>Mars Facts</h3>
		{{mars.mars_html_table|safe}}
      </div>
	  <div class=" col-md-12 container ">
		<div class="panel panel-default">
	  	<h2 align="center">Mars Hemispheres </h2>
		<div class=" col-md-6 container">
		    <div class="panel panel-default">
			<img class ="img-responsive" src= "{{ mars.img_url1}}"/>
			<h4>{{ mars.title1}}</h4>
		   </div>
		</div>
		<div class="col-md-6 container">
		    <div class="panel panel-default">
			<img class ="img-responsive" src= "{{ mars.img_url2}}" />
			<h4>{{ mars.title2}}</h4>
		</div>
        </div>
	   </div>
	  

	  <div class="col-md-6 container">
	    <div class="panel panel-default">
        <img class ="img-responsive" src= "{{ mars.img_url3}}" />
		<h4>{{ mars.title3}}</h4>
		</div>
      </div>
	  <div class="col-md-6 container">
	    <div class="panel panel-default">
        <img class ="img-responsive" src= "{{ mars.img_url4}}"/>
		<h4>{{ mars.title4}}</h4>
		</v>
      </div>
     </div>
    </div>

	
	
  </div>

</body>
</html>


```

# style.css


```python

  body {	
	font-family: 'Source Sans Pro', sans-serif;
	background-color: #f4f1f1;
  }
  .jumbotron {
	background-color: #e0e0eb;	 
  }
  .table {
     background-color: #f4f1f1;
  }
  .panel-body {
	background-color: #f4f1f1; 

  }	
  .panel {
	background-color: #f4f1f1;

  }
  p {
	 font-size: 12pt;
  }
```
	

