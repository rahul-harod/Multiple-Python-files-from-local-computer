# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 17:37:01 2015
Used to find weights of each MERRA 0.5 lat by 0.6667 lon data
This weights are used for interpolating MERRA gridded data to 0.05 degree MODIS pixels
P1-P4 has the row and col numbers of the MERRA image which is to be used for interpolating that particular pixel in MODIS image;
@author: Eswar R
"""
from __future__ import division;
import numpy as np;
import gdal;
from gdalconst import *;
from pyhdf import SD;

"""Function for converting matrix of data into tiff image
   inputs: source file to get map parameters, data to be written, output file full name, type of the data
   output: image will be created for the data with given name
"""  
def writeImage(source_file,data,output_file,data_type):
    driver = gdal.GetDriverByName('GTiff');
    dataset_source = gdal.Open(source_file, GA_ReadOnly);
    geotransform_source = dataset_source.GetGeoTransform();
    if(data_type == "str"):
        dataset_dest = driver.Create(output_file, data.shape[1], data.shape[0], 1,gdal.GDT_Int16);
    elif(data_type == "float"):
        dataset_dest = driver.Create(output_file, data.shape[1], data.shape[0], 1,gdal.GDT_Float32);
    dataset_dest.SetGeoTransform(geotransform_source);
    dataset_dest.SetProjection(dataset_source.GetProjection());
    dataset_dest.GetRasterBand(1).WriteArray(data, 0, 0);
    dataset_source = None;
    dataset_dest = None;
"""
Returns Great circle distance between two points on Lat/Lon SYstem (WGS-84)
Distance is returned in metre (m)
"""
def greatCircleDistance(p1Lat,p1Lon,p2Lat,p2Lon):
    R = 6371000;
    p1LatRad = np.deg2rad(p1Lat);
    p2LatRad = np.deg2rad(p2Lat);
    delLat = np.deg2rad(np.abs(p1Lat-p2Lat));
    delLon = np.deg2rad(np.abs(p1Lon-p2Lon));
    a = (np.sin(delLat/2)*np.sin(delLat/2))+(np.cos(p1LatRad)*np.cos(p2LatRad)*(np.sin(delLon/2)*np.sin(delLon/2)));
    c = 2*np.arctan2(np.sqrt(a),np.sqrt(1-a));
    d = R*c;
    return d;

sampleMerraFile = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/SampleFile/MERRA201.prod.assim.tavg1_2d_rad_Nx.20000103.SUB.hdf';
sd = SD.SD(sampleMerraFile);
ds = sd.select('latitude');
latGrids = ds.get();
ds = sd.select('longitude');
lonGrids = ds.get();
latGrids = latGrids[::-1];
print latGrids,lonGrids,
print latGrids.size,lonGrids.size;

LatFile = 'G:/Satellite_data/DEFrac_MODIS/Karnataka/DEM/Latitude1000.tif';
LonFile = 'G:/Satellite_data/DEFrac_MODIS/Karnataka/DEM/Longitude1000.tif';
P1File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/P1SR.tif';
P2File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/P2SR.tif';
P3File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/P3SR.tif';
P4File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/P4SR.tif';
W1File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/W1SR.tif';
W2File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/W2SR.tif';
W3File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/W3SR.tif';
W4File = 'G:/Satellite_data/KabiniEFTimeSeries/MERRASWGDN/Weights/W4SR.tif';

driver = gdal.GetDriverByName('GTiff');
datasetLat = gdal.Open(LatFile, GA_ReadOnly);
LATITUDE = datasetLat.GetRasterBand(1).ReadAsArray();
datasetLat = None;

datasetLon = gdal.Open(LonFile, GA_ReadOnly);
LONGITUDE = datasetLon.GetRasterBand(1).ReadAsArray();
datasetLon = None;

p1 = np.zeros(LATITUDE.shape); p2 = np.zeros(LATITUDE.shape);
p3 = np.zeros(LATITUDE.shape); p4 = np.zeros(LATITUDE.shape);

weight1 = np.zeros(LATITUDE.shape); weight2 = np.zeros(LATITUDE.shape);
weight3 = np.zeros(LATITUDE.shape); weight4 = np.zeros(LATITUDE.shape);

for i in range(0,LATITUDE.shape[0]):
    for j in range(0,LATITUDE.shape[1]):
        northLat = 0;
        southLat = 0;
        westLon = 0;
        eastLon = 0;
        northlatStr = 0;
        southlatStr = 0;
        westlonStr = 0;
        eastlonStr = 0;
        pixLat = LATITUDE[i,j];
        pixLon = LONGITUDE[i,j];
        for x in range (1,latGrids.size):
            if(latGrids[x-1] > pixLat and latGrids[x] <= pixLat):
                southLat = latGrids[x];
                northLat = latGrids[x-1];
                if((x-1) < 10):
                    northlatStr = '0'+str(int(x-1));
                elif((x-1) >= 10):
                    northlatStr = str(int(x-1));
                
                if(x < 10):
                    southlatStr = '0'+str(int(x));
                elif(x >= 10):
                    southlatStr = str(int(x));
#                break;
        for x in range (1,lonGrids.size):
            if(lonGrids[x-1] <= pixLon and lonGrids[x] > pixLon):
                eastLon = lonGrids[x];
                westLon = lonGrids[x-1];
                
                if((x-1) < 10):
                    westlonStr = '0'+str(int(x-1));
                elif((x-1) >= 10):
                    westlonStr = str(int(x-1));
                
                if(x < 10):
                    eastlonStr = '0'+str(int(x));
                elif(x >= 10):
                    eastlonStr = str(int(x));
#                break;
        
        p1[i,j] = int(northlatStr+westlonStr);
        p2[i,j] = int(northlatStr+eastlonStr);
        p3[i,j] = int(southlatStr+westlonStr);
        p4[i,j] = int(southlatStr+eastlonStr);
        d1 = greatCircleDistance(pixLat,pixLon,northLat,westLon);
        d2 = greatCircleDistance(pixLat,pixLon,northLat,eastLon);
        d3 = greatCircleDistance(pixLat,pixLon,southLat,westLon);
        d4 = greatCircleDistance(pixLat,pixLon,southLat,eastLon);
        dmax = greatCircleDistance(southLat,westLon,northLat,eastLon);
        D1 = np.power(np.cos(np.pi*0.5*(d1/dmax)),4);
        D2 = np.power(np.cos(np.pi*0.5*(d2/dmax)),4);
        D3 = np.power(np.cos(np.pi*0.5*(d3/dmax)),4);
        D4 = np.power(np.cos(np.pi*0.5*(d4/dmax)),4);
        weight1[i,j] = D1/(D1+D2+D3+D4);
        weight2[i,j] = D2/(D1+D2+D3+D4);
        weight3[i,j] = D3/(D1+D2+D3+D4);
        weight4[i,j] = D4/(D1+D2+D3+D4);
        
        
writeImage(LatFile,p1,P1File,'str');
writeImage(LatFile,p2,P2File,'str');
writeImage(LatFile,p3,P3File,'str');
writeImage(LatFile,p4,P4File,'str');

writeImage(LatFile,weight1,W1File,'float');
writeImage(LatFile,weight2,W2File,'float');
writeImage(LatFile,weight3,W3File,'float');
writeImage(LatFile,weight4,W4File,'float');

