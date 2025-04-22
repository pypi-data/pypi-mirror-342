from proapi import ProAPI

app = ProAPI(debug=True)

@app.get("/")
def index(request):
    return {"message": "Hello from simple_run.py!"}

# This file will be run with: python -m proapi.run test/simple_run.py
