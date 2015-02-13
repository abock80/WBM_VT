'''
Created on May 2, 2014

@author: talbertc
'''
import os
import tempfile,sys
import pyGDP as _pyGDP
pyGDP = _pyGDP.pyGDPwebProcessing()

def upload_shapefile(shp_fname):
    '''Uploads a polygon Shapefile to the GDP server for analysis
    '''
    outdir = tempfile.gettempdir()

    justfname = os.path.splitext(os.path.split(shp_fname)[1])[0]
    out_fname = os.path.join(outdir, justfname)

    zip_shp = pyGDP.shapeToZip(shp_fname, out_fname)
    zip_shp = zip_shp.replace("\\", "/")

    return pyGDP.uploadShapeFile(zip_shp)

shp="D:/abock/Water_Balance/WBM_Andy/Prev/G06746095/BASE/G06746095.shp"
ha=upload_shapefile(shp)

