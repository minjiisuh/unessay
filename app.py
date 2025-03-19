from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use SQLite (Change to PostgreSQL if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movable_type.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Hanja character table
class HanjaCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(10), nullable=False)
    pronunciation = db.Column(db.String(50))
    meaning = db.Column(db.Text)

# Home Route
@app.route('/')
def index():
    characters = HanjaCharacter.query.all()
    return render_template('index.html', characters=characters)

# Add New Character Route
@app.route('/add', methods=['POST'])
def add_character():
    character = request.form.get('character')
    pronunciation = request.form.get('pronunciation')
    meaning = request.form.get('meaning')

    new_char = HanjaCharacter(character=character, pronunciation=pronunciation, meaning=meaning)
    db.session.add(new_char)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
