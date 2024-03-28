from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from collections import defaultdict
from itertools import groupby
from operator import itemgetter

bp = Blueprint('blog', __name__)

import re

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, listing'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY listing, created DESC'
    ).fetchall()
    
    # Ensure posts is a list of dicts for easier manipulation
    posts = [dict(post) for post in posts]
    
    # Apply the parsing function to each 'listing' URL
    for post in posts:
        if post['listing']:
            parsed_address, state = parse_address_from_listing(post['listing'])
            post['parsed_address'] = parsed_address
            post['state'] = state  

    # Group posts by listing
    grouped_posts = {k: list(v) for k, v in groupby (posts, key=itemgetter('listing'))}
    
    return render_template('blog/index.html', grouped_posts=grouped_posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        listing = request.form['listing'] 
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            title = request.form['title']
            body = request.form['body']
            listing = request.form['listing']
            parsed_address, state = parse_address_from_listing(listing) 
            
            db.execute(
                'INSERT INTO post (title, body, author_id, listing, state)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], listing, state)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, listing'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post



@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        listing = request.form.get('listing')
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
            parsed_address, state = parse_address_from_listing(listing)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, listing = ?, state = ?'
                ' WHERE id = ?',
                (title, body, listing, state, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


def parse_address_from_listing(listing_url):
    # Unicode for the house emoji
    house_emoji = '\U0001F3E0'
    # Split the URL by slashes and take the part that contains the address
    parts = listing_url.split('/')
    address_part = parts[4]  
     # Replace dashes with spaces
    address = address_part.replace('-', ' ')
    # Extract the state abbreviation based on its position from the end of the address
    # The state is always two characters at the -8 and -7 positions before the zip code
    state = address[-8:-6]
    # Prepend the house emoji to the formatted address and make address a hyperlink
    formatted_address = f"{house_emoji} <a href='{listing_url}' target='_blank'>{address}</a>"
    return formatted_address, state


# This function defines a route for searching the blog and returning results
@bp.route('/search')
def search():
    db = get_db()
    # Query to get all unique states from the 'post' table
    states = db.execute('SELECT DISTINCT state FROM post ORDER BY state ASC').fetchall()
    states = [state['state'] for state in states if state['state']]  # List comprehension to clean up the result
    return render_template('blog/search.html', states=states)


@bp.route('/search/results', methods=['GET'])
def search_results():
    search_type = request.args.get('search_type')
    db = get_db()

    # Search Options based on user selection
    if search_type == 'state':
        state = request.args.get('state')
        query = 'SELECT * FROM post WHERE state = ? ORDER BY created DESC'
        params = (state,)
    elif search_type == 'top_comments':
        query = '''
        SELECT p.id, p.title, p.body, p.created, p.author_id, u.username, p.listing, COUNT(c.id) as comment_count
        FROM post p
        JOIN user u ON p.author_id = u.id
        LEFT JOIN comments c ON c.post_id = p.id
        GROUP BY p.listing
        ORDER BY p.listing, comment_count DESC
        '''
        params = ()
    elif search_type == 'top_votes':
        query = '''
        SELECT p.id, p.title, p.body, p.created, p.author_id, u.username, p.listing, IFNULL(SUM(v.vote_type), 0) as vote_sum
        FROM post p
        JOIN user u ON p.author_id = u.id
        LEFT JOIN vote v ON v.post_id = p.id
        GROUP BY p.listing
        ORDER BY p.listing, vote_sum DESC
        '''
        params = ()
    else:
        query = 'SELECT * FROM post ORDER BY created DESC'
        params = ()

    posts = [dict(row) for row in db.execute(query, params).fetchall()]
    
    # Apply the parsing function to each 'listing' URL for posts in the search result
    for post in posts:
        if post['listing']:
            parsed_address, state = parse_address_from_listing(post['listing'])
            post['parsed_address'] = parsed_address
            post['state'] = state

    # Group posts by 'parsed_address' if you want to group them by the parsed listing addresses
    # Assuming 'listing' is unique and directly corresponds to 'parsed_address'
    grouped_posts = {k: list(v) for k, v in groupby(posts, key=itemgetter('parsed_address'))}
    
    # Use the index.html template to render the search results with grouped posts
    return render_template('blog/index.html', grouped_posts=grouped_posts)


# This function defines a route for handling user votes on listings
@bp.route('/vote', methods=['POST'])
@login_required
def vote():
    user_id = g.user['id']
    post_id = request.form['post_id']
    vote_type = request.form['vote_type']

    db = get_db()
    try:
        db.execute(
            'INSERT INTO vote (user_id, post_id, vote_type) VALUES (?, ?, ?) ON CONFLICT(user_id, post_id) DO UPDATE SET vote_type=?',
            (user_id, post_id, vote_type, vote_type)
        )
        db.commit()
    except db.IntegrityError:
        error = "Database error occurred."
        flash(error)
    return redirect(url_for('index'))
