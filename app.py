import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///pets.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

@app.route('/')
def index():
    animals = Animal.query.all()
    return render_template('index.html', animals=animals)

@app.route('/animal/<int:id>')
def animal_details(id):
    animal = Animal.query.get_or_404(id)
    return render_template('animal_details.html', animal=animal)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        
        flash('Please fill in all fields.', 'danger')
    return render_template('contact.html')

with app.app_context():
    from models import Animal
    db.create_all()
    
    # Add sample data if database is empty
    if not Animal.query.first():
        sample_animals = [
            Animal(
                name="Luna",
                species="Dog",
                breed="Golden Retriever",
                age=2,
                description="Friendly and energetic golden retriever looking for an active family.",
                image_url="https://images.unsplash.com/photo-1616620649762-a20882bc7651"
            ),
            Animal(
                name="Whiskers",
                species="Cat",
                breed="Persian",
                age=3,
                description="Gentle Persian cat who loves to cuddle and play.",
                image_url="https://images.unsplash.com/photo-1632107397704-03eda24af3be"
            ),
            # Add more sample animals here
        ]
        for animal in sample_animals:
            db.session.add(animal)
        db.session.commit()
