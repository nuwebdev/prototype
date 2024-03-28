## "Comment on Houses" App

The idea is simple: a web app which allows users to leave comments on real estate listings. 

The 'comment on houses' app makes use of the Flask's tutorial of how to setup an app for a basic blog website. It includes a SQLite database, and uses Python, and html. 

It builds on the tutorial by adding an additional field on the site/ column in the SQL database for a hyperlink of a house listing. 

To run this app, clone FLASK-DEMO-SEANMAINER code base and open it in the IDE of your choice.

A virtual environment has been created, including all necessary dependencies to ensure reproducibility. 

## HOW TO RUN THE WEB APP:

STEP 1: Make commands have been provided. Setup and activate the virtual environment in your Terminal:

```make venv```

STEP 2: Initialize the app within the virtual environment:

```make run```

STEP 3: After running these make commands, open a browser and visit: 
http://127.0.0.1:5000 

An indexed version of all posts will be displayed. Each post is a (set of) comments on a specific listing. Comments are grouped by houses, all queried and returned from my sql database.

STEP 4: Visit  http://127.0.0.1:5000/auth/register to create a username and password, click 'Register'. 

STEP 5: Re-enter your username/ password, click 'Login'. 

STEP 6: View existing posts. You will land on a page showing existing user comments/ listings. 

STEP 7: You may also generate a new post by clicking 'New' in the top right corner. This will open a page with the requirement that you provide a title and body of text, and a link from Zillow. For a link, simply go to www.zillow.com, find a house you like (or dislike) and copy and paste the full URL. If you do include a listing in the 'House Listing URL' field, it will also auto-generate a LINK within the index of your post. Or, if you create a new post and include a link to a house that already has comments, your comments will be indexed under that existing listing link.


## Acknowledgements:
Flask Pallet Projects Blog Tutorial: https://flask.palletsprojects.com/en/3.0.x/tutorial/

Stack Overflow: https://stackoverflow.com/questions/18178867/how-can-i-use-googles-roboto-font-on-a-website

ChatGPT: https://chat.openai.com/

DaFont: https://www.dafont.com/alpha-clouds.font

Darkroom Society: https://darkroomsociety.com/
