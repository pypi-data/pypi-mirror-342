"""
WebSocket example for ProAPI.

This example demonstrates WebSocket support in ProAPI.
"""

from proapi import ProAPI

# Create the application
app = ProAPI(debug=True)

# Regular HTTP routes
@app.get("/")
def index(request):
    """Home page."""
    return {
        "message": "WebSocket Example",
        "description": "This example demonstrates WebSocket support in ProAPI.",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This endpoint"},
            {"path": "/ws", "method": "WebSocket", "description": "Echo WebSocket endpoint"},
            {"path": "/chat/{room}", "method": "WebSocket", "description": "Chat room WebSocket endpoint"}
        ]
    }

# WebSocket routes
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

# Chat room example with path parameters
@app.websocket("/chat/{room}")
async def websocket_chat(websocket, room):
    """Chat room WebSocket endpoint."""
    # Store active connections
    if not hasattr(app, "_chat_connections"):
        app._chat_connections = {}

    # Create room if it doesn't exist
    if room not in app._chat_connections:
        app._chat_connections[room] = []

    # Accept the connection
    await websocket.accept()

    # Add to room
    app._chat_connections[room].append(websocket)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "system",
            "message": f"Welcome to chat room: {room}",
            "users": len(app._chat_connections[room])
        })

        # Broadcast join message to other users
        for conn in app._chat_connections[room]:
            if conn != websocket:
                await conn.send_json({
                    "type": "system",
                    "message": "A new user has joined the room",
                    "users": len(app._chat_connections[room])
                })

        # Handle messages
        while True:
            data = await websocket.receive_json()

            # Add room information
            data["room"] = room

            # Broadcast to all users in the room
            for conn in app._chat_connections[room]:
                await conn.send_json(data)
    except Exception as e:
        print(f"WebSocket error in room {room}: {e}")
    finally:
        # Remove from room
        if room in app._chat_connections and websocket in app._chat_connections[room]:
            app._chat_connections[room].remove(websocket)

            # Broadcast leave message
            for conn in app._chat_connections[room]:
                await conn.send_json({
                    "type": "system",
                    "message": "A user has left the room",
                    "users": len(app._chat_connections[room])
                })

if __name__ == "__main__":
    print("Running WebSocket example")
    print("Try these endpoints:")
    print("  - http://127.0.0.1:8001/")
    print("  - ws://127.0.0.1:8001/ws")
    print("  - ws://127.0.0.1:8001/chat/room1")

    # Run with fast mode enabled on a different port
    app.run(fast=True, port=8001)
