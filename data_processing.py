# Import file 
import os
import pandas as pd
import sys                 # directory opperations
                           # Custom packages 
    
    
sys.path.append(os.path.join(sys.path[0],'modules'))

import CTire_standardization as CT_S

# here we load the dataset. We can load the sheet names:
# Y dataset.load_detail
# Y dataset.origin
# Y dataset.destination
# dataset.reason 
dataset = CT_S.dataset()





"""
Making data structures for the additional-information sheets
"""
# _________ ORIGIN DATA ________
CT_Dat = dict()
origin_len = len(dataset.origin)
orig_loc = {}

for i in range(0,origin_len):
    loc_key    = dataset.origin.iloc[i]['DC #']
    loc_city   = dataset.origin.iloc[i]['City']
    loc_prov   = dataset.origin.iloc[i]['Prov']
    loc_search = loc_city + ' ' + loc_prov
    orig_loc[loc_key] = loc_search

# _________ DESTINATION DATA ________
dest_len = len(dataset.destination)
dest_loc = {}
    
for i in range(0,dest_len):
    loc_key    = dataset.destination.iloc[i]['Store #']
    loc_city   = dataset.destination.iloc[i]['CITY']
    loc_prov   = dataset.destination.iloc[i]['PROV']
    loc_search = loc_city + ' ' + loc_prov
    dest_loc[loc_key] = loc_search

# _________ REASON DATA ________       
reas_len = len(dataset.reason)
reas_loc = {}
    
for i in range(0,reas_len):
    reas_key    = dataset.reason.iloc[i]['Reason Code']
    reas_code   = dataset.reason.iloc[i]['Reason Code Category']
    reas_loc[reas_key] = reas_code





late_count = 0

for i in range(0,len(dataset.load_detail)): 
    print(i)
    orig_search     = dataset.load_detail.iloc[i]['DC #']
    dest_search     = dataset.load_detail.iloc[i]['Store #']
    origin          = orig_loc[orig_search]
    destin          = dest_loc[dest_search]
    Standard        = CT_S.Standard(origin,destin)
    reas_str        = dataset.load_detail.iloc[i]['Reason Code']   
    if reas_str in reas_loc.keys():
        reas_cod    = reas_loc[reas_str]
    else:
        reas_cod    = 'NA'
    min_late        = dataset.load_detail.iloc[i]['Minutes Late']
    per_late        = min_late/Standard.d
    
    if per_late > 0: 
        late_count += 1

    CT_Dat[i] = {
        'ID'                : dataset.load_detail.iloc[i]['Load #'],
#    'Origin'            : dataset.load_detail.iloc[i]['DC #'],
        'Origin'            : origin,
#    'Destination'       : dataset.load_detail.iloc[i]['Store #'],
        'Destination'       : destin,
        'Distance'          : Standard.d,
        'Late_min'          : min_late,
        'Late_min_per_100km': per_late * 100,
        'Orig_city (DC)'    : dataset.load_detail.iloc[i]['DC #'],
        'Dest_city (DC)'    : dataset.load_detail.iloc[i]['Store #'],
        'Arrival_Plan'      : dataset.load_detail.iloc[i]['Original Plan Arrival'],
        'Arrival_Actual'    : dataset.load_detail.iloc[i]['Actual Arrival'],
        'Reason_str'        : reas_str,
        'Reason_cat'        : reas_cod,
        'Comments'          : dataset.load_detail.iloc[i]['Comments'],
    }
    
return CT_Dat






