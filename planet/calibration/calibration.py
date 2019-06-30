
import json
import numpy as np
from scipy import interp

# Import planet utils
from .utils import *
from .io import Input, Output

class Calibration():
    """
    Class to apply a calibration vector to RapidEye data
    """

    def __init__(self, calibration_filename: str, image_filename: str):
        """
        Class constructor
        """
        self.calibration_filename = calibration_filename
        self.image_filename = image_filename

        # Private method to check input parameters
        self.__check_input_parameters()

        # Create Input object
        # contains data, geotransform and projection info
        input_data = Input(image_filename)
        self.input_data = input_data.get_data()

        self.calibrated_data = None

    def __get_calibration_vector(self):
        """
        Get calibration information and creates a calibration
        vector that marches the number of columns of the data
        to calibrate.
        """
        try:
            with open(self.calibration_filename) as json_file:
                cal_info = json.load(json_file)

        except json.decoder.JSONDecodeError as e:
            msg = f"Invalid JSON file: {self.calibration_filename} \{e}"
            raise ValueError(msg)

        # Get spacing
        # spacing denotes how far away each sample is in the vector (a
        # spacing of 1 means that the vector is not sub-sampled)
        spacing = cal_info['calibration_info']['calibration_spacing']

        # Get calibration vector
        # List of calibration coefficients that need to be applied to
        # the pixels in the image.
        vector = cal_info['calibration_info']['calibration_vector']
        # Transform into a NumPy vector
        vector = np.array(vector)

        if spacing == 1:
            # Calibration vector does not need interpolation
            return vector

        # Calibration vector needs to be interpolated

        # Position of current calibration vector values
        x = np.arange(0, spacing * vector.shape[0], spacing)
        # Current calibration vector values
        y = vector
        # New indices of extended calibration vector
        # First and last element are the same as original 
        new_x = np.arange(0, spacing * vector.shape[0])

        # Liner interpolation
        new_y = interp(new_x, x, y)

        return new_y

    def __check_input_parameters(self):
        """
        Check that parameter datatypes are strings
        """
        try:
            dtype = type(self.calibration_filename)
        except Exception as e:
            raise ValueError("Invalid calibration file name")

        if file_exists(self.calibration_filename) is False:
            raise IOError("Calibration file does not exist!")

        try:
            dtype = type(self.image_filename)
        except Exception as e:
            raise ValueError("Invalid calibration file name")

        if file_exists(self.image_filename) is False:
            raise IOError("Image file does not exist!")

    def apply_calibration(self):
        """
        Doc
        calibration_filename, image_matrix

        The calibration formula is:
        GAMMA = gamma * alpha ^ 2 where:
            GAMMA is the calibrated matrix
            gamma is the uncorrected matrix
            alpha is the calibration vector.
        Note that alpha and gamma must share the same dimension (if the
        matrix of pixels is m by n, then alpha must be length m).
        """
        # Get uncorrected matrix
        gamma = self.input_data.Data

        # Get calibration vector
        alpha = self.__get_calibration_vector()

        # Check dimensions
        self.__check_dimensions(alpha, gamma)

        GAMMA = gamma* np.power(alpha, 2)

        # Scale to unsigned 8-bit
        GAMMA_8bit = (GAMMA/256).astype(np.uint8)

        self.calibrated_data = GAMMA_8bit

    def save_calibrated_data(self, filename):
        """
        Save the content of self.calibrated_data into a
        2D or 3D GeoTiff file
        :param filename: Full path of file to save
        """
        output = Output(output_filename = filename,
                        array = self.calibrated_data,
                        geotransform = self.input_data.GeoTransform,
                        projection = self.input_data.Projection)

        # Save data
        output.save_data()

    @staticmethod
    def __check_dimensions(vector, array):
        """
        Check that the lenght of the vector is the same as the
        number of columns in the 2D or 3D array
        :param vector: NumPY vector
        :param matrix: NumPY array
        :return: True if vector lenght is equal as number of
                 columns in the array, False otherwise
        """
        if len(array.shape) == 3:
            # 3D array
            bands, rows, cols = array.shape
        else:
            # 2D array
            rows, cols = array.shape

        msg = (f"Length of calibration vector does not match"
               f"number of columms in array. Check vector and"
               f"spacing.")
        assert cols == vector.shape[0], msg
