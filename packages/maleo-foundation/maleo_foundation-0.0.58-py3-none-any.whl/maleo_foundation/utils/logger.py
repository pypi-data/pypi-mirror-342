import logging
import os
from datetime import datetime
from typing import Callable
from maleo_foundation.clients.google.cloud.logging import GoogleCloudLogging
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class BaseLogger(logging.Logger):
    def __init__(
        self,
        base_dir:str,
        type:BaseEnums.LoggerType,
        service_name:BaseTypes.OptionalString = None,
        client_name:BaseTypes.OptionalString = None,
        level:BaseEnums.LoggerLevel = BaseEnums.LoggerLevel.INFO
    ):
        """
        Custom extended logger with file, console, and Google Cloud Logging.

        - Logs are stored in `base_dir/logs/{type}`
        - Uses Google Cloud Logging if configured

        Args:
            base_dir (str): Base directory for logs (e.g., "/path/to/maleo_security")
            service_name (str): The service name (e.g., "maleo_security")
            type (str): Log type (e.g., "application", "middleware")
        """
        #* Ensure service_name exists
        service_name = service_name or os.getenv("SERVICE_NAME")
        if service_name is None:
            raise ValueError("SERVICE_NAME environment variable must be set if service_name is set to None")

        #* Ensure client_name is valid if logger type is a client
        if type == BaseEnums.LoggerType.CLIENT and client_name is None:
            raise ValueError("'client_name' parameter must be provided if 'logger_type' is 'client'")

        #* Define logger name
        if type == BaseEnums.LoggerType.CLIENT:
            name = f"{service_name} - {type} - {client_name}"
        else:
            name = f"{service_name} - {type}"
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
        if type == BaseEnums.LoggerType.CLIENT:
            log_dir = f"logs/{type}/{client_name}"
        else:
            log_dir = f"logs/{type}"
        full_log_dir = os.path.join(base_dir, log_dir)
        os.makedirs(full_log_dir, exist_ok=True)

        #* Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(full_log_dir, f"{timestamp}.log")

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

LoggerFactory = Callable[[], BaseLogger]