import requests
import json
import pickle

class GetRasterExecutor():
    def __init__(
            self, 
            variable: str, 
            start_datetime: str,
            end_datetime: str,
            temporal_resolution: str,
            min_lat: float,
            max_lat: float,
            min_lon: float,
            max_lon: float,
            spatial_resolution: float,
            aggregation,
    ):
        #super().__init__()
        self.variable = variable
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.temporal_resolution = temporal_resolution
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.spatial_resolution = spatial_resolution
        self.aggregation = aggregation
      

    def execute(self):
        form_data = {
            "requestType": "",
            "variable": self.variable,  
            "startDateTime": self.start_datetime,
            "endDateTime": self.end_datetime,
            "temporalResolution": self.temporal_resolution,
            "north": self.max_lat,
            "south": self.min_lat,
            "east": self.max_lon,
            "west": self.min_lon,
            "spatialResolution": self.spatial_resolution,
            "aggregation": self.aggregation
        }

        url = "https://iharpv-dev.cs.umn.edu/api/query_pickle/"
    
        response = requests.post(
            url = url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(form_data),
            verify=False
            )
        

        if response.status_code == 201:
            binary_data = response.content
            ds = pickle.loads(binary_data)
            # print(">>> data is:", type(ds))
            # print(ds)
            return ds
        else:
            print("Error:", response.status_code)
            return None