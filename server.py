from flask import Flask, render_template, redirect, request

from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe."

@app.route("/")
def home():
    return redirect("/users")

# CRUD

# Read All
@app.route("/users")
def index():
    mysql = connectToMySQL("users")
    
    query = "SELECT * FROM users;"

    users = mysql.query_db(query)

    return render_template("index.html", all_users = users)


# Create
@app.route("/users/new")
def add_user_form():
    return render_template("create.html")


@app.route("/users/create", methods = ["POST"])
def add_user():
    mysql = connectToMySQL("users")

    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) " \
        "VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"
    
    data = {
        "fname": request.form['first_name'],
        "lname": request.form['last_name'],
        "email": request.form['email']
    }

    user_id = mysql.query_db(query, data)

    return redirect("/users")


if __name__ == "__main__":
    app.run(debug = True)