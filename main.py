from flask import Flask
from waitress import serve
import test
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.register_blueprint(test.blueprint)
    #serve(app, host='127.0.0.1', port=5000)
    app.run()



if __name__ == '__main__':
    main()