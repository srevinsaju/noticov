import time


class MedicalBedsAvailable:
    def __init__(
            self,
            location: str = None,
            rural_hospitals: int = None,
            rural_beds: int = None,
            urban_hospitals: int = None,
            urban_beds: int = None,
            timestamp: int = None,
    ):
        self.location = location
        self.rural_hospitals = rural_hospitals
        self.rural_beds = rural_beds
        self.urban_hospitals = urban_hospitals
        self.urban_beds = urban_beds
        if timestamp is None:
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp

    def __repr__(self):
        return "MedicalBedsAvailable(location={}, rh={}, rb={}, uh={}, ub={}, timestamp={})".format(
            self.location,
            self.rural_hospitals,
            self.rural_beds,
            self.urban_hospitals,
            self.urban_beds,
            self.timestamp,
        )


class MedicalBedsAvailableList:
    def __init__(self):
        self._list = []

    def push(self, data: MedicalBedsAvailable):
        assert isinstance(data, MedicalBedsAvailable)

        self._list.append(data)

    def pop(self) -> MedicalBedsAvailable:
        return self._list.pop()

    def count(self) -> int:
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def copy(self):
        cdl = MedicalBedsAvailableList()
        cdl._list = self._list.copy()
        return cdl
