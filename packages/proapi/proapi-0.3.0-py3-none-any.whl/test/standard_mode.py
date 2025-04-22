"""
Example demonstrating ProAPI's standard mode.

This example shows the standard mode for comparison with fast mode.
"""

from proapi import ProAPI

# Create the application with debug mode enabled
app = ProAPI(debug=True)

@app.get("/")
def index(request):
    """Home page."""
    return {
        "message": "Welcome to ProAPI Standard Mode!",
        "description": "This example demonstrates the standard mode for comparison."
    }

@app.get("/hello/{name}")
def hello(name, request):
    """Get a personalized greeting."""
    return {
        "message": f"Hello, {name}!",
        "description": "This endpoint demonstrates path parameters."
    }

@app.get("/benchmark")
def benchmark(request):
    """Benchmark endpoint."""
    # Simple benchmark that returns a large JSON response
    items = []
    for i in range(1000):
        items.append({
            "id": i,
            "name": f"Item {i}",
            "value": i * 3.14
        })
    
    return {
        "count": len(items),
        "items": items
    }

if __name__ == "__main__":
    print("Running ProAPI in standard mode")
    print("Try these endpoints:")
    print("  - http://127.0.0.1:8000/")
    print("  - http://127.0.0.1:8000/hello/world")
    print("  - http://127.0.0.1:8000/benchmark")
    
    # Run the application with standard mode
    app.run()
