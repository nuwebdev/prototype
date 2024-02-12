## "Comment on Houses" App

The 'comment on houses' app makes use of the Flask's tutorial of how to setup an app for a basic blog website. It includes a SQL database, and uses Python, and html. 

It builds on the tutorial by adding an additional field on the site/ column in the SQL database for a hyperlink of a house listing. 

To run this app, download the code FLASK-DEMO-SEANMAINER code base and open it in the IDE of your choice.

A virtual environment has been created, including
all necessary dependencies to ensure reproducibility. 

Make commands have been provided: Setup and activate the virtual environment in your Terminal:

```make venv```

Then, to initialize the app within the virtual environment"

```make run```

After running these commands, open a browser and visit: 

http://127.0.0.1:5000/auth/register

Create a username and password, click 'Register', then (when the page refreshes), click 'Login'. 

From there, you may generate a new post, with the requirement that you provide a title and body of text, and an option to also include a house listing. 

If you do include a listing in the 'House Listing URL' field, it will also auto-generate a LINK within the index of your post.

Or, you may browse the existing posts.

## New Functional Elements:

This app includes a new column in the SQL schema for a 'listing'.
This listing is a TEXT field, which can hold a url for a house listing. 

Users can add and edit listing urls when creating or updating posts to the blog, because some edits have been made to the Python scripts in blog.py, as well as within index.html - to display a hyperlink to the associated listing in the index of the blog posts, improving the user interface.

## New Design Elements:
The styles.css stylesheet has been edited to make some small adjustments: a new background image of a sunset on an ocean horizon adds some color. This is included in the codebase as bkgrnd.png and comes from 'The Darkroom Society' website. 

Font-wise, I created a new font-family, which I used for the header - AlphaClouds.tff was downloaded from dafont.com and is included as part of the code base.

Further, some small adjustments were made to font color, as well as some reshaping of the header bar, increasing the width of the border line. 

## Challenges Faced:
I used MDN Docs extensively to explore how to edit the fonts, add in a custom font, and make small adjustments to the CSS.

Adding in a new field to the website within the html was straightforward enough, though ensuring this text was written and called from my database was challenging. I had to troubleshoot using stack overflow, as well as ChatGPT. Ultimately, the key was to re-initialize my database, as well as ensure 'listing' was included in all of the Python scripts, and specifically the request.get.form call required parantheses instead of square brackets to 'get' the object (ie. listing) before displaying it.

My biggest learning was how to add a new field to an SQL database, then identify and edit all of the places where this data is accessed, and most importantly - REINITIATILIZE the database using init-db (with the caveat that this will erase all existing data in your database).

Another learning was to ensue my virtual environment has all the appropriate dependencies, and that I am working within my virtual environment. 

## Acknowledgements:
Flask Pallet Projects Blog Tutorial: https://flask.palletsprojects.com/en/3.0.x/tutorial/

Stack Overflow: https://stackoverflow.com/questions/18178867/how-can-i-use-googles-roboto-font-on-a-website

ChatGPT: https://chat.openai.com/

DaFont: https://www.dafont.com/alpha-clouds.font

Darkroom Society: https://darkroomsociety.com/
