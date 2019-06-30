
# Import planet utils
from .utils import *

import gdal
from osgeo import gdal_array

class Output():
    """
    Class to handle output operations
    """
    def __init__(self, output_filename, array,
                       geotransform, projection):
        """
        Class constructor
        """
        self.output_filename = output_filename
        self.array = array
        self.geotransform = geotransform
        self.projection = projection

    def save_data(self):
        """
        Saves data into a local GeoTiff file
        """
        driver = gdal.GetDriverByName('GTiff')
        driver_options = ["COMPRESS=LZW",
                          "BIGTIFF=YES",
                          "PREDICTOR=1",
                          "TILED=YES",
                          "BLOCKXSIZE=256",
                          "BLOCKYSIZE=256",
                          "INTERLEAVE=BAND"]

        # Get GDAL datatype from NumPy datatype
        dtype = gdal_array.NumericTypeCodeToGDALTypeCode(
                    self.array.dtype)

        # Create destination dataset
        if len(self.array.shape) == 3:
            # 3D array
            bands, rows, cols = self.array.shape
        else:
            # 2D array
            bands = 1
            rows, cols = self.array.shape

        dst_ds = driver.Create(self.output_filename, cols, rows,
                               bands, dtype, driver_options)

        # Set cartographic projection
        dst_ds.SetProjection(self.projection)
        dst_ds.SetGeoTransform(self.geotransform)

        # Write bands
        for band in range(bands):
            dst_ds.GetRasterBand(band+1).WriteArray(self.array[band])

        # Flush to disk
        dst_ds = None

class Input():
    """
    Class to handle input operations
    """

    def __init__(self, filename: str):
        """
        Class constructor
        """
        if file_exists(filename) is True:
            self.filename = filename

    def get_data(self):
        """
        Class method to get the data and metadata
        """
        # Open GDAL dataset
        gdal.UseExceptions()
        try:
            d = gdal.Open(self.filename)
        except Exception as e:
            msg = f"Invalid calibration file name: {self.filename}"
            raise RuntimeError(msg)

        # Get data
        data = d.ReadAsArray()

        # Get GeoTransform and Projection
        gt = d.GetGeoTransform()
        proj = d.GetProjection()

        return self.__ReturnGetData(data, gt, proj)

    class __ReturnGetData(object):
        """
        Internal subclass to return a data object
        """
        def __init__(self, data, gt, proj):
            """
            Class constructur parameters
            ----------------------------
            data: NumPy array
                Numpy array of dimensions bands x columns x rows
            gt: Tuple
                GDAL GeoTransform, six element tuple
                Case of a "north up" image without
                any rotation or shearing
                  GeoTransform[0] Top left x
                  GeoTransform[1] w-e pixel reslution
                  GeoTransform[2] 0
                  GeoTransform[3] Top left y
                  GeoTransform[4] 0
                  GeoTransform[5] n-s pixel resolution (negative value)
            proj: String
               Projection in Well-Known Text (WKT)
               Check projection definitions in:
                   https://spatialreference.org/

            Sets
            ----
            All class parameters in constructor
            """
            self.Data = data
            self.GeoTransform = gt
            self.Projection = proj

