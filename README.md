# CCHDO_BATS

This is the final project for the 2020 Effective Computing class. 

Project members: Kimberly Gottschalk, Derya Gumustel, Ian Nisbet.

This project involves scraping data from the web, saving the data as .zip files, extracting the data files to a data subdirectory, and visualizing the data in informative plots. Our data source is the CCHDO BATS (Bermuda-Atlantic Time Series) data (found here: https://cchdo.ucsd.edu/search?q=BATS+timeseries). This data includes depth profiles of multiple seawater parameters, such as temperature, salinity, and dissolved oxygen. 

The code in this repo performs three major tasks based on user inputs: web scraping, processing, and plotting. The user is prompted to choose from a selection of dates for which data is available. After entering a selection, the code scrapes data from web, processes data into pandas dataframes, and creates informative plots including a map of the data collection location, plots of depth profiles for each variable, and a temperature-salinity diagram.  

### User Requirements

Install the following python packages before running the code:

beautifulsoup: conda install -c anaconda beautifulsoup4

requests: conda install -c anaconda requests

basemap: conda install -c anaconda basemap

basemap high resolution data: conda install -c conda-forge basemap-data-hires

gsw teos10: conda install -c conda-forge gsw

cmocean: conda install -c conda-forge cmocean


# Running the code

### User inputs

The code will prompt the user for a month and date according to data availability for the year 2016. 
Available months are presented to the user. If a month has multiple days of available data then the 
user is provided options and prompted to select a date for data scraping. If a month only has one 
day of available data then that day is automatically selected for data scraping. 

### Web Scraping

The data gathering section of the code requests data directly from: https://cchdo.ucsd.edu/cruise/BIOSYYYYMMDD 
where the YYYYMMDD is the user input (see above). The data is downloaded as a .zip file. The code 
then extracts all zipped files to a new data subdirectory named BIOSYYYYMMDD located within a data 
directory parallel to (on the same level as) the code directory. The extracted data is a collection 
of .csv files that each contain depth measurements for several variables at a unique point in time. 
These .csv files can be combined to create a time series analysis. 

### Data Processing

The data files are opened and transformed into a number of pandas dataframes contained within a data 
dictionary. The header information (metadata) of each file is stored in a separate dictionary.

### Data Visualization 

The latitude and longitude coordinates of the data collection site are mapped on a bathymetric plot 
of the Bermuda-Atlantic region. Currently, only data from one .csv file is plotted. The temperature 
and salinity are used to generate a temperature-salinity diagram. Depth profiles of 
conservative temperature (calculated from salinity and temperature), salinity, dissolved oxygen, 
and fluorescence are plotted with appropriate oceanographic colormaps from the cmocean package. 


### What to do next

This code could be greatly improved by expanding the acceptable user inputs in the web scraping section 
to allow users to access all of the BATS data. Currently, the code only accepts data selection for the 
year 2016. 

This code could also be editted to accept user inputs for plot generation. Currently, multiple plots 
are generated automatically. User input could be used to limit the plotting to only desired plots. 

In addition, this code does not currently take advantage of the time-series aspect of the BATS data 
collection. This code visualizes data from a singular point in time, but could be expanded to 
generate informative time series visualizations of measured and calculated variables. 


### Resources 

The following resources were used in writing this code:

https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.subplot.html

https://matplotlib.org/3.1.1/tutorials/introductory/customizing.html?#highlight=contour.negative_linestyle#a-sample-matplotlibrc-file

https://matplotlib.org/basemap/users/examples.html

https://medium.com/@hafezahmad/making-temperature-salinity-diagrams-called-#the-t-s-diagram-with-python-and-r-programming-5deec6378a29

https://oceanpython.org/2013/02/17/t-s-diagram/

