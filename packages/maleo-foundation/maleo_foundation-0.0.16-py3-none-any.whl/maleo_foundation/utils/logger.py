import logging
import os
from datetime import datetime
from maleo_foundation.clients.google.cloud.logging import GoogleCloudLogging
from maleo_foundation.models.enums import BaseEnums

class BaseLogger(logging.Logger):
    def __init__(
        self,
        base_dir:str,
        service_name:str,
        category:str,
        level:BaseEnums.LoggerLevel = BaseEnums.LoggerLevel.INFO
    ):
        """
        Custom extended logger with file, console, and Google Cloud Logging.

        - Logs are stored in `base_dir/logs/{category}`
        - Uses Google Cloud Logging if configured

        Args:
            base_dir (str): Base directory for logs (e.g., "/path/to/maleo_security")
            service_name (str): The service name (e.g., "maleo_security")
            category (str): Log category (e.g., "application", "middleware")
        """
        #* Define logger name
        name = f"{service_name} - {category}"
        super().__init__(name, level)

        #* Clear existing handlers to prevent duplicates
        for handler in list(self.handlers):
            self.removeHandler(handler)
            handler.close()

        #* Formatter for logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        #* Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        #* Google Cloud Logging handler (If enabled)
        try:
            cloud_handler = GoogleCloudLogging.create_handler(name=name.replace(" ", ""))
            self.addHandler(cloud_handler)
        except Exception as e:
            self.warning(f"Failed to initialize Google Cloud Logging: {str(e)}")

        #* Define log directory
        log_dir = os.path.join(base_dir, f"logs/{category}")
        os.makedirs(log_dir, exist_ok=True)

        #* Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(log_dir, f"{timestamp}.log")

        #* File handler
        file_handler = logging.FileHandler(log_filename, mode="a")
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def dispose(self):
        """Dispose of the logger by removing all handlers."""
        for handler in list(self.handlers):
            self.removeHandler(handler)
            handler.close()
        self.handlers.clear()