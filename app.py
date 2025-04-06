from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import pandas as pd
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for session management

#change
# Hardcoded login credentials
VALID_USERS = {"prajval": "123", "annotator2": "securepass"}
#change

# Load posts from CSV
#df = pd.read_csv("posts.csv")
df = pd.read_csv("posts_20_to_140.csv")
annotations_file = "annotations.json"

# Load existing annotations if available
if os.path.exists(annotations_file):
    with open(annotations_file, "r") as f:
        annotations = json.load(f)
else:
    annotations = {str(i): {"words": [], "symptoms": [], "annotator" : []} for i in range(len(df))}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in VALID_USERS and VALID_USERS[username] == password:
            session["username"] = username
            return redirect(url_for("annotate"))
        return "Invalid credentials. Try again."
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/annotate")
def annotate():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/get_posts")
def get_posts():
    return jsonify(df["text"].tolist())

@app.route("/get_annotations")
def get_annotations():
    return jsonify(annotations)

@app.route("/save_annotation", methods=["POST"])
def save_annotation():
    data = request.json
    post_id = str(data["post_id"])
    annotations[post_id] = {"words": data["words"], "symptoms": data["symptoms"], "annotator": session["username"] }
    
    with open(annotations_file, "w") as f:
        json.dump(annotations, f)
    
    return jsonify({"message": "Annotation saved successfully!"})

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 4000))  # Get the port from environment or use 5000 for local
#     app.run(host="0.0.0.0", port=port)