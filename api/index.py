import json
import subprocess

# Simulate persistent storage in a simple JSON file
STATE_FILE = "/tmp/niblit_state.json"

# Load or initialize state
try:
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
except:
    state = {"chat_history": [], "version": 1.0}

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def handler(request):
    try:
        data = json.loads(request.get("body", "{}"))
        user_message = data.get("message", "")

        # Call chat.js to generate response
        result = subprocess.run(
            ["node", "/api/chat.js", user_message],
            capture_output=True, text=True
        )
        chat_response = result.stdout.strip()

        # Update state
        state["chat_history"].append({"user": user_message, "niblit": chat_response})
        save_state()

        # Call evolve.js to possibly evolve
        evolve_result = subprocess.run(
            ["node", "/api/evolve.js"],
            capture_output=True, text=True
        )
        response = {
            "message": chat_response,
            "evolution": evolve_result.stdout.strip(),
            "version": state["version"]
        }

    except Exception as e:
        response = {"error": str(e)}

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }
