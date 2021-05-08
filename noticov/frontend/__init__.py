from flask import Flask


app = Flask("noticov")


@app.route("/")
def main():
    return "Hello World"


if __name__ == "__main__":
    app.run()
