"""Application runner.

This module imports the app factory and runs the development server.
In production you would use a WSGI server instead of this file.
"""

from app import create_app

app = create_app()

# Note: when running directly, this starts Flask's built-in server.
app.run(debug=True, use_reloader=False)