from proapi import ProAPI

app = ProAPI(debug=True)

@app.get("/")
def index(request):
    return {"message": "Hello from simple_test.py!"}

if __name__ == "__main__":
    print("Running simple_test.py with default server")
    app.run(host="127.0.0.1", port=8000, server_type="default", use_reloader=False)
