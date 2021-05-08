import requests

from noticov.covidstats.base import BaseCovidApi
from noticov.covidstats.countries import Countries
from noticov.covidstats.data import CovidDataList, CovidData
from noticov.covidstats.exceptions import ApiEndpointFailed


class IndiaDistrictsCovidApi(BaseCovidApi):
    location = Countries.INDIA
    canonical_url = "https://api.rootnet.in/covid19-in/stats/latest"

    def get_data(self) -> CovidDataList:
        _data = requests.get(self.canonical_url).json()

        if not _data.get("success"):
            # the data was not successfully scraped
            raise ApiEndpointFailed

        _data = _data.get("data")
        covid_data_list = CovidDataList()
        regional_data = _data.get("regional")
        assert isinstance(regional_data, list)

        # loop through all regions
        for region in regional_data:
            cd = CovidData(
                location=region.get("loc"),
                discharged=region.get("discharged"),
                deaths=region.get("deaths"),
                total_cases=region.get("totalConfirmed"),
            )
            covid_data_list.push(cd)

        return covid_data_list
