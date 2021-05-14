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

    user_list = mysql.query_db(query)

    return render_template("index.html", all_users = user_list)


# Read One
@app.route("/users/<int:user_id>")
def show_user(user_id):
    mysql = connectToMySQL("users")

    query = "SELECT * FROM users WHERE id = %(id)s;"

    data = {
        "id": user_id
    }
    
    user_from_db = mysql.query_db(query, data)

    return render_template("user.html", user = user_from_db[0])


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


# Update
@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    mysql = connectToMySQL("users")

    query = "SELECT * FROM users WHERE id = %(id)s;"
    
    data = {
        "id": user_id
    }
    
    user_list = mysql.query_db(query, data)

    return render_template("edit_user.html", user = user_list[0])

@app.route('/users/<int:user_id>/update', methods = ['POST'])
def update_user(user_id):
    mysql = connectToMySQL("users")

    query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
    data = {
        "fname": request.form['first_name'],
        "lname": request.form['last_name'],
        "email": request.form['email'],
        "id": user_id
    }

    mysql.query_db(query, data)

    return redirect(f"/users/{user_id}")

# Delete
@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    mysql = connectToMySQL("users")

    query = "DELETE FROM users WHERE id = %(id)s;"

    data = {
        "id": user_id
    }

    mysql.query_db(query, data)

    return redirect("/users")

if __name__ == "__main__":
    app.run(debug = True)