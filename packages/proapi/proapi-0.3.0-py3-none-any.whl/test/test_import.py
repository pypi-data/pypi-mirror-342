from proapi import ProAPI

app = ProAPI(debug=True)

@app.get("/")
def index(request):
    return {"message": "Hello from test_import.py!"}

if __name__ == "__main__":
    print("Running test_import.py with auto-reloader")
    app.run(host="127.0.0.1", port=8000, use_reloader=True)
