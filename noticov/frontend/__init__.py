import os.path

from flask import Flask, render_template


static_folder = os.path.join(os.path.dirname(__file__), "static")
template_folder = os.path.join(os.path.dirname(__file__), "templates")
app = Flask("noticov", static_folder=static_folder, template_folder=template_folder)


default_arguments = {
    "app_name": "noticov",
}

@app.route("/")
def main():
    return render_template(
        "index.html",

        **default_arguments
    )


if __name__ == "__main__":
    app.run()
