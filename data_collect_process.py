"""
This code is for the final project of the 2020 Effective Computing course at UW. 
This code scrapes BATS data from the web and saves it into a data subdirectory as .csv files. 
This data is then put into a dictionary where the dict key is the filename and the dict value 
is a pandas DataFrames containg data from the corresponding .csv file. 
"""

#imports
import sys, os
import os
from zipfile import ZipFile
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import glob
import numpy as np
import pickle

# local imports
sys.path.append(os.path.abspath('shared'))
import my_module as mymod
from importlib import reload
reload(mymod)

# make sure the output directory exists
try:    # try for Mac OS
    this_dir = os.path.abspath('.').split('/')[-1]
    this_parent = os.path.abspath('.').split('/')[-2]
    out_dir = '../../' + this_parent + '/' + this_dir + '_data'
    print('Creating ' + out_dir + ', if needed \n')
    mymod.make_dir(out_dir)
except:    # default to Windows OS if error occurs above
    this_dir = os.path.abspath('.').split('\\')[-1]
    this_parent = os.path.abspath('.').split('\\')[-2]
    out_dir = '../../' + this_parent + '/' + this_dir + '_data'
    print('Creating ' + out_dir + ', if needed \n')
    mymod.make_dir(out_dir)



# USER INPUT ########################################################

# ask user to select a date
class ValueError(Exception):
    pass

# first select year -- currently only 2016 is functional
print('\nWhat year would you like to look at? \nData is available for:')
print('\n    2016')
year = input('\nYear: ')

# then select month -- only 6 months are available for 2016
if year == '2016':
    print('\nWhat month would you like to look at? \nData is available for:')
    print('\n    03: March          04: April')
    print('\n    06: June           07: July')
    print('\n    11: November       12: December')
    print('\nPlease enter the number corresponding to your month of interest')
    month = input('\nMonth: ')
else:
    raise ValueError('Invalid selection or data unvailable. Please try again.')
    
# then select day -- only a handful of days are available for 2016
# raise errors if user does not select appropriate date
if month == '03':
    print('What cruise start date would you like to look at? \nData is available for:')
    print('\n    08: March 8th \n    23: March 23rd')
    print('\nPlease enter the number corresponding to your date of interest')
    day = input('\nDay: ')
    if day != '08' and day != '23':
        raise ValueError('Invalid selection or data unvailable. Please try again.')
elif month == '04':
    print('What cruise start date would you like to look at? \nData is available for:')
    print('\n    04: April 4th \n    14: April 14th')
    print('\nPlease enter the number corresponding to your date of interest')
    day = input('\nDay: ')
    if day != '04' and day != '14':
        raise ValueError('Invalid selection or data unvailable. Please try again.')
elif month == '06':    # some months only have data from one cruise
    print('\nData is available for June 13th')
    day = '13'
elif month == '07':
    print('\nData is available for July 21st')
    day = '21'
elif month == '11':
    print('\nData is available for November 18th')
    day = '18'
elif month == '12':
    print('\nData is available for December 12th')
    day = '12'

else:    # stop program if user did not select appropriate month
    raise ValueError('Invalid selection or data unvailable. Please try again.')

selection = year + month + day
print('\nYour selection is: ' + year + ' ' + month + ' ' + day)



# DATA COLLECTION ########################################################

# define the desired domain, url, and filetype
DOMAIN = 'https://cchdo.ucsd.edu'
URL = 'https://cchdo.ucsd.edu/cruise/' + selection
FILETYPE = '.zip'

# preemptively define zip_file for file removal later
zip_file = ''

# define function to get text from URL and parse as html
def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')
    
# scrape data from URL
for link in get_soup(URL).find_all('a'):
    file_link = link.get('href')
    if FILETYPE in file_link:    # check text for .zip files
        print('\nCollecting data: ' + file_link)
        with open(link.text, 'wb') as file:
            response = requests.get(DOMAIN + file_link)    # get file
            file.write(response.content)    # write file to machine
            #print(file)
            
            # extract all files from zip_file to a new data subdirectory
            zip_file = file.name
            with ZipFile(zip_file, 'r') as zipObj:
                print('\nExtracting data files to: ' + out_dir + '/' + file.name[:-8])
                zipObj.extractall(out_dir + '/' + file.name[:-8])

# the time selection code will not catch all input errors, so include a raise error here
if os.path.exists(zip_file):    # remove corresponding zip_file if it exists
    os.remove(zip_file)
else:    # stop program if no corresponding exists
    raise ValueError('Invalid selection or data unvailable. Please try again.')



# DATA PROCESSING ########################################################

# define path to extracted data
path = '../CCHDO_BATS_data/BIOS' + selection

# create list of CCHDO BATS file names
csvs = [x for x in os.listdir(path) if x.endswith('.csv')]
fns = [os.path.splitext(os.path.basename(x))[0] for x in csvs]

# glob files
all_files = glob.glob(path + "/*.csv")

# create df for time
li = []

# turn files in pandas dataframes
for filename in all_files:
    df = pd.read_csv(filename, index_col=None,  nrows=8,usecols=[0])
    li.append(df)

# get metadata from header:
# get times
time = pd.concat(li, axis=0, ignore_index=True)
time = time.iloc[5::8, :]
time = time['CTD'].str.extract('(\d+)').astype(int)
# get latitudes
lat = pd.concat(li, axis=0, ignore_index=True)
lat = lat.iloc[6::8, :]
lat = lat['CTD'].str.extract('(\d+)').astype(int)
# get longitudes
lon = pd.concat(li, axis=0, ignore_index=True)
lon = lon.iloc[7::8, :]
lon = lon['CTD'].str.extract('(\d+)').astype(int)

# create df for measurements
li2 = []

# fill dataframe with measurements
for filename in all_files:
    df2 = pd.read_csv(filename, index_col=None,  skiprows=11)
    li2.append(df2)

data = pd.concat(li2, axis=0, ignore_index=True)

# create and fill dictionary for the data
d = {}
for i in range(len(fns)):
    d[fns[i]] = pd.read_csv(path + '/' + csvs[i], skiprows=11)
# create and fill dictionary for the time
d2 = {}
for i in range(len(fns)):
    d2[fns[i]] = pd.read_csv(path + '/' + csvs[i], nrows=8,usecols=[0])

# get list of dict keys
xx = []
for key in d:
    xx.append(key)

# series of data to plot

sal = [None]*len(d)
for i in range(len(d)):
    sal[i]= data.iloc[:len(d[xx[i]]), 2]

temp = [None]*len(d)
for i in range(len(d)):
    temp[i]= data.iloc[:len(d[xx[i]]), 1]
    
oxy = [None]*len(d)
for i in range(len(d)):
    oxy[i]= data.iloc[:len(d[xx[i]]), 3]
    
flo = [None]*len(d)
for i in range(len(d)):
    flo[i]= data.iloc[:len(d[xx[i]]), 5]
    
depth = [None]*len(d)
for i in range(len(d)):
    depth[i]= data.iloc[:len(d[xx[i]]), 0]
    
#sal1 = np.array(sal[0])    # see example salinity data

# save data as pickle files for plotting
f = open('store.pckl', 'wb')
pickle.dump([temp, sal, oxy, flo, depth, time, lat, lon], f)
f.close()

f = open('store.pckl', 'rb')
obj = pickle.load(f)
f.close()

print('\nReady to plot.')