from flask import Flask
from flask import abort

app = Flask(__name__)


@app.route('/')
def index():
    abort(405)
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
