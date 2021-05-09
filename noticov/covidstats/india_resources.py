import requests

from noticov.covidstats.base import BaseCovidApi
from noticov.covidstats.countries import Countries
from noticov.covidstats.data import MedicalBedsAvailable, MedicalBedsAvailableList
from noticov.covidstats.exceptions import ApiEndpointFailed


class IndiaResourcesDistrictsCovidApi(BaseCovidApi):
    location = Countries.INDIA
    canonical_url = "https://api.rootnet.in/covid19-in/hospitals/beds"

    def get_data(self) -> MedicalBedsAvailableList:
        _data = requests.get(self.canonical_url).json()

        if not _data.get("success"):
            # the data was not successfully scraped
            raise ApiEndpointFailed

        _data = _data.get("data")
        covid_data_list = MedicalBedsAvailableList()
        regional_data = _data.get("regional")
        assert isinstance(regional_data, list)

        # loop through all regions
        for region in regional_data:
            cd = MedicalBedsAvailable(
                location=region.get("state"),
                rural_hospitals=region.get("ruralHospitals"),
                rural_beds=region.get("ruralBeds"),
                urban_beds=region.get("urbanBeds"),
                urban_hospitals=region.get("urbanHospitals"),
            )
            covid_data_list.push(cd)

        cd = MedicalBedsAvailable(
            location=Countries.INDIA.value,
            rural_hospitals=_data["summary"].get("ruralHospitals"),
            rural_beds=_data["summary"].get("ruralBeds"),
            urban_beds=_data["summary"].get("urbanBeds"),
            urban_hospitals=_data["summary"].get("urbanHospitals"),
        )
        covid_data_list.push(cd)
        return covid_data_list
