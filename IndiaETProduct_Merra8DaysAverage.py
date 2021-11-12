# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:18:14 2016
To get 8 days avarage of spatially interpolated MERRA SWRAD images
@author: Eswar R
"""
from __future__ import division;
import numpy as np;
import os;
import gdal;
from gdalconst import *;
import datetime;

def writeImage(source_file,data,output_file,data_type):
    driver = gdal.GetDriverByName('GTiff');
    dataset_source = gdal.Open(source_file, GA_ReadOnly);
    geotransform_source = dataset_source.GetGeoTransform();
    if(data_type == "int"):
        dataset_dest = driver.Create(output_file, data.shape[1], data.shape[0], 1,gdal.GDT_Int16);
    elif(data_type == "float"):
        dataset_dest = driver.Create(output_file, data.shape[1], data.shape[0], 1,gdal.GDT_Float32);
    dataset_dest.SetGeoTransform(geotransform_source);
    dataset_dest.SetProjection(dataset_source.GetProjection());
    dataset_dest.GetRasterBand(1).WriteArray(data, 0, 0);
    dataset_source = None;
    dataset_dest = None;

ipPath = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/MERRA_SWGDN';
opPath = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/SWRAD8Days';

ipFiles = np.array(os.listdir(ipPath));
for i in range(0,ipFiles.size):
    if(ipFiles[i][-3:].lower() != 'tif'):
        print ipFiles[i];
        ipFiles[i] = '-999';
ipFiles = ipFiles[ipFiles != '-999'];
ipFiles = np.sort(ipFiles);

driver = gdal.GetDriverByName('GTiff');
datasetDummy = gdal.Open(ipPath+'/'+ipFiles[0], GA_ReadOnly);
dummy = datasetDummy.GetRasterBand(1).ReadAsArray();
datasetDummy = None;
SWRADSum = np.zeros(dummy.shape);
dummy = None;
i = 0;
while(i < ipFiles.size):
    iFile = ipPath+'/'+ipFiles[i];
    print ipFiles[i];
    oFile = opPath+'/'+ipFiles[i][0:7]+'_SWRAD8Days.tif';
    year = int(ipFiles[i][0:4]);
    doy = int(ipFiles[i][4:7]);
    maxDOY = 0;
    if(doy < 360):
        maxDOY = 8;
    else:
        if(year % 4 == 0):
            maxDOY = 6;
        else:
            maxDOY = 5;
    SWRADSum[:,:] = 0;
    for t in range(i,i+maxDOY):
        ipFile = ipPath+'/'+ipFiles[t];
        dataset = gdal.Open(ipFile, GA_ReadOnly);
        data = dataset.GetRasterBand(1).ReadAsArray();
        dataset= None;
        SWRADSum = SWRADSum+data;
        data = None;
    SWRADAverage = SWRADSum/maxDOY;
#    SWRADAverage = np.round(SWRADAverage,0);
    writeImage(iFile,SWRADAverage,oFile,'float');
    i = i+maxDOY;
    
    
