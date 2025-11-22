import json

def handler(request):
    try:
        # Parse incoming JSON
        data = json.loads(request.get("body", "{}"))
        user_message = data.get("message", "")

        # Respond with a simple echo
        response = {"message": f"Niblit heard: {user_message}"}

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
