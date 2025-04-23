"""Plugin COD Drive
"""
import logging
from abc import ABC, abstractmethod


class CODPlugin(ABC):
    """
    Plugin COD Drive.
    """

    def __init__(self, zip_input_path, ouptut_folder, api_url=None, cookies=None, logger=None, **kwargs):
        self.zip_input_path = zip_input_path
        self.ouptut_folder = ouptut_folder
        self.api_url = api_url
        self.cookies = cookies

        if logger:
            self.logger = logger
        else:
            self.logger = logging.Logger(CODPlugin.__class__.__name__)

            # Create a formatter with the desired format for error messages
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # Create a handler for printing errors to the console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)  # Set the level to ERROR to capture only error messages
            console_handler.setFormatter(formatter)

            # Add the console handler to the logger
            self.logger.addHandler(console_handler)

        self.logger.info(f"Others arguments passed to COD Plugin : {kwargs}")

    @abstractmethod
    def generate_before_modification_report(self) -> None:
        """
        Generate report before modification.
        """

    @abstractmethod
    def generate_after_modification_report(self) -> None:
        """
        Generate report after modification.
        """

    @abstractmethod
    def generate_report(self) -> None:
        """
        Generate report.
        """
