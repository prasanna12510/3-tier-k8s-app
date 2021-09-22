from flask import Flask, render_template, url_for, request
import operator
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///words.sqlite3'

db = SQLAlchemy(app)

class Words(db.Model):
    # Defines the Table Name user
    __tablename__ = "words"

    # Makes three columns into the table id, name, email
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word_count = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    # A constructor function where we will pass the word_count and it gets add as a new entry in the table.
    def __init__(self, word_count,content):
        self.word_count = word_count
        self.content = content


# home
@app.route('/')
def home():
    return render_template('home.html')

# Word Count
@app.route('/count', methods=['GET', 'POST'])
def count():
    if request.method == 'POST':
        data = request.form['fulltextarea']
        word_list = data.split()
        list_length = len(word_list)


        db.session.add(Words(list_length, data))
        db.session.commit()
        user_data = Words.query.all()

        word_disc = {}
        for word in word_list:
            if word in word_disc:
                word_disc[word] += 1
            else:
                word_disc[word] = 1

        sort_list = sorted(word_disc.items(), key=operator.itemgetter(1), reverse=True)
        return render_template('count.html', fulltext=data, words=list_length, worddisc=sort_list, user_data=user_data)

    return render_template('home.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
