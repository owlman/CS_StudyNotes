from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world() -> str:
    return 'Hello, World!'

def say_hello() -> None:
    print("Hello, World!")

def main() -> None:
    app.run()

if __name__ == '__main__':
    # say_hello()
    app.run(debug=True)
    
