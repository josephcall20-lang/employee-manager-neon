"""Initialize the database tables on the configured DATABASE_URL.

Run this script once after setting the DATABASE_URL and SECRET_KEY in your `.env` file.
This will create all SQLAlchemy tables defined across the application.
"""

from index import create_app, db


def main() -> None:
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")


if __name__ == "__main__":
    main()