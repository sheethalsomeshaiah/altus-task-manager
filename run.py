from app import create_app
import os
import dotenv

dotenv.load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config.get("DEBUG"), port=app.config.get("PORT"))