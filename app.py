from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Library Data
library_name = "My Library"
book_list = {"Harry Potter": 2, "Money Heist": 4}
lend_records = {}

@app.route("/")
def home():
    return render_template("index.html", library_name=library_name, books=book_list, lend_records=lend_records)

@app.route("/add_book", methods=["POST"])
def add_book():
    bookname = request.form["bookname"]
    no_of_books = int(request.form["quantity"])
    
    if bookname in book_list:
        book_list[bookname] += no_of_books
    else:
        book_list[bookname] = no_of_books
    
    flash(f"Added {no_of_books} copies of {bookname}!", "success")
    return redirect(url_for("home"))

@app.route("/lend_book", methods=["POST"])
def lend_book():
    person_name = request.form["person_name"]
    bookname = request.form["bookname"]

    if bookname in book_list and book_list[bookname] > 0:
        book_list[bookname] -= 1
        if bookname in lend_records:
            lend_records[bookname].append(person_name)
        else:
            lend_records[bookname] = [person_name]

        flash(f"{person_name} borrowed {bookname}.", "success")
    else:
        flash(f"{bookname} is not available!", "danger")

    return redirect(url_for("home"))

@app.route("/return_book", methods=["POST"])
def return_book():
    bookname = request.form["bookname"]
    person_name = request.form["person_name"]

    if bookname in lend_records and person_name in lend_records[bookname]:
        lend_records[bookname].remove(person_name)
        book_list[bookname] += 1
        flash(f"{person_name} returned {bookname}.", "success")
    else:
        flash(f"Return failed! {person_name} does not have {bookname}.", "danger")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
