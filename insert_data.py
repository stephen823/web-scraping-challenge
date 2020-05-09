from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

import os
cwd = os.getcwd()
print("My current working directory is: {} ".format(cwd))
os.chdir("/Users/apple/Desktop/bootcamp/12-Web-Scraping-and-Document-Databases/Homework/web-scraping-challenge/Missions_to_Mars")
cwd = os.getcwd()
print("My current working directory is: {} ".format(cwd))

# Create an instance of Flask
app = Flask(__name__,template_folder='../Missions_to_Mars')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdata_app")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    Mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", Mars_data=Mars_data)


@app.route("/")
def home1():



    # Find one record of data from the mongo database
    Mars_data = mongo.db.collection.find_one()

    import os
    cwd = os.getcwd()
    print("My current working directory is: {} ".format(cwd))
    os.chdir("/Users/apple/Desktop/bootcamp/12-Web-Scraping-and-Document-Databases/Homework/web-scraping-challenge/Missions_to_Mars")
    cwd = os.getcwd()
    print("My current working directory is: {} ".format(cwd))


    # Return template and data
    return render_template("index.html", Mars_data=Mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    Mars_data = scrape_mars.scrape_info()
    print(Mars_data)
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, Mars_data, upsert=True)



    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)