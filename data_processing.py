# Import file 
import os
import pandas as pd
import sys                 # directory opperations
from time import sleep
                           # Custom packages 
    
    
sys.path.append(os.path.join(sys.path[0],'modules'))

import CTire_standardization as CT_S
import geopy
from geopy.geocoders import Nominatim            

# here we load the dataset. We can load the sheet names:
# Y dataset.load_detail
# Y dataset.origin
# Y dataset.destination
# dataset.reason 


dataset = CT_S.dataset()


"""
Making data structures for the additional-information sheets
"""
CT_Data = {}
# _________ ORIGIN DATA ________
def org_gen(origin=dataset.origin):
	origin_len = len(origin)
	orig_loc = {}
	geolocator      = Nominatim(user_agent="Thomas_Kosciuch") 

	for i in range(0,origin_len):
		sleep(2)
		loc_key    = origin.iloc[i]['DC #']
		loc_city   = origin.iloc[i]['City']
		loc_prov   = origin.iloc[i]['Prov']
		loc_search = loc_city + ' ' + loc_prov + ' Canada'
		j = 0
		k = 0
		while j == 0 and k < 100:   
			try:
				lat_lon    = geolocator.geocode(loc_search)
				j = 1
				print('succ: ', loc_search)
			except:
				k          += 1
				lat_lon    = (0,0)
				if k == 100: 
					print('fail:  ', loc_search)
		orig_loc[loc_key] = lat_lon
	return orig_loc

	# _________ DESTINATION DATA ________
def des_gen(destination=dataset.destination):
	dest_len = len(destination)
	dest_loc = {}
	geolocator      = Nominatim(user_agent="Thomas_Kosciuch") 
	for i in range(0,dest_len):
		sleep(1)   ### requir sleep for http://wiki.openstreetmap.org/wiki/Nominatim_usage_policy
		loc_key    = destination.iloc[i]['Store #']
		loc_city   = destination.iloc[i]['CITY']
		loc_prov   = destination.iloc[i]['PROV']
		loc_search = loc_city + ' ' + loc_prov + ' Canada'
		j = 0
		k = 0
		while j == 0 and k < 100:                                                  
			try:                                                                
				lat_lon    = geolocator.geocode(loc_search)                     
				j = 1
				print("succ: ", loc_search)
			except:                                                             
				k          += 1        
				lat_lon     = (0,0)
				if k == 100:
					print('fail ', loc_search)
		dest_loc[loc_key] = lat_lon
	return dest_loc
# _________ REASON DATA ________       
def rea_gen(reason = dataset.reason):
	reas_len = len(reason)
	reas_loc = {}
	for i in range(0,reas_len):
		reas_key    = reason.iloc[i]['Reason Code']
		reas_code   = reason.iloc[i]['Reason Code Category']
		reas_loc[reas_key] = reas_code
	return reas_loc







