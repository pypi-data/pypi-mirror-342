from proapi import ProAPI, session, render, redirect, jsonify, request

app = ProAPI(enable_sessions=True, session_secret_key="test-secret-key")

@app.get("/")
async def index():
    return await render("index.html")

@app.get("/about")
async def about():
    return jsonify({"message": "Hello World!"})

@app.get("/policy")
async def policy():
    return {
        "title": "Privacy Policy",
        "content": "<p>This is a sample privacy policy.</p>"}

@app.get("/login")
async def login():
    return await render("login.html")

@app.post("/login")
async def login_submit():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "password":
        session["username"] = username
        return redirect("/admin")
    else:
        return await render("login.html", error="Invalid credentials")

@app.get("/admin")
async def admin():
    if "username" not in session:
        return redirect("/login")

    return await render("admin.html", username=session["username"])

@app.get("/logout")
async def logout():
    # Clear the session
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
