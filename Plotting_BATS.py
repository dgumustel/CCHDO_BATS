#download

# basemap at https://matplotlib.org/basemap/users/download.html Download
# gsw teos10: To install with Anaconda: conda install -c conda-forge cmocean
#remember to restart ipython after install to intialize 

#imports
import cmocean
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gsw
from matplotlib.ticker import MaxNLocator

#make bathy map of BATS study area
m = Basemap(width=6000000,height=5000000,projection='lcc',
            resolution=None,lat_1=31,lat_2=33,lat_0=32,lon_0=-64.5)
m.etopo()

#scatter plot lons and lat coordinates on top of bathy
x, y = m(qcdf['LONGITUDE'],qcdf['LATITUDE'])
m.scatter(x,y,3,marker='o',color='k')
plt.title('Locations of BATS Array’)

plt.show()

##

# PLOT 1 - T/S 

# plot t/s
didx=len(qcdf['CTDPRS'])

qcdf = qcdf[:-didx]
ar=qcdf.to_numpy()
     

SA=gsw.SA_from_SP(qcdf['SALNTY'],qcdf['CTDPRS'],qcdf['LONGITUDE'],qcdf['LATITUDE'])

CT=gsw.CT_from_t(SA,qcdf['CTDTMP'],qcdf['CTDPRS'])

for i=0:len(SA(:,1))
CT_5mean=np.mean(CT(i,:))
SA_5mean=np.mean(SA(i,:))
end

# plot T/S diagram - altered from example from https://medium.com@hafezahmad/making-temperature-salinity-diagrams-called-the-t-s-diagram-with-python-and-r-programming-5deec6378a29

mint=np.min(CT_5_day_mean)
maxt=np.max(CT_5_day_mean)
mins=np.min(SA_5_day_mean)
maxs=np.max(SA_5_day_mean)
tempL=np.linspace(mint-1,maxt+1,50)
salL=np.linspace(mins-1,maxs+1,50)

Tg, Sg = np.meshgrid(tempL,salL)
sigma_theta = gsw.sigma0(Sg, Tg)
cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),50)
fig,ax=plt.subplots(figsize=(10,10))
cs = ax.contour(Sg, Tg, sigma_theta,colors='grey',zorder=1)
cl=plt.clabel(cs,fontsize=10)
sc=plt.scatter(SA_5_day_mean,CT_5_day_mean,c=cnt)
cb=plt.colorbar(sc)
cb.set_label('Density')
plt.xlabel('SA 5 Day Mean')
plt.ylabel('CT 5 Day Mean')
plt.title('Five-day Average T-S at BATS')
cb.set_label(‘Density[kg m$^{-3}$]’)
plt.show()


##

## Subplots of contoured properties v time

#calculate MLD
mld=gsw.mlp(SA,CT,depth)

ax1=subplot(411)
plt.contourf(time, qcdf['CTDPRS'], CT, alpha=0.7,cmap=cmocean.cm.thermal);
Hold on
plt.contour(time,qcdf['CTDPRS'],mld, linestyle=dash,linecolor=white)
plt.setp(ax1.get_xticklabels(), fontsize=6)
cb=plt.colorbar(CT)
cb.set_label(‘CT’)

ax2=subplot(412,sharex=ax1)
plt.contourf(time,qcdf['CTDPRS'],SA,alpha=20, cmap=cmocean.cm.haline)
plt.setp(ax2.get_xticklabels(), visible=False)
cb=plt.colorbar(SA)
cb.set_label(‘SA’)

ax3=(413,sharex=ax1)
plt.contourf(time,qcdf['CTDPRS'],qcdf['OXY'],alpha=20, cmap=cmocean.cm.oxy)
plt.setp(ax3.get_xticklabels(), visible=False)

ax4=(414,sharex=ax1)
plt.contourf(time,qcdf['CTDPRS'],qcdf['PP'],alpha=.7,cmap=cmocean.cm.algae)
plt.setp(ax4.get_xticklabels(), fontsize=12, visible=True)
plt.show()

##refs
#https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.subplot.html
#https://matplotlib.org/3.1.1/tutorials/introductory/customizing.html?#highlight=contour.negative_linestyle#a-sample-matplotlibrc-file
#https://matplotlib.org/basemap/users/examples.html#
#https://medium.com/@hafezahmad/making-temperature-salinity-diagrams-called-#the-t-s-diagram-with-python-and-r-programming-5deec6378a29
#https://oceanpython.org/2013/02/17/t-s-diagram/

