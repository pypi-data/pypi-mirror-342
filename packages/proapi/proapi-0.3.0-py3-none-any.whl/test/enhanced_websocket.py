"""
Enhanced WebSocket example for ProAPI.

This example demonstrates the enhanced WebSocket support in ProAPI.
"""

from proapi import ProAPI
from proapi.websocket_middleware import AuthMiddleware, LoggingMiddleware, RateLimitMiddleware

# Create the application
app = ProAPI(debug=True)

# Create custom logging middleware
class CustomLoggingMiddleware(LoggingMiddleware):
    """Custom logging middleware that adds more detailed logs."""

    def __init__(self):
        super().__init__(log_messages=True)

    async def __call__(self, websocket, next_middleware):
        """Log WebSocket connections with custom format."""
        print(f"[WebSocket] New connection to {websocket.path}")
        result = await super().__call__(websocket, next_middleware)
        print(f"[WebSocket] Connection to {websocket.path} closed")
        return result

# Add global WebSocket middleware
app.use_websocket(CustomLoggingMiddleware())

# Authentication function for WebSockets
def authenticate_websocket(websocket):
    """Authenticate a WebSocket connection using a token query parameter."""
    token = websocket.query_params.get("token")

    if token == "secret":
        # Return a user object
        return {"username": "admin"}

    # Return None to indicate authentication failure
    return None

# Create authentication middleware
auth_middleware = AuthMiddleware(authenticate_websocket)

# Create rate limiting middleware
rate_limit_middleware = RateLimitMiddleware(max_messages=5, window_seconds=10)

# Regular HTTP routes
@app.get("/")
def index(request):
    """Home page."""
    return {
        "message": "Enhanced WebSocket Example",
        "description": "This example demonstrates enhanced WebSocket support in ProAPI.",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This endpoint"},
            {"path": "/ws", "method": "WebSocket", "description": "Echo WebSocket endpoint"},
            {"path": "/secure", "method": "WebSocket", "description": "Secure WebSocket endpoint (requires token=secret)"},
            {"path": "/chat/{room}", "method": "WebSocket", "description": "Chat room WebSocket endpoint"}
        ]
    }

# Basic WebSocket route
@app.websocket("/ws")
async def websocket_echo(websocket):
    """Echo WebSocket endpoint."""
    # Accept the connection
    await websocket.accept()

    try:
        # Echo messages back to the client
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Echo: {message}")
    except Exception as e:
        print(f"WebSocket error: {e}")

# Secure WebSocket route with authentication middleware
@app.websocket("/secure", middlewares=[auth_middleware, rate_limit_middleware])
async def secure_websocket(websocket):
    """Secure WebSocket endpoint with authentication and rate limiting."""
    # Accept the connection (authentication already done by middleware)
    await websocket.accept()

    # Get the authenticated user
    user = websocket.user_data.get("user")

    # Send welcome message
    await websocket.send_json({
        "type": "welcome",
        "message": f"Welcome, {user['username']}!",
        "note": "This connection is rate-limited to 5 messages per 10 seconds."
    })

    try:
        # Echo messages back to the client
        while True:
            message = await websocket.receive_text()
            await websocket.send_json({
                "type": "echo",
                "message": message,
                "user": user["username"]
            })
    except Exception as e:
        print(f"Secure WebSocket error: {e}")

# Chat room example with room management
@app.websocket("/chat/{room}")
async def websocket_chat(websocket, room):
    """Chat room WebSocket endpoint with room management."""
    # Accept the connection
    await websocket.accept()

    # Join the room
    await websocket.join_room(room)
    room_size = await websocket.get_room_size(room)

    # Store username in user_data
    username = websocket.query_params.get("username", f"User-{room_size}")
    websocket.user_data["username"] = username

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "system",
            "message": f"Welcome to chat room: {room}",
            "users": room_size
        })

        # Broadcast join message to other users
        await websocket.broadcast_json(room, {
            "type": "system",
            "message": f"{username} has joined the room",
            "users": room_size
        })

        # Handle messages
        while True:
            data = await websocket.receive_json()

            # Add user information
            data["username"] = username
            data["room"] = room

            # Broadcast to all users in the room
            await websocket.broadcast_json_to_all(room, data)
    except Exception as e:
        print(f"WebSocket error in room {room}: {e}")
    finally:
        # Leave the room
        room_size = await websocket.leave_room(room)

        # Broadcast leave message
        await websocket.broadcast_json(room, {
            "type": "system",
            "message": f"{username} has left the room",
            "users": room_size
        })

if __name__ == "__main__":
    print("Running Enhanced WebSocket Example")
    print("Try these endpoints:")
    print("  - http://127.0.0.1:8003/")
    print("  - ws://127.0.0.1:8003/ws")
    print("  - ws://127.0.0.1:8003/secure?token=secret")
    print("  - ws://127.0.0.1:8003/chat/room1?username=Alice")

    # Run with fast mode enabled on a different port
    app.run(fast=True, port=8003)
