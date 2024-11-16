from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
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

    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )

    users = Users(client)

    try:
        response = users.list()
        context.log("Total users: " + str(response["total"]))
    except AppwriteException as err:
        context.error("Could not list users: " + repr(err))

    if context.req.path == "/ping":
        return context.res.text("Pong")

    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
