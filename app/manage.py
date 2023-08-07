from settings import TEST_MODE, APP_HOST, APP_PORT
from flask_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=TEST_MODE, host=APP_HOST, port=APP_PORT)
