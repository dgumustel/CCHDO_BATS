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
import argparse

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

# create the parser object
parser = argparse.ArgumentParser()

print('\nWhat year would you like to look at? (enter an integer)')
year = input('\nYear: ')
print('\nWhat month would you like to look at? (enter an integer)')
month = input('\nMonth: ')
print('\nWhat day would you like to look at? (enter an integer)')
day = input('\nDay: ')

selection = year + month + day
print('\nYour selection is: ' + selection)

class ValueError(Exception):
    pass

# DATA COLLECTION

# define desired URL and filetype
DOMAIN = 'https://cchdo.ucsd.edu'
URL = 'https://cchdo.ucsd.edu/cruise/' + selection
FILETYPE = '.zip'

# function to get text from URL and parse as html
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
            print(file)
            
            # extract all files from .zip to a new data directory
            zip_file = file.name
            with ZipFile(zip_file, 'r') as zipObj:
                zipObj.extractall(out_dir + '/' + file.name[:-8])
    #else:
      #  raise ValueError('Invalid input for time period')

path = '../CCHDO_BATS_data/BIOS' + selection

# Create list of CCHDO BATS file names
csvs = [x for x in os.listdir(path) if x.endswith('.csv')]
fns = [os.path.splitext(os.path.basename(x))[0] for x in csvs]



## imprt the csv files
import glob
#path = '../CCHDO_BATS_data/BIOS20160414/' # use your path
all_files = glob.glob(path + "/*.csv")

## Create df for time
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None,  nrows=8,usecols=[0])
    li.append(df)

# time
time = pd.concat(li, axis=0, ignore_index=True)
time = time.iloc[5::8, :]
time = time['CTD'].str.extract('(\d+)').astype(int)
# latitde
lat = pd.concat(li, axis=0, ignore_index=True)
lat = lat.iloc[6::8, :]
lat = lat['CTD'].str.extract('(\d+)').astype(int)
# longitude
lon = pd.concat(li, axis=0, ignore_index=True)
lon = lon.iloc[7::8, :]
lon = lon['CTD'].str.extract('(\d+)').astype(int)


## Create df for other data
li2 = []

for filename in all_files:
    df2 = pd.read_csv(filename, index_col=None,  skiprows=11)
    li2.append(df2)

data = pd.concat(li2, axis=0, ignore_index=True)



# Dictionary for the data
d = {}
for i in range(len(fns)):
    d[fns[i]] = pd.read_csv(path + '/' + csvs[i], skiprows=11)
# Dictionary for the time
d2 = {}
for i in range(len(fns)):
    d2[fns[i]] = pd.read_csv(path + '/' + csvs[i], nrows=8,usecols=[0])

# list of dict keys
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
    
