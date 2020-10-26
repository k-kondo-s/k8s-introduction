from flask import Flask
import uuid

app = Flask(__name__)
id = str(uuid.uuid1()) + '-v1.0.1\n'


@app.route('/')
def get():
    return id


@app.route('/readiness')
def readiness():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
