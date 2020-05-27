# CCHDO_BATS

This is the final project for the 2020 Effective Computing class. 
Project members: Kimberly Gottschalk, Derya Gumustel, Ian Nisbet.

This project is an analysis and visualization of CCHDO BATS (Bermuda Atlantic Time Series) data. 



### Web Scraping

The data_collector.py script requests data directly from: https://cchdo.ucsd.edu/cruise/BIOS20160414. The downloaded data is a .zip file. The program data_collector.py extracts all files to a new subdirectory within the CCHDO_BATS_data directory. The extracted data is a collection of .csv files that each contain depth measurements for a number of variables at a unique point in time. These .csv files can be combined to create a time series analysis. 
