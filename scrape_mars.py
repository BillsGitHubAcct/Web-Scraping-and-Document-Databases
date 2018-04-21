

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