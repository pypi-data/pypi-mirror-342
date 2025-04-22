from proapi import ProAPI

app = ProAPI(debug=True)

@app.get("/")
def index(request):
    return {"message": "Hello from ASGI adapter!"}

# Create an ASGI application
async def asgi_app(scope, receive, send):
    """
    ASGI application.
    
    Args:
        scope: ASGI scope
        receive: ASGI receive function
        send: ASGI send function
    """
    if scope["type"] != "http":
        # We only handle HTTP requests for now
        await send({
            "type": "http.response.start",
            "status": 500,
            "headers": [(b"content-type", b"application/json")]
        })
        await send({
            "type": "http.response.body",
            "body": b'{"error": "Only HTTP requests are supported"}'
        })
        return
    
    try:
        # Extract method and path
        method = scope["method"]
        path = scope["path"]
        
        # Extract headers
        headers = {k.decode("utf-8"): v.decode("utf-8") for k, v in scope["headers"]}
        
        # Extract query parameters
        query_params = {}
        query_string = scope.get("query_string", b"").decode("utf-8")
        if query_string:
            for param in query_string.split("&"):
                if "=" in param:
                    k, v = param.split("=", 1)
                    if k in query_params:
                        if isinstance(query_params[k], list):
                            query_params[k].append(v)
                        else:
                            query_params[k] = [query_params[k], v]
                    else:
                        query_params[k] = v
        
        # Extract client address
        client_address = scope.get("client", ("127.0.0.1", 0))
        
        # Read request body
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
        
        # Create ProAPI request
        from proapi.server import Request
        request = Request(
            method=method,
            path=path,
            headers=headers,
            query_params=query_params,
            body=body,
            remote_addr=client_address[0]
        )
        
        # Process the request
        response = app.handle_request(request)
        
        # Convert headers
        headers = []
        for k, v in response.headers.items():
            headers.append((k.encode("utf-8"), str(v).encode("utf-8")))
        
        # Send response start
        await send({
            "type": "http.response.start",
            "status": response.status,
            "headers": headers
        })
        
        # Send response body
        if isinstance(response.body, str):
            body = response.body.encode("utf-8")
        elif isinstance(response.body, bytes):
            body = response.body
        else:
            body = b""
        
        await send({
            "type": "http.response.body",
            "body": body
        })
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        
        # Send error response
        await send({
            "type": "http.response.start",
            "status": 500,
            "headers": [(b"content-type", b"application/json")]
        })
        
        error_body = {"error": "Internal Server Error"}
        if app.debug:
            error_body["detail"] = str(e)
            error_body["traceback"] = error_traceback
        
        import json
        await send({
            "type": "http.response.body",
            "body": json.dumps(error_body).encode("utf-8")
        })

# This is the ASGI application that uvicorn will use
application = asgi_app
