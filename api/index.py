import json
import os

# Use a persistent file for memory (simple JSON storage)
MEMORY_FILE = "api/memory.json"

# Load memory from file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def handler(request):
    try:
        data = json.loads(request.get("body", "{}"))
        user_message = data.get("message", "").strip()
        memory = load_memory()

        if user_message:
            # Store user message in memory
            memory.append({"user": user_message})
            
            # Generate simple evolving response based on previous messages
            reply = f"Niblit remembers {len(memory)} messages. You said: '{user_message}'"
            memory.append({"bot": reply})
        else:
            reply = "Niblit: Say something!"

        save_memory(memory)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
