import pandas as pd
import geopy     
# required for city conversion
from geopy.geocoders import Nominatim

class dataset:
    """
    This loads all of the data, and merges it into a helpful data structure. First I load
    the datasheet. 
    
    """

    #__ Class variables __#

    # __ Constructor __ #
    def __init__(self):  
        xlsx_file = pd.ExcelFile("CTC.xlsx")
        dfs = {sheet_name: xlsx_file.parse(sheet_name) 
        for sheet_name in xlsx_file.sheet_names}
    
        self.load_detail = dfs['Load Detail']
        self.origin      = dfs['Origin DC Location']
        self.destination = dfs['Destination Store Location']
        self.reason      = dfs['Reason Codes']

        
class Standard:
    #import math

    """
        STANDARDIZATION
      [5 minutes late on a 1h journey] <(less punctual than)< [30 minutes late on a 10h]
      Therefore it is misleading to view the time late in isolation.
      The first thing that we must do is compare apples to apples.
      
      __PROBLEM__
      There is no data for the duration of the trip
      __SOLUTION__
      We can use the cities as a distance and divide the time late by the z-score of the trip distance.
      further reading on z-scores: __________________________________________________
    """
    
    def __init__(self, city_a, city_b):
        import math
        self.city_a     = city_a
        self.city_b     = city_b
        geolocator      = Nominatim(user_agent="thomas_jaroslaw_kosciuch")
        try: 
            self.lat_long_a = geolocator.geocode(city_a)[1]
        except:
            self.lat_long_a = (0,0)
        try:
            self.lat_long_b = geolocator.geocode(city_b)[1]
        except:
            self.lat_long_b = (0,0)

        lat_a   =  self.lat_long_a[0]
        lat_b   =  self.lat_long_b[0]
        lon_a   =  self.lat_long_a[0]
        lon_b   =  self.lat_long_b[0]
        d_lat   = (lat_b - lat_a) * 110.574            # distance per lat
        d_lon   = 111.320* math.cos(lon_b - lon_a)   # distance for lon
        # a^2 + b^2 = c^2
        # for simplicity assume that world is a circle and that all roads are direct
        
        d_diff  = math.sqrt(d_lat**2 + d_lon**2)
        self.d  = d_diff    
