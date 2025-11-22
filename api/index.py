import json

def handler(request):
    try:
        # Parse the JSON body if sent via POST
        data = json.loads(request.get("body", "{}"))
        message = data.get("message", "")

        # Simple AI-style reply
        if message.strip() == "":
            reply = "Niblit: Say something!"
        else:
            reply = f"Niblit: I heard '{message}'"

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
