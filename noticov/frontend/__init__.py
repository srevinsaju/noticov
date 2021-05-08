from flask import Flask


app = Flask("noticov")


@app.route("/")
def main():
    pass


if __name__ == "__main__":
    app.run()
