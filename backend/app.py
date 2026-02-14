from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE CONNECTION ----------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rayna@22*",
    database="mindswitch"
)

cursor = db.cursor(dictionary=True)


# ---------------- ROOT ----------------

@app.route("/")
def home():
    return "MindSwitch Backend Running with MySQL"


# ---------------- GENERATE HINT ----------------

@app.route("/generate_hint", methods=["POST"])
def generate_hint():
    data = request.json
    mode = data.get("mode")
    page_content = data.get("page_content", "").lower()

    # For now use dummy user id = 1
    user_id = 1

    # Create session
    cursor.execute(
        "INSERT INTO sessions (user_id, mode) VALUES (%s, %s)",
        (user_id, mode)
    )
    db.commit()

    session_id = cursor.lastrowid

    # Store session_id temporarily in response
    if mode == "DSA":

        if "binary search" in page_content:
            pattern_hint = "This problem may require Binary Search."
        elif "graph" in page_content:
            pattern_hint = "Graph problems usually involve BFS or DFS."
        elif "subarray" in page_content:
            pattern_hint = "Subarray problems often use Sliding Window."
        else:
            pattern_hint = "Match constraints with a known algorithm pattern."

        response = {
            "level1": "Read constraints carefully.",
            "level2": pattern_hint,
            "level3": "Define algorithm steps before coding.",
            "session_id": session_id
        }

    elif mode == "INTERVIEW":
        response = {
            "level1": "Clarify requirements.",
            "level2": "Use STAR method.",
            "level3": "Discuss trade-offs.",
            "session_id": session_id
        }

    elif mode == "STUDY":
        response = {
            "level1": "Identify core idea.",
            "level2": "Extract 3 key points.",
            "level3": "Create 2 self-test questions.",
            "session_id": session_id
        }

    else:
        response = {
            "level1": "Invalid mode.",
            "level2": "",
            "level3": "",
            "session_id": session_id
        }

    return jsonify(response)


# ---------------- TRACK USAGE ----------------

@app.route("/track_usage", methods=["POST"])
def track_usage():
    data = request.json
    mode = data.get("mode")
    level_unlocked = data.get("level_unlocked")
    session_id = data.get("session_id")

    cursor.execute(
        "INSERT INTO unlock_logs (session_id, mode, level_unlocked) VALUES (%s, %s, %s)",
        (session_id, mode, level_unlocked)
    )
    db.commit()

    return jsonify({"status": "tracked"})


# ---------------- ANALYTICS ----------------

@app.route("/analytics", methods=["GET"])
def analytics():

    cursor.execute("SELECT COUNT(*) AS total FROM unlock_logs")
    total_unlocks = cursor.fetchone()["total"]

    cursor.execute("SELECT mode, COUNT(*) as count FROM unlock_logs GROUP BY mode")
    mode_data = cursor.fetchall()

    cursor.execute("SELECT level_unlocked, COUNT(*) as count FROM unlock_logs GROUP BY level_unlocked")
    level_data = cursor.fetchall()

    level_usage = {2: 0, 3: 0}

    for row in level_data:
        level_usage[row["level_unlocked"]] = row["count"]

    dependency_score = 0
    if total_unlocks > 0:
        dependency_score = round((level_usage.get(3, 0) / total_unlocks) * 100, 2)

    return jsonify({
        "total_unlocks": total_unlocks,
        "mode_usage": mode_data,
        "level_usage": level_usage,
        "level3_dependency_percent": dependency_score
    })


if __name__ == "__main__":
    app.run(debug=True)
