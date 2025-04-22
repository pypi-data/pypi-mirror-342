from proapi import ProAPI

app = ProAPI()

@app.get("/")
def index(request):
    return {"message": "Hello, World!"}


app.run(debug=True, port=8000, host="127.0.0.1")