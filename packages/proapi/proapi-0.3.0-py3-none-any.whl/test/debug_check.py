from proapi import ProAPI

# Create app with debug=False
app = ProAPI(debug=False)

# Print initial debug state
print(f"Initial debug state: {app.debug}")

# Override debug in run method
print("Setting debug=True in run method")
app.run(debug=True, port=8000, host="127.0.0.1", use_reloader=False)

# This won't be reached due to the server running
print(f"Final debug state: {app.debug}")
