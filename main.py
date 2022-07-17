from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

all_books = []
# db = sqlite3.connect('books-collection.db')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable = False)
    def __repr__(self):
        return f'<Book {self.title}>'



db.create_all()
# book_1 = Book(title="Harry Potter",author="J.K Rowlings", rating="9.3")
# db.session.add(book_1)
# db.session.commit()
# book_to_delete = Book.query.get(1)
# db.session.delete(book_to_delete)
# db.session.commit()
# cursor = db.cursor()



# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY,title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL )")

# Let's break this down.

# cursor - We created this in step 4 and this is the mouse pointer in our database that is going to do all the work.

# .execute() - This method will tell the cursor to execute an action. All actions in SQLite databases are expressed as SQL (Structured Query Language) commands. These are almost like English sentences with keywords written in ALL-CAPS. There are quite a few SQL commands. But don't worry, you don't have to memorise them.

# CREATE TABLE -  This will create a new table in the database. The name of the table comes after this keyword.

# Docs: https://www.w3schools.com/sql/sql_ref_create_table.asp

# books -  This is the name that we've given the new table we're creating.

# () -  The parts that come inside the parenthesis after CREATE TABLE books ( ) are going to be the fields in this table. Or you can imagine it as the Column headings in an Excel sheet.


# id INTEGER PRIMARY KEY -  This is the first field, it's a field called "id" which is of data type INTEGER and it will be the PRIMARY KEY for this table. The primary key is the one piece of data that will uniquely identify this record in the table. e.g. The primary key of humans might be their passport number because no two people in the same country has the same passport number.

# title varchar(250) NOT NULL UNIQUE -  This is the second field, it's called "title" and it accepts a variable-length string composed of characters. The 250 in brackets is the maximum length of the text. NOT NULL means it must have a value and cannot be left empty. UNIQUE means no two records in this table can have the same title.

# author varchar(250) NOT NULL -  A field that accepts variable-length Strings up to 250 characters called author that cannot be left empty.

# rating FLOAT NOT NULL -  A field that accepts FLOAT data type numbers, cannot be empty and the field is called rating.


# cursor.execute("INSERT into books values(1, 'Harry Potter', 'J.K Rowlings', '9.3') ")
# db.commit()

@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template("index.html", books = all_books)

@app.route("/add", methods=['POST','GET'])
def add():
    if request.method == 'POST':
        book_name = request.form.get("book-name")
        author = request.form.get("author")
        rating = request.form.get("rating")
        
        # print(book_name)
        books = Book(title =book_name, author=author, rating=rating)
        db.session.add(books)
        db.session.commit()
        # all_books.append(books)
        return redirect(url_for('home'))
    else:
        return render_template("add.html")

@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit_rating(id):
    book_to_update = Book.query.get(id)
    if request.method == "POST":
        new_rating = request.form.get("new_rating")
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('edit-rating.html', name=book_to_update.title, rating = book_to_update.rating)

@app.route("/delete/<int:id>")
def delete_book(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


