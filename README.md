
### Mission to Mars
 
1. A Jupyter Notebook script that scrapes Mars data  (mission_to_mars.ipynb) 

2. A Python version of the Jupyter Notebook written as a function  (scrape_mars.py) 	

3. A Flask Python Mongodb (app.py) script that: 

	* calls the above scrape function to retrieve the scraped Mars data
	* inserts the scraped data into a mongodb app's mars collection
	* reads the scraped data from mongodb
	* passes scraped data to index.html (in templates folder)
	* and renders the web 

