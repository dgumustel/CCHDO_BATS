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

# identify data directory
data_dir = '../' + this_parent + '/' + this_dir + '_data/'



# DATA COLLECTION

# define desired URL and filetype
DOMAIN = 'https://cchdo.ucsd.edu'
URL = 'https://cchdo.ucsd.edu/cruise/BIOS20160414'
FILETYPE = '.zip'

# function to get text from URL and parse as html
def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')
    
# scrape data from URL
for link in get_soup(URL).find_all('a'):
    file_link = link.get('href')
    if FILETYPE in file_link:    # check text for .zip files
        print('collecting data: ' + file_link)
        with open(link.text, 'wb') as file:
            response = requests.get(DOMAIN + file_link)    # get file
            file.write(response.content)    # write file to machine
            
            # extract all files from .zip to a new data directory
            zip_file = file.name
            with ZipFile(zip_file, 'r') as zipObj:
                zipObj.extractall(out_dir + '/' + file.name[:-8])



# DATA PROCESSING

# Create list of CCHDO BATS file names
csvs = [x for x in os.listdir('../CCHDO_BATS_data/BIOS20160414/') if x.endswith('.csv')]
fns = [os.path.splitext(os.path.basename(x))[0] for x in csvs]

# Dictionary for the data
d = {}
for i in range(len(fns)):
    d[fns[i]] = pd.read_csv('../CCHDO_BATS_data/BIOS20160414/' + csvs[i], skiprows=11)
    
# Dictionary for the time

d2 = {}
for i in range(len(fns)):
    d2[fns[i]] = pd.read_csv('../CCHDO_BATS_data/BIOS20160414/' + csvs[i], nrows=8,usecols=[0])


#############

# get raw data of one file
a = d.get('BIOS20160414_10323001_ct1')

# get one column of file
b = a['DBAR']

# create empty dataframe for times
df_ = pd.DataFrame(columns=["Time"])

ff = pd.DataFrame.from_dict(d2,orient='index',columns=['A'])

time = d2.get('BIOS20160414_10323001_ct1')

#time = time['CTD'].str.extract('(\d+)').astype(int)
#time = time.loc[5,]

