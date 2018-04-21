
### Mission to Mars
 
- A Jupyter Notebook script that scrapes Mars data (see below) --> mission_to_mars.ipynb 

- A Python version of the Jupyter Notebook written as a function  --> scrape_mars.py 	

- A Flask Python Mongodb (app.py) script that: 

* calls the above scrape function to retrieve the scraped Mars data
* inserts the scraped data into a mongodb app's mars collection
* reads the scraped data from mongodb
* passes scraped data to index.html (in templates folder)
* and renders the web 

