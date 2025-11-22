import json

def handler(request):
    try:
        data = json.loads(request.get("body", "{}"))
        user_message = data.get("message", "")

        # Basic AI logic placeholder (echo)
        if user_message.strip() == "":
            reply = "Niblit: Say something!"
        else:
            reply = f"Niblit: I heard '{user_message}'"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
