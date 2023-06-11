from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
from random import choice
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
# app.config['SECRET_KEY'] can be any key, and it will work
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)
# Connects to the database
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Café table configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Café form configuration
class CafeForm(FlaskForm):
    name = StringField('Café name', validators=[DataRequired()])
    map_url = StringField('Café location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Café image (URL)', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    has_toilet = SelectField(
        u'Does the café have toilet available?',
        choices=['Yes', 'No'],
        validators=[DataRequired()]
    )
    has_wifi = SelectField(
        u'Does the café have Wi-Fi available?',
        choices=['Yes', 'No'],
        validators=[DataRequired()]
    )
    has_sockets = SelectField(
        u'Does the café have sockets available?',
        choices=['Yes', 'No'],
        validators=[DataRequired()]
    )
    can_take_calls = SelectField(
        u'Can the café take calls?',
        choices=['Yes', 'No'],
        validators=[DataRequired()]
    )
    coffee_price = StringField('Coffee price (e.g. $2.50)', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def cafes():
    """Returns a page with the whole Café database."""
    all_cafes = Cafe.query.all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return render_template('cafes.html', cafes=cafes)


@app.route('/all')
def all_cafes():
    """Returns the whole database as a JSON page."""
    all_cafes = Cafe.query.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route('/random')
def get_random_cafe():
    """Returns a random café from the list."""
    all_cafes = Cafe.query.all()
    random_choice = choice(all_cafes)
    cafe = random_choice.to_dict()
    return render_template('random_cafe.html', cafe=cafe)


@app.route('/search', methods=['POST'])
def search_cafe():
    """Searches for cafés within a location."""
    location = request.form['location'].title()
    cafes_found = Cafe.query.filter_by(location=location).all()
    cafes = [cafe.to_dict() for cafe in cafes_found]
    if cafes:
        return render_template('search_result.html', cafes=cafes)
    else:
        return render_template('not_found.html', location=True)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    """Adds a new café into the database."""
    form = CafeForm()

    # Verifies if the information in the form has been properly filled in
    if form.validate_on_submit():
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        seats = form.seats.data
        if form.has_toilet.data == 'Yes':
            has_toilet = 1
        elif form.has_toilet.data == 'No':
            has_toilet = 0
        if form.has_wifi.data == 'Yes':
            has_wifi = 1
        elif form.has_wifi.data == 'No':
            has_wifi = 0
        if form.has_sockets.data == 'Yes':
            has_sockets = 1
        elif form.has_sockets.data == 'No':
            has_sockets = 0
        if form.can_take_calls.data == 'Yes':
            can_take_calls = 1
        elif form.can_take_calls.data == 'No':
            can_take_calls = 0
        coffee_price = form.coffee_price.data

        # Creates a new entry in the database
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            seats=seats,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            has_sockets=has_sockets,
            can_take_calls=can_take_calls,
            coffee_price=coffee_price
        )
        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/update/<int:cafe_id>', methods=['GET', 'POST'])
def update_cafe(cafe_id):
    cafe_to_be_updated = Cafe.query.filter_by(id=cafe_id).first()

    # Checks if there's a café with that ID in the database
    if cafe_to_be_updated:
        form = CafeForm(
            name=cafe_to_be_updated.name,
            map_url=cafe_to_be_updated.map_url,
            img_url=cafe_to_be_updated.img_url,
            location=cafe_to_be_updated.location,
            seats=cafe_to_be_updated.seats,
            has_toilet=cafe_to_be_updated.seats,
            has_wifi=cafe_to_be_updated.has_wifi,
            has_sockets=cafe_to_be_updated.has_sockets,
            can_take_calls=cafe_to_be_updated.can_take_calls,
            coffee_price=cafe_to_be_updated.coffee_price,
        )

        # Verifies if the information in the form has been properly filled in
        if form.validate_on_submit():
            # Gets hold of the information from the form
            new_name = form.name.data
            new_map_url = form.map_url.data
            new_img_url = form.img_url.data
            new_location = form.location.data
            new_seats = form.seats.data
            if form.has_toilet.data == 'Yes':
                new_has_toilet = 1
            elif form.has_toilet.data == 'No':
                new_has_toilet = 0
            if form.has_wifi.data == 'Yes':
                new_has_wifi = 1
            elif form.has_wifi.data == 'No':
                new_has_wifi = 0
            if form.has_sockets.data == 'Yes':
                new_has_sockets = 1
            elif form.has_sockets.data == 'No':
                new_has_sockets = 0
            if form.can_take_calls.data == 'Yes':
                new_can_take_calls = 1
            elif form.can_take_calls.data == 'No':
                new_can_take_calls = 0
            new_coffee_price = form.coffee_price.data

            # Updates the database data
            cafe_to_be_updated.name = new_name
            cafe_to_be_updated.map_url = new_map_url
            cafe_to_be_updated.img_url = new_img_url
            cafe_to_be_updated.location = new_location
            cafe_to_be_updated.seats = new_seats
            cafe_to_be_updated.has_toilet = new_has_toilet
            cafe_to_be_updated.has_wifi = new_has_wifi
            cafe_to_be_updated.has_sockets = new_has_sockets
            cafe_to_be_updated.can_take_calls = new_can_take_calls
            cafe_to_be_updated.coffee_price = new_coffee_price

            db.session.commit()

            cafe = cafe_to_be_updated.to_dict()
            return redirect(url_for('cafes')), 200

        cafe_name = cafe_to_be_updated.name
        return render_template('update.html', cafe=cafe_name, form=form)

    else:
        # If there isn't a café with the specified ID, returns an error page
        return render_template('not_found.html', id=True)


@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    """Deletes a café from the database."""
    cafe_to_be_deleted = Cafe.query.filter_by(id=cafe_id).first()
    if cafe_to_be_deleted:
        db.session.delete(cafe_to_be_deleted)
        db.session.commit()
        return redirect(url_for('cafes'))
    else:
        return render_template('not_found.html', id=True)


if __name__ == '__main__':
    app.run(debug=True)
