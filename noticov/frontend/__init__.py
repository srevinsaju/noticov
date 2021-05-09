import os.path

from noticov.app import initialize
from flask import Flask, render_template, jsonify

from noticov.backend.tables import Tables
from noticov.covidstats.countries import Countries

static_folder = os.path.join(os.path.dirname(__file__), "static")
template_folder = os.path.join(os.path.dirname(__file__), "templates")
app = Flask("noticov", static_folder=static_folder, template_folder=template_folder)
ncb = initialize()

default_arguments = {
    "app_name": "noticov",
}


@app.route("/api/in/summary")
def country_summary():
    data = ncb.conn.get_all_covid_data(Tables.INDIA, location=Countries.INDIA.value)
    total_cases = []
    for i in data:
        total_cases.append(i.to_dict())
    print(total_cases)
    return jsonify({"success": True, "data": total_cases})


@app.route("/api/in/top_covid_cases")
def top_covid_cases():
    data = ncb.conn.get_top_covid_cases(Tables.INDIA)
    total_cases = []
    for i in data:
        total_cases.append({"location": i.location, "total_cases": i.total_cases})
    return jsonify({"success": True, "data": total_cases})


@app.route("/api/in/states")
def available_states():
    data = ncb.conn.get_available_states_countries(Tables.INDIA)
    return jsonify({"success": True, "data": data})


@app.route("/")
def main():
    return render_template("index.html", **default_arguments)


if __name__ == "__main__":
    app.run()
