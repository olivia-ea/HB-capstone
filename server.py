"""Server"""

from views import app
# from model import connect_to_db

if __name__ == '__main__':

    app.secret_key = 'SECRETSECRETSECRET'
    app.debug = False
    app.run(host="0.0.0.0")
    # connect_to_db(app)
