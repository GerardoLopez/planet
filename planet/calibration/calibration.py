
# Import planet utils
from .utils import *
from .io import Input #, Output

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

        self.__check_input_parameters()

        # Create InputOutput object
        self.input = Input(image_filename)

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
        """
        # Input array
        input_data = self.input.get_data()
        # Get data
        image_matrix = input_data.Data
        
