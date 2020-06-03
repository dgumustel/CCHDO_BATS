#download

# basemap: conda install -c anaconda basemap
# basemap highres: conda install -c conda-forge basemap-data-hires
# gsw teos10: To install with Anaconda: conda install -c conda-forge cmocean
#remember to restart ipython after install to initialize 


#imports
import sys as sys
import cmocean
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gsw
from matplotlib.ticker import MaxNLocator

# what variables do you have



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

print('Question for the class: how do you add a colorbar to a basemap background graphics object?')


## Needs to be updated one CTDPRS variable added to processing

# PLOT 1 - T/S 

print('Plotting T/S')
plt.figure(2)

# plot t/s
didx=len(depth)

# to use gsw - must be numpy array

sal_s = np.asarray(sal)
depth_s = np.asarray(depth)
temp_s = np.asarray(temp)

SA=gsw.SA_from_SP(sal,depth,lon_plot,lat_plot)

CT=gsw.CT_from_t(SA,temp,depth)


#CT_5mean=np.mean(CT)
#SA_5mean=np.mean(SA)
# took this out since not a daily record

# plot T/S diagram - altered from example from https://medium.com@hafezahmad/making-#temperature-salinity-diagrams-called-the-t-s-diagram-with-python-and-r-#programming-5deec6378a29

mint=np.min(CT)
maxt=np.max(CT
mins=np.min(SA)
maxs=np.max(SA)
tempL=np.linspace(mint-1,maxt+1,len(SA))
salL=np.linspace(mins-1,maxs+1,len(SA))

Tg, Sg = np.meshgrid(tempL,salL)
sigma_theta = gsw.sigma0(Sg, Tg)
cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),50)
fig,ax=plt.subplots(figsize=(10,10))
cs = ax.contour(Sg, Tg, sigma_theta,colors='grey',zorder=1)
cl=plt.clabel(cs,fontsize=10)
sc=plt.scatter(SA_5_day_mean,CT_5_day_mean,c=cnt)
cb=plt.colorbar(sc)
cb.set_label('Density')
plt.xlabel('Salinity A')
plt.ylabel('Conservative Temperature')
plt.title('T-S at BATS')
cb.set_label('Density')
plt.show()


##

## Subplots of contoured properties v time

print('Property Plots are Next')
plt.figure(3)

#calculate MLD - apparently this doesn't exist for the python gsw
#mld=gsw.mlp(SA,CT,depth)

#plt.subplots(4,1,sharex=True)

time=time.to_numpy()
ax1=subplot(411)
plt.contourf(time, depth, CT, alpha=0.7,cmap=cmocean.cm.thermal);
#plt.contour(time,depth,mld,linestyle=dash,linecolor=white)
plt.setp(ax1.get_xticklabels(), fontsize=6)
cb=plt.colorbar(CT)
cb.set_label('CT')

ax2=subplot(412,sharex=ax1)
plt.contourf(time,depth,SA,alpha=20, cmap=cmocean.cm.haline)
plt.setp(ax2.get_xticklabels(), visible=False)
cb=plt.colorbar(SA)
cb.set_label('SA')

ax3=subplot(413,sharex=ax1)
plt.contourf(time,depth,oxy,alpha=20, cmap=cmocean.cm.oxy)
plt.setp(ax3.get_xticklabels(), visible=False)
cb=plt.colorbar(oxy)
cb.set_label('Oxygen')

ax4=subplot(414,sharex=ax1)
plt.contourf(time,depth,flo,alpha=.7,cmap=cmocean.cm.algae)
plt.setp(ax4.get_xticklabels(), fontsize=12, visible=True)
plt.show()
cb=plt.colorbar(flo)
cb.set_label('Fluorescence')

plt.xlabel('Time')
plt.ylabel('Depth (dbar)')

##refs
#https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.subplot.html
#https://matplotlib.org/3.1.1/tutorials/introductory/customizing.html?#highlight=contour.negative_linestyle#a-sample-matplotlibrc-file
#https://matplotlib.org/basemap/users/examples.html#
#https://medium.com/@hafezahmad/making-temperature-salinity-diagrams-called-#the-t-s-diagram-with-python-and-r-programming-5deec6378a29
#https://oceanpython.org/2013/02/17/t-s-diagram/

