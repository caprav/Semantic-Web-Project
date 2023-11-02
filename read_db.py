from   flask_migrate import Migrate 
from   flask_minify  import Minify
from flask import Flask
from apps.config import config_dict
from apps import create_app, db
from apps import Users  # Import the Users model


# ...

# WARNING: Don't run with debug turned on in production!
DEBUG =  'True'

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


# Create the Flask app instance
app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

# Define a route to view and print Users data on the backend
@app.route('/view_users', methods=['GET'])
def view_users():
    with app.app_context():
        users = Users.query.all()  # Query all users from the "Users" table
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
        return "User data printed on the backend"  # Return a message indicating the data was printed

if __name__ == "__main__":
    app.run()
