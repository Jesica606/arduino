import os

from flask import Flask, render_template

from pag.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev')

    from . import db
    db.init_app(app)

    
    @app.route('/datos')
    def index():
        db = get_db()
        films = db.execute(
            'SELECT title, description, rating, release_year, film_id'
            ' FROM film'
            ' ORDER BY title ASC'
        ).fetchall()
        return render_template('datos.html', films=films)


    return app