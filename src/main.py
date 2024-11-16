import os
from dotenv import load_dotenv

load_dotenv()

def main(context):
    expected_token = os.getenv("EXPECTED_BEARER_TOKEN")
    auth_header = context.req.headers.get("Authorization")

    if not auth_header:
        context.error("Authorization header is missing")
        return context.res.json({"error": "Authorization header is missing"})

    try:
        bearer_token = auth_header.split(" ")[1]
    except IndexError:
        context.error("Bearer token malformed")
        return context.res.json({"error": "Bearer token malformed"})

    if bearer_token != expected_token:
        context.error("Unauthorized access attempt with invalid token")
        return context.res.json({"error": "Unauthorized"})

    if context.req.path == "/ping":
        return context.res.text("Pong")