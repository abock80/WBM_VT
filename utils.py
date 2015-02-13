from osgeo import ogr

def get_feature_area(shp_fname, field_name, feature_value):
    """given a shapefile file name, a field name and a feature value
    returns the area (in map units) of the first feature with that
    feature value in the named field

    TODO: add error checks for missing file, field, or feature value
    add error checks for multipart features or multiple matching feature values
    """

    print (shp_fname)
    print (field_name)
    print (feature_value)
    driver = ogr.GetDriverByName("ESRI Shapefile")

    dataSource = driver.Open(shp_fname, 0)
    layer = dataSource.GetLayer()
    print len(layer)
    print layer[0]
    #if the gage contains a leading 0
    #if feature_value[0] == '0':
    #    layer.SetAttributeFilter(field_name + " = '" + feature_value[1:] + "'")
    #else:
    layer.SetAttributeFilter(field_name + " = '" + feature_value + "'")
    print (field_name + " = '" + feature_value[1:] + "'")
    feature = layer[0]  #  the first matching feature
    print ("hi")
    return feature.geometry().GetArea()


def get_feature_centroid(shp_fname, field_name, feature_value):
    """given a shapefile file name, a field name and a feature value
    returns the area (in map units) of the first feature with that
    feature value in the named field

    TODO: add error checks for missing file, field, or feature value
    add error checks for multipart features or multiple matching feature values
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shp_fname, 0)
    layer = dataSource.GetLayer()

    layer.SetAttributeFilter(field_name + " = '" + feature_value + "'")

    feature = layer[0]  #  the first matching feature
    return feature.geometry().Centroid()
