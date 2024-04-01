from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Cấu hình kết nối với MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "username"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "database_name"

mysql = MySQL(app)


@app.route("/")
def search():
    return render_template("search.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        keyword = request.form["keyword"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM your_table WHERE column LIKE %s", ("%" + keyword + "%",)
        )
        data = cur.fetchall()
        count = sum(row[1].count(keyword) for row in data)
        cur.close()
        return render_template("results.html", data=data, keyword=keyword, count=count)


@app.route("/group_members")
def group_members():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM group_members_table")
    data = cur.fetchall()
    cur.close()
    return render_template("group_members.html", data=data)


@app.route("/topics")
def topics():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM topics_table")
    data = cur.fetchall()
    cur.close()
    return render_template("topics.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
