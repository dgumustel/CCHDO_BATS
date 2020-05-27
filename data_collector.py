#imports
import sys, os
import os
from zipfile import ZipFile

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

        