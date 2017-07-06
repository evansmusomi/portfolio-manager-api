""" Flask API definition """

from routes import init_api_routes
from routes import init_website_routes
from routes import init_error_handlers

from flask import Flask

# create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "You'll never guess :)"

# define routes
init_api_routes(app)
init_website_routes(app)
init_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True)
