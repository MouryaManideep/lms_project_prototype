class Config:
    """Configuration for the Flask app.

    Keep secrets out of source control in real projects.
    """

    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///lms.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False