import os.path

from noticov.app import initialize
from flask import Flask, render_template, jsonify


static_folder = os.path.join(os.path.dirname(__file__), "static")
template_folder = os.path.join(os.path.dirname(__file__), "templates")
app = Flask("noticov", static_folder=static_folder, template_folder=template_folder)
ncb = initialize()

default_arguments = {
    "app_name": "noticov",
}


@app.route("/api/top_covid_cases")
def top_covid_cases():
    ncb.conn.get()
    return jsonify({
        "success": True,
        "data": data
    })


@app.route("/")
def main():
    return render_template(
        "index.html",

        **default_arguments
    )


if __name__ == "__main__":
    app.run()
