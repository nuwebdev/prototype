from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from itertools import groupby
from operator import itemgetter

bp = Blueprint('blog', __name__)

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
            post['parsed_address'] = parse_address_from_listing(post['listing'])

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
            db.execute(
                'INSERT INTO post (title, body, author_id, listing)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], listing)
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
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, listing = ?, body = ?'
                ' WHERE id = ?',
                (title, listing, body, id)
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
    # Prepend the house emoji to the formatted address and make address a hyperlink
    return f"{house_emoji} <a href='{listing_url}' target='_blank'>{address}</a>"


# This function defines a route for searching the blog and returning results
@bp.route('/search')
def search():
    return render_template('blog/search.html')

@bp.route('/search/results', methods=['GET'])
def search_results():
    # Retrieve the query parameters from request.args
    state = request.args.get('state')
    sort_by = request.args.get('sort')

    # Perform your search logic against the database based on state and sort_by
    # For example, if you want to find posts from a specific state:
    db = get_db()
    if sort_by == 'top_comments':
        # An example query that sorts by the number of comments
        # Modify the query to match your database structure
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username, listing, COUNT(c.id) as comment_count'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' LEFT JOIN comments c ON c.post_id = p.id'
            ' WHERE p.state = ?'
            ' GROUP BY p.id'
            ' ORDER BY comment_count DESC',
            (state,)
        ).fetchall()
    elif sort_by == 'top_listings':
        # Similar query that sorts by another metric
        # Modify the query to match your database structure
        posts = db.execute('YOUR QUERY HERE').fetchall()
    else:
        # Default query if no sort_by is provided
        posts = db.execute('YOUR QUERY HERE').fetchall()

    # Transform the query results into a suitable format if needed
    # posts = [dict(row) for row in posts]

    # Use the index.html template to render the search results
    return render_template('index.html', posts=posts)

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
