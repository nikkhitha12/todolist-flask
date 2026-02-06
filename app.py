from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    # check if completed column exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    # add column if missing
    if "completed" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()

    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (task, completed) VALUES (?,0)", (task,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = CASE WHEN completed=1 THEN 0 ELSE 1 END
        WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
 
    app.run(host="0.0.0.0", port=10000)

