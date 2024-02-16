import logging
import os

def create_logger(log_file_name, logger_name, log_directory='logs'):
    # Create the directory if it does not exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    full_log_path = os.path.join(log_directory, log_file_name)

    # Create a uniquely named logger object
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Check if the logger already has handlers
    if not logger.handlers:
        # Create a file handler and set the log file path
        file_handler = logging.FileHandler(full_log_path)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter and set the format for log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger

# Usage example
server_logger = create_logger('server.log', 'server_logger')
fast_api_logger = create_logger('fast_api.log', 'fast_api_logger')
