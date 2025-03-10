from flask import (
    jsonify,
    render_template
)
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


# TODO: remove after debugging
def _config_to_dict(config):
    return {key: str(value) for key, value in config.items()}


@app.route('/config')
def app_config():
    app.logger.info("Config: %s", app.config)
    config_dict = _config_to_dict(app.config)
    return jsonify(config_dict)
