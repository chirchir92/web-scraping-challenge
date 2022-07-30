from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# creating instance for Flask
app=Flask(__name__)

# use pymongo to establish mongo connection
mongo=PyMongo(app, uri='mongodb://localhost:27017/mars_app')


# route to render index.html template using data from mongo
@app.route('/')
def home():
    # find all record of data from mongo database
    mars_data=mongo.db.mars.find_one()
    # return template and data
    return render_template('index.html',mars=mars_data)

# route to trigger scrape function
@app.route('/scrape')
def scrape():

    # run the scrape function
    mars_info=scrape_mars.scrape()
    
    # update the mongo db using update and upsert=True
    mongo.db.mars.update({}, mars_info, upsert=True)
    
    # redirect back to home page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)