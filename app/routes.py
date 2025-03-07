from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'paalso'}
    return render_template(
        'index.html',
        user=user
    )

@app.route('/posts')
def posts_index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('posts_index.html', posts=posts)