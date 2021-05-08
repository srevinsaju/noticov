import requests

from noticov.covidstats.base import BaseCovidApi
from noticov.covidstats.countries import Countries


class IndiaDistrictsCovidApi(BaseCovidApi):
    location = Countries.INDIA
    canonical_url = "https://api.rootnet.in/covid19-in/stats/latest"

    def get_data(self):
        requests.get(self.canonical_url).json()
