from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")

todos = []
max_length = 100

@app.route("/")
def index():
    return render_template("base.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    todo = request.form["todo"].strip()

    if not todo:
        return render_template("base.html", todos=todos, error="Task cannot be empty.")
    elif len(todo) > max_length:
        return render_template("base.html", todos=todos, error=f"Task cannot exceed {max_length} characters.")
    elif any(t["task"].lower() == todo.lower() for t in todos):
        return render_template("base.html", todos=todos, error="Task already exists.")

    todos.append({"task": todo, "done": False})
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todo = todos[index]
    if request.method == "POST":
        new_task = request.form["todo"].strip()
        # Input Validation Checks
        if not new_task:
            return render_template("edit.html", todo=todo, index=index, error="Task cannot be empty.")
        elif len(new_task) > max_length:
            return render_template("edit.html", todo=todo, index=index, error=f"Task cannot exceed {max_length} characters.")
        elif any(t["task"].lower() == new_task.lower() for t in todos if t != todo):
            return render_template("edit.html", todo=todo, index=index, error="Task already exists.")
        
        todo["task"] = new_task
        return redirect(url_for("index"))
    
    return render_template("edit.html", todo=todo, index=index)

@app.route("/check/<int:index>")
def check(index):
    todos[index]["done"] = not todos[index]["done"]
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    del todos[index]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
