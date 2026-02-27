"""Application runner.

This module imports the app factory and runs the development server.
In production you would use a WSGI server instead of this file.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()