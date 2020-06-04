"""
This code is for the final project of the 2020 Effective Computing course at UW. 
This code scrapes BATS data from the web and saves it into a data subdirectory as .csv files. 
This data is then put into a dictionary where the dict key is the filename and the dict value 
is a pandas DataFrames containg data from the corresponding .csv file. 
"""

# packages to install:
# basemap: conda install -c anaconda basemap
# basemap highres: conda install -c conda-forge basemap-data-hires
# gsw teos10: conda install -c conda-forge gsw
# cmocean: conda install -c conda-forge cmocean
# remember to restart ipython after install to initialize 


#imports
import sys, os
from zipfile import ZipFile
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import glob
import numpy as np
import pickle
import cmocean
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import gsw
from matplotlib.ticker import MaxNLocator

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
path = out_dir + '/BIOS' + selection

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
    
#sal1 = np.array(sal[0])    # example of indexing salinity data

# save data as pickle files just in case
f = open('store.pckl', 'wb')
pickle.dump([temp, sal, oxy, flo, depth, time, lat, lon], f)
f.close()


print('\nReady to plot.')


# Plotting ########################################################

##make bathy map of BATS study area, Note: -180 t0 180
print('Making Map of BATS study area')
plt.figure(1)
m = Basemap(width=1000000,height=1000000,projection='lcc',
            resolution='h',lat_1=31,lat_2=33,lat_0=32,lon_0=-64.5)
im = m.etopo()
cb = m.colorbar(im,location='right',pad='10%')
#scatter plot lons and lat coordinates on top of bathy
lon_plot=lon.to_numpy() 
lat_plot=lat.to_numpy()
x, y = m(-lon_plot,lat_plot)
m.scatter(x,y,c='k',s=50,marker='*')
# meridians on bottom and left
parallels = np.arange(0.,81,2.)
# labels = [left,right,top,bottom]
m.drawparallels(parallels,labels=[True,False,True,True])
meridians = np.arange(5.,351.,2.)
m.drawmeridians(meridians,labels=[False,False,False,True])
plt.title('BATS Study Area')
plt.show()

plt.savefig('Bat_Map.png')

print('Question for the class: how do you add a colorbar to a basemap background graphics object?')


## Needs to be updated one CTDPRS variable added to processing

# PLOT 1 - T/S 

print('Plotting T/S')
plt.figure(2)

# plot t/s
didx=len(depth)

# to use gsw - must be numpy array

sal_s = np.asarray(sal[0])
depth_s = np.asarray(depth[0])
didx=len(depth_s)-1
depth_s=depth_s[:didx]
sal_s=sal_s[:didx]
depth_s = depth_s.astype(np.float)
temp_s = np.asarray(temp[0])
temp_s=temp_s[:didx]
oxy_s=np.asarray(oxy[0])
flo_s=np.asarray(flo[0])
flo_s=flo_s[:didx]
oxy_s=oxy_s[:didx]


SA=gsw.SA_from_SP(sal_s,depth_s,lon_plot[0],lat_plot[0])

CT=gsw.CT_from_t(SA,temp_s,depth_s)


#CT_5mean=np.mean(CT)
#SA_5mean=np.mean(SA)


# plot T/S diagram - altered from example from https://medium.com@hafezahmad/making-#temperature-salinity-diagrams-called-the-t-s-diagram-with-python-and-r-#programming-5deec6378a29

mint=np.min(CT)
maxt=np.max(CT)
mins=np.min(SA)
maxs=np.max(SA)
tempL=np.linspace(mint-1,maxt+1,len(SA))
salL=np.linspace(mins-1,maxs+1,len(SA))

Tg, Sg = np.meshgrid(tempL,salL)
sigma_theta = gsw.sigma0(Sg, Tg)
cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),len(SA))
fig,ax=plt.subplots(figsize=(10,10))
cs = ax.contour(Sg, Tg, sigma_theta,colors='grey',zorder=1)
cl=plt.clabel(cs,fontsize=10)
#sc=plt.scatter(SA_5_day_mean,CT_5_day_mean,c=cnt)
sc=plt.scatter(SA,CT,c=cnt)
cb=plt.colorbar(sc)
cb.set_label('Density')
plt.xlabel('Salinity A')
plt.ylabel('Conservative Temperature')
plt.title('T-S at BATS at T={}'.format(selection))')
cb.set_label('Density')
plt.show()

plt.savefig('T_S_plot.png')

##
print('Property Plots Coming Up')
#plt.figure(3)

#plt.subplots(1,4,sharey=True)
fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(nrows=1, ncols=4, sharex=False, sharey=True)

ax1.grid(True)
ctm= ax1.scatter(CT,-depth_s,c=CT,cmap=cmocean.cm.thermal);
ax1.set_xlabel('CT')
#ax1.set_xticks(np.arange(min(CT),max(CT), step=1))
fig.colorbar(ctm, ax=ax1)

sam=ax2.scatter(SA,-depth_s,c=SA,cmap=cmocean.cm.haline)
ax2.set_xlabel('SA')
ax2.grid(True)
#ax2.set_xticks(np.arange(min(SA),max(SA), step=0.5))
fig.colorbar(sam, ax=ax2)

oxm=ax3.scatter(oxy_s,-depth_s,c=oxy_s,cmap=cmocean.cm.oxy)
ax3.set_xlabel('Oxygen')
ax3.grid(True)
ax3.set_xticks(np.arange(min(oxy_s),max(oxy_s), step=10))
fig.colorbar(oxm, ax=ax3)

flm=ax4.scatter(flo_s,-depth_s,c=flo_s,cmap=cmocean.cm.algae)
ax4.set_xlabel('Fluorescence')
ax4.grid(True)
ax4.set_xticks(np.arange(min(flo_s),max(flo_s), step=0.1))
fig.colorbar(flm, ax=ax4)

ax1.set_ylabel('Depth (dbar)')
fig.title('Properties at T={}'.format(selection))')

plt.show()

plt.savefig('prop_plots.png')



## Subplots of contoured properties v time # so, I took this out for now but would like to add back in at some point in time. 

#print('Property Plots Over Time are Next')
#plt.figure(4)

#calculate MLD - apparently this doesn't exist for the python gsw
#mld=gsw.mlp(SA,CT,depth)

#plt.subplots(4,1,sharex=True)

#time_s=time.to_numpy()
#ax1=subplot(411)
#plt.contourf(time, depth_s, CT, alpha=0.7,cmap=cmocean.cm.thermal);
#plt.contour(time,depth,mld,linestyle=dash,linecolor=white)
#plt.setp(ax1.get_xticklabels(), fontsize=6)
#cb=plt.colorbar(CT)
#cb.set_label('CT')

#ax2=subplot(412,sharex=ax1)
#plt.contourf(time,depth_s,SA,alpha=20, cmap=cmocean.cm.haline)
#plt.setp(ax2.get_xticklabels(), visible=False)
#cb=plt.colorbar(SA)
#cb.set_label('SA')

#ax3=subplot(413,sharex=ax1)
#plt.contourf(time,depth_s,oxy_s,alpha=20, cmap=cmocean.cm.oxy)
#plt.setp(ax3.get_xticklabels(), visible=False)
#cb=plt.colorbar(oxy)
#cb.set_label('Oxygen')

#ax4=subplot(414,sharex=ax1)
#plt.contourf(time,depth_s,flo_s,alpha=.7,cmap=cmocean.cm.algae)
#plt.setp(ax4.get_xticklabels(), fontsize=12, visible=True)
#plt.show()
#cb=plt.colorbar(flo)
#cb.set_label('Fluorescence')

#plt.xlabel('Time')
#plt.ylabel('Depth (dbar)')

##refs
#https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.subplot.html
#https://matplotlib.org/3.1.1/tutorials/introductory/customizing.html?#highlight=contour.negative_linestyle#a-sample-matplotlibrc-file
#https://matplotlib.org/basemap/users/examples.html#
#https://medium.com/@hafezahmad/making-temperature-salinity-diagrams-called-#the-t-s-diagram-with-python-and-r-programming-5deec6378a29
#https://oceanpython.org/2013/02/17/t-s-diagram/
