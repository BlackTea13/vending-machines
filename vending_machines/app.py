from flask import Flask
from vending_machine import vending_machine

app = Flask(__name__)
app.register_blueprint(vending_machine)

@app.route('/', endpoint="home")
def index():
    return "Welcome to the vending machine tracker!"

if __name__ == '__main__':
    app.run(debug=True)
