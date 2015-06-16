from flask import Flask, render_template, redirect, url_for
from collections import namedtuple
app = Flask(__name__)

Member = namedtuple("Member", "id name")
pelle = Member(0, "Pelle")
joppe = Member(1, "Joppe")

@app.route("/", methods=["GET"])
def index():
    checked_in = [pelle]
    not_checked_in = [joppe]
    return render_template("index.html", 
                           checked_in=checked_in, not_checked_in=not_checked_in)

@app.route("/checked_in", methods=["POST"])
def check_in():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

