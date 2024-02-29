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
    address_part = parts[4]  # This is based on the URL structure you've given
     # Replace dashes with spaces
    address = address_part.replace('-', ' ')
    # Prepend the house emoji to the formatted address and make address a hyperlink
    return f"{house_emoji} <a href='{listing_url}' target='_blank'>{address}</a>"
