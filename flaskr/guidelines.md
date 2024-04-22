## Guidelines/ How to Use 'Comment on House Listings'"

The idea is simple: a web app which allows users to leave comments on real estate listings. 

The 'comment on houses' app makes use of the Flask's tutorial of how to setup an app for a basic blog website. It includes a SQLite database, and uses Python, and html. 

It builds on the tutorial by adding an additional field on the site/ column in the SQL database for a hyperlink of a house listing, as well as various search functionality, voting functionality. 

Once this repo is cloned, follow the instructions below to use the web application. 

STEP 1: Make commands have been provided. Setup and activate the virtual environment in your Terminal:

```make venv```

STEP 2: Initialize the app within the virtual environment:

```make run```

STEP 3: After running these make commands, open a browser and visit: 
http://127.0.0.1:5000 

An indexed version of all posts will be displayed. Each post is a (set of) comments on a specific listing. Comments are grouped by houses, all queried and returned from my sql database, organized by most recent to oldest posts.

STEP 4: Visit  http://127.0.0.1:5000/auth/register to create a username and password, click 'Register'. 

STEP 5: Re-enter your username/ password, click 'Login'. 

STEP 6: View existing posts. You will land on a page showing existing user comments/ listings. 

GENERATE A NEW POST:

- Click 'New' in the top right corner. This will open a page with the requirement that you provide a title and body of text, and a link from Zillow. For a link, simply go to www.zillow.com, find a house you like (or dislike) and copy and paste the full URL. If you do include a listing in the 'House Listing URL' field, it will also auto-generate a LINK within the index of your post. Or, if you create a new post and include a link to a house that already has comments, your comments will be indexed under that existing listing link.

UPDATE/ EDIT/ DELETE A POST:
- A user may update or edit any of their own posts (and not others posts). Simply find the existing comment on the index.html page, then click 'Edit'. Make edits, click 'Save' and your edits will be saved. OR click 'Delete' when on the edit page, and the post will be deleted.

SEARCH POSTS:
- Users have the ability to search through posts by 'State', Most Comments, or Best Comments by navigating to the 'Search' page, accessible via the top navbar 'Search Listings' selection.
- Search by State: This allows users to sarch for all listings from a specific state. The dropdown menu is automatically populated with all (and only) those states for which users have added thus far.
- Most Comments: This will return an indexed version of posts which are organized by the listings with the most number of comments, down to those with the least number of comments. 
- Best Comments: This will return an indexed version of the posts which are organized by the posts which have the comments with the most upvotes. 

ALL LISTINGS:
- Selecting 'All Listings' from the top navbar will return an indexed version of all listings, with posts/ comments grouped underneath listings, organized from most recent posts to oldest created posts. 

VOTING:
- Each post has up and down arrows associated with the post. These can be clicked by a user to 'vote' for that specific post. Only one vote per post is allowed per post, per user. These votes are captured in a Votes table, and used for search functionality. 