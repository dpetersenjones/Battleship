from flask import Flask, abort, render_template, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route("/")
def main():
    return render_template("board.html")



if __name__ == "__main__":
    app.run(debug=True, port=5002)