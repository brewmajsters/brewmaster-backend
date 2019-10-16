"""App entry point."""
from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config['SERVER_HOST'])