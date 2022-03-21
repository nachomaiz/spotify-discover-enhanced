from app.scripts.dev import register_environment_variables

register_environment_variables()

from app import app

if __name__ == "__main__":
    app.run(debug=True)
