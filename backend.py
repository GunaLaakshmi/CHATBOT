from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# In-memory storage for tasks (replace with database in production)
tasks = []

# Sample responses for task scheduling
task_responses = [
    "I can help you schedule that! Click the 'Add to Schedule' button below to set the time and priority. ✅",
    "I'll help you plan that! Use the scheduling form below to set the details. 🗓",
    "Great idea! Click 'Add to Schedule' below to set when you'd like to do this. ⏰"
]

# Sample responses for general inquiries
general_responses = [
    "How can I assist with your daily planning?",
    "Need help organizing your day? Let me know your tasks!",
    "I'm here to help you schedule tasks and set reminders!"
]

@app.route("/daily-planner", methods=["POST"])
def daily_planner():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    
    if any(word in user_message.lower() for word in ["schedule", "remind", "plan", "set", "task", "todo"]):
        bot_response = random.choice(task_responses)
    elif "thank" in user_message.lower():
        bot_response = "You're welcome! Let me know if you need more planning help. 😊"
    elif any(word in user_message.lower() for word in ["bye", "exit", "quit"]):
        bot_response = "Goodbye! Have a productive day. 🏆"
    else:
        bot_response = random.choice(general_responses)
    
    return jsonify({"response": bot_response})

@app.route("/add-task", methods=["POST"])
def add_task():
    """Add a new task to the schedule."""
    data = request.get_json()
    
    task = {
        "task": data.get("task"),
        "time": data.get("time"),
        "priority": data.get("priority"),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tasks.append(task)
    return jsonify({"message": "Task added successfully", "task": task})

@app.route("/schedule", methods=["GET"])
def get_schedule():
    """Return the current schedule with task status updates."""
    current_time = datetime.now().time()
    
    # Update task statuses
    for task in tasks:
        task_time = datetime.strptime(task["time"], "%H:%M").time()
        if task["status"] == "pending":
            if current_time > task_time:
                task["status"] = "overdue"
    
    return jsonify({"tasks": tasks})

@app.route("/complete-task/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    """Mark a task as completed."""
    if 0 <= task_id < len(tasks):
        tasks[task_id]["status"] = "completed"
        return jsonify({"message": "Task marked as completed"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)