from proapi import ProAPI

app = ProAPI(debug=True)

@app.get("/")
def index(request):
    return {"message": "Hello from run_test.py!"}

if __name__ == "__main__":
    from proapi.run import run_app
    
    print("Running run_test.py with proapi.run")
    run_app(__file__, host="127.0.0.1", port=8000, reload=True)
