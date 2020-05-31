#imports
import sys, os
import os
from zipfile import ZipFile
import pandas as pd

# local imports
sys.path.append(os.path.abspath('shared'))
import my_module as mymod
from importlib import reload
reload(mymod)

# make sure the output directory exists
try:
    this_dir = os.path.abspath('.').split('/')[-1]
    this_parent = os.path.abspath('.').split('/')[-2]
    out_dir = '../../' + this_parent + '/' + this_dir + '_data'
    print('Creating ' + out_dir + ', if needed \n')
    mymod.make_dir(out_dir)
except:
    this_dir = os.path.abspath('.').split('\\')[-1]
    this_parent = os.path.abspath('.').split('\\')[-2]
    out_dir = '../../' + this_parent + '/' + this_dir + '_data'
    print('Creating ' + out_dir + ', if needed \n')
    mymod.make_dir(out_dir)

# access the data
data_dir = '../' + this_parent + '/' + this_dir + '_data/'


from bs4 import BeautifulSoup as bs
import requests

DOMAIN = 'https://cchdo.ucsd.edu'
URL = 'https://cchdo.ucsd.edu/cruise/BIOS20160414'
FILETYPE = '.zip'

def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')
    
for link in get_soup(URL).find_all('a'):
    file_link = link.get('href')
    if FILETYPE in file_link:
        print(file_link)
        print('working')
        with open(link.text, 'wb') as file:
            response = requests.get(DOMAIN + file_link)
            file.write(response.content)
            zip_file = file.name
            with ZipFile(zip_file, 'r') as zipObj:
                zipObj.extractall(out_dir + '/' + file.name[:-8])

# Create list of CCHDO BATS file names
csvs = [x for x in os.listdir('../CCHDO_BATS_data/BIOS20160414/') if x.endswith('.csv')]
fns = [os.path.splitext(os.path.basename(x))[0] for x in csvs]



## imprt the csv files
import glob
path = '../CCHDO_BATS_data/BIOS20160414/' # use your path
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
    d[fns[i]] = pd.read_csv('../CCHDO_BATS_data/BIOS20160414/' + csvs[i], skiprows=11)
# Dictionary for the time
d2 = {}
for i in range(len(fns)):
    d2[fns[i]] = pd.read_csv('../CCHDO_BATS_data/BIOS20160414/' + csvs[i], nrows=8,usecols=[0])

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
    
    
